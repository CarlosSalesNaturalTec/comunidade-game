import { EstadoDaLista } from "comum/react";
import type { PontoDeApoioDaLista, SaldoDoTipoDeRecurso } from "../pontos-de-apoio/api";

export interface SaldoDoPontoDeApoio {
  pontoDeApoio: PontoDeApoioDaLista;
  saldos: SaldoDoTipoDeRecurso[];
}

interface Props {
  gruposDeSaldo: SaldoDoPontoDeApoio[] | null;
}

// O saldo vem apurado por ponto de apoio, como o núcleo o devolve — a lista
// nunca soma nem recalcula entre pontos de apoio (`RF-02-45`, `RF-02-97`).
export function ListaDeSaldosDisponiveis({ gruposDeSaldo }: Props) {
  if (gruposDeSaldo === null) {
    return <EstadoDaLista>Carregando o saldo disponível…</EstadoDaLista>;
  }

  const gruposComSaldo = gruposDeSaldo.filter((grupo) => grupo.saldos.length > 0);

  if (gruposComSaldo.length === 0) {
    return <EstadoDaLista>Não há saldo disponível em nenhum ponto de apoio.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-saldos" aria-label="Saldo disponível por ponto de apoio">
      {gruposComSaldo.map((grupo) => (
        <li key={grupo.pontoDeApoio.id} className="lista-de-saldos__ponto">
          <span className="lista-de-saldos__ponto-nome">{grupo.pontoDeApoio.nome}</span>
          <ul className="lista-de-saldos__tipos">
            {grupo.saldos.map((saldo) => (
              <li key={saldo.tipo_de_recurso_id} className="lista-de-saldos__tipo">
                {saldo.nome}: {saldo.saldo}
              </li>
            ))}
          </ul>
        </li>
      ))}
    </ul>
  );
}
