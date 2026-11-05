import type { EstadoDaVivacidade } from "comum/biometria";

// O retorno a quem opera é **abstrato**: diz o que o laço de detecção está
// vendo, nunca mostra a imagem capturada (`RF-04-64`, `RN-04-34`, documento 03
// §3.3, documento 99 §6 invariante 12).
//
// A redação é da App 01 porque o público dela é **quem opera o aparelho** — o
// Mestre ou o Admin do ponto de apoio. A entrada da App 05 fala com uma
// criança de 6 anos e declara as suas próprias frases (`RF-05-95`, PRD-05
// §10).
const FRASE_DO_LACO: Record<EstadoDaVivacidade, string> = {
  procurando_rosto: "Procurando um rosto…",
  rosto_encontrado: "Rosto encontrado. Confirmando que há uma pessoa…",
  vivacidade_confirmada: "Pessoa confirmada.",
};

export function fraseDoLaco(estado: EstadoDaVivacidade | null): string | null {
  return estado && FRASE_DO_LACO[estado];
}
