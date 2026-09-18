import { ErroDaApi } from "comum/api";
import {
  acoplarEspelho,
  type EstadoDaVivacidade,
  encerrarCaptura,
  gerarDescritor,
  prepararCaptura,
  provarVivacidade,
} from "comum/biometria";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useRef, useState } from "react";
import { enviarDescritor } from "../api/descritor";
import { Visor } from "../captura/Visor";
import { AreaDetalhadaDeDireitos } from "../direitos/AreaDetalhadaDeDireitos";

interface Props {
  tokenDeTrabalho: string;
  guerreiroId: string;
  aoConcluir: () => void;
  aoVoltar: () => void;
  /** Só existe no onboarding: aqui o consentimento acabou de ser registrado,
   * e é a única situação em que a bancada pode medir um Guerreiro(a)
   * (`RF-04-63`, `RN-04-33`). */
  aoMedirOLimiar?: () => void;
}

type Estado =
  | "pronta"
  | "preparando"
  | "capturando"
  | "vivacidade_reprovada"
  | "falha_de_preparo"
  | "erro";

// A prova de vivacidade sempre antes do descritor, e nenhum envio acontece
// sem ela passar (`RF-04-13`, `RF-04-48`, documento 03 §3.3). O módulo de
// biometria é o único que toca a câmera — esta tela só chama as duas
// funções que ele expõe e nunca vê a fotografia (`RN-04-08`, `RN-04-12`).
export function TelaDeCaptura({
  tokenDeTrabalho,
  guerreiroId,
  aoConcluir,
  aoVoltar,
  aoMedirOLimiar,
}: Props) {
  const [estado, definirEstado] = useState<Estado>("pronta");
  const [estadoDoLaco, definirEstadoDoLaco] = useState<EstadoDaVivacidade | null>(null);
  const [mensagemDeErro, definirMensagemDeErro] = useState<string | null>(null);
  const [mostrarDireitos, definirMostrarDireitos] = useState(false);
  const lugarDoVisor = useRef<HTMLDivElement>(null);

  useEffect(() => {
    return () => {
      encerrarCaptura();
    };
  }, []);

  if (mostrarDireitos) {
    return <AreaDetalhadaDeDireitos aoVoltar={() => definirMostrarDireitos(false)} />;
  }

  async function iniciarCaptura() {
    definirEstado("preparando");
    definirEstadoDoLaco(null);
    definirMensagemDeErro(null);

    // O preparo tem desfecho próprio: modelo que não carregou NEVER sai pela
    // frase da vivacidade reprovada (`RF-04-65`).
    try {
      await prepararCaptura();
    } catch {
      definirEstado("falha_de_preparo");
      return;
    }

    if (lugarDoVisor.current) acoplarEspelho(lugarDoVisor.current);
    definirEstado("capturando");

    try {
      const vivacidadeAprovada = await provarVivacidade(definirEstadoDoLaco);
      if (!vivacidadeAprovada) {
        definirEstado("vivacidade_reprovada");
        return;
      }
      const descritor = await gerarDescritor();
      await enviarDescritor(guerreiroId, { descritor }, tokenDeTrabalho);
      aoConcluir();
    } catch (erroCapturado) {
      definirEstado("erro");
      // A recusa do núcleo chega inteira ao Mestre, como a `TelaDoTermo` ao
      // lado já faz: a rota tem mais de um motivo para recusar com 422, e
      // trocar todos por uma frase própria fez um erro de dimensão do
      // descritor ser lido como falta de consentimento por semanas
      // (`RF-04-13`, `RF-04-20`, `RF-01-02`). Frase própria só onde não há
      // corpo de erro — a falha que acontece antes de a resposta existir.
      definirMensagemDeErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível concluir a captura. Tente novamente.",
      );
    }
  }

  const emAndamento = estado === "preparando" || estado === "capturando";

  return (
    <Moldura>
      <Cabecalho
        titulo="Captura da imagem"
        subtitulo="Olhe para a câmera. A fotografia não sai deste aparelho."
        acao={{ rotulo: "Voltar ao início", aoAcionar: aoVoltar }}
      />
      <Visor lugar={lugarDoVisor} estado={estado === "capturando" ? estadoDoLaco : null} />
      {estado === "preparando" && <EstadoDaLista>Preparando a câmera…</EstadoDaLista>}
      {estado === "falha_de_preparo" && (
        <Aviso tipo="erro">
          A câmera não pôde ser preparada neste aparelho. Tente de novo; se continuar, use
          outro aparelho para a captura.
        </Aviso>
      )}
      {estado === "vivacidade_reprovada" && (
        <Aviso tipo="atencao">
          Não foi possível confirmar que há uma pessoa diante da câmera. Tente de novo, com o
          rosto bem posicionado.
        </Aviso>
      )}
      {estado === "erro" && mensagemDeErro && <Aviso tipo="erro">{mensagemDeErro}</Aviso>}
      <Botao onClick={iniciarCaptura} desabilitado={emAndamento}>
        {emAndamento ? "Capturando…" : "Iniciar captura"}
      </Botao>
      {aoMedirOLimiar && (
        <Botao variante="secundaria" onClick={aoMedirOLimiar} desabilitado={emAndamento}>
          Medir o limiar com este Guerreiro(a)
        </Botao>
      )}
      <p className="cg-aviso-de-coleta">
        A câmera aparece na tela só para você se ver; a foto é apagada assim que o descritor é
        gerado, e nem uma nem outra sai deste aparelho.{" "}
        <button type="button" className="cg-link" onClick={() => definirMostrarDireitos(true)}>
          Veja o que a gente coleta e para quê
        </button>
        .
      </p>
    </Moldura>
  );
}
