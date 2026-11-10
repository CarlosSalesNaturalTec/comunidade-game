import { Aviso } from "../react/Aviso";
import type { DesafioDeDesbloqueio as Desafio } from "./api";
import { DesafioDeDesbloqueio } from "./DesafioDeDesbloqueio";

interface Props {
  missaoId: string;
  desafio: Desafio;
  /** O **Concluir** da tela final: é só ali que a trilha recarrega
   * (`RF-05-100`, design — decisão 8). */
  aoResponder: () => void;
  /** A resposta da sondagem é a mesma submissão do desbloqueio, e é ela
   * que abre a trilha — liga junto com ele (design — decisão 3). */
  submissaoLigada?: boolean;
}

// Primeiro passo de toda trilha recém inscrita: mede de onde o Guerreiro(a)
// parte, para o Mestre ajustar o que vem pela frente. Nunca é apresentada
// como prova, e a resposta não muda nível nem saldo (`RF-05-72`,
// `RF-05-73`, `RN-05-34`). É também o único quiz que responde por voz, com o
// áudio ligado (`RF-05-97`, `RN-05-54`), e o único com retorno por pergunta e
// tela final com Refazer e Concluir (`RF-05-99`, `RF-05-100`).
export function Sondagem({ missaoId, desafio, aoResponder, submissaoLigada }: Props) {
  return (
    <section aria-label="Sondagem">
      <Aviso tipo="andamento">
        Isso aqui é a sondagem — ela ajuda o Mestre a preparar o que vem pela frente. Ela não
        muda o seu nível, então relaxa e responda do seu jeito.
      </Aviso>
      <DesafioDeDesbloqueio
        missaoId={missaoId}
        desafio={desafio}
        aoDesbloquear={aoResponder}
        submissaoLigada={submissaoLigada}
        ehSondagem
      />
    </section>
  );
}
