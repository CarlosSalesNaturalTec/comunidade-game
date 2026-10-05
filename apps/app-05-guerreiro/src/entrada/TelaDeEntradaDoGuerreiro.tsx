import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import {
  andamentoDosModelos,
  encerrarCaptura,
  existeCamera,
  gerarDescritor,
  precarregarModelos,
  provarVivacidade,
} from "comum/biometria";
import { useNarrarAoEntrar } from "comum/narracao";
import { Aviso, Botao, Cabecalho, Campo, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import { abrirSessaoPorReconhecimento } from "../api/sessoesDeGuerreiro";
import { ConfirmacaoAssistida } from "./ConfirmacaoAssistida";

type Tela = "verificandoCamera" | "entrada" | "confirmando";
type MotivoDaConfirmacao = "semCamera" | "conferenciaRecusada";

const MENSAGEM_DE_RECUSA =
  "Não foi possível reconhecer. Tente de novo, com o rosto bem posicionado, ou chame um Mestre ou Admin.";

const MENSAGEM_SEM_CAMERA =
  "Esse aparelho não tem câmera para tirar sua foto. Peça ajuda a um Mestre no ponto de apoio!";

// A falha de camada nunca veste a frase do rosto (`RN-05-48`, invariante 25).
// Em linguagem de criança, sem código de erro nem termo técnico (`RF-05-02`).
const MENSAGEM_DE_FALHA_DE_COMUNICACAO =
  "Não consegui falar com a plataforma agora. Tente de novo daqui a pouco!";

const MENSAGEM_DE_FALHA_APOS_RECONHECIMENTO =
  "Reconheci você, mas não consegui terminar de abrir sua área. Tente de novo!";

const MENSAGEM_DE_FALHA_INESPERADA = "Algo não funcionou aqui. Tente de novo!";

// A falha da pré-carga é outra coisa que não a recusa do rosto: diz o que
// aconteceu, convida a entrar do mesmo jeito e não empresta frase alguma do
// caminho da conferência (`RN-05-48`, invariante 25). Em linguagem de criança,
// sem termo técnico nem código de erro (PRD-05 §10).
const MENSAGEM_DE_FALHA_DA_PRECARGA =
  "Não consegui deixar o reconhecimento pronto antes. Pode tentar entrar do mesmo jeito!";

// A biblioteca não informa bytes: o andamento só se lê perguntando quantos
// modelos já carregaram. Daí a leitura periódica, e daí o andamento ser por
// modelo e nunca percentual (`RF-05-90`).
const ESPERA_ENTRE_LEITURAS_DO_ANDAMENTO_MS = 300;

// O código que o núcleo declara na recusa da conferência (`RF-01-27`). É ele,
// e não o status, que separa o rosto que não confere de sessão expirada e de
// chave recusada, que são outra coisa.
const CODIGO_DE_RECUSA_DA_CONFERENCIA = "autenticacao_biometrica_invalida";

function ehRecusaDaConferencia(erro: unknown): boolean {
  return erro instanceof ErroDaApi && erro.codigo === CODIGO_DE_RECUSA_DA_CONFERENCIA;
}

// A falha é **dita, e não interrompe**. Por isso não é `Aviso`: os dois tipos
// vermelhos dele — `erro` e `atencao` — são `role="alert"`, e o fundador fixou
// em 2026-10-02 que não interromper vem antes do vermelho. Sem cor, a frase
// inteira carrega a informação, e o documento 15 §5 fica satisfeito sem
// precisar de rótulo. A narração é pedida à mão, já que não vem do `Aviso`
// (`RF-05-90`, design — decisão 3).
function FalhaDaPrecarga() {
  useNarrarAoEntrar(MENSAGEM_DE_FALHA_DA_PRECARGA);
  return <EstadoDaLista>{MENSAGEM_DE_FALHA_DA_PRECARGA}</EstadoDaLista>;
}

// Porta de entrada da App 05: a sessão do Guerreiro(a) é pré-requisito de
// toda tela do PRD-05 (proposal — Why). Entrada por nick e imagem primeiro,
// com a confirmação humana como alternativa de quem não tem câmera, de quem
// a conferência recusa e de quem ainda não tem imagem gravada (`RF-05-01`
// a `RF-05-04`, `RN-05-01`, `RN-05-02`).
export function TelaDeEntradaDoGuerreiro() {
  // `erroDeEntrada` vem do provedor: `entrarComToken` NÃO lança quando o
  // núcleo não reconhece o token — ele guarda o erro. Sem ler isto aqui, a
  // falha depois do reconhecimento não produziria frase alguma, e tela muda é
  // a mesma falha silenciosa por outro caminho (`RN-05-48`).
  const { entrarComToken, erroDeEntrada } = useSessao();
  const [nick, definirNick] = useState("");
  const [tela, definirTela] = useState<Tela>("verificandoCamera");
  const [emAndamento, definirEmAndamento] = useState(false);
  const [recusado, definirRecusado] = useState(false);
  // A falha de camada não é recusa do rosto, e por isso não vive no mesmo
  // estado dela (`RN-05-48`).
  const [falhaDeCamada, definirFalhaDeCamada] = useState<string | null>(null);
  const [motivoDaConfirmacao, definirMotivoDaConfirmacao] =
    useState<MotivoDaConfirmacao>("conferenciaRecusada");
  // A pré-carga vive aqui, e não na tela de entrada: voltar do caminho do
  // adulto não pode recomeçar o download nem reacender o indicador.
  const [andamentoDaPrecarga, definirAndamentoDaPrecarga] = useState<{
    carregados: number;
    total: number;
  } | null>(null);
  const [precargaFalhou, definirPrecargaFalhou] = useState(false);

  // A pré-carga começa **depois de a câmera aparecer**, e só aqui: aparelho
  // sem câmera é recusado pelo `RF-05-02` e vai ao adulto do `RN-05-02` sem
  // nunca gerar descritor, então não gasta a banda dele. Carrega **modelo só**:
  // nada acende a câmera neste momento, porque ninguém pediu nada
  // (`RF-05-90`, `RN-05-49`, design — decisões 1 e 2).
  useEffect(() => {
    let cancelado = false;
    let relogio: ReturnType<typeof setInterval> | undefined;
    // Verificação que **falha** é tratada como aparelho sem câmera: a recusa
    // do `RF-05-02` é apresentada e o caminho do adulto é oferecido. Sem o
    // `catch`, `enumerateDevices()` rejeitado — contexto não seguro, política
    // de permissão — deixaria a criança diante de tela vazia, que é a falha
    // silenciosa que o `RN-05-48` proíbe.
    existeCamera()
      .catch(() => false)
      .then((temCamera) => {
        if (cancelado) return;
        if (!temCamera) {
          definirMotivoDaConfirmacao("semCamera");
          definirTela("confirmando");
          return;
        }
        definirTela("entrada");
        definirAndamentoDaPrecarga(andamentoDosModelos());
        relogio = setInterval(() => {
          if (!cancelado) definirAndamentoDaPrecarga(andamentoDosModelos());
        }, ESPERA_ENTRE_LEITURAS_DO_ANDAMENTO_MS);
        // `precarregarModelos()` nunca lança: devolve se conseguiu.
        precarregarModelos().then((conseguiu) => {
          clearInterval(relogio);
          if (cancelado) return;
          // O indicador sai mesmo na falha: parado no passo em que travou,
          // ele mentiria sobre haver carga em curso.
          definirAndamentoDaPrecarga(null);
          definirPrecargaFalhou(!conseguiu);
        });
      });
    return () => {
      cancelado = true;
      clearInterval(relogio);
    };
  }, []);

  // Três zonas, e nenhuma empresta a frase da outra (`RN-05-48`): a captura
  // local, cujos desfechos são indistinguíveis da recusa por exigência do
  // `RN-01-22`; a conferência, em que só o código declarado pelo núcleo é
  // recusa; e o que roda depois dela, já com o rosto reconhecido.
  async function tentarReconhecimento() {
    definirRecusado(false);
    definirFalhaDeCamada(null);
    definirEmAndamento(true);
    try {
      let descritor: number[];
      try {
        const vivacidadeAprovada = await provarVivacidade();
        if (!vivacidadeAprovada) {
          definirRecusado(true);
          return;
        }
        descritor = await gerarDescritor();
      } catch {
        definirRecusado(true);
        return;
      }

      let token: string;
      try {
        // Sem aula: é a ausência dela que empresta o limiar da comunidade
        // (`RN-01-57`).
        const abertura = await abrirSessaoPorReconhecimento({
          nick: nick.trim(),
          descritor,
        });
        token = abertura.token;
      } catch (erroCapturado) {
        if (ehRecusaDaConferencia(erroCapturado)) definirRecusado(true);
        else definirFalhaDeCamada(MENSAGEM_DE_FALHA_DE_COMUNICACAO);
        return;
      }

      try {
        await entrarComToken(token);
      } catch {
        definirFalhaDeCamada(MENSAGEM_DE_FALHA_APOS_RECONHECIMENTO);
      }
    } catch {
      // Nenhuma tentativa termina sem frase: tela muda é a mesma falha
      // silenciosa por outro caminho.
      definirFalhaDeCamada(MENSAGEM_DE_FALHA_INESPERADA);
    } finally {
      encerrarCaptura();
      definirEmAndamento(false);
    }
  }

  // O desfecho que a tela guardou e o que o provedor guardou são a mesma
  // coisa para quem está diante do aparelho: a entrada não se completou, e por
  // uma causa que não é o rosto (`RN-05-48`).
  const falhaDeCamadaVisivel =
    falhaDeCamada ?? (erroDeEntrada ? MENSAGEM_DE_FALHA_APOS_RECONHECIMENTO : null);

  if (tela === "verificandoCamera") {
    return null;
  }

  if (tela === "confirmando") {
    return (
      <Moldura>
        <Cabecalho
          titulo="Quem está chegando?"
          subtitulo="Diga seu nick, e um adulto responsável por você confirma quem você é."
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
      {/* Informação, nunca erro: `andamento` é `role="status"` e leva rótulo
          textual, então se entende sem depender de cor. O campo do nick fica
          abaixo e segue utilizável — o indicador não é portão
          (`RF-05-90`, documento 15 §5). */}
      {andamentoDaPrecarga && (
        <Aviso tipo="andamento">
          {`Preparando o reconhecimento do seu rosto (${andamentoDaPrecarga.carregados} de ${andamentoDaPrecarga.total})`}
        </Aviso>
      )}
      {precargaFalhou && <FalhaDaPrecarga />}
      <Campo rotulo="Nick" valor={nick} aoAlterar={definirNick} />
      <Botao
        onClick={tentarReconhecimento}
        desabilitado={emAndamento || nick.trim().length === 0}
      >
        {emAndamento ? "Reconhecendo…" : "Entrar"}
      </Botao>
      {/* A causa que o núcleo declarou, nunca a frase do rosto (`RN-05-48`).
          O caminho do adulto continua oferecido: falha de camada também
          deixaria a criança fora da própria área. */}
      {falhaDeCamadaVisivel && (
        <>
          <Aviso tipo="erro">{falhaDeCamadaVisivel}</Aviso>
          <Botao
            variante="secundaria"
            onClick={() => {
              definirMotivoDaConfirmacao("conferenciaRecusada");
              definirTela("confirmando");
            }}
          >
            Pedir ajuda a um adulto
          </Botao>
        </>
      )}
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
            Pedir ajuda a um adulto
          </Botao>
        </>
      )}
    </Moldura>
  );
}
