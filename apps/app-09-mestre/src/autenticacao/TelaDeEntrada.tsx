import { BotaoDeEntradaGoogle, useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, Moldura } from "comum/react";
import { GOOGLE_CLIENT_ID } from "../api/configuracao";

interface Props {
  /** Recusa decidida pela própria App 09 — hoje só o Guerreiro(a), que essa
   * aplicação nunca abre sessão (PRD-09 §4). Em linguagem simples, sem
   * código de erro cru na tela. */
  mensagemDeRecusa?: string | null;
}

export function TelaDeEntrada({ mensagemDeRecusa }: Props) {
  const { entrarComGoogle, entrando, erroDeEntrada } = useSessao();

  return (
    <Moldura>
      <Cabecalho
        titulo="Comunidade Game — Mestre"
        subtitulo="Entre com a conta Google vinculada ao seu cadastro."
      />
      <BotaoDeEntradaGoogle clientId={GOOGLE_CLIENT_ID} aoReceberIdToken={entrarComGoogle} />
      {entrando && <Aviso tipo="andamento">Entrando…</Aviso>}
      {erroDeEntrada && <Aviso tipo="erro">{erroDeEntrada}</Aviso>}
      {mensagemDeRecusa && <Aviso tipo="erro">{mensagemDeRecusa}</Aviso>}
    </Moldura>
  );
}
