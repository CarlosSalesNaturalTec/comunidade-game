import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import {
  type AporteDeEfetividade,
  type DesafioDeEfetividade,
  lerPainelDeEfetividade,
  type PainelDeEfetividade,
} from "./api";

const RÓTULO_DO_GRUPO: Record<"propostos" | "publicados" | "concluidos", string> = {
  propostos: "Propostos",
  publicados: "Publicados",
  concluidos: "Concluídos",
};

const RÓTULO_DO_CUSTEIO: Record<AporteDeEfetividade["custeio_tipo"], string> = {
  missao: "Missão",
  necessidade: "Necessidade",
  desafio_extra: "Desafio extra",
  livre: "Aporte livre",
};

function formatarData(isoDeData: string): string {
  const data = new Date(isoDeData);
  return Number.isNaN(data.getTime())
    ? isoDeData
    : data.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric" });
}

// Um desafio do painel: `direcionado` mostra só se houve conclusão — nem
// avatar, nem nick, nem trilha do destinatário; `aberto` mostra contagem,
// período e concluintes exibíveis (`RF-14-42`, `RF-14-45` a `RF-14-47`).
function CartaoDeDesafio({ desafio }: { desafio: DesafioDeEfetividade }) {
  return (
    <article className="cg-cartao-de-desafio-de-efetividade">
      <p>
        <strong>Trilha:</strong> {desafio.trilha_nome}
      </p>
      {desafio.modalidade === "direcionado" ? (
        <p>{desafio.houve_conclusao ? "Concluído." : "Ainda não concluído."}</p>
      ) : (
        <>
          <p>
            {desafio.quantidade_de_conclusoes ?? 0} Guerreiro(a) concluíram
            {desafio.primeira_conclusao_em && desafio.ultima_conclusao_em && (
              <>
                {" "}
                — de {formatarData(desafio.primeira_conclusao_em)} a{" "}
                {formatarData(desafio.ultima_conclusao_em)}
              </>
            )}
          </p>
          {desafio.concluintes_exibiveis && desafio.concluintes_exibiveis.length > 0 && (
            <ul>
              {desafio.concluintes_exibiveis.map((concluinte) => (
                <li key={concluinte.nick}>{concluinte.nick}</li>
              ))}
            </ul>
          )}
          {!!desafio.concluintes_nao_identificados && (
            <p>{desafio.concluintes_nao_identificados} sem divulgação autorizada</p>
          )}
        </>
      )}
      {desafio.etiquetas_ods.length > 0 && <p>ODS: {desafio.etiquetas_ods.join(", ")}</p>}
    </article>
  );
}

// O painel vivo do Apoiador: o que o apoio produziu, sempre agregado e sem
// identificar criança além de avatar e nick autorizados (`RF-14-40` a
// `RF-14-47`, `RN-14-21`).
export function TelaDeEfetividade() {
  const { sessao } = useSessao();
  const [painel, definirPainel] = useState<PainelDeEfetividade | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    lerPainelDeEfetividade(sessao.token)
      .then(definirPainel)
      .catch(() => definirErro("Não foi possível carregar a efetividade. Tente novamente."));
  }, [sessao]);

  const semNenhumDesafio =
    painel !== null &&
    painel.desafios.propostos.length === 0 &&
    painel.desafios.publicados.length === 0 &&
    painel.desafios.concluidos.length === 0;

  return (
    <Moldura>
      <Cabecalho titulo="Efetividade do apoio" />
      <p>
        Este painel é vivo: atualiza a cada conclusão registrada. Não há relatório fechado nem
        periodicidade.
      </p>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {painel === null && !erro && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {semNenhumDesafio && (
        <EstadoDaLista>
          Você ainda não propôs nenhum desafio extra. Proponha um desafio para acompanhar o que
          ele produziu.
        </EstadoDaLista>
      )}
      {painel &&
        !semNenhumDesafio &&
        (["propostos", "publicados", "concluidos"] as const).map((grupo) =>
          painel.desafios[grupo].length > 0 ? (
            <section key={grupo}>
              <h3>{RÓTULO_DO_GRUPO[grupo]}</h3>
              {painel.desafios[grupo].map((desafio) => (
                <CartaoDeDesafio key={desafio.id} desafio={desafio} />
              ))}
            </section>
          ) : null,
        )}
      {painel && (
        <section>
          <h3>Moedas aportadas</h3>
          <p>Total: {painel.moedas.total_em_moedas} moedas</p>
          {painel.moedas.aportes.length === 0 && (
            <EstadoDaLista>Ainda não há aporte homologado.</EstadoDaLista>
          )}
          {painel.moedas.aportes.map((aporte) => (
            <article key={aporte.id} className="cg-cartao-de-aporte-de-efetividade">
              <p>
                {formatarData(aporte.data_do_aporte)} — {aporte.valor_em_moedas} moedas
              </p>
              <p>
                {RÓTULO_DO_CUSTEIO[aporte.custeio_tipo]}
                {aporte.custeio_descricao ? `: ${aporte.custeio_descricao}` : ""}
              </p>
            </article>
          ))}
        </section>
      )}
      {painel && (
        <section>
          <h3>Cobertura de ODS</h3>
          <p>Descrição do que foi tocado pelo apoio — não é nota nem classificação.</p>
          {painel.cobertura_de_ods.por_comunidade.length === 0 && (
            <EstadoDaLista>Nenhuma cobertura agregada ainda.</EstadoDaLista>
          )}
          {painel.cobertura_de_ods.por_comunidade.map((cobertura) => (
            <article key={cobertura.comunidade_virtual_id}>
              <p>
                {cobertura.comunidade_virtual_nome} — {cobertura.ciclo_rotulo}
              </p>
              <p>Objetivos: {cobertura.objetivos.join(", ")}</p>
            </article>
          ))}
        </section>
      )}
    </Moldura>
  );
}
