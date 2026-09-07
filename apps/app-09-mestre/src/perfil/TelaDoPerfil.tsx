import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type FormEvent, useCallback, useEffect, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import {
  type ArtefatoDoMestre,
  conferirDisponibilidadeDeNick,
  declararArtefato,
  editarArtefato,
  gravarIdentidade,
  type IdentidadeDoMestre,
  lerIdentidade,
  listarArtefatos,
  removerArtefato,
} from "./api";

const DADO_COLETADO_DA_IDENTIDADE = "o seu nick e o seu avatar";
const DADO_COLETADO_DOS_ARTEFATOS = "os artefatos que comprovam a sua habilidade";

// Formulário de edição de um artefato — o do cadastro incluído, que
// continua sem caminho de remoção (`RF-09-66`, `RN-09-14`).
function FormularioDeEdicaoDeArtefato({
  artefato,
  onSalvar,
  onCancelar,
}: {
  artefato: ArtefatoDoMestre;
  onSalvar: (endereco: string, rotulo: string) => Promise<void>;
  onCancelar: () => void;
}) {
  const [endereco, definirEndereco] = useState(artefato.endereco);
  const [rotulo, definirRotulo] = useState(artefato.rotulo);
  const [erro, definirErro] = useState<string | null>(null);
  const [salvando, definirSalvando] = useState(false);

  async function aoSalvar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    if (!endereco.trim() || !rotulo.trim()) {
      definirErro("Informe o endereço e o rótulo do artefato.");
      return;
    }
    definirSalvando(true);
    definirErro(null);
    try {
      await onSalvar(endereco.trim(), rotulo.trim());
    } catch {
      definirErro("Não foi possível salvar a edição. Tente novamente em instantes.");
    } finally {
      definirSalvando(false);
    }
  }

  return (
    <form onSubmit={aoSalvar} aria-label={`Editar artefato ${artefato.rotulo}`}>
      <Campo rotulo="Rótulo" valor={rotulo} aoAlterar={definirRotulo} />
      <Campo rotulo="Endereço" valor={endereco} aoAlterar={definirEndereco} />
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Botao tipo="submit" desabilitado={salvando}>
        Salvar
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}

