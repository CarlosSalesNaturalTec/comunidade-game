import { EstadoDaLista } from "comum/react";
import "./ListaDeChaves.css";
import type { ChaveDeAplicacao } from "./api";
import { RevogarChave } from "./RevogarChave";

interface Props {
  chaves: ChaveDeAplicacao[] | null;
  aoRevogar: () => void;
}

const ROTULO_DA_SITUACAO: Record<ChaveDeAplicacao["situacao"], string> = {
  vigente: "Vigente",
  revogada: "Revogada",
};

function formatarPrazo(valorComFuso: string | null): string {
  if (!valorComFuso) return "—";
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

// A vencer: vigente, sem URL apresentada ainda — o relógio da revogação
// automática está correndo (`RF-02-91`). Revogada por decurso: só se infere
// pelos campos que a leitura de gestão já expõe, sem tocar
// `chave-de-aplicacao` (design — Non-Goals): revogada, nunca apresentada, e
// com o prazo já vencido — a única forma como o decurso acontece
// (`ciclo-de-vida-da-chave-de-terceiro`). Nenhuma das duas depende só de
// cor (documento 15 §5).
function rotuloDeDestaque(chave: ChaveDeAplicacao): string | null {
  if (
    chave.situacao === "vigente" &&
    chave.prazo_de_apresentacao !== null &&
    chave.url_apresentada === null
  ) {
    return "Prazo a vencer";
  }
  if (
    chave.situacao === "revogada" &&
    chave.url_apresentada === null &&
    chave.prazo_de_apresentacao !== null &&
    new Date(chave.prazo_de_apresentacao).getTime() < Date.now()
  ) {
    return "Revogada por prazo vencido";
  }
  return null;
}

// Painel das chaves emitidas, ao lado das Filas — mostra pedido já resolvido
// em chave, nunca pedido em aberto (design — decisão 4). O segredo nunca
// aparece aqui (`RN-02-28`).
export function ListaDeChaves({ chaves, aoRevogar }: Props) {
  if (chaves === null) {
    return <EstadoDaLista>Carregando as chaves…</EstadoDaLista>;
  }

  if (chaves.length === 0) {
    return <EstadoDaLista>Nenhuma chave emitida ainda.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-chaves" aria-label="Chaves emitidas">
      {chaves.map((chave) => {
        const destaque = rotuloDeDestaque(chave);
        return (
          <li key={chave.id} className="lista-de-chaves__item">
            <span className="lista-de-chaves__aplicacao">{chave.aplicacao}</span>
            <span className="lista-de-chaves__situacao">
              {ROTULO_DA_SITUACAO[chave.situacao]}
            </span>
            {destaque && <span className="lista-de-chaves__destaque">{destaque}</span>}
            <span>Prazo: {formatarPrazo(chave.prazo_de_apresentacao)}</span>
            <span>URL: {chave.url_apresentada ?? "—"}</span>
            {chave.situacao === "vigente" && (
              <RevogarChave idDaChave={chave.id} onRevogada={aoRevogar} />
            )}
          </li>
        );
      })}
    </ul>
  );
}
