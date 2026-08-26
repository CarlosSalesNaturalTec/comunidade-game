import { useSessao } from "comum/autenticacao";
import { AreaDoGuerreiro } from "./AreaDoGuerreiro";
import { TelaDeEntradaDoGuerreiro } from "./TelaDeEntradaDoGuerreiro";

// Sem sessão aberta, só o pedido de nick aparece — a App 05 é inteiramente
// autenticada, sem tela de visitante (`RF-05-01`, PRD-05 §4).
export function AparelhoDaAreaDoGuerreiro() {
  const { sessao, restaurando } = useSessao();

  if (restaurando) {
    return null;
  }

  if (!sessao) {
    return <TelaDeEntradaDoGuerreiro />;
  }

  return <AreaDoGuerreiro />;
}
