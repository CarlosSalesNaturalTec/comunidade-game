import { Cabecalho } from "comum/react";
import { useState } from "react";
import { DialogoDeEntrada } from "../entrada/DialogoDeEntrada";

/** O cabeçalho e o diálogo de entrada, juntos porque o botão abre o diálogo:
 * é o único estado da moldura, e por isso a moldura é ilha e o resto da tela
 * não precisa ser.
 *
 * O "Entrar" fica em toda tela pública (`RF-03-58`), e nada da escolha é
 * guardado (`RF-03-60`, `RN-03-22`). */
export function CabecalhoDaVitrine() {
  const [entradaAberta, definirEntradaAberta] = useState(false);

  return (
    <>
      <Cabecalho
        titulo="Comunidade Game"
        subtitulo="A vitrine pública do projeto — aberta, sem cadastro e sem login."
        acao={{ rotulo: "Entrar", aoAcionar: () => definirEntradaAberta(true) }}
      />
      <DialogoDeEntrada aberto={entradaAberta} aoFechar={() => definirEntradaAberta(false)} />
    </>
  );
}
