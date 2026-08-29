import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type FormEvent, useEffect, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import {
  type ArtefatoDoMestre,
  declararArtefato,
  listarArtefatos,
  removerArtefato,
} from "./api";

const DADO_COLETADO = "os artefatos que comprovam a sua habilidade";

// Currículo, portfólio, redes sociais e artefatos comprobatórios, sempre
// por endereço e rótulo — nunca upload de arquivo. O artefato do cadastro
// aparece marcado e sem caminho de remoção; a área não cadastra Mestre nem
// altera o próprio cadastro (`RF-09-66`, `RF-09-67`, `RN-09-14`).
export function TelaDoPerfil() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [artefatos, definirArtefatos] = useState<ArtefatoDoMestre[] | null>(null);
  const [endereco, definirEndereco] = useState("");
  const [rotulo, definirRotulo] = useState("");
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  function recarregar() {
    if (!sessao) return;
    listarArtefatos(sessao.persona_id, sessao.token)
      .then(definirArtefatos)
      .catch(() => definirArtefatos([]));
  }

  useEffect(recarregar, [sessao]);

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
      recarregar();
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
      recarregar();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível remover o artefato. Tente novamente em instantes.");
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Meu perfil"
        subtitulo="A prova da sua habilidade — currículo, portfólio, redes sociais e artefatos"
      />
      <AvisoDeColeta dado={DADO_COLETADO} />

      <p>
        O cadastro de Mestre é ato exclusivo de Admin, com habilidade comprovada. Esta área
        alcança apenas os artefatos que comprovam a sua habilidade.
      </p>

      {artefatos === null ? (
        <p>Carregando…</p>
      ) : (
        <ul aria-label="Artefatos comprobatórios">
          {artefatos.map((artefato) => (
            <li key={artefato.id}>
              <a href={artefato.endereco} target="_blank" rel="noreferrer">
                {artefato.rotulo}
              </a>
              {artefato.declarado_no_cadastro ? (
                <span> — declarado no cadastro</span>
              ) : (
                <Botao variante="secundaria" onClick={() => aoRemover(artefato.id)}>
                  Remover
                </Botao>
              )}
            </li>
          ))}
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
