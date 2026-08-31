import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { eu } from "comum/autenticacao/api";
import {
  encerrarCaptura,
  existeCamera,
  gerarDescritor,
  provarVivacidade,
} from "comum/biometria";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { useState } from "react";
import { registrarPresenca } from "../api/presencas";
import {
  abrirSessaoPorReconhecimento,
  confirmarSessaoDeGuerreiro,
} from "../api/sessoesDeGuerreiro";
import { enfileirarPresenca } from "../fila/filaDePresenca";
import { useEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";

interface Props {
  tokenDeTrabalho: string;
  aulaId: string;
  aoVoltar: () => void;
  /** Avisa por qual caminho a sessão do Guerreiro(a) abriu — é o que
   * autoriza o recadastro da imagem atrás da confirmação presencial
   * (`RF-04-22`, design — decisão 4). */
  aoAbrirSessao?: (via: "reconhecimento" | "confirmacao") => void;
}

type Tela = "entrada" | "confirmando" | "presencaJaRegistrada" | "presencaEnfileirada";

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
  const { semRede } = useEstadoDeRede();
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
    // Sem rede, a presença não se perde: entra na fila local do aparelho e
    // sincroniza sozinha depois — nunca abre sessão nem tenta a chamada
    // (`RF-04-23`, `RN-04-12`, `RN-04-13`, design — decisões 7, 8).
    if (semRede) {
      enfileirarPresenca({
        aula_id: aulaId,
        nick: nick.trim(),
        momento_do_fato: new Date().toISOString(),
      });
      definirTela("presencaEnfileirada");
      return;
    }
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

  if (tela === "presencaEnfileirada") {
    return (
      <Moldura>
        <Cabecalho titulo="Presença registrada" />
        <Aviso tipo="atencao">
          A rede está fora. A presença de {nick.trim()} foi guardada neste aparelho e entra na
          aula sozinha assim que a rede voltar.
        </Aviso>
        <Botao onClick={aoVoltar}>Voltar ao início</Botao>
      </Moldura>
    );
  }

  // Sem rede, a entrada por reconhecimento facial não é oferecida — o
  // descritor nasce no aparelho, mas a comparação é no núcleo (`RF-04-24`,
  // `RN-04-12`). A alternativa equivalente é a mesma tela de confirmação
  // (`RN-04-09`), só que também sem chamar o núcleo.
  const semRedeNaEntrada = tela === "entrada" && semRede;

  if (tela === "confirmando" || semRedeNaEntrada) {
    return (
      <Moldura>
        <Cabecalho
          titulo="Quem está chegando?"
          subtitulo="A criança diz o nick, e um Mestre ou Admin confirma quem ela é."
          acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
        />
        {semRedeNaEntrada && (
          <Aviso tipo="atencao">
            Sem rede, a entrada por reconhecimento facial não funciona. Confirme pelo nick.
          </Aviso>
        )}
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
