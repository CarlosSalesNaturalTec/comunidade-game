import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { eu } from "comum/autenticacao/api";
import {
  acoplarEspelho,
  type EstadoDaVivacidade,
  encerrarCaptura,
  existeCamera,
  gerarDescritor,
  prepararCaptura,
  provarVivacidade,
} from "comum/biometria";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { useRef, useState } from "react";
import { registrarPresenca } from "../api/presencas";
import {
  abrirSessaoPorReconhecimento,
  confirmarSessaoDeGuerreiro,
} from "../api/sessoesDeGuerreiro";
import { Visor } from "../captura/Visor";
import { enfileirarPresenca } from "../fila/filaDePresenca";
import {
  FORMATO_DO_PIN,
  marcarPinBloqueado,
  pinBloqueadoNoAparelho,
  pinConfereNoAparelho,
  registrarErroDePin,
  verificadorGuardado,
  zerarErrosDePin,
} from "../pin/pinDeConfirmacao";
import { useEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";

interface Props {
  tokenDeTrabalho: string;
  aulaId: string;
  /** O caminho que chamou a entrada. Só `presenca` registra a presença do
   * dia e termina o atendimento ali; nos demais a entrada apenas abre a
   * sessão (`RF-04-67`, design — decisão 1). */
  caminho: CaminhoDaEntrada;
  aoVoltar: () => void;
  /** Avisa por qual caminho a sessão do Guerreiro(a) abriu — é o que
   * autoriza o recadastro da imagem atrás da confirmação presencial
   * (`RF-04-22`, design — decisão 4). */
  aoAbrirSessao?: (via: "reconhecimento" | "confirmacao") => void;
}

export type CaminhoDaEntrada = "presenca" | "equipes" | "quiz" | "troca";

type Tela =
  | "entrada"
  | "confirmando"
  | "presencaRegistrada"
  | "presencaJaRegistrada"
  | "presencaEnfileirada";

const MENSAGEM_DE_RECUSA =
  "Não foi possível reconhecer. Tente de novo, com o rosto bem posicionado, ou chame um Mestre ou Admin.";

// Distinta da recusa acima de propósito: a indistinguibilidade do `RF-04-20`
// cobre as três causas da recusa do núcleo, não a câmera que nem chegou a
// funcionar. Preparo que falhou NEVER se disfarça de rosto que não confere
// (`RF-04-65`).
const MENSAGEM_DE_FALHA_DE_PREPARO =
  "A câmera não pôde ser preparada neste aparelho. Tente de novo ou chame um Mestre ou Admin.";

// A falha que não chega a produzir corpo de erro — rede fora, resposta
// ilegível. Havendo corpo, quem fala é o núcleo, pela mensagem dele
// (`RN-04-36`, `RF-01-27`).
const MENSAGEM_DE_FALHA_DE_COMUNICACAO =
  "Não foi possível falar com a plataforma. Tente de novo ou chame um Mestre ou Admin.";

// O que roda depois de o núcleo ter reconhecido o rosto: a sessão já abriu no
// núcleo, e falha aqui NEVER é recusa dele (`RN-04-36`, `RF-04-18`).
const MENSAGEM_DE_FALHA_APOS_RECONHECIMENTO =
  "O rosto foi reconhecido, mas a entrada não pôde ser concluída. Tente de novo ou chame um " +
  "Mestre ou Admin.";

// Nenhuma tentativa termina sem frase: tela muda é a falha silenciosa que a
// invariante 25 fecha, e não diz causa que não se conhece (`RN-04-36`).
const MENSAGEM_DE_FALHA_INESPERADA =
  "Não foi possível concluir a entrada. Tente de novo ou chame um Mestre ou Admin.";

// O código que o núcleo declara na recusa da conferência (`RF-01-27`). É ele,
// e não o status, que separa a recusa do rosto de sessão expirada e de chave
// recusada, que são outra coisa (design — decisão 2).
const CODIGO_DE_RECUSA_DA_CONFERENCIA = "autenticacao_biometrica_invalida";

// A recusa do PIN de quem confirma, conferido antes do nick — a frase nunca
// diz nada da criança (`RN-04-37`, `RN-01-22`).
const MENSAGEM_DE_PIN_ERRADO = "PIN errado. Digite de novo o PIN de quem abriu o aparelho.";
const MENSAGEM_DE_PIN_BLOQUEADO =
  "PIN bloqueado neste aparelho depois de cinco erros seguidos. Para confirmar de novo, " +
  "entre outra vez pelo Google.";
const MENSAGEM_DE_PIN_NAO_CADASTRADO =
  "Quem abriu o aparelho ainda não tem PIN de confirmação. O Mestre cadastra na App 09, e o " +
  "Admin, na App 03.";
const MENSAGEM_SEM_VERIFICADOR_SEM_REDE =
  "Sem rede, a confirmação confere o PIN no aparelho, e este aparelho foi aberto sem PIN " +
  "cadastrado. Cadastre o PIN e abra o aparelho de novo com rede.";

// A tela anuncia o caminho que serve: quem escolheu equipes, quiz ou troca na
// tela inicial precisa reconhecer que chegou onde quis, e não ao caminho da
// presença — os quatro se apresentavam iguais (`RF-04-01`, `RF-04-67`,
// `RF-04-68`, design — decisão 1). O subtítulo não entra aqui: ele descreve o
// ato, que é o mesmo nos quatro.
const TITULO_DO_CAMINHO: Record<CaminhoDaEntrada, string> = {
  presenca: "Quem está chegando?",
  equipes: "Quem vai formar equipe?",
  quiz: "Quem vai jogar o Quiz?",
  troca: "Quem vai trocar recompensa?",
};

const MENSAGENS_DO_PIN: Record<string, string> = {
  pin_recusado: MENSAGEM_DE_PIN_ERRADO,
  pin_bloqueado: MENSAGEM_DE_PIN_BLOQUEADO,
  pin_nao_cadastrado: MENSAGEM_DE_PIN_NAO_CADASTRADO,
};

// Falha de camada aparece pelo que é: a mensagem que o núcleo declarou no
// corpo único quando há corpo, a frase própria quando não há (`RN-04-36`).
function mensagemDaFalhaDeCamada(erro: unknown): string {
  return erro instanceof ErroDaApi ? erro.message : MENSAGEM_DE_FALHA_DE_COMUNICACAO;
}

function ehRecusaDaConferencia(erro: unknown): boolean {
  return erro instanceof ErroDaApi && erro.codigo === CODIGO_DE_RECUSA_DA_CONFERENCIA;
}

// A entrada por nick e imagem entra antes da confirmação humana, que passa
// a ser a alternativa de quem não tem câmera, de quem a recusa persiste e
// de quem não tem _template_ (`RF-04-18`, `RF-04-29`, `RN-04-09`, design —
// decisão 5). A recusa do núcleo — nick inexistente, sem _template_ ou
// descritor que não confere — é sempre a mesma frase (`RF-04-20`,
// `RN-01-22`).
export function TelaDeEntradaDoGuerreiro({
  tokenDeTrabalho,
  aulaId,
  caminho,
  aoVoltar,
  aoAbrirSessao,
}: Props) {
  const { entrarComToken } = useSessao();
  const { semRede } = useEstadoDeRede();
  const [nick, definirNick] = useState("");
  // O PIN vive só neste estado, limpo a cada tentativa, e nunca é gravado no
  // aparelho (`RN-04-38`).
  const [pin, definirPin] = useState("");
  const [bloqueado, definirBloqueado] = useState(pinBloqueadoNoAparelho);
  const [tela, definirTela] = useState<Tela>("entrada");
  const [emAndamento, definirEmAndamento] = useState(false);
  const [recusado, definirRecusado] = useState(false);
  const [falhaDePreparo, definirFalhaDePreparo] = useState(false);
  // A falha de camada não é recusa do rosto e por isso não vive no mesmo
  // estado dela: carrega a causa que o núcleo declarou (`RN-04-36`).
  const [falhaDeCamada, definirFalhaDeCamada] = useState<string | null>(null);
  const [estadoDoLaco, definirEstadoDoLaco] = useState<EstadoDaVivacidade | null>(null);
  const [erroDeConfirmacao, definirErroDeConfirmacao] = useState<string | null>(() =>
    pinBloqueadoNoAparelho() ? MENSAGEM_DE_PIN_BLOQUEADO : null,
  );
  const lugarDoVisor = useRef<HTMLDivElement>(null);

  // Só o caminho Presença registra a presença: nos caminhos das equipes, do
  // quiz e da troca a entrada apenas abre a sessão, e quem chega sem
  // presença é barrado pela guarda, não pela entrada (`RF-04-67`,
  // `RF-04-68`, design — decisão 1).
  //
  // Registrando, grava sempre com o token da sessão de trabalho
  // (`RF-04-18`, `RF-04-21`), e só o reconhecimento avisa que a presença já
  // constava — comparando o momento do fato como instante, não como texto,
  // porque o núcleo devolve a data com precisão diferente da enviada
  // (`RF-04-19`, design — decisão 3).
  async function concluirEntrada(
    token: string,
    modo: "reconhecimento" | "confirmacao",
  ): Promise<void> {
    if (caminho !== "presenca") {
      aoAbrirSessao?.(modo);
      await entrarComToken(token);
      return;
    }
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
    // Registrada a presença, o atendimento termina aqui: o caminho Presença
    // não leva às equipes, que são outro momento (`RF-04-67`, PRD-04 §5.4).
    definirTela("presencaRegistrada");
  }

  // Cada desfecho tem tratamento próprio, e nenhum empresta a frase do outro
  // (`RN-04-36`, invariante 25). São três zonas: a captura local, cujos
  // desfechos são indistinguíveis da recusa por exigência do `RF-04-20`; a
  // conferência, em que só o código declarado pelo núcleo é recusa; e o que
  // roda depois dela, já com o rosto reconhecido.
  async function tentarReconhecimento() {
    definirRecusado(false);
    definirFalhaDePreparo(false);
    definirFalhaDeCamada(null);
    definirEstadoDoLaco(null);
    definirEmAndamento(true);
    try {
      // Sondar a câmera, prepará-la e acoplar o espelho são a mesma zona: o
      // aparelho que nem chegou a funcionar (`RF-04-65`).
      try {
        const temCamera = await existeCamera();
        if (!temCamera) {
          definirTela("confirmando");
          return;
        }
        await prepararCaptura();
        if (lugarDoVisor.current) acoplarEspelho(lugarDoVisor.current);
      } catch {
        definirFalhaDePreparo(true);
        return;
      }

      // Captura local: vivacidade reprovada e descritor que não saiu dizem à
      // criança a mesma coisa que a recusa do núcleo, e distingui-los
      // revelaria o que o `RF-04-20` manda esconder.
      let descritor: number[];
      try {
        const vivacidadeAprovada = await provarVivacidade(definirEstadoDoLaco);
        if (!vivacidadeAprovada) {
          definirRecusado(true);
          return;
        }
        descritor = await gerarDescritor();
      } catch {
        definirRecusado(true);
        return;
      }

      // Conferência: só o código que o núcleo declara como recusa vira a
      // frase do rosto. Todo o resto é falha de camada, e aparece pelo que é.
      let token: string;
      try {
        const abertura = await abrirSessaoPorReconhecimento({
          nick: nick.trim(),
          descritor,
          aula_id: aulaId,
        });
        token = abertura.token;
      } catch (erroCapturado) {
        if (ehRecusaDaConferencia(erroCapturado)) definirRecusado(true);
        else definirFalhaDeCamada(mensagemDaFalhaDeCamada(erroCapturado));
        return;
      }

      // Depois da conferência o rosto já foi reconhecido: o que falhar aqui
      // NEVER se apresenta como recusa dele.
      try {
        await concluirEntrada(token, "reconhecimento");
      } catch {
        definirFalhaDeCamada(MENSAGEM_DE_FALHA_APOS_RECONHECIMENTO);
      }
    } catch {
      // Rede de segurança: nenhum desfecho pode sair desta tela sem frase.
      // Tela muda é a falha silenciosa que esta change existe para fechar.
      definirFalhaDeCamada(MENSAGEM_DE_FALHA_INESPERADA);
    } finally {
      encerrarCaptura();
      definirEmAndamento(false);
    }
  }

  function bloquear() {
    marcarPinBloqueado();
    definirBloqueado(true);
    definirErroDeConfirmacao(MENSAGEM_DE_PIN_BLOQUEADO);
  }

  // Só quem abriu a sessão de trabalho confirma, e só com o próprio PIN
  // digitado no ato — a sessão de trabalho sozinha não confirma ninguém
  // (`RF-04-21`, `RN-04-37`). O PIN sai do estado a cada tentativa.
  async function confirmar() {
    definirErroDeConfirmacao(null);
    const pinDigitado = pin;
    definirPin("");
    if (pinBloqueadoNoAparelho()) {
      bloquear();
      return;
    }
    // Sem rede, a presença não se perde: o PIN é conferido no aparelho,
    // contra o verificador de quem abriu a sessão de trabalho, e só então a
    // presença entra na fila — nunca abre sessão nem tenta a chamada
    // (`RF-04-23`, `RN-04-38`, `RN-04-12`, `RN-04-13`).
    if (semRede) {
      const verificador = verificadorGuardado();
      if (!verificador) {
        definirErroDeConfirmacao(MENSAGEM_SEM_VERIFICADOR_SEM_REDE);
        return;
      }
      definirEmAndamento(true);
      try {
        if (!(await pinConfereNoAparelho(pinDigitado, verificador))) {
          if (registrarErroDePin()) {
            bloquear();
          } else {
            definirErroDeConfirmacao(MENSAGEM_DE_PIN_ERRADO);
          }
          return;
        }
        zerarErrosDePin();
        enfileirarPresenca({
          aula_id: aulaId,
          nick: nick.trim(),
          momento_do_fato: new Date().toISOString(),
        });
        definirTela("presencaEnfileirada");
      } finally {
        definirEmAndamento(false);
      }
      return;
    }
    definirEmAndamento(true);
    try {
      const abertura = await confirmarSessaoDeGuerreiro(
        nick.trim(),
        pinDigitado,
        tokenDeTrabalho,
      );
      zerarErrosDePin();
      await concluirEntrada(abertura.token, "confirmacao");
    } catch (erroCapturado) {
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "pin_bloqueado") {
        bloquear();
      } else if (erroCapturado instanceof ErroDaApi) {
        definirErroDeConfirmacao(
          MENSAGENS_DO_PIN[erroCapturado.codigo] ?? erroCapturado.message,
        );
      } else {
        definirErroDeConfirmacao("Não foi possível confirmar. Tente novamente.");
      }
    } finally {
      definirEmAndamento(false);
    }
  }

  if (tela === "presencaRegistrada") {
    return (
      <Moldura>
        <Cabecalho titulo="Presença registrada" />
        <Aviso tipo="sucesso">
          Pronto, {nick.trim()}! A presença de hoje está registrada. Para trabalhar em equipe,
          volte ao início e escolha Equipes.
        </Aviso>
        <Botao onClick={aoVoltar}>Voltar ao início</Botao>
      </Moldura>
    );
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

  // Sem rede, só o caminho Presença tem desfecho: a fila local é dele
  // (`RF-04-23`). Formar equipe, responder ao quiz e trocar recompensa
  // exigem rede, e nenhum deles enfileira coisa alguma (`RF-04-58`,
  // `RF-04-68`).
  if (semRede && caminho !== "presenca") {
    return (
      <Moldura>
        <Cabecalho
          titulo="Este caminho precisa de rede"
          acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
        />
        <Aviso tipo="atencao">
          A rede está fora. Assim que ela voltar, dá para entrar de novo por aqui. A presença
          do dia continua sendo registrada no caminho Presença.
        </Aviso>
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
          titulo={TITULO_DO_CAMINHO[caminho]}
          subtitulo="A criança diz o nick, e quem abriu o aparelho confirma com o próprio PIN."
          acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
        />
        {semRedeNaEntrada && (
          <Aviso tipo="atencao">
            Sem rede, a entrada por reconhecimento facial não funciona. Confirme pelo nick e
            pelo PIN.
          </Aviso>
        )}
        <Campo rotulo="Nick" valor={nick} aoAlterar={definirNick} focoInicial />
        <Campo
          rotulo="PIN de quem confirma"
          tipo="password"
          valor={pin}
          aoAlterar={(valor) => definirPin(valor.replace(/\D/g, "").slice(0, 4))}
        />
        <Botao
          onClick={confirmar}
          desabilitado={
            bloqueado || emAndamento || nick.trim().length === 0 || !FORMATO_DO_PIN.test(pin)
          }
        >
          {emAndamento ? "Confirmando…" : "Confirmar identidade"}
        </Botao>
        {erroDeConfirmacao && <Aviso tipo="erro">{erroDeConfirmacao}</Aviso>}
      </Moldura>
    );
  }

  return (
    <Moldura>
      <Cabecalho
        titulo={TITULO_DO_CAMINHO[caminho]}
        subtitulo="Digite o nick e olhe para a câmera."
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />
      <Campo rotulo="Nick" valor={nick} aoAlterar={definirNick} focoInicial />
      {/* O retorno do laço vale enquanto a tentativa corre e cala no desfecho: sem
          isto, o visor congela em "Pessoa confirmada." e fica ao lado da recusa do
          núcleo, como se a tela se contradissesse (`RF-04-64`, `RN-04-34`, design —
          decisão 1). É o mesmo condicionamento da `TelaDeCaptura` e da bancada. */}
      <Visor lugar={lugarDoVisor} estado={emAndamento ? estadoDoLaco : null} />
      <Botao
        onClick={tentarReconhecimento}
        desabilitado={emAndamento || nick.trim().length === 0}
      >
        {emAndamento ? "Reconhecendo…" : "Entrar"}
      </Botao>
      {falhaDePreparo && <Aviso tipo="erro">{MENSAGEM_DE_FALHA_DE_PREPARO}</Aviso>}
      {/* A causa que o núcleo declarou, nunca a frase do rosto (`RN-04-36`). O
          caminho humano continua oferecido: falha de camada também deixaria o
          Guerreiro(a) fora da aula, e sem rede a confirmação enfileira a
          presença (`RN-04-09`, `RF-04-23`). */}
      {falhaDeCamada && (
        <>
          <Aviso tipo="erro">{falhaDeCamada}</Aviso>
          <Botao variante="secundaria" onClick={() => definirTela("confirmando")}>
            Chamar Mestre ou Admin
          </Botao>
        </>
      )}
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
