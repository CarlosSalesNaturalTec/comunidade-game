import { useSessao } from "comum/autenticacao";
import { HistoricoDePontuacao, lerHistoricoDePontuacaoDoGuerreiro } from "comum/pontuacao";
import { Botao } from "comum/react";
import { useCallback } from "react";
import type { GuerreiroDaLista } from "./api";

interface Props {
  guerreiro: GuerreiroDaLista;
  onVoltar: () => void;
}

// A ficha do Guerreiro(a) na gestão: o nick e o histórico de pontuação com os
// saldos, para o Admin conferir como e quando cada saldo se formou
// (`RF-02-116`, `RN-01-68`).
export function FichaDoGuerreiro({ guerreiro, onVoltar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const token = sessao?.token ?? "";
  const ler = useCallback(
    (cursor: string | null) => lerHistoricoDePontuacaoDoGuerreiro(token, guerreiro.id, cursor),
    [token, guerreiro.id],
  );

  return (
    <section aria-label={`Ficha de ${guerreiro.nick}`}>
      <Botao variante="secundaria" onClick={onVoltar}>
        Voltar à lista
      </Botao>
      <h2>Ficha de {guerreiro.nick}</h2>
      <HistoricoDePontuacao ler={ler} aoRecusarSessao={tratarRecusaDeSessao} />
    </section>
  );
}
