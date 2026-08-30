import { ErroDaApi } from "comum/api";
import { Aviso, Botao } from "comum/react";
import { useRef, useState } from "react";
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

const MENSAGEM_DE_REENVIO = "Não deu para ler agora. Tente gravar ou fotografar de novo.";

const MENSAGEM_SEM_MICROFONE =
  "Não foi possível usar o microfone deste aparelho. Você pode entregar por texto.";

// A entrega da produção da equipe — texto, fala ou foto do manuscrito — e
// a devolutiva construtiva, que nunca credita ponto (`RF-04-45` a
// `RF-04-47`, `RN-04-20`, `RN-04-12`). O microfone abre só por ação da
// criança e fecha ao fim da fala; nem a foto nem o áudio ficam no
// aparelho depois do envio, com sucesso ou não (documento 03 §12.2). O
// texto está sempre entre as formas oferecidas — quem recusa câmera e
// microfone não perde a missão (`RN-04-09`).
export function EntregaDaProducao({ equipeId, token, producaoEsperada }: Props) {
  const [forma, definirForma] = useState<FormaDeEntregaDaProducao>("texto");
  const [texto, definirTexto] = useState("");
  const [arquivo, definirArquivo] = useState<Blob | null>(null);
  const [gravando, definirGravando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [pedirReenvio, definirPedirReenvio] = useState(false);
  const [resultado, definirResultado] = useState<ProducaoDaMissao | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const gravadorRef = useRef<MediaRecorder | null>(null);

  async function alternarGravacao() {
    if (gravando) {
      gravadorRef.current?.stop();
      return;
    }
    definirErro(null);
    try {
      const fluxo = await navigator.mediaDevices.getUserMedia({ audio: true });
      const gravador = new MediaRecorder(fluxo);
      const pedacos: BlobPart[] = [];
      gravador.ondataavailable = (evento) => pedacos.push(evento.data);
      gravador.onstop = () => {
        definirArquivo(new Blob(pedacos, { type: "audio/webm" }));
        for (const trilha of fluxo.getTracks()) trilha.stop();
        definirGravando(false);
      };
      gravadorRef.current = gravador;
      gravador.start();
      definirGravando(true);
    } catch {
      definirErro(MENSAGEM_SEM_MICROFONE);
    }
  }

  async function enviar() {
    definirErro(null);
    definirPedirReenvio(false);

    if (forma === "texto" && !texto.trim()) {
      definirErro("Escreva a produção antes de entregar.");
      return;
    }
    if (forma !== "texto" && !arquivo) {
      definirErro(
        forma === "audio"
          ? "Grave a fala antes de entregar."
          : "Escolha a foto antes de entregar.",
      );
      return;
    }

    definirEnviando(true);
    try {
      const producao = await entregarProducao(
        equipeId,
        {
          forma,
          texto: forma === "texto" ? texto : undefined,
          arquivo: forma === "texto" ? undefined : (arquivo ?? undefined),
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
          }}
        >
          <option value="texto">Texto</option>
          <option value="audio">Fala</option>
          <option value="foto">Foto do que fizeram à mão</option>
        </select>
      </div>

      {forma === "texto" && (
        <div className="cg-campo">
          <label htmlFor="producao-texto">O que a equipe produziu</label>
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
          <Botao variante="secundaria" onClick={alternarGravacao}>
            {gravando ? "Parar a gravação" : arquivo ? "Gravar de novo" : "Gravar a fala"}
          </Botao>
          {arquivo && !gravando && <p role="status">Fala gravada — pronta para enviar.</p>}
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

      <Botao onClick={enviar} desabilitado={enviando || gravando}>
        Entregar
      </Botao>
    </section>
  );
}
