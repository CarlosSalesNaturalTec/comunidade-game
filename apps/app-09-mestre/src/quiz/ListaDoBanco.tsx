import { EstadoDaLista } from "comum/react";
import { useId } from "react";
import type { TrilhaDoMestre } from "../trilhas/api";
import type { PerguntaDeQuiz } from "./api";

interface Props {
  perguntas: PerguntaDeQuiz[] | null;
  trilhas: TrilhaDoMestre[];
  trilhaId: string;
  missaoId: string;
  aoAlterarTrilha: (trilhaId: string) => void;
  aoAlterarMissao: (missaoId: string) => void;
}

// Os dois filtros são independentes na rota (`RF-09-40`), mas a missão só
// faz sentido dentro da trilha escolhida — trocar a trilha limpa a missão.
export function ListaDoBanco({
  perguntas,
  trilhas,
  trilhaId,
  missaoId,
  aoAlterarTrilha,
  aoAlterarMissao,
}: Props) {
  const idDaTrilha = useId();
  const idDaMissao = useId();
  const trilhaSelecionada = trilhas.find((trilha) => trilha.id === trilhaId) ?? null;
  const missoesDaTrilha = trilhaSelecionada?.missoes ?? [];

  function trocarTrilha(valor: string) {
    aoAlterarTrilha(valor);
    aoAlterarMissao("");
  }

  return (
    <section aria-label="Banco de perguntas">
      <h2>Banco de perguntas</h2>

      <div className="cg-campo">
        <label htmlFor={idDaTrilha}>Filtrar por trilha</label>
        <select
          id={idDaTrilha}
          value={trilhaId}
          onChange={(evento) => trocarTrilha(evento.target.value)}
        >
          <option value="">Todas as trilhas</option>
          {trilhas.map((trilha) => (
            <option key={trilha.id} value={trilha.id}>
              {trilha.nome}
            </option>
          ))}
        </select>
      </div>

      <div className="cg-campo">
        <label htmlFor={idDaMissao}>Filtrar por missão</label>
        <select
          id={idDaMissao}
          value={missaoId}
          onChange={(evento) => aoAlterarMissao(evento.target.value)}
          disabled={!trilhaId}
        >
          <option value="">Todas as missões</option>
          {missoesDaTrilha.map((missao) => (
            <option key={missao.id} value={missao.id}>
              {missao.titulo}
            </option>
          ))}
        </select>
      </div>

      {perguntas === null && <EstadoDaLista>Carregando o banco de perguntas…</EstadoDaLista>}
      {perguntas !== null && perguntas.length === 0 && (
        <EstadoDaLista>Nenhuma pergunta cadastrada ainda.</EstadoDaLista>
      )}
      {perguntas !== null && perguntas.length > 0 && (
        <ul className="lista-do-banco-de-quiz" aria-label="Perguntas do banco">
          {perguntas.map((pergunta) => (
            <li key={pergunta.id} className="lista-do-banco-de-quiz__item">
              <p className="lista-do-banco-de-quiz__enunciado">{pergunta.enunciado}</p>
              <ul className="lista-do-banco-de-quiz__alternativas">
                {pergunta.alternativas.map((alternativa, indice) => (
                  <li
                    // biome-ignore lint/suspicious/noArrayIndexKey: a posição é o identificador da alternativa
                    key={indice}
                    className={
                      indice + 1 === pergunta.alternativa_correta
                        ? "lista-do-banco-de-quiz__alternativa--correta"
                        : undefined
                    }
                  >
                    {alternativa}
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
