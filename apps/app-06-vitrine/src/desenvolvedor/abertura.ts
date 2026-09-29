import type { MensagemDaConversa } from "../api/desenvolvedor";

/** A abertura é **texto da própria aplicação**, e não resposta do modelo
 * (decisão do fundador de 2026-09-29): nenhuma chamada ao núcleo acontece ao
 * abrir a área, e por isso ela continua de pé com o assistente fora do ar
 * (`RF-03-68`, `RF-03-72`). Como toda mensagem do assistente, termina com a
 * pergunta de múltipla escolha do próximo passo (`RF-03-69`). */
export const TEXTO_DA_ABERTURA =
  "Olá! O Comunidade Game é uma plataforma educacional gamificada, aberta e de código " +
  "livre. Ela é uma API única — o núcleo — e oito aplicações web que a consomem: a aula " +
  "presencial, a gestão, a Área do Guerreiro(a), a dos responsáveis, a do Mestre, a do " +
  "Apoiador, o jogo e esta vitrine. Toda aplicação de terceiro fala com a API por uma " +
  "chave própria, e o contrato dela é de somente leitura: nada que você construir escreve " +
  "no domínio.";

export const OPCOES_DA_ABERTURA: readonly string[] = [
  "Como a API se autentica por chave",
  "O que o contrato de somente leitura permite",
  "Como pedir a chave de aplicação",
];

export const MENSAGEM_DE_ABERTURA: MensagemDaConversa = {
  de: "assistente",
  texto: TEXTO_DA_ABERTURA,
};
