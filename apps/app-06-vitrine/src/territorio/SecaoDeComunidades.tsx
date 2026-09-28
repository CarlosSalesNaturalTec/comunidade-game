import { Aviso, CartaDoPersonagem, type DadosDaCarta, EstadoDaLista } from "comum/react";
import { type ComunidadeNaLista, listarComunidades } from "../api/leituras";
import { useLeitura } from "../leitura/useLeitura";
import type { PropsDaSecao } from "../navegacao/recortes";
import { caminhoDaComunidade } from "../navegacao/recortes";

// A seção **Comunidades Virtuais** do `RF-03-02`, com a variante Comunidade
// Virtual da carta (documento 11 §8.2). Uma **única** leitura monta todos os
// cards: uma consulta por card cairia no freio por origem, como a fatia 2 já
// evitou na carta do Guerreiro(a) (design — Decisão 7).
//
// A comunidade abaixo do piso de coletores chega com os quatro indicadores
// nulos. Carta pela metade não se apresenta: ela sai em **outra forma**, com
// o que a leitura devolveu — nome, localização e vitalidade —, e não como
// card incompleto (documento 09 §1).

function cartaDaComunidade(comunidade: ComunidadeNaLista): DadosDaCarta {
  return {
    variante: "comunidade-virtual",
    nome: comunidade.nome,
    territorio: comunidade.localizacao,
    seriesAtivas: comunidade.series_ativas,
    seriesAbertas: comunidade.series_abertas,
    vinculados: comunidade.guerreiros_vinculados,
    // A lista não traz recorte por tipo de coleta: o desenho do card é o
    // contorno com a vitalidade, e as camadas por tipo aparecem na página da
    // comunidade, que lê a série.
    camadas: [],
    bairrosPublicados: 0,
  };
}

export function SecaoDeComunidades({ irPara }: PropsDaSecao) {
  const estado = useLeitura(listarComunidades, "comunidades");

  if (estado.situacao === "carregando") {
    return <EstadoDaLista>Carregando as Comunidades Virtuais…</EstadoDaLista>;
  }
  if (estado.situacao === "falhou") {
    return (
      <Aviso tipo="erro">Não foi possível carregar as comunidades agora. Tente de novo.</Aviso>
    );
  }
  if (estado.dado.itens.length === 0) {
    return <EstadoDaLista>Nenhuma Comunidade Virtual publicada por enquanto.</EstadoDaLista>;
  }

  return (
    <ul className="cg-comunidades">
      {estado.dado.itens.map((comunidade) => {
        const dados = cartaDaComunidade(comunidade);
        return (
          <li key={comunidade.id} className="cg-comunidades__item">
            <button
              type="button"
              className="cg-comunidades__abrir"
              onClick={() => irPara(caminhoDaComunidade(comunidade.id))}
            >
              <CartaDoPersonagem dados={dados} />
              {comunidade.series_ativas === null && (
                <div className="cg-comunidades__resumo">
                  <p className="cg-comunidades__nome">{comunidade.nome}</p>
                  <p>{comunidade.localizacao}</p>
                  <p>{comunidade.guerreiros_vinculados} Guerreiros e Guerreiras vinculados</p>
                  <p className="cg-comunidades__sem-indicadores">
                    Indicadores ainda não publicados — a comunidade tem menos coletores do que
                    o piso que protege quem coletou.
                  </p>
                </div>
              )}
              <span className="cg-comunidades__chamada">Ver o território</span>
            </button>
          </li>
        );
      })}
      <li className="cg-comunidades__ciclo">Ciclo corrente: {estado.dado.ciclo_rotulo}</li>
    </ul>
  );
}
