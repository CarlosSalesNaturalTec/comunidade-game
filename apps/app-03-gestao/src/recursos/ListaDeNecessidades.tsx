import { type ColunaDaTabela, EstadoDaLista, Tabela } from "comum/react";
import type { NecessidadeDeRecurso } from "./api";
import { formatarMoedas, formatarQuantidade } from "./formatacao";

interface Props {
  necessidades: NecessidadeDeRecurso[] | null;
  nomeDoTipoDeRecurso: (id: string) => string;
  unidadeDoTipoDeRecurso: (id: string) => string | undefined;
  nomeDaComunidade: (id: string) => string;
  nomeDoPontoDeApoio: (id: string) => string;
}

const TITULO = "Necessidades em aberto";

function formatarHorario(valorComFuso: string): string {
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

// A lista vem do núcleo já derivada — nunca soma, ordena por saldo nem
// recalcula a falta; cada campo na sua coluna, sem coluna recolhida
// (`RF-02-58`, `RN-02-19`, design — decisões 1 e 2).
export function ListaDeNecessidades({
  necessidades,
  nomeDoTipoDeRecurso,
  unidadeDoTipoDeRecurso,
  nomeDaComunidade,
  nomeDoPontoDeApoio,
}: Props) {
  if (necessidades === null) {
    return (
      <section>
        <h2>{TITULO}</h2>
        <EstadoDaLista>Carregando as necessidades…</EstadoDaLista>
      </section>
    );
  }

  if (necessidades.length === 0) {
    return (
      <section>
        <h2>{TITULO}</h2>
        <EstadoDaLista>Não há necessidade de recurso em aberto.</EstadoDaLista>
      </section>
    );
  }

  const colunas: ColunaDaTabela<NecessidadeDeRecurso>[] = [
    {
      chave: "aula",
      rotulo: "Aula",
      renderizar: (item) =>
        `${formatarHorario(item.inicio_em)} – ${formatarHorario(item.fim_em)}`,
    },
    {
      chave: "comunidade",
      rotulo: "Comunidade",
      renderizar: (item) => nomeDaComunidade(item.comunidade_virtual_id),
    },
    {
      chave: "ponto-de-apoio",
      rotulo: "Ponto de apoio",
      renderizar: (item) => nomeDoPontoDeApoio(item.ponto_de_apoio_id),
    },
    {
      chave: "recurso",
      rotulo: "Recurso",
      cabecalhoDeLinha: true,
      renderizar: (item) => nomeDoTipoDeRecurso(item.tipo_de_recurso_id),
    },
    {
      chave: "falta",
      rotulo: "Falta",
      renderizar: (item) =>
        formatarQuantidade(
          item.quantidade_faltante,
          unidadeDoTipoDeRecurso(item.tipo_de_recurso_id),
        ),
    },
    {
      chave: "valor",
      rotulo: "Valor",
      renderizar: (item) =>
        item.valor_em_moedas !== null
          ? formatarMoedas(item.valor_em_moedas)
          : "Sem valor de referência vigente",
    },
  ];

  return (
    <section aria-label="Necessidades de recurso em aberto">
      <h2>{TITULO}</h2>
      <Tabela
        colunas={colunas}
        linhas={necessidades}
        chaveDaLinha={(item) => `${item.aula_id}-${item.tipo_de_recurso_id}`}
      />
    </section>
  );
}
