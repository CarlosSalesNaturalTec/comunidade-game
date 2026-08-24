import { BotaoDeEntradaGoogle, useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, Moldura } from "comum/react";
import { GOOGLE_CLIENT_ID } from "../api/configuracao";

interface Props {
  /** Recusa decidida pela própria App 01 — o Guerreiro(a) nunca abre a
   * sessão de trabalho do aparelho (`RF-04-05`). */
  mensagemDeRecusa?: string | null;
}

export function TelaDeEntradaDeTrabalho({ mensagemDeRecusa }: Props) {
  const { entrarComGoogle, entrando, erroDeEntrada } = useSessao();

  return (
    <Moldura>
      <Cabecalho
        titulo="Comunidade Game — Aula"
        subtitulo="Mestre ou Admin: entre para abrir a sessão de trabalho deste aparelho."
      />
      <BotaoDeEntradaGoogle clientId={GOOGLE_CLIENT_ID} aoReceberIdToken={entrarComGoogle} />
      {entrando && <Aviso tipo="andamento">Entrando…</Aviso>}
      {erroDeEntrada && <Aviso tipo="erro">{erroDeEntrada}</Aviso>}
      {mensagemDeRecusa && <Aviso tipo="erro">{mensagemDeRecusa}</Aviso>}
    </Moldura>
  );
}
