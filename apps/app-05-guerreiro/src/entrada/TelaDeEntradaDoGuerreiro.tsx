import { ErroDaApi } from "comum/api";
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

// A falha de camada nunca veste a frase do rosto (`RN-05-48`, invariante 25).
// Em linguagem de criança, sem código de erro nem termo técnico (`RF-05-02`).
const MENSAGEM_DE_FALHA_DE_COMUNICACAO =
  "Não consegui falar com a plataforma agora. Tente de novo daqui a pouco!";

const MENSAGEM_DE_FALHA_APOS_RECONHECIMENTO =
  "Reconheci você, mas não consegui terminar de abrir sua área. Tente de novo!";

const MENSAGEM_DE_FALHA_INESPERADA = "Algo não funcionou aqui. Tente de novo!";

// O código que o núcleo declara na recusa da conferência (`RF-01-27`). É ele,
// e não o status, que separa o rosto que não confere de sessão expirada e de
// chave recusada, que são outra coisa.
const CODIGO_DE_RECUSA_DA_CONFERENCIA = "autenticacao_biometrica_invalida";

function ehRecusaDaConferencia(erro: unknown): boolean {
  return erro instanceof ErroDaApi && erro.codigo === CODIGO_DE_RECUSA_DA_CONFERENCIA;
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
