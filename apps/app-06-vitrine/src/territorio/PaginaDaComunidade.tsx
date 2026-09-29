import { Aviso, EstadoDaLista, TerritorioDaComunidade } from "comum/react";
import {
  type CoberturaDeOds,
  type ComunidadePublica,
  lerCoberturaDeOds,
  lerSerieDaComunidade,
  type MetodologiaDoRecorte,
  obterComunidade,
  type PontoDaSerie,
  type SeriePublica,
} from "../api/leituras";
import { ChamadaDeParticipacao } from "../convite/ChamadaDeParticipacao";
import { useLeitura } from "../leitura/useLeitura";
import { DestaqueDaMeta1718 } from "./DestaqueDaMeta1718";

// A página da comunidade: as séries históricas do território **agregadas até
// o bairro**, a metodologia de cada recorte, o sinal de série inativa, a
// representação visual e a vitalidade (`RF-03-15` a `RF-03-22`).
//
// Três leituras, nunca uma por recorte (design — Decisão 7): a ficha, a série
// com a metodologia e a cobertura de ODS, esta filtrada na tela pela
// comunidade — `/v1/comunidades/{id}/ods` não existe, e a rota agregada já
// devolve objetivos e ciclo por comunidade (decisão do fundador de
// 2026-09-28).
//
// Nenhum recorte abaixo do bairro é pedido nem apresentado: o núcleo não o
// serve, e a tela diz por onde se pede o conjunto completo (`RN-03-09`).

interface Props {
  comunidadeId: string;
  irPara: (destino: string) => void;
}

function chaveDoRecorte(recorte: { tipo_de_coleta_id: string; local_publicado_id: string }) {
  return `${recorte.tipo_de_coleta_id}|${recorte.local_publicado_id}`;
}

function pontosDoRecorte(
  serie: SeriePublica,
  metodologia: MetodologiaDoRecorte,
): PontoDaSerie[] {
  const chave = chaveDoRecorte(metodologia.recorte);
  return serie.itens.filter((ponto) => chaveDoRecorte(ponto.recorte) === chave);
}

function BlocoDoRecorte({
  metodologia,
  pontos,
}: {
  metodologia: MetodologiaDoRecorte;
  pontos: PontoDaSerie[];
}) {
  const { recorte } = metodologia;
  return (
    <li
      className="cg-territorio-painel__recorte"
      data-ativo={metodologia.ativo ? "sim" : "nao"}
    >
      <h4>
        {recorte.tipo_de_coleta_nome} — {recorte.local_publicado_rotulo}
      </h4>
      {/* O sinal de inativo se lê em **texto**, nunca só por cor
          (`RF-03-19`, documento 15 §5). */}
      <p className="cg-territorio-painel__situacao">
        {metodologia.ativo
          ? "Série ativa"
          : "Série inativa — a coleta parou, o dado permanece"}
      </p>
      <dl className="cg-territorio-painel__metodologia">
        <dt>O que mede</dt>
        <dd>
          {recorte.tipo_de_coleta_nome}
          {metodologia.unidade ? ` (${metodologia.unidade})` : " (por evidência, sem número)"}
        </dd>
        <dt>Cadência</dt>
        <dd>{metodologia.cadencias.join(", ")}</dd>
        <dt>Período coberto</dt>
        <dd>
          {metodologia.primeira_medicao.slice(0, 10)} a{" "}
          {metodologia.ultima_medicao.slice(0, 10)}
        </dd>
        <dt>Origem da medição</dt>
        <dd>{metodologia.origens.join(", ")}</dd>
        <dt>Registros válidos</dt>
        <dd>{metodologia.registros_validos}</dd>
      </dl>
      <ul className="cg-territorio-painel__pontos">
        {pontos.map((ponto) => (
          <li key={`${ponto.momento_da_medicao}-${ponto.valor ?? "midia"}`}>
            {ponto.momento_da_medicao.slice(0, 10)}:{" "}
            {ponto.valor === null ? "registro por evidência" : ponto.valor}
          </li>
        ))}
      </ul>
    </li>
  );
}

