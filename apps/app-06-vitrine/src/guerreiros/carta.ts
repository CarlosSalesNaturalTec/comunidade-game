import type { DadosDaCarta, FamiliaDeBadge } from "comum/react";
import type { GuerreiroPublico } from "../api/leituras";

// Da resposta pública para a **carta do personagem** de `comum/react`, na
// variante Guerreiro(a) do documento 11 §8.2. A carta não tem campo de
// imagem real, nome civil, rede social ou canal de contato, e é por não
// existir que nenhuma tela os põe nela (`RF-03-06`, invariantes 9 e 10).

const FAMILIAS: Record<string, FamiliaDeBadge> = {
  de_nivel: "de_nivel",
  de_conquista: "de_conquista",
  de_valores_e_causas: "de_valores_e_causas",
  de_territorio: "de_territorio",
  de_autoria: "de_autoria",
  de_protagonismo: "de_protagonismo",
};

export const FORMATADOR_DE_DATA = new Intl.DateTimeFormat("pt-BR", { dateStyle: "short" });

/** A leitura como ela chega. Cada campo é opcional aqui **de propósito**:
 * quem decide se a carta se apresenta é `cartaEstaCompleta`, e para decidir
 * ela precisa poder receber `undefined` — leitura incompleta não pode
 * derrubar a tela nem virar carta pela metade (documento 11 §8.2). */
export type LeituraDoGuerreiro = Partial<GuerreiroPublico>;

/** O desempenho que o §8.2 exige da variante, em uma frase: a posição no
 * ranking público e os pontos regulares acumulados. */
export function desempenhoDoGuerreiro(guerreiro: LeituraDoGuerreiro): string | undefined {
  if (guerreiro.pontos_regulares === undefined || guerreiro.posicao_no_ranking === undefined) {
    return undefined;
  }
  const pontos =
    guerreiro.pontos_regulares === 1 ? "1 ponto" : `${guerreiro.pontos_regulares} pontos`;
  return `${guerreiro.posicao_no_ranking}º no ranking · ${pontos} regulares`;
}

export function cartaDoGuerreiro(guerreiro: LeituraDoGuerreiro): DadosDaCarta {
  return {
    variante: "guerreiro",
    avatar: guerreiro.avatar,
    nick: guerreiro.nick,
    badges: guerreiro.badges?.map((badge) => ({
      familia: FAMILIAS[badge.familia] ?? "de_nivel",
      poder: badge.poder ?? undefined,
    })),
    poderes: guerreiro.poderes,
    desempenho: desempenhoDoGuerreiro(guerreiro),
    criacoes: guerreiro.criacoes?.map(
      (criacao) =>
        `${criacao.trilha} — ${FORMATADOR_DE_DATA.format(new Date(criacao.validada_em))}`,
    ),
  };
}
