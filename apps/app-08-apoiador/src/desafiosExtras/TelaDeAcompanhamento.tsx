import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import { type DesafioExtra, listarMeusDesafiosExtras } from "./api";

const RÓTULO_DA_SITUAÇÃO: Record<DesafioExtra["situacao"], string> = {
  em_validacao_do_mestre: "Em validação do Mestre",
  em_aprovacao_do_admin: "Em aprovação do Admin",
  publicado: "Publicado",
  recusado: "Recusado",
};

// O acompanhamento: estado no fluxo, motivo da recusa em linguagem simples,
// o que falta de lastro e a quantidade restante do publicado — sem edição
// alguma, sem identificação de Guerreiro(a) e sem campo de mensagem
// (`RF-14-34` a `RF-14-39`, `RN-14-20`).
export function TelaDeAcompanhamento() {
  const { sessao } = useSessao();
  const [desafios, definirDesafios] = useState<DesafioExtra[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    listarMeusDesafiosExtras(sessao.token)
      .then(definirDesafios)
      .catch(() => definirErro("Não foi possível carregar seus desafios. Tente novamente."));
  }, [sessao]);

  return (
    <Moldura>
      <Cabecalho titulo="Meus desafios extras" />
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {desafios === null && !erro && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {desafios !== null && desafios.length === 0 && (
        <EstadoDaLista>Você ainda não propôs nenhum desafio extra.</EstadoDaLista>
      )}
      {desafios?.map((desafio) => (
        <article key={desafio.id} className="cg-cartao-de-desafio-extra">
          <p>
            <strong>Situação:</strong> {RÓTULO_DA_SITUAÇÃO[desafio.situacao]}
          </p>
          {desafio.situacao === "recusado" && desafio.motivo_da_recusa && (
            <Aviso tipo="atencao">{desafio.motivo_da_recusa}</Aviso>
          )}
          {desafio.modalidade === "direcionado" && desafio.nick_do_destinatario && (
            <p>Direcionado ao nick: {desafio.nick_do_destinatario}</p>
          )}
          {!desafio.lastro_provido && desafio.lastro_faltante && (
            <Aviso tipo="atencao">{desafio.lastro_faltante}</Aviso>
          )}
          {desafio.situacao === "publicado" && (
            <p>
              Recompensas restantes: {desafio.quantidade_restante}. Publicado não se edita —
              para corrigir, proponha de novo.
            </p>
          )}
        </article>
      ))}
    </Moldura>
  );
}
