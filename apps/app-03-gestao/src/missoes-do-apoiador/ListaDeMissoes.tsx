import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useState } from "react";
import { despublicarMissao, type MissaoDoApoiador } from "./api";

interface Props {
  missoes: MissaoDoApoiador[] | null;
  token: string;
  aoDespublicada: (missao: MissaoDoApoiador) => void;
}

const ROTULO_DA_SITUACAO: Record<MissaoDoApoiador["situacao"], string> = {
  aberta: "Aberta",
  concluida: "Concluída",
  despublicada: "Despublicada",
};

function formatarPrazo(iso: string): string {
  const data = new Date(iso);
  return Number.isNaN(data.getTime())
    ? iso
    : data.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric" });
}

// As missões publicadas em qualquer situação, com o coberto, o que falta e
// a situação — sem nick de quem cobriu —, e a despublicação da que foi
// publicada por engano, sem estornar aporte já homologado (`RF-02-104`,
// `RF-02-105`, `RN-14-34`).
export function ListaDeMissoes({ missoes, token, aoDespublicada }: Props) {
  const [despublicando, definirDespublicando] = useState<string | null>(null);
  const [erroPorMissao, definirErroPorMissao] = useState<Record<string, string>>({});

  if (missoes === null) {
    return <EstadoDaLista>Carregando as missões…</EstadoDaLista>;
  }

  if (missoes.length === 0) {
    return <EstadoDaLista>Nenhuma missão publicada ainda.</EstadoDaLista>;
  }

  async function aoClicarDespublicar(missao: MissaoDoApoiador) {
    definirDespublicando(missao.id);
    definirErroPorMissao((atual) => {
      const { [missao.id]: _descartado, ...resto } = atual;
      return resto;
    });
    try {
      const atualizada = await despublicarMissao(missao.id, token);
      aoDespublicada(atualizada);
    } catch {
      definirErroPorMissao((atual) => ({
        ...atual,
        [missao.id]: "Missão concluída não se despublica.",
      }));
    } finally {
      definirDespublicando(null);
    }
  }

  return (
    <ul aria-label="Missões publicadas">
      {missoes.map((missao) => (
        <li key={missao.id}>
          <article>
            <h3>{missao.titulo}</h3>
            <p>
              Situação: {ROTULO_DA_SITUACAO[missao.situacao]}
              {missao.vencida ? " — vencida" : ""}
            </p>
            <p>
              Coberto: {missao.coberto} — falta: {missao.falta} — prazo:{" "}
              {formatarPrazo(missao.prazo)}
            </p>
            {missao.situacao === "aberta" && (
              <>
                <Botao
                  variante="secundaria"
                  onClick={() => aoClicarDespublicar(missao)}
                  desabilitado={despublicando === missao.id}
                >
                  Despublicar
                </Botao>
                <p>Despublicar não estorna aporte já homologado.</p>
              </>
            )}
            {erroPorMissao[missao.id] && <Aviso tipo="erro">{erroPorMissao[missao.id]}</Aviso>}
          </article>
        </li>
      ))}
    </ul>
  );
}
