import { Aviso, EstadoDaLista } from "comum/react";
import { listarPoderes } from "../api/leituras";
import { useLeitura } from "../leitura/useLeitura";
import { PREFIXO_DA_PAGINA_DO_MESTRE } from "../navegacao/caminhos";

// A seção de poderes do `RF-03-02`: cada poder com as **trilhas** dele e os
// **Mestres responsáveis** que o documento 11 §8.2 pede — os autores das
// trilhas publicadas daquele poder, cada um levando à página individual dele
// (decisão do fundador, 2026-09-29). Poder sem trilha publicada não tem
// responsável, e a seção **não reserva espaço vazio** para ele (decisão do
// fundador, 2026-09-28).

interface Props {
  irPara: (destino: string) => void;
}

export function SecaoDePoderes({ irPara }: Props) {
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
      {estado.dado.map((poder) => {
        // Leitura incompleta não derruba a tela: a seção segue com o que
        // veio, como toda leitura pública desta App.
        const responsaveis = poder.mestres_responsaveis ?? [];
        return (
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
            {responsaveis.length > 0 && (
              <>
                <p className="cg-poderes__rotulo">Mestres responsáveis</p>
                <ul className="cg-poderes__mestres">
                  {responsaveis.map((mestre) => (
                    <li key={mestre.id}>
                      <button
                        type="button"
                        onClick={() =>
                          irPara(
                            `${PREFIXO_DA_PAGINA_DO_MESTRE}${encodeURIComponent(mestre.id)}`,
                          )
                        }
                      >
                        {mestre.identificacao.valor}
                      </button>
                    </li>
                  ))}
                </ul>
              </>
            )}
          </li>
        );
      })}
    </ul>
  );
}
