import { ErroDaApi } from "comum/api";
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
import { gravarMedicaoDoLimiar } from "../api/medicoesDoLimiar";
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
  /** A aula em curso determina o **ponto de apoio** que recebe o limiar, e o
   * token é o de quem confirma — Mestre ou Admin (`RF-04-66`, `RF-01-73`). */
  tokenDeTrabalho: string;
  aulaId: string;
  aoVoltar: () => void;
}

/** Qual das duas séries está sendo capturada. O piso é a mesma pessoa contra
 * a referência; o teto, pessoas diferentes dela. É a folga entre as duas que
 * diz se existe limiar viável (`RF-04-66`, `RN-04-35`). */
type Serie = "piso" | "teto";

interface Medicao {
  distancia: number;
  momento: number;
}

type Estado =
  | "pronta"
  | "preparando"
  | "capturando"
  | "gravando"
  | "gravada"
  | "vivacidade_reprovada"
  | "falha_de_preparo"
  | "erro";

// Os mínimos do `RN-04-35`, os mesmos que o núcleo reconfere ao gravar: o
// cálculo do aparelho não é autoridade sobre o que fica guardado.
const MINIMO_DE_MEDICOES_POR_SERIE = 8;
const MINIMO_DE_PESSOAS_NO_TETO = 2;

/** O ponto médio entre o maior piso e o menor teto — equidistante das duas
 * formas de errar: recusar quem é e aceitar quem não é (`RN-04-35`). O núcleo
 * calcula o mesmo número das mesmas séries; aqui ele existe para quem opera
 * ver o que está confirmando. */
export function limiarProposto(piso: number[], teto: number[]): number {
  return (Math.max(...piso) + Math.min(...teto)) / 2;
}

