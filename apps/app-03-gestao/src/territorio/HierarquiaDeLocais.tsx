import { EstadoDaLista } from "comum/react";
import "./Territorio.css";
import type { LocalDaLista } from "./api";

interface Props {
  locais: LocalDaLista[] | null;
}

interface NoDaArvore extends LocalDaLista {
  filhos: NoDaArvore[];
}

// A lista chega plana, paginada até o fim (`GET /v1/locais`); a árvore é
// montada aqui, no cliente — não há rota que devolva a hierarquia pronta
// (`RF-02-16`, design — decisão 7).
function montarArvore(locais: LocalDaLista[]): NoDaArvore[] {
  const porId = new Map<string, NoDaArvore>();
  for (const local of locais) {
    porId.set(local.id, { ...local, filhos: [] });
  }
  const raizes: NoDaArvore[] = [];
  for (const no of porId.values()) {
    const pai = no.local_pai_id ? porId.get(no.local_pai_id) : undefined;
    if (pai) {
      pai.filhos.push(no);
    } else {
      raizes.push(no);
    }
  }
  return raizes;
}

function NoDeLocal({ no, profundidade }: { no: NoDaArvore; profundidade: number }) {
  return (
    <li
      className="hierarquia-de-locais__item"
      style={{ paddingLeft: `calc(${profundidade} * var(--espaco-16))` }}
    >
      <span className="hierarquia-de-locais__rotulo">{no.rotulo}</span>
      <span className="hierarquia-de-locais__nivel">{no.nivel}</span>
      {no.filhos.length > 0 && (
        <ul className="hierarquia-de-locais__lista">
          {no.filhos.map((filho) => (
            <NoDeLocal key={filho.id} no={filho} profundidade={profundidade + 1} />
          ))}
        </ul>
      )}
    </li>
  );
}

// Comunidade sem local é o estado normal de quem acabou de nascer
// (`RN-08-01`) — informação, nunca falha (`RF-02-16`, documento 15 §6).
export function HierarquiaDeLocais({ locais }: Props) {
  if (locais === null) {
    return <EstadoDaLista>Carregando os locais…</EstadoDaLista>;
  }

  if (locais.length === 0) {
    return <EstadoDaLista>Esta comunidade ainda não tem locais cadastrados.</EstadoDaLista>;
  }

  const arvore = montarArvore(locais);

  return (
    <ul className="hierarquia-de-locais" aria-label="Hierarquia de locais">
      {arvore.map((no) => (
        <NoDeLocal key={no.id} no={no} profundidade={0} />
      ))}
    </ul>
  );
}
