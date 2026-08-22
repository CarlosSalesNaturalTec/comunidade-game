import { Botao, EstadoDaLista } from "comum/react";
import type { PoderDoCatalogo } from "../poderes/api";
import type { TrilhaDoMestre } from "./api";

interface Props {
  trilhas: TrilhaDoMestre[] | null;
  poderes: PoderDoCatalogo[];
  aoAbrir: (trilha: TrilhaDoMestre) => void;
}

const ROTULO_DA_SITUACAO: Record<string, string> = {
  rascunho: "Rascunho",
  publicada: "Publicada",
  despublicada: "Despublicada",
};

// As trilhas do Mestre autor, rascunho incluso — a trilha de outro Mestre
// nunca chega aqui, porque `GET /trilhas/minhas` já filtra por autoria
// (`RF-09-04`).
export function ListaDeTrilhas({ trilhas, poderes, aoAbrir }: Props) {
  if (trilhas === null) {
    return <EstadoDaLista>Carregando as suas trilhas…</EstadoDaLista>;
  }

  if (trilhas.length === 0) {
    return <EstadoDaLista>Nenhuma trilha criada ainda.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-trilhas" aria-label="Minhas trilhas">
      {trilhas.map((trilha) => {
        const poder = poderes.find((p) => p.id === trilha.poder_id);
        return (
          <li key={trilha.id} className="lista-de-trilhas__item">
            <div className="lista-de-trilhas__linha">
              <span className="lista-de-trilhas__nome">{trilha.nome}</span>
              <span className="lista-de-trilhas__situacao">
                {ROTULO_DA_SITUACAO[trilha.situacao] ?? trilha.situacao}
              </span>
            </div>
            <p className="lista-de-trilhas__detalhe">
              {poder?.nome ?? "Poder"} · {trilha.area_do_conhecimento}
            </p>
            {trilha.situacao === "despublicada" && trilha.motivo_da_situacao && (
              <p className="lista-de-trilhas__motivo">{trilha.motivo_da_situacao}</p>
            )}
            <Botao variante="secundaria" onClick={() => aoAbrir(trilha)}>
              Abrir
            </Botao>
          </li>
        );
      })}
    </ul>
  );
}
