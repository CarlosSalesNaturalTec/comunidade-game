import { Aviso, Cabecalho, Moldura } from "comum/react";
import { BotaoDeEntradaGoogle } from "./BotaoDeEntradaGoogle";
import { useSessao } from "./ContextoDeSessao";

export function TelaDeEntrada() {
  const { entrarComGoogle, entrando, erroDeEntrada } = useSessao();

  return (
    <Moldura>
      <Cabecalho
        titulo="Comunidade Game — Gestão"
        subtitulo="Entre com a conta Google vinculada ao seu cadastro."
      />
      <BotaoDeEntradaGoogle aoReceberIdToken={entrarComGoogle} />
      {entrando && <Aviso tipo="andamento">Entrando…</Aviso>}
      {erroDeEntrada && <Aviso tipo="erro">{erroDeEntrada}</Aviso>}
    </Moldura>
  );
}
