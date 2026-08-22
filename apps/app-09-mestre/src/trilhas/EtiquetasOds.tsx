import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { useId, useState } from "react";
import {
  type EtiquetaOds,
  type EtiquetaOdsDeclarada,
  substituirEtiquetasOdsDaMissao,
  substituirEtiquetasOdsDaTrilha,
} from "./api";

type Alvo = "trilha" | "missao";

interface Props {
  alvo: Alvo;
  id: string;
  etiquetas: EtiquetaOds[];
  onSalvo: (etiquetas: EtiquetaOds[]) => void;
}

interface LinhaEmEdicao {
  objetivo: string;
  meta: string;
}

// De 1 a 18 — o 18 é adoção voluntária do Brasil, e a faixa é a que o
// núcleo aceita (`RF-09-92`).
const OBJETIVOS = Array.from({ length: 18 }, (_, indice) => indice + 1);

const ROTULO_DO_ALVO: Record<Alvo, string> = {
  trilha: "ODS da trilha",
  missao: "ODS da missão",
};

function rotuloDaEtiqueta(etiqueta: EtiquetaOds): string {
  return etiqueta.meta
    ? `ODS ${etiqueta.objetivo} — meta ${etiqueta.meta}`
    : `ODS ${etiqueta.objetivo}`;
}

// O Mestre acrescenta, altera e remove à vontade, e só a confirmação
// grava: a rota recebe a lista completa e substitui o conjunto do alvo de
// uma vez (`RF-09-92`, `RF-09-98`, `RF-09-12`).
export function EtiquetasOds({ alvo, id, etiquetas, onSalvo }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idBase = useId();
  const [editando, definirEditando] = useState(false);
  const [linhas, definirLinhas] = useState<LinhaEmEdicao[]>([]);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  function abrir() {
    definirLinhas(
      etiquetas.map((etiqueta) => ({
        objetivo: String(etiqueta.objetivo),
        meta: etiqueta.meta ?? "",
      })),
    );
    definirErro(null);
    definirEditando(true);
  }

  function alterarLinha(indice: number, mudanca: Partial<LinhaEmEdicao>) {
    definirLinhas((atuais) =>
      atuais.map((linha, posicao) => (posicao === indice ? { ...linha, ...mudanca } : linha)),
    );
  }

  function removerLinha(indice: number) {
    definirLinhas((atuais) => atuais.filter((_, posicao) => posicao !== indice));
  }

  async function confirmar() {
    if (!sessao) return;
    definirErro(null);

    const declaradas: EtiquetaOdsDeclarada[] = [];
    for (const linha of linhas) {
      const objetivo = Number(linha.objetivo);
      if (!Number.isInteger(objetivo) || objetivo === 0) {
        definirErro("Escolha o objetivo de cada linha antes de confirmar.");
        return;
      }
      declaradas.push({ objetivo, meta: linha.meta.trim() || null });
    }

    definirEnviando(true);
    try {
      const gravadas =
        alvo === "trilha"
          ? await substituirEtiquetasOdsDaTrilha(id, declaradas, sessao.token)
          : await substituirEtiquetasOdsDaMissao(id, declaradas, sessao.token);
      definirEditando(false);
      onSalvo(gravadas);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi) {
        definirErro(erroCapturado.message);
        return;
      }
      definirErro("Não foi possível gravar os ODS. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <section className="etiquetas-ods" aria-label={ROTULO_DO_ALVO[alvo]}>
      <h3>{ROTULO_DO_ALVO[alvo]}</h3>

      {alvo === "missao" && (
        <p className="etiquetas-ods__nota">
          Etiquete a missão só quando ela tocar objetivo diferente do da trilha. Missão sem
          etiqueta própria responde pela etiqueta da trilha.
        </p>
      )}

      {etiquetas.length > 0 ? (
        <ul aria-label={`Objetivos declarados — ${ROTULO_DO_ALVO[alvo]}`}>
          {etiquetas.map((etiqueta) => (
            <li key={etiqueta.id}>{rotuloDaEtiqueta(etiqueta)}</li>
          ))}
        </ul>
      ) : (
        <p>Sem ODS declarado.</p>
      )}

      {editando ? (
        <div>
          {linhas.map((linha, indice) => {
            const idDoObjetivo = `${idBase}-objetivo-${indice}`;
            return (
              // As linhas são posicionais e não têm identidade estável
              // enquanto não gravam — a posição é a chave honesta aqui.
              // biome-ignore lint/suspicious/noArrayIndexKey: linha sem id até gravar
              <div className="etiquetas-ods__linha" key={indice}>
                <div className="cg-campo">
                  <label htmlFor={idDoObjetivo}>{`Objetivo ${indice + 1}`}</label>
                  <select
                    id={idDoObjetivo}
                    value={linha.objetivo}
                    onChange={(evento) =>
                      alterarLinha(indice, { objetivo: evento.target.value })
                    }
                  >
                    <option value="">Selecione</option>
                    {OBJETIVOS.map((objetivo) => (
                      <option key={objetivo} value={String(objetivo)}>
                        {`ODS ${objetivo}`}
                      </option>
                    ))}
                  </select>
                </div>

                <Campo
                  rotulo={`Meta do objetivo ${indice + 1} (opcional)`}
                  valor={linha.meta}
                  aoAlterar={(valor) => alterarLinha(indice, { meta: valor })}
                />

                <Botao variante="secundaria" onClick={() => removerLinha(indice)}>
                  {`Remover objetivo ${indice + 1}`}
                </Botao>
              </div>
            );
          })}

          {erro && <Aviso tipo="erro">{erro}</Aviso>}

          <Botao
            variante="secundaria"
            onClick={() => definirLinhas((atuais) => [...atuais, { objetivo: "", meta: "" }])}
          >
            Acrescentar objetivo
          </Botao>
          <Botao onClick={confirmar} desabilitado={enviando}>
            {`Confirmar ${ROTULO_DO_ALVO[alvo]}`}
          </Botao>
          <Botao variante="secundaria" onClick={() => definirEditando(false)}>
            Cancelar
          </Botao>
        </div>
      ) : (
        <Botao variante="secundaria" onClick={abrir}>
          {etiquetas.length > 0
            ? `Alterar ${ROTULO_DO_ALVO[alvo]}`
            : `Etiquetar ${ROTULO_DO_ALVO[alvo]}`}
        </Botao>
      )}
    </section>
  );
}
