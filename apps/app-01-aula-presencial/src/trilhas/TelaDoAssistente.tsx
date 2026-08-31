import { ErroDaApi } from "comum/api";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useRef, useState } from "react";
import { consultarAssistenteDeTrilhas } from "../api/assistente";
import { useEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";

interface Props {
  equipeId: string;
  token: string;
  aoVoltar: () => void;
}

interface TrocaDeConversa {
  pergunta: string;
  resposta: string;
}

const MENSAGEM_SEM_MICROFONE =
  "Não foi possível usar o microfone deste aparelho. Você pode perguntar por texto.";

const MENSAGEM_SEM_REDE =
  "Sem rede, o assistente de trilhas fica indisponível. Assim que a rede voltar, a equipe pode perguntar de novo.";

const MENSAGEM_DE_INDISPONIBILIDADE = "O assistente não respondeu agora. Pergunte de novo.";

// O terceiro verbo do caminho das trilhas, ao lado de ler e produzir
// (`RF-04-36` a `RF-04-40`, PRD-04 §9). A conversa vive só no estado desta
// tela — nunca em `localStorage` nem em `sessionStorage` — e some com o
// atendimento, porque o aparelho é compartilhado (`RF-04-28`). O microfone
// abre só por toque e fecha ao fim da fala, no mesmo padrão de
// `EntregaDaProducao` (`RN-04-20`); o texto está sempre disponível ao lado
// dele, nunca escondido atrás de uma escolha de forma (`RF-04-39`).
export function TelaDoAssistente({ equipeId, token, aoVoltar }: Props) {
  const { semRede, marcarFalhaDeRede, marcarSucessoDeRede } = useEstadoDeRede();
  const [conversa, definirConversa] = useState<TrocaDeConversa[]>([]);
  const [texto, definirTexto] = useState("");
  const [arquivo, definirArquivo] = useState<Blob | null>(null);
  const [gravando, definirGravando] = useState(false);
  const [enviando, definirEnviando] = useState(false);
  const [indisponivel, definirIndisponivel] = useState(false);
  const [erroDeMicrofone, definirErroDeMicrofone] = useState<string | null>(null);
  const gravadorRef = useRef<MediaRecorder | null>(null);

  async function alternarGravacao() {
    if (gravando) {
      gravadorRef.current?.stop();
      return;
    }
    definirErroDeMicrofone(null);
    try {
      const fluxo = await navigator.mediaDevices.getUserMedia({ audio: true });
      const gravador = new MediaRecorder(fluxo);
      const pedacos: BlobPart[] = [];
      gravador.ondataavailable = (evento) => pedacos.push(evento.data);
      gravador.onstop = () => {
        definirArquivo(new Blob(pedacos, { type: "audio/webm" }));
        definirTexto("");
        for (const trilha of fluxo.getTracks()) trilha.stop();
        definirGravando(false);
      };
      gravadorRef.current = gravador;
      gravador.start();
      definirGravando(true);
    } catch {
      definirErroDeMicrofone(MENSAGEM_SEM_MICROFONE);
    }
  }

  function alterarTexto(valor: string) {
    definirTexto(valor);
    if (valor) definirArquivo(null);
  }

  async function enviar() {
    if (semRede || (!texto.trim() && !arquivo)) return;
    definirEnviando(true);
    definirIndisponivel(false);
    try {
      const consulta = await consultarAssistenteDeTrilhas(
        equipeId,
        { texto: arquivo ? undefined : texto, arquivo: arquivo ?? undefined },
        token,
      );
      marcarSucessoDeRede();
      definirConversa((atual) => [
        ...atual,
        { pergunta: consulta.pergunta, resposta: consulta.resposta },
      ]);
      definirTexto("");
      definirArquivo(null);
    } catch (erroCapturado) {
      if (erroCapturado instanceof ErroDaApi) {
        definirIndisponivel(true);
      } else {
        marcarFalhaDeRede();
      }
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho titulo="Assistente de trilhas" acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }} />

      {semRede ? (
        <Aviso tipo="atencao">{MENSAGEM_SEM_REDE}</Aviso>
      ) : (
        <>
          <ul aria-label="Conversa com o assistente" className="cg-conversa-do-assistente">
            {conversa.map((troca) => (
              <li key={`${troca.pergunta}::${troca.resposta}`}>
                <p className="cg-pergunta">{troca.pergunta}</p>
                <p className="cg-resposta">{troca.resposta}</p>
              </li>
            ))}
          </ul>

          {indisponivel && <Aviso tipo="atencao">{MENSAGEM_DE_INDISPONIBILIDADE}</Aviso>}

          <div className="cg-campo">
            <label htmlFor="assistente-pergunta">Pergunta</label>
            <textarea
              id="assistente-pergunta"
              value={texto}
              onChange={(evento) => alterarTexto(evento.target.value)}
              rows={3}
            />
          </div>

          <Botao variante="secundaria" onClick={alternarGravacao} desabilitado={enviando}>
            {gravando ? "Parar a gravação" : arquivo ? "Gravar de novo" : "Perguntar por voz"}
          </Botao>
          {arquivo && !gravando && <p role="status">Pergunta gravada — pronta para enviar.</p>}
          {erroDeMicrofone && <Aviso tipo="erro">{erroDeMicrofone}</Aviso>}

          <Botao
            onClick={enviar}
            desabilitado={enviando || gravando || (!texto.trim() && !arquivo)}
          >
            {enviando ? "Perguntando…" : "Perguntar"}
          </Botao>
        </>
      )}
    </Moldura>
  );
}
