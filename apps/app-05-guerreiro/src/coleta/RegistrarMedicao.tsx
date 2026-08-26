import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { useState } from "react";
import { type RegistroGravado, registrarMedicao, type SerieDoGuerreiro } from "../api/coleta";
import { AvisoDeColeta } from "./AvisoDeColeta";

// Sem rede, a recusa é imediata e nada fica guardado no aparelho — nenhuma
// fila, nenhuma medição, nenhuma mídia (`RF-05-85`, PRD-05 §§10, 13).
const SEM_REDE =
  "Sem internet agora — não deu para gravar. Espere a conexão voltar e tente de novo.";

type ConstrutorDeReconhecimento = new () => {
  lang: string;
  start: () => void;
  onresult:
    | ((evento: {
        results: { [indice: number]: { [indice: number]: { transcript: string } } };
      }) => void)
    | null;
  onerror: (() => void) | null;
  onend: (() => void) | null;
};

// A API de voz do navegador não existe em todo aparelho modesto — o
// ditado é oferecido só quando ela existe, e a digitação continua sendo o
// caminho sempre disponível (design — Risks).
function obterConstrutorDeReconhecimento(): ConstrutorDeReconhecimento | null {
  const global = window as unknown as {
    SpeechRecognition?: ConstrutorDeReconhecimento;
    webkitSpeechRecognition?: ConstrutorDeReconhecimento;
  };
  return global.SpeechRecognition ?? global.webkitSpeechRecognition ?? null;
}

function extrairNumero(transcricao: string): number | null {
  const encontrado = transcricao.match(/-?\d+(?:[.,]\d+)?/);
  if (!encontrado) return null;
  return Number.parseFloat(encontrado[0].replace(",", "."));
}

interface Props {
  serie: SerieDoGuerreiro;
  aoConcluir: () => void;
}

// Registro da medição — digitado, ditado por voz, foto ou vídeo — com a
// origem gravada; dentro da faixa pontua na hora, fora da faixa entra "a
// conferir" (`RF-05-33`, `RF-05-34`, `RF-05-35`, PRD-05 §§6.4, 11).
export function RegistrarMedicao({ serie, aoConcluir }: Props) {
  const { sessao } = useSessao();
  const [valorDigitado, definirValorDigitado] = useState("");
  const [origem, definirOrigem] = useState<"manual" | "voz">("manual");
  const [midia, definirMidia] = useState<File | null>(null);
  const [ouvindo, definirOuvindo] = useState(false);
  const [enviando, definirEnviando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [resultado, definirResultado] = useState<RegistroGravado | null>(null);

  const formaDeRegistro = serie.tipo_de_coleta.forma_de_registro;
  const construtorDeReconhecimento = obterConstrutorDeReconhecimento();

  function ditarPorVoz() {
    if (!construtorDeReconhecimento) return;
    const reconhecimento = new construtorDeReconhecimento();
    reconhecimento.lang = "pt-BR";
    reconhecimento.onresult = (evento) => {
      const transcricao = evento.results[0][0].transcript;
      const numero = extrairNumero(transcricao);
      if (numero === null) {
        definirErro("Não entendi o valor dito. Tente digitar.");
        return;
      }
      definirErro(null);
      definirValorDigitado(String(numero));
      definirOrigem("voz");
    };
    reconhecimento.onerror = () => definirOuvindo(false);
    reconhecimento.onend = () => definirOuvindo(false);
    definirOuvindo(true);
    reconhecimento.start();
  }

  async function aoEnviar() {
    if (!sessao) return;
    if (!navigator.onLine) {
      definirErro(SEM_REDE);
      return;
    }
    definirEnviando(true);
    definirErro(null);
    try {
      const gravado = await registrarMedicao(
        {
          serieId: serie.id,
          momentoDoFato: new Date().toISOString(),
          origem: formaDeRegistro === "numero" ? origem : "manual",
          valor: formaDeRegistro === "numero" ? Number(valorDigitado) : undefined,
          unidade:
            formaDeRegistro === "numero"
              ? (serie.tipo_de_coleta.unidade ?? undefined)
              : undefined,
          midia: formaDeRegistro !== "numero" && midia ? midia : undefined,
        },
        sessao.token,
      );
      definirResultado(gravado);
    } catch (erroCapturado) {
      definirErro(erroCapturado instanceof ErroDaApi ? erroCapturado.message : SEM_REDE);
    } finally {
      definirEnviando(false);
    }
  }

  if (resultado) {
    return (
      <section aria-label="Resultado do registro">
        {resultado.pontuou ? (
          <Aviso tipo="sucesso">
            Sua medição valeu! Você ganhou {resultado.pontos_creditados} pontos.
          </Aviso>
        ) : resultado.a_conferir ? (
          <Aviso tipo="andamento">
            Sua medição foi guardada! O Mestre vai dar uma olhada nela. Se estiver tudo certo,
            os pontos entram depois.
          </Aviso>
        ) : (
          <Aviso tipo="sucesso">Sua medição foi guardada!</Aviso>
        )}
        <Botao onClick={aoConcluir}>Voltar às minhas séries</Botao>
      </section>
    );
  }

  const podeEnviar =
    formaDeRegistro === "numero" ? valorDigitado.trim() !== "" : midia !== null;

  return (
    <section aria-label="Registrar medição">
      <AvisoDeColeta />
      <h2>{serie.tipo_de_coleta.nome}</h2>

      {formaDeRegistro === "numero" && (
        <>
          <Campo
            rotulo={`Valor${serie.tipo_de_coleta.unidade ? ` (${serie.tipo_de_coleta.unidade})` : ""}`}
            valor={valorDigitado}
            tipo="number"
            aoAlterar={(valor) => {
              definirValorDigitado(valor);
              definirOrigem("manual");
            }}
          />
          {construtorDeReconhecimento && (
            <Botao variante="secundaria" onClick={ditarPorVoz} desabilitado={ouvindo}>
              {ouvindo ? "Ouvindo…" : "Falar o valor"}
            </Botao>
          )}
        </>
      )}

      {formaDeRegistro !== "numero" && (
        <div className="cg-campo">
          <label htmlFor="cg-midia-do-registro">
            {formaDeRegistro === "foto" ? "Envie uma foto" : "Envie um vídeo"}
          </label>
          <input
            id="cg-midia-do-registro"
            type="file"
            accept={formaDeRegistro === "foto" ? "image/*" : "video/*"}
            onChange={(evento) => definirMidia(evento.target.files?.[0] ?? null)}
          />
        </div>
      )}

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      <Botao desabilitado={!podeEnviar || enviando} onClick={aoEnviar}>
        Gravar medição
      </Botao>
    </section>
  );
}
