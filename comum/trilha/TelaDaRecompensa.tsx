import { Botao } from "../react/Botao";
import { RetornoDeConquista } from "../react/RetornoDeConquista";
import { TrioDeEstrelas } from "../react/TrioDeEstrelas";
import type { RecompensaConquistada } from "./api";

interface Props {
  recompensa: RecompensaConquistada;
  /** O avançar: grava a ciência e segue. Quem monta é dono do que vem depois
   * — a próxima recompensa da fila, ou a missão. */
  aoAvancar: () => void;
  /** Enquanto a ciência está sendo gravada, para o toque repetido não
   * disparar duas vezes numa rede ruim. */
  gravando?: boolean;
}

// O que foi conquistado, dito em uma linha: "1 Camisa do Comunidade Game".
// A unidade entra só quando diz algo além do nome — tipo de recurso cuja
// unidade é "unidade" viraria "1 unidade de Camisa", que é pior do que
// "1 Camisa" para quem tem 6 anos (`RF-05-45`).
export function descreverRecompensa(recompensa: {
  tipo_de_recurso_nome: string;
  tipo_de_recurso_unidade: string;
  quantidade: number;
}): string {
  const quantidade = Number(recompensa.quantidade);
  const unidade = recompensa.tipo_de_recurso_unidade.trim();
  const nome = recompensa.tipo_de_recurso_nome.trim();
  const temUnidadePropria = unidade !== "" && unidade.toLowerCase() !== "unidade";
  return temUnidadePropria ? `${quantidade} ${unidade} de ${nome}` : `${quantidade} ${nome}`;
}

// A **tela da recompensa de desbloqueio**: entra depois do marco alcançado e
// **antes** da próxima missão, por decisão do fundador de 2026-10-19, que
// quita o `RF-05-45` — requisito essencial que nunca havia sido implementado,
// porque a lista de conquistas da App 05 cobria só a metade "lê".
//
// Quatro elementos, nesta ordem:
//
// 1. o **trio de estrelas**, que é a exceção declarada ao documento 15 §9;
// 2. o **nome** do que foi conquistado, com a quantidade — a via que não
//    depende da forma nem da cor (§5);
// 3. o aviso de que **o Mestre confirma a entrega**, que a §5.6.1 do PRD-05
//    **obriga**: sem ele a criança sai achando que já recebeu o livro;
// 4. o **avançar**, que grava a ciência e leva adiante.
//
// Uma decisão por tela (documento 15 §6): aqui a única é avançar. Nenhum
// caminho de aquisição é oferecido e nenhum valor em moedas ou reais aparece
// — recompensa de marco se conquista e nunca se compra (`RF-05-46`,
// invariantes 16 e 23) —, e nenhum ponto é creditado por este caminho.
export function TelaDaRecompensa({ recompensa, aoAvancar, gravando = false }: Props) {
  return (
    <section aria-label="Recompensa conquistada" className="cg-trilha__recompensa">
      {/* O fato é `missao_desbloqueada`, um dos quatro do documento 11 §8.5 —
          e ele é real aqui, porque esta tela só existe depois do desbloqueio.
          O movimento é a segunda via: o texto abaixo diz tudo sozinho, e
          `prefers-reduced-motion` suprime a animação pelos tokens. */}
      <RetornoDeConquista fato="missao_desbloqueada">
        <TrioDeEstrelas />
      </RetornoDeConquista>

      <h3>Você conquistou!</h3>
      <p className="cg-trilha__recompensa-descricao">{descreverRecompensa(recompensa)}</p>
      <p>Peça ao seu Mestre no próximo encontro — é ele que confirma a entrega.</p>

      <Botao onClick={aoAvancar} desabilitado={gravando}>
        {gravando ? "Avançando…" : "Avançar"}
      </Botao>
    </section>
  );
}
