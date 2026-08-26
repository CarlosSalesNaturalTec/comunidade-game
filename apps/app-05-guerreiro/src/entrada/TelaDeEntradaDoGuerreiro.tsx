import { useSessao } from "comum/autenticacao";
import {
  encerrarCaptura,
  existeCamera,
  gerarDescritor,
  provarVivacidade,
} from "comum/biometria";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import { abrirSessaoPorReconhecimento } from "../api/sessoesDeGuerreiro";
import { ConfirmacaoAssistida } from "./ConfirmacaoAssistida";

type Tela = "verificandoCamera" | "entrada" | "confirmando";
type MotivoDaConfirmacao = "semCamera" | "conferenciaRecusada";

const MENSAGEM_DE_RECUSA =
  "Não foi possível reconhecer. Tente de novo, com o rosto bem posicionado, ou chame um Mestre ou Admin.";

const MENSAGEM_SEM_CAMERA =
  "Esse aparelho não tem câmera para tirar sua foto. Peça ajuda a um Mestre no ponto de apoio!";

// Porta de entrada da App 05: a sessão do Guerreiro(a) é pré-requisito de
// toda tela do PRD-05 (proposal — Why). Entrada por nick e imagem primeiro,
// com a confirmação humana como alternativa de quem não tem câmera, de quem
// a conferência recusa e de quem ainda não tem imagem gravada (`RF-05-01`
// a `RF-05-04`, `RN-05-01`, `RN-05-02`).
export function TelaDeEntradaDoGuerreiro() {
  const { entrarComToken } = useSessao();
  const [nick, definirNick] = useState("");
  const [tela, definirTela] = useState<Tela>("verificandoCamera");
  const [emAndamento, definirEmAndamento] = useState(false);
  const [recusado, definirRecusado] = useState(false);
  const [motivoDaConfirmacao, definirMotivoDaConfirmacao] =
    useState<MotivoDaConfirmacao>("conferenciaRecusada");

  useEffect(() => {
    let cancelado = false;
    existeCamera().then((temCamera) => {
      if (cancelado) return;
      if (temCamera) {
        definirTela("entrada");
      } else {
        definirMotivoDaConfirmacao("semCamera");
        definirTela("confirmando");
      }
    });
    return () => {
      cancelado = true;
    };
  }, []);

  async function tentarReconhecimento() {
    definirRecusado(false);
    definirEmAndamento(true);
    try {
      const vivacidadeAprovada = await provarVivacidade();
      if (!vivacidadeAprovada) {
        definirRecusado(true);
        return;
      }
      const descritor = await gerarDescritor();
      const abertura = await abrirSessaoPorReconhecimento({ nick: nick.trim(), descritor });
      await entrarComToken(abertura.token);
    } catch {
      definirRecusado(true);
    } finally {
      encerrarCaptura();
      definirEmAndamento(false);
    }
  }

  if (tela === "verificandoCamera") {
    return null;
  }

  if (tela === "confirmando") {
    return (
      <Moldura>
        <Cabecalho
          titulo="Quem está chegando?"
          subtitulo="A criança diz o nick, e um Mestre ou Admin confirma quem ela é."
        />
        {motivoDaConfirmacao === "semCamera" && (
          <Aviso tipo="atencao">{MENSAGEM_SEM_CAMERA}</Aviso>
        )}
        <ConfirmacaoAssistida
          nick={nick}
          aoAlterarNick={definirNick}
          aoConfirmar={entrarComToken}
          aoVoltar={() => {
            definirTela("entrada");
            definirRecusado(false);
          }}
        />
      </Moldura>
    );
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Quem está chegando?"
        subtitulo="Digite o nick e olhe para a câmera."
      />
      <Campo rotulo="Nick" valor={nick} aoAlterar={definirNick} />
      <Botao
        onClick={tentarReconhecimento}
        desabilitado={emAndamento || nick.trim().length === 0}
      >
        {emAndamento ? "Reconhecendo…" : "Entrar"}
      </Botao>
      {recusado && (
        <>
          <Aviso tipo="erro">{MENSAGEM_DE_RECUSA}</Aviso>
          <Botao
            variante="secundaria"
            onClick={() => {
              definirMotivoDaConfirmacao("conferenciaRecusada");
              definirTela("confirmando");
            }}
          >
            Chamar Mestre ou Admin
          </Botao>
        </>
      )}
    </Moldura>
  );
}
