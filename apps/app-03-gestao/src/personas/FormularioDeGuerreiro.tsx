import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useEffect, useId, useState } from "react";
import { type AulaDaAgenda, listarAgenda } from "../agenda/api";
import { ErroDaApi, ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import type { ComunidadeDaLista } from "../comunidades/api";
import { cadastrarGuerreiro, editarGuerreiro, type GuerreiroDaLista } from "./api";

interface Props {
  comunidades: ComunidadeDaLista[];
  guerreiroExistente?: GuerreiroDaLista;
  onSalvo: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const RECUSA_POR_PAPEL = "Só o Admin cadastra ou edita Guerreiro(a).";

// Nenhuma imagem real do Guerreiro(a) circula por esta tela: só o avatar e o
// nick, como qualquer superfície da gestão (`RN-02-22`, PRD-02 §11).
const AVISO_DE_COLETA =
  "Este cadastro coleta nome, data de nascimento, nick e avatar da criança, usados só para a " +
  "operação da comunidade e visíveis apenas à gestão e à família. Nenhuma imagem real é " +
  "exibida aqui — a representação pública é sempre o avatar.";

export function FormularioDeGuerreiro({
  comunidades,
  guerreiroExistente,
  onSalvo,
  onCancelar,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoCampoDeComunidade = useId();
  const idDoCampoDeAula = useId();
  const emEdicao = guerreiroExistente !== undefined;

  const [nome, definirNome] = useState(guerreiroExistente?.nome ?? "");
  const [nascimento, definirNascimento] = useState(guerreiroExistente?.nascimento ?? "");
  const [nick, definirNick] = useState(guerreiroExistente?.nick ?? "");
  const [avatar, definirAvatar] = useState(guerreiroExistente?.avatar ?? "");
  const [comunidadeId, definirComunidadeId] = useState(comunidades[0]?.id ?? "");
  const [aulas, definirAulas] = useState<AulaDaAgenda[]>([]);
  const [aulaId, definirAulaId] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  // A aula é só do cadastro — é dela que vem a comunidade do vínculo
  // (`RF-08-02`, `RN-08-02`); a edição nunca a pede de novo.
  useEffect(() => {
    if (emEdicao || !sessao || !comunidadeId) {
      definirAulas([]);
      return;
    }
    let cancelado = false;
    listarAgenda(sessao.token, { comunidadeId })
      .then((pagina) => {
        if (!cancelado) definirAulas(pagina.itens);
      })
      .catch(() => {
        if (!cancelado) definirAulas([]);
      });
    return () => {
      cancelado = true;
    };
  }, [emEdicao, sessao, comunidadeId]);

  useEffect(() => {
    definirAulaId((atual) =>
      aulas.some((aula) => aula.id === atual) ? atual : (aulas[0]?.id ?? ""),
    );
  }, [aulas]);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome." });
      return;
    }
    if (!nascimento) {
      definirErroDeCampo({ campo: "nascimento", mensagem: "Informe a data de nascimento." });
      return;
    }
    if (!nick.trim()) {
      definirErroDeCampo({ campo: "nick", mensagem: "Informe o nick." });
      return;
    }
    if (!avatar.trim()) {
      definirErroDeCampo({ campo: "avatar", mensagem: "Escolha o avatar." });
      return;
    }
    if (!emEdicao && !aulaId) {
      definirErroDeCampo({
        campo: "aula_id",
        mensagem: "Escolha a aula em que ele se cadastra.",
      });
      return;
    }

    if (!sessao) return;

    definirEnviando(true);
    try {
      if (emEdicao) {
        await editarGuerreiro(
          guerreiroExistente.id,
          { nome, nascimento, nick, avatar },
          sessao.token,
        );
      } else {
        await cadastrarGuerreiro(
          { nome, nascimento, nick, avatar, aula_id: aulaId },
          sessao.token,
        );
      }
      onSalvo();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "permissao_negada") {
        definirErroDeRecusa(RECUSA_POR_PAPEL);
        return;
      }
      if (
        erro instanceof ErroDaApi &&
        erro.codigo === "erro_de_validacao" &&
        erro.campo === "nick"
      ) {
        // O nick em uso nunca revela de quem é (`RN-01-30`).
        definirErroDeCampo({
          campo: "nick",
          mensagem: "Este nick já está em uso. Escolha outro.",
        });
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa(
        "Não foi possível salvar o Guerreiro(a). Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form
      onSubmit={aoSubmeter}
      aria-label={emEdicao ? "Editar Guerreiro(a)" : "Novo Guerreiro(a)"}
    >
      <Aviso tipo="atencao">{AVISO_DE_COLETA}</Aviso>

      <Campo
        rotulo="Nome"
        valor={nome}
        aoAlterar={definirNome}
        erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Data de nascimento"
        tipo="date"
        valor={nascimento}
        aoAlterar={definirNascimento}
        erro={erroDeCampo?.campo === "nascimento" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Nick"
        valor={nick}
        aoAlterar={definirNick}
        erro={erroDeCampo?.campo === "nick" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Avatar"
        valor={avatar}
        aoAlterar={definirAvatar}
        erro={erroDeCampo?.campo === "avatar" ? erroDeCampo.mensagem : null}
      />

      {!emEdicao && (
        <>
          <div className="cg-campo">
            <label htmlFor={idDoCampoDeComunidade}>Comunidade</label>
            <select
              id={idDoCampoDeComunidade}
              value={comunidadeId}
              onChange={(evento) => definirComunidadeId(evento.target.value)}
            >
              <option value="">Selecione</option>
              {comunidades.map((comunidade) => (
                <option key={comunidade.id} value={comunidade.id}>
                  {comunidade.nome}
                </option>
              ))}
            </select>
          </div>

          <div className="cg-campo">
            <label htmlFor={idDoCampoDeAula}>Aula em que se cadastra</label>
            <select
              id={idDoCampoDeAula}
              value={aulaId}
              onChange={(evento) => definirAulaId(evento.target.value)}
              aria-invalid={erroDeCampo?.campo === "aula_id" || undefined}
            >
              <option value="">Selecione</option>
              {aulas.map((aula) => (
                <option key={aula.id} value={aula.id}>
                  {new Date(aula.inicio_em).toLocaleString("pt-BR")}
                </option>
              ))}
            </select>
            {erroDeCampo?.campo === "aula_id" && (
              <p role="alert" className="cg-campo__erro">
                {erroDeCampo.mensagem}
              </p>
            )}
          </div>
        </>
      )}

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        {emEdicao ? "Salvar" : "Cadastrar"}
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
