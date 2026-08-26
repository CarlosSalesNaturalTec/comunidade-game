import { ProvedorDeSessao } from "comum/autenticacao";
import { AparelhoDaAreaDoGuerreiro } from "./entrada/AparelhoDaAreaDoGuerreiro";

// Chave própria de `sessionStorage`, distinta da sessão do adulto que a
// confirmação assistida abre e encerra em seguida (design — decisão 6).
export const CHAVE_DE_SESSAO_GUERREIRO = "app-05:sessao-guerreiro";

export default function App() {
  return (
    <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO_GUERREIRO}>
      <AparelhoDaAreaDoGuerreiro />
    </ProvedorDeSessao>
  );
}
