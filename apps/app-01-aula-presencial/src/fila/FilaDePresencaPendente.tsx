import { Botao } from "comum/react";
import type { ItemDaFilaComSituacao } from "./sincronizacao";

interface Props {
  itens: ItemDaFilaComSituacao[];
  aoTentarDeNovo: (item: ItemDaFilaComSituacao) => void;
}

// Visível só ao Mestre ou Admin da sessão de trabalho, fora de qualquer
// tela de atendimento do Guerreiro(a) — a fila é estado do aparelho, nunca
// do Guerreiro(a) (`RF-04-23`, `RF-04-25`, `RN-04-14`).
export function FilaDePresencaPendente({ itens, aoTentarDeNovo }: Props) {
  if (itens.length === 0) return null;

  return (
    <section aria-label="Presenças pendentes de sincronização" className="cg-fila-de-presenca">
      <h3>Fila de presença</h3>
      <ul>
        {itens.map((item) => (
          <li key={`${item.nick}::${item.momento_do_fato}`}>
            <span>{item.nick}</span>
            <span>{new Date(item.momento_do_fato).toLocaleTimeString()}</span>
            <span>{item.falhou ? "Falhou" : "Aguardando rede"}</span>
            <Botao variante="secundaria" onClick={() => aoTentarDeNovo(item)}>
              Tentar de novo
            </Botao>
          </li>
        ))}
      </ul>
    </section>
  );
}
