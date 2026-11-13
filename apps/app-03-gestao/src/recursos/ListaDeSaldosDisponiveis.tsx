import { type ColunaDaTabela, EstadoDaLista, Tabela } from "comum/react";
import type { PontoDeApoioDaLista, SaldoDoTipoDeRecurso } from "../pontos-de-apoio/api";
import { formatarQuantidade } from "./formatacao";

export interface SaldoDoPontoDeApoio {
  pontoDeApoio: PontoDeApoioDaLista;
  saldos: SaldoDoTipoDeRecurso[];
}

interface Props {
  gruposDeSaldo: SaldoDoPontoDeApoio[] | null;
  nomeDaComunidade: (id: string) => string;
  unidadeDoTipoDeRecurso: (id: string) => string | undefined;
}

const TITULO = "Saldo disponível";

// O saldo vem apurado por ponto de apoio, como o núcleo o devolve — uma
// tabela por ponto, que nunca soma nem recalcula entre pontos de apoio
// (`RF-02-45`, `RF-02-97`, design — decisões 1 e 5).
export function ListaDeSaldosDisponiveis({
  gruposDeSaldo,
  nomeDaComunidade,
  unidadeDoTipoDeRecurso,
}: Props) {
  if (gruposDeSaldo === null) {
    return (
      <section>
        <h2>{TITULO}</h2>
        <EstadoDaLista>Carregando o saldo disponível…</EstadoDaLista>
      </section>
    );
  }

  const gruposComSaldo = gruposDeSaldo.filter((grupo) => grupo.saldos.length > 0);

  if (gruposComSaldo.length === 0) {
    return (
      <section>
        <h2>{TITULO}</h2>
        <EstadoDaLista>Não há saldo disponível em nenhum ponto de apoio.</EstadoDaLista>
      </section>
    );
  }

  const colunas: ColunaDaTabela<SaldoDoTipoDeRecurso>[] = [
    {
      chave: "recurso",
      rotulo: "Recurso",
      cabecalhoDeLinha: true,
      renderizar: (saldo) => saldo.nome,
    },
    {
      chave: "saldo",
      rotulo: "Saldo",
      renderizar: (saldo) =>
        formatarQuantidade(saldo.saldo, unidadeDoTipoDeRecurso(saldo.tipo_de_recurso_id)),
    },
  ];

  return (
    <section aria-label="Saldo disponível por ponto de apoio">
      <h2>{TITULO}</h2>
      {gruposComSaldo.map((grupo) => (
        <section key={grupo.pontoDeApoio.id}>
          <h3>
            {grupo.pontoDeApoio.nome} —{" "}
            {nomeDaComunidade(grupo.pontoDeApoio.comunidade_virtual_id)}
          </h3>
          <Tabela
            colunas={colunas}
            linhas={grupo.saldos}
            chaveDaLinha={(saldo) => saldo.tipo_de_recurso_id}
          />
        </section>
      ))}
    </section>
  );
}
