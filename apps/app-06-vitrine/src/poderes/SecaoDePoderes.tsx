import { Aviso, EstadoDaLista } from "comum/react";
import { listarPoderes } from "../api/leituras";
import { useLeitura } from "../leitura/useLeitura";

// A seção de poderes do `RF-03-02`: cada poder com as **trilhas** dele. Os
// **Mestres responsáveis** que o documento 11 §8.2 pede da página do poder
// chegam com a rota de Mestres, na fatia 7 — até lá a seção sai sem eles, e
// não reserva espaço vazio nem promete o que ainda não existe (decisão do
// fundador, 2026-09-28).
export function SecaoDePoderes() {
  const estado = useLeitura(listarPoderes, "vitrine/poderes");

  if (estado.situacao === "carregando") {
    return <EstadoDaLista>Carregando os poderes…</EstadoDaLista>;
  }
  if (estado.situacao === "falhou") {
    return (
      <Aviso tipo="erro">Não foi possível carregar os poderes agora. Tente de novo.</Aviso>
    );
  }
  if (estado.dado.length === 0) {
    return <EstadoDaLista>Nenhum poder publicado por enquanto.</EstadoDaLista>;
  }

  return (
    <ul className="cg-poderes">
      {estado.dado.map((poder) => (
        <li key={poder.id} className="cg-poderes__item">
          <h3>{poder.nome}</h3>
          <p>{poder.descricao}</p>
          {poder.trilhas.length === 0 ? (
            <EstadoDaLista>Nenhuma trilha publicada neste poder ainda.</EstadoDaLista>
          ) : (
            <ul className="cg-poderes__trilhas">
              {poder.trilhas.map((trilha) => (
                <li key={trilha.id}>{trilha.nome}</li>
              ))}
            </ul>
          )}
        </li>
      ))}
    </ul>
  );
}
