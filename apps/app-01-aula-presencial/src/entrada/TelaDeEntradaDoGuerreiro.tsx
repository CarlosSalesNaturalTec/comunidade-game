import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { eu } from "comum/autenticacao/api";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { useState } from "react";
import { registrarPresenca } from "../api/presencas";
import {
  abrirSessaoPorReconhecimento,
  confirmarSessaoDeGuerreiro,
} from "../api/sessoesDeGuerreiro";
import {
  encerrarCaptura,
  existeCamera,
  gerarDescritor,
  provarVivacidade,
} from "../biometria/biometria";

interface Props {
  tokenDeTrabalho: string;
  aulaId: string;
  aoVoltar: () => void;
  /** Avisa por qual caminho a sessão do Guerreiro(a) abriu — é o que
   * autoriza o recadastro da imagem atrás da confirmação presencial
   * (`RF-04-22`, design — decisão 4). */
  aoAbrirSessao?: (via: "reconhecimento" | "confirmacao") => void;
}

type Tela = "entrada" | "confirmando" | "presencaJaRegistrada";

const MENSAGEM_DE_RECUSA =
  "Não foi possível reconhecer. Tente de novo, com o rosto bem posicionado, ou chame um Mestre ou Admin.";

// A entrada por nick e imagem entra antes da confirmação humana, que passa
// a ser a alternativa de quem não tem câmera, de quem a recusa persiste e
// de quem não tem _template_ (`RF-04-18`, `RF-04-29`, `RN-04-09`, design —
// decisão 5). A recusa do núcleo — nick inexistente, sem _template_ ou
// descritor que não confere — é sempre a mesma frase (`RF-04-20`,
// `RN-01-22`).
export function TelaDeEntradaDoGuerreiro({
  tokenDeTrabalho,
  aulaId,
  aoVoltar,
  aoAbrirSessao,
}: Props) {
  const { entrarComToken } = useSessao();
  const [nick, definirNick] = useState("");
  const [tela, definirTela] = useState<Tela>("entrada");
  const [emAndamento, definirEmAndamento] = useState(false);
  const [recusado, definirRecusado] = useState(false);
  const [erroDeConfirmacao, definirErroDeConfirmacao] = useState<string | null>(null);

  // Grava a presença no mesmo ato em que a sessão abre, sempre com o token
  // da sessão de trabalho (`RF-04-18`, `RF-04-21`). Só o reconhecimento
  // bloqueia a entrada quando a presença já constava — comparando o
  // momento do fato como instante, não como texto, porque o núcleo
  // devolve a data com precisão diferente da enviada (`RF-04-19`, design —
  // decisão 3).
  async function registrarPresencaEEntrar(
    token: string,
    modo: "reconhecimento" | "confirmacao",
  ): Promise<void> {
    const quemSou = await eu(token);
    const momentoDoFato = new Date().toISOString();
    const presenca = await registrarPresenca(
      aulaId,
      { guerreiro_id: quemSou.persona_id, modo, momento_do_fato: momentoDoFato },
      tokenDeTrabalho,
    );
    const jaConstava =
      modo === "reconhecimento" &&
      new Date(presenca.momento_do_fato).getTime() !== new Date(momentoDoFato).getTime();
    if (jaConstava) {
      definirTela("presencaJaRegistrada");
      return;
    }
    aoAbrirSessao?.(modo);
    await entrarComToken(token);
  }

  async function tentarReconhecimento() {
    definirRecusado(false);
    definirEmAndamento(true);
    try {
      const temCamera = await existeCamera();
      if (!temCamera) {
        definirTela("confirmando");
        return;
      }
      const vivacidadeAprovada = await provarVivacidade();
      if (!vivacidadeAprovada) {
        definirRecusado(true);
        return;
      }
      const descritor = await gerarDescritor();
      const abertura = await abrirSessaoPorReconhecimento({ nick: nick.trim(), descritor });
      await registrarPresencaEEntrar(abertura.token, "reconhecimento");
    } catch {
      definirRecusado(true);
    } finally {
      encerrarCaptura();
      definirEmAndamento(false);
    }
  }

  async function confirmar() {
    definirErroDeConfirmacao(null);
    definirEmAndamento(true);
    try {
      const abertura = await confirmarSessaoDeGuerreiro(nick.trim(), tokenDeTrabalho);
      await registrarPresencaEEntrar(abertura.token, "confirmacao");
    } catch (erroCapturado) {
      definirErroDeConfirmacao(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível confirmar. Tente novamente.",
      );
    } finally {
      definirEmAndamento(false);
    }
  }

  if (tela === "presencaJaRegistrada") {
    return (
      <Moldura>
        <Cabecalho titulo="Presença já registrada" />
        <Aviso tipo="atencao">
          A presença deste Guerreiro(a) já constava nesta aula. Nada foi duplicado.
        </Aviso>
        <Botao onClick={aoVoltar}>Voltar ao início</Botao>
      </Moldura>
    );
  }

  if (tela === "confirmando") {
    return (
      <Moldura>
        <Cabecalho
          titulo="Quem está chegando?"
          subtitulo="A criança diz o nick, e um Mestre ou Admin confirma quem ela é."
          acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
        />
        <Campo rotulo="Nick" valor={nick} aoAlterar={definirNick} />
        <Botao onClick={confirmar} desabilitado={emAndamento || nick.trim().length === 0}>
          {emAndamento ? "Confirmando…" : "Confirmar identidade"}
        </Botao>
        {erroDeConfirmacao && <Aviso tipo="erro">{erroDeConfirmacao}</Aviso>}
      </Moldura>
    );
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Quem está chegando?"
        subtitulo="Digite o nick e olhe para a câmera."
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
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
          <Botao variante="secundaria" onClick={() => definirTela("confirmando")}>
            Chamar Mestre ou Admin
          </Botao>
        </>
      )}
    </Moldura>
  );
}
