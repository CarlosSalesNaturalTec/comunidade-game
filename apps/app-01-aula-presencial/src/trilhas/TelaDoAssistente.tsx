import { ErroDaApi } from "comum/api";
import { existeTranscricaoDeFala, iniciarTranscricao } from "comum/fala";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useEffect, useRef, useState } from "react";
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

const MENSAGEM_SEM_TRANSCRICAO =
  "Este aparelho não transcreve fala. Digite a pergunta no campo abaixo.";

const MENSAGEM_DE_FALHA_NA_FALA =
  "Não foi possível entender a fala. Fale de novo ou digite a pergunta.";

const MENSAGEM_SEM_REDE =
  "Sem rede, o assistente de trilhas fica indisponível. Assim que a rede voltar, a equipe pode perguntar de novo.";

const MENSAGEM_DE_INDISPONIBILIDADE = "O assistente não respondeu agora. Pergunte de novo.";

// O terceiro verbo do caminho das trilhas, ao lado de ler e produzir
// (`RF-04-36` a `RF-04-40`, PRD-04 §9). A conversa vive só no estado desta
// tela — nunca em `localStorage` nem em `sessionStorage` — e some com o
// atendimento, porque o aparelho é compartilhado (`RF-04-28`). O microfone
// abre só por toque e fecha ao fim da fala (`RN-04-20`); a fala é
// transcrita no próprio aparelho, por `comum/fala`, e só o texto segue ao
// núcleo — o áudio nunca sai dele (`RF-04-40`, `RN-04-21`, documento 03
// §1.12). O texto está sempre disponível ao lado do botão de falar, nunca
// escondido atrás de uma escolha de forma (`RF-04-39`); onde o aparelho
// não transcreve, o botão de falar nem aparece.
export function TelaDoAssistente({ equipeId, token, aoVoltar }: Props) {
  const { semRede, marcarFalhaDeRede, marcarSucessoDeRede } = useEstadoDeRede();
  const [conversa, definirConversa] = useState<TrocaDeConversa[]>([]);
  const [texto, definirTexto] = useState("");
  const [ouvindo, definirOuvindo] = useState(false);
  const [enviando, definirEnviando] = useState(false);
  const [indisponivel, definirIndisponivel] = useState(false);
  const [avisoDeFala, definirAvisoDeFala] = useState<string | null>(null);
  const encerradorRef = useRef<(() => void) | null>(null);

  // O aparelho é compartilhado: se a tela sair enquanto o microfone ainda
  // ouve, ele fecha junto — nunca fica captando sozinho (`RN-04-20`).
  useEffect(() => {
    return () => encerradorRef.current?.();
  }, []);

  function alternarFala() {
    if (ouvindo) {
      encerradorRef.current?.();
      return;
    }
    definirAvisoDeFala(null);
    definirOuvindo(true);
    encerradorRef.current = iniciarTranscricao({
      aoTranscrever: (transcricao) => definirTexto(transcricao),
      aoFalhar: () => definirAvisoDeFala(MENSAGEM_DE_FALHA_NA_FALA),
      aoEncerrar: () => {
        definirOuvindo(false);
        encerradorRef.current = null;
      },
    });
  }

  async function enviar() {
    if (semRede || !texto.trim()) return;
    definirEnviando(true);
    definirIndisponivel(false);
    try {
      const consulta = await consultarAssistenteDeTrilhas(equipeId, texto, token);
      marcarSucessoDeRede();
      definirConversa((atual) => [
        ...atual,
        { pergunta: consulta.pergunta, resposta: consulta.resposta },
      ]);
      definirTexto("");
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
      <Cabecalho
        titulo="Assistente de trilhas"
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />

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
              onChange={(evento) => definirTexto(evento.target.value)}
              rows={3}
            />
          </div>

          {existeTranscricaoDeFala() ? (
            <>
              <Botao variante="secundaria" onClick={alternarFala} desabilitado={enviando}>
                {ouvindo ? "Parar de ouvir" : "Perguntar por voz"}
              </Botao>
              {ouvindo && <p role="status">Ouvindo…</p>}
              {avisoDeFala && <Aviso tipo="atencao">{avisoDeFala}</Aviso>}
            </>
          ) : (
            <Aviso tipo="atencao">{MENSAGEM_SEM_TRANSCRICAO}</Aviso>
          )}

          <Botao onClick={enviar} desabilitado={enviando || ouvindo || !texto.trim()}>
            {enviando ? "Perguntando…" : "Perguntar"}
          </Botao>
        </>
      )}
    </Moldura>
  );
}
