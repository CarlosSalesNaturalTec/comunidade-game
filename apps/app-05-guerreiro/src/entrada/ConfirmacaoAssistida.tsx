import { ErroDaApi } from "comum/api";
import { BotaoDeEntradaGoogle, ProvedorDeSessao, useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useState } from "react";
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
// criança — o adulto nunca opera a aplicação em nome dela (`RF-05-03`,
// `RF-05-04`, `RN-05-02`, design — decisão 6).
export function ConfirmacaoAssistida(props: Props) {
  return (
    <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO_ADULTO}>
      <ConteudoDaConfirmacaoAssistida {...props} />
    </ProvedorDeSessao>
  );
}

// A troca da senha provisória acontece **aqui dentro**, e não noutra
// aplicação: o primeiro uso da credencial do responsável costuma ser
// justamente o resgate da criança depois de uma recusa, e mandá-lo sair para
// trocar a senha terminaria o atendimento com os dois sem porta (`RF-01-12`,
// `RF-14-09`, design — decisão 4).
function TrocaDaSenhaProvisoria() {
  const { trocarSenhaProvisoria, trocandoSenha, erroDeTrocaDeSenha } = useSessao();
  const [senhaNova, definirSenhaNova] = useState("");
  const [confirmacao, definirConfirmacao] = useState("");
  const [erroLocal, definirErroLocal] = useState<string | null>(null);

  function aoEnviar(evento: FormEvent) {
    evento.preventDefault();
    if (senhaNova !== confirmacao) {
      definirErroLocal("As duas senhas precisam ser iguais.");
      return;
    }
    definirErroLocal(null);
    trocarSenhaProvisoria(senhaNova);
  }

  return (
    <>
      <Aviso tipo="atencao">
        Esta senha foi criada pela gestão. Troque-a para continuar — a confirmação segue logo
        depois.
      </Aviso>
      <form onSubmit={aoEnviar}>
        <Campo
          rotulo="Senha nova"
          tipo="password"
          valor={senhaNova}
          aoAlterar={definirSenhaNova}
        />
        <Campo
          rotulo="Confirme a senha nova"
          tipo="password"
          valor={confirmacao}
          aoAlterar={definirConfirmacao}
        />
        <Botao tipo="submit" desabilitado={trocandoSenha}>
          Trocar senha
        </Botao>
      </form>
      {trocandoSenha && <Aviso tipo="andamento">Trocando…</Aviso>}
      {erroLocal && <Aviso tipo="erro">{erroLocal}</Aviso>}
      {erroDeTrocaDeSenha && <Aviso tipo="erro">{erroDeTrocaDeSenha}</Aviso>}
    </>
  );
}

// Os **dois** caminhos de login que o documento 03 §1.1 dá ao adulto — social
// e usuário e senha. Oferecer só um deles trancaria fora quem tem o outro,
// que é o mesmo defeito que esta fatia corrige (design — decisão 3).
function EntradaDoAdulto() {
  const { entrarComGoogle, entrarComCredencial, entrando, erroDeEntrada } = useSessao();
  const [usuario, definirUsuario] = useState("");
  const [senha, definirSenha] = useState("");

  function aoEnviar(evento: FormEvent) {
    evento.preventDefault();
    entrarComCredencial(usuario, senha);
  }

  return (
    <>
      <p>Responsável, Mestre ou Admin: entrem para confirmar quem está chegando.</p>
      <BotaoDeEntradaGoogle clientId={GOOGLE_CLIENT_ID} aoReceberIdToken={entrarComGoogle} />
      <form onSubmit={aoEnviar}>
        <Campo rotulo="Usuário" valor={usuario} aoAlterar={definirUsuario} />
        <Campo rotulo="Senha" tipo="password" valor={senha} aoAlterar={definirSenha} />
        <Botao
          tipo="submit"
          desabilitado={entrando || usuario.trim().length === 0 || senha.length === 0}
        >
          Entrar com usuário e senha
        </Botao>
      </form>
      {entrando && <Aviso tipo="andamento">Entrando…</Aviso>}
      {erroDeEntrada && <Aviso tipo="erro">{erroDeEntrada}</Aviso>}
    </>
  );
}

function ConteudoDaConfirmacaoAssistida({
  nick,
  aoAlterarNick,
  aoConfirmar,
  aoVoltar,
}: Props) {
  const { sessao, sair, trocaDeSenhaPendente } = useSessao();
  const [confirmando, definirConfirmando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);

  async function confirmar() {
    if (!sessao) return;
    definirErro(null);
    definirConfirmando(true);
    try {
      // O núcleo é quem confere o escopo: o responsável só alcança quem está
      // sob a responsabilidade dele, e a recusa por criança alheia chega aqui
      // idêntica à recusa por nick inexistente. A tela não pode desfazer isso
      // escrevendo "essa criança não é sua" (`RN-01-58`, `RN-01-22`).
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
      {!sessao && !trocaDeSenhaPendente && <EntradaDoAdulto />}
      {trocaDeSenhaPendente && <TrocaDaSenhaProvisoria />}
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