// A bancada do `RF-04-63`, alargada pelo `RF-04-66`: mede a distância entre
// descritores no aparelho do encontro, na mesma unidade que o núcleo usa, em
// **duas séries declaradas** — e, concluída a medição, grava o limiar no ponto
// de apoio da aula. Descritor e imagem **nunca** saem daqui; o que sai é o
// número e as distâncias (`RN-04-32`, documento 03 §3.3).
//
// Guarda **um** descritor de referência por vez. Cada captura seguinte é
// comparada com ele e descartada no mesmo ato: os dois só coexistem dentro de
// `medir`, e a comparada nunca chega ao estado do React (`RN-04-32`).
export function TelaDeMedicaoDoLimiar({
  alcance,
  nickDoGuerreiro,
  tokenDeTrabalho,
  aulaId,
  aoVoltar,
}: Props) {
  const [referencia, definirReferencia] = useState<number[] | null>(null);
  const [serie, definirSerie] = useState<Serie>("piso");
  const [piso, definirPiso] = useState<Medicao[]>([]);
  const [teto, definirTeto] = useState<Medicao[]>([]);
  const [pessoasNoTeto, definirPessoasNoTeto] = useState(0);
  const [estado, definirEstado] = useState<Estado>("pronta");
  const [estadoDoLaco, definirEstadoDoLaco] = useState<EstadoDaVivacidade | null>(null);
  const [mensagemDeErro, definirMensagemDeErro] = useState<string | null>(null);
  const [limiarGravado, definirLimiarGravado] = useState<number | null>(null);
  const lugarDoVisor = useRef<HTMLDivElement>(null);

  useEffect(() => {
    return () => {
      encerrarCaptura();
    };
  }, []);

  function recomecar() {
    definirPiso([]);
    definirTeto([]);
    definirPessoasNoTeto(0);
    definirSerie("piso");
    definirLimiarGravado(null);
  }

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
      recomecar();
      definirEstado("pronta");
    } catch {
      definirEstado("erro");
      definirMensagemDeErro("Não foi possível capturar. Tente de novo.");
    }
  }

  // A captura comparada morre dentro desta função: o que sobrevive é o
  // número, na série que quem opera declarou (`RN-04-32`, `RF-04-66`).
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
      const nova = { distancia, momento: Date.now() };
      if (serie === "piso") {
        definirPiso((anteriores) => [...anteriores, nova]);
      } else {
        definirTeto((anteriores) => [...anteriores, nova]);
        // A primeira captura do teto já é de uma pessoa: quem opera só declara
        // as trocas seguintes.
        definirPessoasNoTeto((quantas) => (quantas === 0 ? 1 : quantas));
      }
    } catch {
      definirEstado("erro");
      definirMensagemDeErro("Não foi possível capturar. Tente de novo.");
    }
  }

  const distanciasDoPiso = piso.map((medicao) => medicao.distancia);
  const distanciasDoTeto = teto.map((medicao) => medicao.distancia);
  const maiorPiso = distanciasDoPiso.length > 0 ? Math.max(...distanciasDoPiso) : null;
  const menorTeto = distanciasDoTeto.length > 0 ? Math.min(...distanciasDoTeto) : null;

  const seriesCompletas =
    piso.length >= MINIMO_DE_MEDICOES_POR_SERIE &&
    teto.length >= MINIMO_DE_MEDICOES_POR_SERIE &&
    pessoasNoTeto >= MINIMO_DE_PESSOAS_NO_TETO;
  const temFolga = maiorPiso !== null && menorTeto !== null && maiorPiso < menorTeto;
  const concluida = seriesCompletas && temFolga;
  const proposto = concluida ? limiarProposto(distanciasDoPiso, distanciasDoTeto) : null;

  async function confirmarEGravar() {
    if (proposto === null) return;
    definirEstado("gravando");
    definirMensagemDeErro(null);
    try {
      const gravada = await gravarMedicaoDoLimiar(
        {
          aula_id: aulaId,
          distancias_do_piso: distanciasDoPiso,
          distancias_do_teto: distanciasDoTeto,
          pessoas_no_teto: pessoasNoTeto,
        },
        tokenDeTrabalho,
      );
      definirLimiarGravado(gravada.limiar);
      definirEstado("gravada");
    } catch (erroCapturado) {
      definirEstado("erro");
      definirMensagemDeErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível gravar o limiar. Tente de novo.",
      );
    }
  }

  const emAndamento =
    estado === "preparando" || estado === "capturando" || estado === "gravando";
  const sujeito =
    alcance === "guerreiro" ? (nickDoGuerreiro ?? "o Guerreiro(a) do cadastro") : "quem opera";

  return (
    <Moldura>
      <Cabecalho
        titulo="Medição do limiar"
        subtitulo={`Mede a distância entre capturas de ${sujeito}. Descritor e imagem não saem deste aparelho.`}
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
      {estado === "gravando" && <EstadoDaLista>Gravando o limiar…</EstadoDaLista>}
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
      {estado === "gravada" && limiarGravado !== null && (
        <Aviso tipo="sucesso">
          Limiar <strong>{limiarGravado.toFixed(3)}</strong> gravado para o ponto de apoio
          desta aula. A partir de agora, o reconhecimento facial passa a conferir aqui.
        </Aviso>
      )}

      <Botao onClick={guardarReferencia} desabilitado={emAndamento}>
        {referencia === null ? "Capturar a referência" : "Trocar a referência"}
      </Botao>

      {referencia === null ? (
        <EstadoDaLista>
          Capture a referência primeiro: é a pessoa com quem todas as outras capturas serão
          comparadas. Cada captura seguinte é comparada com ela e descartada no mesmo ato.
        </EstadoDaLista>
      ) : (
        <>
          <fieldset className="cg-series">
            <legend>O que está sendo medido agora</legend>
            <Botao
              variante={serie === "piso" ? "primaria" : "secundaria"}
              onClick={() => definirSerie("piso")}
              desabilitado={emAndamento}
            >
              Piso — a mesma pessoa da referência
            </Botao>
            <Botao
              variante={serie === "teto" ? "primaria" : "secundaria"}
              onClick={() => definirSerie("teto")}
              desabilitado={emAndamento}
            >
              Teto — outra pessoa
            </Botao>
          </fieldset>

          <Botao variante="secundaria" onClick={medir} desabilitado={emAndamento}>
            Capturar e comparar com a referência
          </Botao>

          {serie === "teto" && (
            <Botao
              variante="secundaria"
              onClick={() => definirPessoasNoTeto((quantas) => quantas + 1)}
              desabilitado={emAndamento || teto.length === 0}
            >
              Trocou a pessoa diante da câmera
            </Botao>
          )}

          <section className="cg-serie-medida">
            <h3>
              Piso — {piso.length} de {MINIMO_DE_MEDICOES_POR_SERIE}
            </h3>
            <ol className="cg-medicoes">
              {piso.map((medicao) => (
                <li key={medicao.momento}>
                  distância <strong>{medicao.distancia.toFixed(3)}</strong>
                </li>
              ))}
            </ol>
            {maiorPiso !== null && (
              <p>
                maior piso <strong>{maiorPiso.toFixed(3)}</strong>
              </p>
            )}
          </section>

          <section className="cg-serie-medida">
            <h3>
              Teto — {teto.length} de {MINIMO_DE_MEDICOES_POR_SERIE}, com {pessoasNoTeto} de{" "}
              {MINIMO_DE_PESSOAS_NO_TETO} pessoas
            </h3>
            <ol className="cg-medicoes">
              {teto.map((medicao) => (
                <li key={medicao.momento}>
                  distância <strong>{medicao.distancia.toFixed(3)}</strong>
                </li>
              ))}
            </ol>
            {menorTeto !== null && (
              <p>
                menor teto <strong>{menorTeto.toFixed(3)}</strong>
              </p>
            )}
          </section>

          {!seriesCompletas && (
            <EstadoDaLista>
              Faltam capturas: o piso e o teto precisam de {MINIMO_DE_MEDICOES_POR_SERIE} cada,
              e o teto precisa de ao menos {MINIMO_DE_PESSOAS_NO_TETO} pessoas diferentes da
              referência.
            </EstadoDaLista>
          )}

          {seriesCompletas && !temFolga && (
            <Aviso tipo="erro">
              As séries se sobrepõem: o maior piso alcança o menor teto, e não existe limiar
              viável com estas capturas. Meça de novo, com o rosto de frente e boa luz.
            </Aviso>
          )}

          {concluida && proposto !== null && estado !== "gravada" && (
            <>
              <Aviso tipo="atencao">
                Limiar proposto: <strong>{proposto.toFixed(3)}</strong> — o ponto médio entre o
                maior piso e o menor teto. Confirmando, ele passa a valer para o ponto de apoio
                desta aula.
              </Aviso>
              <Botao onClick={confirmarEGravar} desabilitado={emAndamento}>
                Confirmar e gravar o limiar
              </Botao>
            </>
          )}
        </>
      )}

      <p className="cg-aviso-de-coleta">
        A distância aparece na mesma unidade que o núcleo usa para comparar. Ao confirmar, só o
        limiar e as distâncias medidas são gravados — nunca a imagem nem o descritor.
      </p>
    </Moldura>
  );
}
