import { ErroDaApi } from "comum/api";
import { existeTranscricaoDeFala, iniciarTranscricao } from "comum/fala";
import { Aviso, Botao } from "comum/react";
import { useEffect, useRef, useState } from "react";
import {
  entregarProducao,
  type FormaDeEntregaDaProducao,
  type ProducaoDaMissao,
} from "../api/producao";

interface Props {
  equipeId: string;
  token: string;
  producaoEsperada: string;
}

const MENSAGEM_DE_REENVIO = "Não deu para ler a foto agora. Tente fotografar de novo.";

const MENSAGEM_SEM_TRANSCRICAO =
  "Este aparelho não transcreve fala. A equipe pode entregar por texto ou por foto.";

const MENSAGEM_DE_FALHA_NA_FALA =
  "Não foi possível entender a fala. Fale de novo ou escreva a produção.";

// A entrega da produção da equipe — texto, fala ou foto do manuscrito — e
// a devolutiva construtiva, que nunca credita ponto (`RF-04-45` a
// `RF-04-47`, `RN-04-20`, `RN-04-12`). O microfone abre só por ação da
// criança e fecha ao fim da fala; a fala é transcrita no próprio aparelho,
// por `comum/fala`, e ao núcleo segue só o texto — o áudio nunca sai dele
// (`RF-05-76`, `RN-05-32`, documento 03 §1.12). A transcrição cai no campo
// da produção, editável antes do envio. A foto não fica no aparelho depois
// do envio, com sucesso ou não (documento 03 §12.2). O texto está sempre
// entre as formas oferecidas — quem recusa câmera e microfone não perde a
// missão (`RN-04-09`); onde o aparelho não transcreve, a fala nem é
// oferecida.
export function EntregaDaProducao({ equipeId, token, producaoEsperada }: Props) {
  const [forma, definirForma] = useState<FormaDeEntregaDaProducao>("texto");
  const [texto, definirTexto] = useState("");
  const [arquivo, definirArquivo] = useState<Blob | null>(null);
  const [ouvindo, definirOuvindo] = useState(false);
  const [avisoDeFala, definirAvisoDeFala] = useState<string | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [pedirReenvio, definirPedirReenvio] = useState(false);
  const [resultado, definirResultado] = useState<ProducaoDaMissao | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const encerradorRef = useRef<(() => void) | null>(null);
  const transcreve = existeTranscricaoDeFala();

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
    definirErro(null);
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
    definirErro(null);
    definirPedirReenvio(false);

    if (forma !== "foto" && !texto.trim()) {
      definirErro(
        forma === "audio"
          ? "Fale ou escreva a produção antes de entregar."
          : "Escreva a produção antes de entregar.",
      );
      return;
    }
    if (forma === "foto" && !arquivo) {
      definirErro("Escolha a foto antes de entregar.");
      return;
    }

    definirEnviando(true);
    try {
      const producao = await entregarProducao(
        equipeId,
        {
          forma,
          texto: forma === "foto" ? undefined : texto,
          arquivo: forma === "foto" ? (arquivo ?? undefined) : undefined,
        },
        token,
      );
      definirResultado(producao);
      definirTexto("");
      definirArquivo(null);
    } catch (erroCapturado) {
      definirArquivo(null);
      if (erroCapturado instanceof ErroDaApi && erroCapturado.status === 503) {
        definirPedirReenvio(true);
      } else if (erroCapturado instanceof ErroDaApi) {
        definirErro(erroCapturado.message);
      } else {
        definirErro("Não foi possível entregar agora. Tente novamente.");
      }
    } finally {
      definirEnviando(false);
    }
  }

  if (resultado) {
    return (
      <section aria-label="Devolutiva da produção" className="cg-devolutiva">
        <Aviso tipo="sucesso">
          {resultado.devolutiva
            ? resultado.devolutiva
            : "Sua produção foi registrada. O retorno não veio desta vez, mas o que vocês " +
              "escreveram está garantido."}
        </Aviso>
        <p>Isso não vale ponto — quem lança o resultado da atividade é o Mestre.</p>
      </section>
    );
  }

  return (
    <section aria-label="Entrega da produção" className="cg-entrega-da-producao">
      <h3>Entregar a produção</h3>
      <p>{producaoEsperada}</p>

      <div className="cg-campo">
        <label htmlFor="producao-forma">Como vocês querem entregar</label>
        <select
          id="producao-forma"
          value={forma}
          onChange={(evento) => {
            definirForma(evento.target.value as FormaDeEntregaDaProducao);
            definirArquivo(null);
            definirErro(null);
            definirAvisoDeFala(null);
          }}
        >
          <option value="texto">Texto</option>
          {transcreve && <option value="audio">Fala</option>}
          <option value="foto">Foto do que fizeram à mão</option>
        </select>
      </div>

      {!transcreve && <Aviso tipo="atencao">{MENSAGEM_SEM_TRANSCRICAO}</Aviso>}

      {forma !== "foto" && (
        <div className="cg-campo">
          <label htmlFor="producao-texto">
            {forma === "audio" ? "O que a equipe falou" : "O que a equipe produziu"}
          </label>
          <textarea
            id="producao-texto"
            value={texto}
            onChange={(evento) => definirTexto(evento.target.value)}
            rows={6}
          />
        </div>
      )}

      {forma === "audio" && (
        <div className="cg-campo">
          <Botao variante="secundaria" onClick={alternarFala} desabilitado={enviando}>
            {ouvindo ? "Parar de ouvir" : "Falar a produção"}
          </Botao>
          {ouvindo && <p role="status">Ouvindo…</p>}
          {avisoDeFala && <Aviso tipo="atencao">{avisoDeFala}</Aviso>}
          <p>A gravação não sai deste aparelho — ao Mestre vai só o texto da fala.</p>
        </div>
      )}

      {forma === "foto" && (
        <div className="cg-campo">
          <label htmlFor="producao-foto">Foto do manuscrito</label>
          <input
            id="producao-foto"
            type="file"
            accept="image/*"
            capture="environment"
            onChange={(evento) => definirArquivo(evento.target.files?.[0] ?? null)}
          />
        </div>
      )}

      {pedirReenvio && <Aviso tipo="atencao">{MENSAGEM_DE_REENVIO}</Aviso>}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      <Botao onClick={enviar} desabilitado={enviando || ouvindo}>
        Entregar
      </Botao>
    </section>
  );
}
