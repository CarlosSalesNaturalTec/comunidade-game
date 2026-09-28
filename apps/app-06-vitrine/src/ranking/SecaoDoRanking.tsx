import { Aviso, EstadoDaLista } from "comum/react";
import { listarRanking } from "../api/leituras";
import { useLeitura } from "../leitura/useLeitura";

// O ranking público do `RF-03-09`: **só pontos regulares** e **só quem tem
// divulgação autorizada**, portão que o núcleo aplica (`RN-03-02`). Ponto
// extra, moeda e valor em reais não entram aqui (invariante 16 do documento
// 99 §6).
export function SecaoDoRanking() {
  const estado = useLeitura(listarRanking, "vitrine/rankings");

  if (estado.situacao === "carregando") {
    return <EstadoDaLista>Carregando o ranking…</EstadoDaLista>;
  }
  if (estado.situacao === "falhou") {
    return (
      <Aviso tipo="erro">Não foi possível carregar o ranking agora. Tente de novo.</Aviso>
    );
  }
  if (estado.dado.itens.length === 0) {
    return <EstadoDaLista>Nenhuma posição publicada por enquanto.</EstadoDaLista>;
  }

  return (
    <ol className="cg-ranking">
      {estado.dado.itens.map((item) => (
        <li key={item.nick}>
          <span className="cg-ranking__posicao">{item.posicao}º</span> {item.nick} —{" "}
          {item.pontos_regulares} pontos regulares
        </li>
      ))}
    </ol>
  );
}
