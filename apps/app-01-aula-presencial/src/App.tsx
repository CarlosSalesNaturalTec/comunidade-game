import { ProvedorDeSessao } from "comum/autenticacao";
import { AparelhoDaAula } from "./sessao-de-trabalho/AparelhoDaAula";

// A sessão de trabalho do aparelho — Mestre ou Admin, dura a janela da
// aula (`RF-04-05`, `RN-04-29`) — vive numa chave própria de
// `sessionStorage`, distinta da sessão do Guerreiro(a) que a área de
// trilhas abre em seguida (design — decisão 1).
export const CHAVE_DE_SESSAO_DE_TRABALHO = "app-01:sessao-trabalho";

export default function App() {
  return (
    <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO_DE_TRABALHO}>
      <AparelhoDaAula />
    </ProvedorDeSessao>
  );
}
