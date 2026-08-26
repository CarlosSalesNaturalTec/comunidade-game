import { Botao } from "comum/react";
import { useState } from "react";
import type { SerieDoGuerreiro } from "../api/coleta";
import { AbrirSerie } from "./AbrirSerie";
import { HistoricoDaSerie } from "./HistoricoDaSerie";
import { ListaDeSeries } from "./ListaDeSeries";
import { RegistrarMedicao } from "./RegistrarMedicao";
import { type ContextoDeNovoPedido, SolicitacoesDeLocal } from "./SolicitacoesDeLocal";

type Tela =
  | { nome: "lista" }
  | { nome: "abrir" }
  | { nome: "solicitacoes"; contexto: ContextoDeNovoPedido | null }
  | { nome: "registrar"; serie: SerieDoGuerreiro }
  | { nome: "historico"; serie: SerieDoGuerreiro };

// O bloco da coleta na Área do Guerreiro(a) em sessão — do abrir série ao
// histórico, sem exibir nenhum dado de outra criança em nenhuma tela
// (`RN-05-21`, proposal — App 05).
export function Coleta() {
  const [tela, definirTela] = useState<Tela>({ nome: "lista" });
  const [versaoDaLista, definirVersaoDaLista] = useState(0);

  function voltarParaLista() {
    definirVersaoDaLista((versao) => versao + 1);
    definirTela({ nome: "lista" });
  }

  if (tela.nome === "abrir") {
    return (
      <div className="cg-coleta">
        <Botao variante="secundaria" onClick={voltarParaLista}>
          Voltar
        </Botao>
        <AbrirSerie
          aoAbrir={voltarParaLista}
          aoSolicitarLocalFaltante={(contexto) =>
            definirTela({ nome: "solicitacoes", contexto })
          }
        />
      </div>
    );
  }

  if (tela.nome === "solicitacoes") {
    return (
      <div className="cg-coleta">
        <Botao variante="secundaria" onClick={voltarParaLista}>
          Voltar
        </Botao>
        <SolicitacoesDeLocal contexto={tela.contexto} />
      </div>
    );
  }

  if (tela.nome === "registrar") {
    return (
      <div className="cg-coleta">
        <Botao variante="secundaria" onClick={voltarParaLista}>
          Voltar
        </Botao>
        <RegistrarMedicao serie={tela.serie} aoConcluir={voltarParaLista} />
      </div>
    );
  }

  if (tela.nome === "historico") {
    return (
      <div className="cg-coleta">
        <HistoricoDaSerie serie={tela.serie} aoVoltar={voltarParaLista} />
      </div>
    );
  }

  return (
    <div className="cg-coleta">
      <ListaDeSeries
        key={versaoDaLista}
        aoAbrirNovaSerie={() => definirTela({ nome: "abrir" })}
        aoVerSolicitacoes={() => definirTela({ nome: "solicitacoes", contexto: null })}
        aoRegistrarNaSerie={(serie) => definirTela({ nome: "registrar", serie })}
        aoVerHistorico={(serie) => definirTela({ nome: "historico", serie })}
      />
    </div>
  );
}
