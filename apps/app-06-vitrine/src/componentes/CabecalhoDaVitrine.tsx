import { Cabecalho } from "comum/react";

/** O cabeçalho da vitrine: a saudação, e só.
 *
 * O nome do projeto **não se repete aqui**: ele é da `MarcaDoProjeto`, logo
 * acima, que o apresenta nas oito aplicações. O que o cabeçalho diz é a
 * saudação, e dentro dela a ideia do jogo — as partidas acontecem na vida real
 * (decisão do fundador de 2026-11-12). A vitrine segue sem cadastro e sem
 * login (`RF-03-51`, `RN-03-01`): isso é cumprido pela aplicação, não pela frase.
 *
 * **Não traz o "Entrar".** Na vitrine ele existe uma vez, no herói da
 * abertura, e nenhuma outra tela pública o apresenta (`RF-03-58`, documento 03
 * §8, decisão do fundador de 2026-10-10). Quem está em outra tela chega à
 * abertura pela marca.
 *
 * Por isso este componente **não tem estado e não é ilha**: sem o botão não há
 * diálogo a abrir, e o cabeçalho sai no documento servido sem custar JS em
 * tela nenhuma (documento 15 §1, princípio 4). */
export function CabecalhoDaVitrine() {
  return (
    <Cabecalho
      titulo="Boas-vindas!"
      subtitulo="Este é um jogo em que as partidas acontecem na vida real"
    />
  );
}