export function PaginaDaComunidade({ comunidadeId, irPara }: Props) {
  const ficha = useLeitura<ComunidadePublica>(
    () => obterComunidade(comunidadeId),
    `comunidade/${comunidadeId}`,
  );
  const serie = useLeitura<SeriePublica>(
    () => lerSerieDaComunidade(comunidadeId),
    `comunidade/${comunidadeId}/series`,
  );
  const cobertura = useLeitura<CoberturaDeOds[]>(lerCoberturaDeOds, "vitrine/ods/cobertura");

  if (ficha.situacao === "carregando") {
    return <EstadoDaLista>Carregando a comunidade…</EstadoDaLista>;
  }
  if (ficha.situacao === "falhou") {
    return <Aviso tipo="erro">Não foi possível carregar esta comunidade agora.</Aviso>;
  }

  const comunidade = ficha.dado;
  const recortes = serie.situacao === "pronta" ? serie.dado.recortes : [];
  const bairrosPublicados = new Set(
    recortes
      .filter((metodologia) => metodologia.recorte.local_publicado_nivel === "bairro")
      .map((metodologia) => metodologia.recorte.local_publicado_id),
  ).size;
  const camadasPorTipo = new Map<string, { registrosValidos: number; ativo: boolean }>();
  for (const metodologia of recortes) {
    const anterior = camadasPorTipo.get(metodologia.recorte.tipo_de_coleta_nome);
    camadasPorTipo.set(metodologia.recorte.tipo_de_coleta_nome, {
      registrosValidos: (anterior?.registrosValidos ?? 0) + metodologia.registros_validos,
      ativo: (anterior?.ativo ?? false) || metodologia.ativo,
    });
  }
  const daComunidade =
    cobertura.situacao === "pronta"
      ? cobertura.dado.find((linha) => linha.comunidade_id === comunidade.id)
      : undefined;

  return (
    <section className="cg-territorio-painel">
      <h2>{comunidade.nome}</h2>
      <TerritorioDaComunidade
        nome={comunidade.nome}
        bairrosPublicados={bairrosPublicados}
        camadas={[...camadasPorTipo].map(([tipo, dados]) => ({ tipo, ...dados }))}
      />
      <p className="cg-territorio-painel__vitalidade">
        {comunidade.guerreiros_vinculados} Guerreiros e Guerreiras vinculados
      </p>
      <p className="cg-territorio-painel__locais">
        Território: {comunidade.locais.map((local) => local.rotulo).join(", ")}
      </p>

      <h3>Séries do território</h3>
      {/* O painel para no bairro, e quem precisa de mais fino é encaminhado
          ao formulário de solicitação de dados (`RN-03-09`, `RN-03-13`). */}
      <p className="cg-territorio-painel__corte">
        Os dados saem agregados até o bairro, sem identificar quem coletou. Rua, condomínio,
        bloco e quadra só saem no conjunto completo, pela solicitação de dados avaliada por um
        Admin.
      </p>
      {serie.situacao === "carregando" && <EstadoDaLista>Carregando as séries…</EstadoDaLista>}
      {serie.situacao === "falhou" && (
        <Aviso tipo="erro">Não foi possível carregar as séries desta comunidade agora.</Aviso>
      )}
      {serie.situacao === "pronta" &&
        (recortes.length === 0 ? (
          <EstadoDaLista>
            Nenhuma série publicada nesta comunidade ainda — o território segue vazio.
          </EstadoDaLista>
        ) : (
          <ul className="cg-territorio-painel__recortes">
            {recortes.map((metodologia) => (
              <BlocoDoRecorte
                key={chaveDoRecorte(metodologia.recorte)}
                metodologia={metodologia}
                pontos={pontosDoRecorte(serie.dado, metodologia)}
              />
            ))}
          </ul>
        ))}

      <h3>Cobertura da Agenda 2030</h3>
      {daComunidade === undefined ? (
        <EstadoDaLista>Nenhum objetivo coberto por esta comunidade ainda.</EstadoDaLista>
      ) : (
        <>
          <p>
            Ciclo {daComunidade.ciclo}: objetivos {daComunidade.objetivos.join(", ")}
          </p>
          <DestaqueDaMeta1718 />
        </>
      )}

      {/* A chamada fecha a página individual da comunidade (`RF-03-39`): o
          apoio é ao projeto, nunca àquela comunidade (`RF-03-41`). */}
      <ChamadaDeParticipacao irPara={irPara} />
    </section>
  );
}