// Currículo, portfólio, redes sociais e artefatos comprobatórios, sempre
// por endereço e rótulo — nunca upload de arquivo. O artefato do cadastro
// aparece marcado, edita e não remove; a área não cadastra Mestre nem
// altera nome, e-mail ou papel (`RF-09-66`, `RF-09-67`, `RN-09-14`).
// Ganha também o nick e o avatar do próprio Mestre, sem piso de moeda
// algum, que é regra de marca do Apoiador (`RF-09-114`, `RN-14-11`).
export function TelaDoPerfil() {
  const { sessao, tratarRecusaDeSessao } = useSessao();

  const [identidade, definirIdentidade] = useState<IdentidadeDoMestre | null>(null);
  const [nick, definirNick] = useState("");
  const [erroDeNick, definirErroDeNick] = useState<string | null>(null);
  const [sugestoesDeNick, definirSugestoesDeNick] = useState<string[]>([]);
  const [gravandoNick, definirGravandoNick] = useState(false);
  const [sucessoDeNick, definirSucessoDeNick] = useState(false);

  const [avatar, definirAvatar] = useState("");
  const [erroDeAvatar, definirErroDeAvatar] = useState<string | null>(null);
  const [gravandoAvatar, definirGravandoAvatar] = useState(false);
  const [sucessoDeAvatar, definirSucessoDeAvatar] = useState(false);

  const [artefatos, definirArtefatos] = useState<ArtefatoDoMestre[] | null>(null);
  const [endereco, definirEndereco] = useState("");
  const [rotulo, definirRotulo] = useState("");
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [artefatoEmEdicao, definirArtefatoEmEdicao] = useState<string | null>(null);

  const carregarIdentidade = useCallback(async () => {
    if (!sessao) return;
    try {
      const lida = await lerIdentidade(sessao.token);
      definirIdentidade(lida);
      definirNick(lida.nick ?? "");
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
      }
    }
  }, [sessao, tratarRecusaDeSessao]);

  function recarregarArtefatos() {
    if (!sessao) return;
    listarArtefatos(sessao.persona_id, sessao.token)
      .then(definirArtefatos)
      .catch(() => definirArtefatos([]));
  }

  useEffect(() => {
    carregarIdentidade();
  }, [carregarIdentidade]);
  useEffect(recarregarArtefatos, [sessao]);

  async function aoGravarNick(evento: FormEvent) {
    evento.preventDefault();
    if (!sessao) return;
    definirGravandoNick(true);
    definirErroDeNick(null);
    definirSugestoesDeNick([]);
    definirSucessoDeNick(false);
    try {
      const atualizada = await gravarIdentidade({ nick }, sessao.token);
      definirIdentidade(atualizada);
      definirSucessoDeNick(true);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.campo === "nick") {
        definirErroDeNick(erroCapturado.message);
        const disponibilidade = await conferirDisponibilidadeDeNick(nick).catch(() => null);
        definirSugestoesDeNick(disponibilidade?.sugestoes ?? []);
      } else {
        definirErroDeNick("Não foi possível gravar o nick. Tente novamente.");
      }
    } finally {
      definirGravandoNick(false);
    }
  }

  async function aoGravarAvatar(evento: FormEvent) {
    evento.preventDefault();
    if (!sessao) return;
    definirGravandoAvatar(true);
    definirErroDeAvatar(null);
    definirSucessoDeAvatar(false);
    try {
      const atualizada = await gravarIdentidade({ avatar }, sessao.token);
      definirIdentidade(atualizada);
      definirSucessoDeAvatar(true);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDeAvatar("Não foi possível gravar o avatar. Tente novamente.");
    } finally {
      definirGravandoAvatar(false);
    }
  }

  async function aoPublicar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErro(null);

    if (!endereco.trim() || !rotulo.trim()) {
      definirErro("Informe o endereço e o rótulo do artefato.");
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      await declararArtefato(
        sessao.persona_id,
        { endereco: endereco.trim(), rotulo: rotulo.trim() },
        sessao.token,
      );
      definirEndereco("");
      definirRotulo("");
      recarregarArtefatos();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível publicar o artefato. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  async function aoRemover(artefatoId: string) {
    if (!sessao) return;
    definirErro(null);
    try {
      await removerArtefato(sessao.persona_id, artefatoId, sessao.token);
      recarregarArtefatos();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível remover o artefato. Tente novamente em instantes.");
    }
  }

  async function aoEditar(artefatoId: string, novoEndereco: string, novoRotulo: string) {
    if (!sessao) return;
    await editarArtefato(
      sessao.persona_id,
      artefatoId,
      { endereco: novoEndereco, rotulo: novoRotulo },
      sessao.token,
    );
    definirArtefatoEmEdicao(null);
    recarregarArtefatos();
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Meu perfil"
        subtitulo="A sua identidade e a prova da sua habilidade — currículo, portfólio e redes sociais"
      />

      <AvisoDeColeta dado={DADO_COLETADO_DA_IDENTIDADE} />

      <p>
        O cadastro de Mestre é ato exclusivo de Admin, com habilidade comprovada. Esta área não
        altera o seu nome, e-mail ou papel.
      </p>

      {identidade && (
        <>
          <form onSubmit={aoGravarNick}>
            <Campo rotulo="Nick" valor={nick} aoAlterar={definirNick} erro={erroDeNick} />
            {sugestoesDeNick.length > 0 && (
              <p>Sugestões disponíveis: {sugestoesDeNick.join(", ")}</p>
            )}
            <Botao tipo="submit" desabilitado={gravandoNick}>
              Gravar nick
            </Botao>
          </form>
          {sucessoDeNick && <Aviso tipo="sucesso">Nick gravado.</Aviso>}

          <form onSubmit={aoGravarAvatar}>
            <Campo
              rotulo="Avatar (endereço da imagem)"
              valor={avatar}
              aoAlterar={definirAvatar}
              erro={erroDeAvatar}
            />
            <Botao tipo="submit" desabilitado={gravandoAvatar}>
              Gravar avatar
            </Botao>
          </form>
          {sucessoDeAvatar && <Aviso tipo="sucesso">Avatar gravado.</Aviso>}
        </>
      )}

      <AvisoDeColeta dado={DADO_COLETADO_DOS_ARTEFATOS} />

      {artefatos === null ? (
        <p>Carregando…</p>
      ) : (
        <ul aria-label="Artefatos comprobatórios">
          {artefatos.map((artefato) =>
            artefatoEmEdicao === artefato.id ? (
              <li key={artefato.id}>
                <FormularioDeEdicaoDeArtefato
                  artefato={artefato}
                  onSalvar={(novoEndereco, novoRotulo) =>
                    aoEditar(artefato.id, novoEndereco, novoRotulo)
                  }
                  onCancelar={() => definirArtefatoEmEdicao(null)}
                />
              </li>
            ) : (
              <li key={artefato.id}>
                <a href={artefato.endereco} target="_blank" rel="noreferrer">
                  {artefato.rotulo}
                </a>
                {artefato.declarado_no_cadastro && <span> — declarado no cadastro</span>}
                <Botao
                  variante="secundaria"
                  onClick={() => definirArtefatoEmEdicao(artefato.id)}
                >
                  Editar
                </Botao>
                {!artefato.declarado_no_cadastro && (
                  <Botao variante="secundaria" onClick={() => aoRemover(artefato.id)}>
                    Remover
                  </Botao>
                )}
              </li>
            ),
          )}
        </ul>
      )}

      <form onSubmit={aoPublicar} aria-label="Publicar artefato">
        <Campo rotulo="Rótulo" valor={rotulo} aoAlterar={definirRotulo} />
        <Campo rotulo="Endereço" valor={endereco} aoAlterar={definirEndereco} />
        {erro && <Aviso tipo="erro">{erro}</Aviso>}
        <Botao tipo="submit" desabilitado={enviando}>
          Publicar artefato
        </Botao>
      </form>
    </Moldura>
  );
}
