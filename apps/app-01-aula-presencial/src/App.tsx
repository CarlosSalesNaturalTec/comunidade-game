import { ProvedorDeSessao } from "comum/autenticacao";
import { ProvedorDeNarracao } from "comum/narracao";
import { AparelhoDaAula } from "./sessao-de-trabalho/AparelhoDaAula";

// A sessão de trabalho do aparelho — Mestre ou Admin, dura a janela da
// aula (`RF-04-05`, `RN-04-29`) — vive numa chave própria de
// `sessionStorage`, distinta da sessão do Guerreiro(a) que a área de
// trilhas abre em seguida (design — decisão 1).
export const CHAVE_DE_SESSAO_DE_TRABALHO = "app-01:sessao-trabalho";

export default function App() {
  return (
    // A narração das telas envolve a aplicação inteira, como a sessão de
    // trabalho: o estado dela é do **aparelho**, não do atendimento, e por
    // isso NUNCA cai junto com a sessão (documento 15 §5.1).
    <ProvedorDeNarracao>
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO_DE_TRABALHO}>
        <AparelhoDaAula />
      </ProvedorDeSessao>
    </ProvedorDeNarracao>
  );
}
