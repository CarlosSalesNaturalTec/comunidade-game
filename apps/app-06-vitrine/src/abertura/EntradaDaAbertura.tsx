import { useState } from "react";
import { DialogoDeEntrada } from "../entrada/DialogoDeEntrada";

/**
 * O "Entrar" do herói, com o diálogo que ele abre (`RF-03-58`).
 *
 * É **ilha**, e o herói não: o diálogo tem estado, a ilustração e a frase não.
 * Assim a abertura continua saindo inteira no documento servido, e só o que
 * precisa de JS custa JS (documento 15 §1, princípio 4; PRD-03 §10).
 *
 * Na tela que tem herói este é o **único** "Entrar": `Vitrine.astro` diz ao
 * cabeçalho para não trazer o dele. Dois botões de mesmo nome na mesma tela
 * não acrescentam ação alguma e atrapalham quem navega por leitor de tela — a
 * razão de 2026-10-09 segue valendo, e o que mudou em 2026-10-10 foi **onde**
 * o botão único mora.
 *
 * Não usa o `Botao` de `comum/react`: ele oferece primária e secundária, e o
 * par da abertura quer as duas ações **cheias, em cores diferentes**. A forma
 * vem da mesma classe `cg-botao`, então o alvo de toque e o foco continuam os
 * da camada comum (documento 15 §5).
 */
export function EntradaDaAbertura() {
  const [aberto, definirAberto] = useState(false);

  return (
    <>
      <button
        type="button"
        className="cg-botao cg-botao--entrada cg-heroi__acao"
        onClick={() => definirAberto(true)}
      >
        Entrar
      </button>
      <DialogoDeEntrada aberto={aberto} aoFechar={() => definirAberto(false)} />
    </>
  );
}
