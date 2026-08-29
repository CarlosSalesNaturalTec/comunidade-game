import { EstadoDaLista } from "comum/react";
import type { EntregaDeRecompensa } from "./api";

interface Props {
  itens: EntregaDeRecompensa[] | null;
  tipoDeRecursoPorId: Map<string, string>;
  pontoDeApoioPorId: Map<string, string>;
  nomeDoMestrePorId: Map<string, string>;
  nickDoGuerreiroPorId: Map<string, string>;
}

function formatarData(valorComFuso: string): string {
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

// Leitura das entregas de recompensa de marco já confirmadas pelo Mestre —
// o exemplar da linha Alpha, a camisa e o que mais o Ciclo 01 declarar
// (`RF-02-50`, `RF-02-51`). Sempre a baixa definitiva, nunca um valor em
// moedas ou em reais, e nenhum caminho de confirmar, corrigir ou desfazer:
// quem confirma é o Mestre que esteve no encontro (`RN-02-17`).
export function ListaDeEntregas({
  itens,
  tipoDeRecursoPorId,
  pontoDeApoioPorId,
  nomeDoMestrePorId,
  nickDoGuerreiroPorId,
}: Props) {
  if (itens === null) {
    return <EstadoDaLista>Carregando as entregas…</EstadoDaLista>;
  }

  if (itens.length === 0) {
    return <EstadoDaLista>Nenhuma entrega confirmada nesta comunidade.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-entregas" aria-label="Entregas confirmadas">
      {itens.map((entrega) => (
        <li key={entrega.id} className="lista-de-entregas__item">
          <span className="lista-de-entregas__guerreiro">
            {nickDoGuerreiroPorId.get(entrega.guerreiro_id) ?? entrega.guerreiro_id}
          </span>
          <span>
            {tipoDeRecursoPorId.get(entrega.tipo_de_recurso_id) ?? entrega.tipo_de_recurso_id}
          </span>
          <span>
            Entregue por {nomeDoMestrePorId.get(entrega.autor_id) ?? entrega.autor_id}
          </span>
          <span>
            {pontoDeApoioPorId.get(entrega.ponto_de_apoio_id) ?? entrega.ponto_de_apoio_id}
          </span>
          <span>{formatarData(entrega.registrado_em)}</span>
          <span className="lista-de-entregas__baixa">Baixa definitiva no livro-razão</span>
        </li>
      ))}
    </ul>
  );
}
