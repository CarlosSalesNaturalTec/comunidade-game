import { ErroDaApi } from "comum/api";
import { BotaoDeEntradaGoogle, ProvedorDeSessao, useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { useState } from "react";
import { GOOGLE_CLIENT_ID } from "../api/configuracao";
import { confirmarSessaoDeGuerreiro } from "../api/sessoesDeGuerreiro";

const CHAVE_DE_SESSAO_ADULTO = "app-05:sessao-adulto";

interface Props {
  nick: string;
  aoAlterarNick: (nick: string) => void;
  aoConfirmar: (token: string) => Promise<void>;
  aoVoltar: () => void;
}

// A sessão do adulto vive só durante este ato: um `ProvedorDeSessao`
// próprio, com chave de armazenamento distinta da sessão do Guerreiro(a),
// que o componente interno encerra assim que a confirmação abre a sessão da
// criança — o Mestre ou Admin nunca opera a aplicação em nome dela
// (`RF-05-03`, `RF-05-04`, `RN-05-02`, design — decisão 6).
export function ConfirmacaoAssistida(props: Props) {
  return (
    <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO_ADULTO}>
      <ConteudoDaConfirmacaoAssistida {...props} />
    </ProvedorDeSessao>
  );
}

function ConteudoDaConfirmacaoAssistida({
  nick,
  aoAlterarNick,
  aoConfirmar,
  aoVoltar,
}: Props) {
  const { sessao, entrando, erroDeEntrada, entrarComGoogle, sair } = useSessao();
  const [confirmando, definirConfirmando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);

  async function confirmar() {
    if (!sessao) return;
    definirErro(null);
    definirConfirmando(true);
    try {
      const abertura = await confirmarSessaoDeGuerreiro(nick.trim(), sessao.token);
      await sair();
      await aoConfirmar(abertura.token);
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível confirmar. Tente novamente.",
      );
    } finally {
      definirConfirmando(false);
    }
  }

  return (
    <>
      <Campo rotulo="Nick" valor={nick} aoAlterar={aoAlterarNick} />
      {!sessao && (
        <>
          <p>Mestre ou Admin: entrem para confirmar quem está chegando.</p>
          <BotaoDeEntradaGoogle
            clientId={GOOGLE_CLIENT_ID}
            aoReceberIdToken={entrarComGoogle}
          />
          {entrando && <Aviso tipo="andamento">Entrando…</Aviso>}
          {erroDeEntrada && <Aviso tipo="erro">{erroDeEntrada}</Aviso>}
        </>
      )}
      {sessao && (
        <Botao onClick={confirmar} desabilitado={confirmando || nick.trim().length === 0}>
          {confirmando ? "Confirmando…" : "Confirmar identidade"}
        </Botao>
      )}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Botao variante="secundaria" onClick={aoVoltar}>
        Voltar
      </Botao>
    </>
  );
}
