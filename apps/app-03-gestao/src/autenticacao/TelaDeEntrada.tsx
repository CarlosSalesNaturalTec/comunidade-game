import { BotaoDeEntradaGoogle, useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, Moldura } from "comum/react";
import { GOOGLE_CLIENT_ID } from "../api/configuracao";

export function TelaDeEntrada() {
  const { entrarComGoogle, entrando, erroDeEntrada } = useSessao();

  return (
    <Moldura>
      <Cabecalho
        titulo="Comunidade Game — Gestão"
        subtitulo="Entre com a conta Google vinculada ao seu cadastro."
      />
      <BotaoDeEntradaGoogle clientId={GOOGLE_CLIENT_ID} aoReceberIdToken={entrarComGoogle} />
      {entrando && <Aviso tipo="andamento">Entrando…</Aviso>}
      {erroDeEntrada && <Aviso tipo="erro">{erroDeEntrada}</Aviso>}
    </Moldura>
  );
}
