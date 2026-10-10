import { Cabecalho } from "comum/react";
import { useState } from "react";
import { DialogoDeEntrada } from "../entrada/DialogoDeEntrada";

interface Props {
  /** Traz o "Entrar"? A tela que abre com herói diz que **não**: ali o botão é
   * do herói, ao lado do "Quero participar". O botão é **um só por tela**
   * (`RF-03-58`, decisão do fundador de 2026-10-10). */
  comEntrar?: boolean;
}

/** O cabeçalho e o diálogo de entrada, juntos porque o botão abre o diálogo:
 * é o único estado da moldura, e por isso a moldura é ilha e o resto da tela
 * não precisa ser.
 *
 * O nome do projeto **não se repete aqui**: ele é da `MarcaDoProjeto`, logo
 * acima, que o apresenta nas oito aplicações. O que o cabeçalho da vitrine diz
 * é a saudação, e dentro dela a promessa que distingue esta aplicação — nada
 * aqui pede cadastro nem login (`RF-03-51`, `RN-03-01`).
 *
 * Nada da escolha de persona é guardado (`RF-03-60`, `RN-03-22`). */
export function CabecalhoDaVitrine({ comEntrar = true }: Props) {
  const [entradaAberta, definirEntradaAberta] = useState(false);

  return (
    <>
      <Cabecalho
        titulo="Boas-vindas!"
        subtitulo="Tudo aqui é aberto — sem cadastro e sem login."
        acao={
          comEntrar
            ? { rotulo: "Entrar", aoAcionar: () => definirEntradaAberta(true) }
            : undefined
        }
      />
      {comEntrar && (
        <DialogoDeEntrada
          aberto={entradaAberta}
          aoFechar={() => definirEntradaAberta(false)}
        />
      )}
    </>
  );
}
