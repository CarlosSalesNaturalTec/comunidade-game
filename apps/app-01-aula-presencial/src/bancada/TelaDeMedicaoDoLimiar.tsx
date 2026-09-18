import {
  acoplarEspelho,
  distanciaEntreDescritores,
  type EstadoDaVivacidade,
  encerrarCaptura,
  gerarDescritor,
  prepararCaptura,
  provarVivacidade,
} from "comum/biometria";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useRef, useState } from "react";
import { Visor } from "../captura/Visor";

interface Props {
  /** Sobre quem a bancada pode abrir a câmera. `operador` é o caminho do
   * diagnóstico, alcançado da tela inicial; `guerreiro` só existe dentro do
   * onboarding, depois de o consentimento ter sido registrado naquela mesma
   * sessão — a aplicação não tem outra forma de saber que o termo existe
   * (`RN-04-33`, `RN-04-07`). */
  alcance: "operador" | "guerreiro";
  /** O nick de quem está sendo medido, só para a tela dizer sobre quem ela
   * fala. Nunca sai daqui. */
  nickDoGuerreiro?: string;
  aoVoltar: () => void;
}

interface Medicao {
  distancia: number;
  momento: number;
}

type Estado =
  | "pronta"
  | "preparando"
  | "capturando"
  | "vivacidade_reprovada"
  | "falha_de_preparo"
  | "erro";

// A bancada do `RF-04-63`: mede a distância entre descritores no aparelho do
// encontro, na mesma unidade que o núcleo usa para decidir se confere, e
// **nada envia ao núcleo** — nem descritor, nem distância. O que sai daqui é
// o número que quem opera lê na tela.
//
// Guarda **um** descritor de referência por vez. Cada captura seguinte é
// comparada com ele e descartada no mesmo ato: os dois só coexistem dentro de
// `medir`, e a comparada nunca chega ao estado do React (`RN-04-32`).
export function TelaDeMedicaoDoLimiar({ alcance, nickDoGuerreiro, aoVoltar }: Props) {
  const [referencia, definirReferencia] = useState<number[] | null>(null);
  const [medicoes, definirMedicoes] = useState<Medicao[]>([]);
  const [estado, definirEstado] = useState<Estado>("pronta");
  const [estadoDoLaco, definirEstadoDoLaco] = useState<EstadoDaVivacidade | null>(null);
  const [mensagemDeErro, definirMensagemDeErro] = useState<string | null>(null);
  const lugarDoVisor = useRef<HTMLDivElement>(null);

  useEffect(() => {
    return () => {
      encerrarCaptura();
    };
  }, []);

  async function capturar(): Promise<number[] | null> {
    definirEstado("preparando");
    definirEstadoDoLaco(null);
    definirMensagemDeErro(null);

    try {
      await prepararCaptura();
    } catch {
      definirEstado("falha_de_preparo");
      return null;
    }

    if (lugarDoVisor.current) acoplarEspelho(lugarDoVisor.current);
    definirEstado("capturando");

    const vivacidadeAprovada = await provarVivacidade(definirEstadoDoLaco);
    if (!vivacidadeAprovada) {
      definirEstado("vivacidade_reprovada");
      return null;
    }
    return await gerarDescritor();
  }

  async function guardarReferencia() {
    try {
      const descritor = await capturar();
      if (descritor === null) return;
      definirReferencia(descritor);
      definirMedicoes([]);
      definirEstado("pronta");
    } catch {
      definirEstado("erro");
      definirMensagemDeErro("Não foi possível capturar. Tente de novo.");
    }
  }

  // A captura comparada morre dentro desta função: o que sobrevive é o
  // número (`RN-04-32`).
  async function medir() {
    if (referencia === null) return;
    try {
      const descritor = await capturar();
      if (descritor === null) return;
      const distancia = distanciaEntreDescritores(descritor, referencia);
      definirEstado("pronta");
      if (distancia === null) {
        definirMensagemDeErro("Os descritores têm tamanhos diferentes.");
        definirEstado("erro");
        return;
      }
      definirMedicoes((anteriores) => [...anteriores, { distancia, momento: Date.now() }]);
    } catch {
      definirEstado("erro");
      definirMensagemDeErro("Não foi possível capturar. Tente de novo.");
    }
  }

  const emAndamento = estado === "preparando" || estado === "capturando";
  const sujeito =
    alcance === "guerreiro" ? (nickDoGuerreiro ?? "o Guerreiro(a) do cadastro") : "quem opera";

  return (
    <Moldura>
      <Cabecalho
        titulo="Medição do limiar"
        subtitulo={`Mede a distância entre capturas de ${sujeito}. Nada sai deste aparelho.`}
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />

      {alcance === "operador" && (
        <Aviso tipo="atencao">
          Aqui a câmera só mede quem opera. Para medir um Guerreiro(a), use a medição do
          onboarding, depois do termo assinado.
        </Aviso>
      )}

      <Visor lugar={lugarDoVisor} estado={estado === "capturando" ? estadoDoLaco : null} />
      {estado === "preparando" && <EstadoDaLista>Preparando a câmera…</EstadoDaLista>}
      {estado === "falha_de_preparo" && (
        <Aviso tipo="erro">
          A câmera não pôde ser preparada neste aparelho. Tente de novo; se continuar, a
          medição exige outro aparelho.
        </Aviso>
      )}
      {estado === "vivacidade_reprovada" && (
        <Aviso tipo="atencao">
          Não foi possível confirmar que há uma pessoa diante da câmera. Tente de novo.
        </Aviso>
      )}
      {estado === "erro" && mensagemDeErro && <Aviso tipo="erro">{mensagemDeErro}</Aviso>}

      <Botao onClick={guardarReferencia} desabilitado={emAndamento}>
        {referencia === null ? "Capturar a referência" : "Trocar a referência"}
      </Botao>

      <Botao
        variante="secundaria"
        onClick={medir}
        desabilitado={emAndamento || referencia === null}
      >
        Capturar e comparar com a referência
      </Botao>

      {referencia === null ? (
        <EstadoDaLista>
          Capture a referência primeiro. Depois, cada nova captura é comparada com ela e
          descartada no mesmo ato.
        </EstadoDaLista>
      ) : (
        <ol className="cg-medicoes">
          {medicoes.map((medicao) => (
            <li key={medicao.momento}>
              distância <strong>{medicao.distancia.toFixed(3)}</strong>
            </li>
          ))}
        </ol>
      )}

      <p className="cg-aviso-de-coleta">
        A distância aparece na mesma unidade que o núcleo usa para comparar. Anote os números:
        a mesma pessoa em capturas seguidas dá o piso; pessoas diferentes dão o teto.
      </p>
    </Moldura>
  );
}
