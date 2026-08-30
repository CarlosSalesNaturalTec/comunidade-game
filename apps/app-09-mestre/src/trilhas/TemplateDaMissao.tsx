import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useState } from "react";
import {
  type AtividadeSugerida,
  criarAtividade,
  declararCadenciaDeRetomada,
  type EstruturaSugerida,
  type MissaoDaTrilha,
  pedirEstruturaDaMissao,
  registrarDesfechoDaSugestao,
  substituirEtiquetasOdsDaMissao,
} from "./api";

interface Props {
  missao: MissaoDaTrilha;
  onAtualizada: (missao: MissaoDaTrilha) => void;
}

const ROTULO_DA_MODALIDADE: Record<string, string> = {
  individual: "Individual",
  em_equipe: "Em equipe",
  em_equipe_com_familiar: "Em equipe com familiar",
};

const ROTULO_DO_FORMATO: Record<string, string> = {
  presencial: "Presencial",
  on_line_assincrona: "On-line assíncrona",
};

function ehIgual(a: AtividadeSugerida, b: AtividadeSugerida): boolean {
  return (
    a.titulo === b.titulo &&
    a.modalidade === b.modalidade &&
    a.formato === b.formato &&
    a.natureza === b.natureza &&
    a.producao_esperada === b.producao_esperada
  );
}

// O tópico em texto corrente vira estrutura sugerida e checklist de
// lacunas — o Mestre escreve como falaria, sem pedido de formato, marcação
// ou palavra-chave (`RF-09-85`, `RF-09-91`, `RN-09-16`). Cada item vem
// marcado como proposta, e nada é gravado na missão sem o Mestre aceitar,
// recusar ou alterar (`RF-09-86`, `RF-09-87`, `RF-09-89`, `RN-09-33`).
export function TemplateDaMissao({ missao, onAtualizada }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [topico, definirTopico] = useState("");
  const [resultado, definirResultado] = useState<EstruturaSugerida | null>(null);
  const [atividadesEditaveis, definirAtividadesEditaveis] = useState<AtividadeSugerida[]>([]);
  const [erro, definirErro] = useState<string | null>(null);
  const [pedindo, definirPedindo] = useState(false);
  const [processando, definirProcessando] = useState<number | "desfecho" | null>(null);

  async function aoPedirEstrutura(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    if (!sessao) return;
    if (!topico.trim()) {
      definirErro("Escreva o tópico que você quer ensinar.");
      return;
    }

    definirErro(null);
    definirPedindo(true);
    try {
      const estrutura = await pedirEstruturaDaMissao(missao.id, topico, sessao.token);
      definirResultado(estrutura);
      definirAtividadesEditaveis(estrutura.atividades);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro(
        "Não foi possível pedir a estrutura agora. Você pode seguir escrevendo a missão à mão.",
      );
    } finally {
      definirPedindo(false);
    }
  }

  function alterarAtividade(indice: number, mudanca: Partial<AtividadeSugerida>) {
    definirAtividadesEditaveis((atuais) =>
      atuais.map((atividade, posicao) =>
        posicao === indice ? { ...atividade, ...mudanca } : atividade,
      ),
    );
  }

  async function aceitarAtividade(indice: number) {
    if (!sessao || !resultado) return;
    const editada = atividadesEditaveis[indice];
    const original = resultado.atividades[indice];
    definirErro(null);
    definirProcessando(indice);
    try {
      const atividade = await criarAtividade(
        missao.id,
        {
          titulo: editada.titulo,
          descricao: editada.descricao ?? undefined,
          modalidade: editada.modalidade,
          formato: editada.formato,
          natureza: editada.natureza,
          producao_esperada: editada.producao_esperada,
        },
        sessao.token,
      );
      await registrarDesfechoDaSugestao(
        resultado.sugestao_id,
        ehIgual(editada, original) ? "aceita" : "alterada",
        sessao.token,
      );
      onAtualizada({ ...missao, atividades: [...missao.atividades, atividade] });
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível gravar a atividade aceita. Tente novamente em instantes.");
    } finally {
      definirProcessando(null);
    }
  }

  async function usarCadenciaSugerida() {
    if (!sessao || !resultado) return;
    definirErro(null);
    definirProcessando("desfecho");
    try {
      const atualizada = await declararCadenciaDeRetomada(
        missao.id,
        resultado.cadencia_de_retomada,
        sessao.token,
      );
      onAtualizada(atualizada);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro(
        "Não foi possível declarar a cadência sugerida. Tente novamente em instantes.",
      );
    } finally {
      definirProcessando(null);
    }
  }

  async function usarOdsSugerido() {
    if (!sessao || !resultado || resultado.objetivo_ods === null) return;
    definirErro(null);
    definirProcessando("desfecho");
    try {
      const semODuplicado = missao.etiquetas_ods.filter(
        (etiqueta) => etiqueta.objetivo !== resultado.objetivo_ods,
      );
      const etiquetas = await substituirEtiquetasOdsDaMissao(
        missao.id,
        [
          ...semODuplicado.map((etiqueta) => ({
            objetivo: etiqueta.objetivo,
            meta: etiqueta.meta,
          })),
          { objetivo: resultado.objetivo_ods, meta: resultado.meta_ods },
        ],
        sessao.token,
      );
      onAtualizada({ ...missao, etiquetas_ods: etiquetas });
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível gravar o ODS sugerido. Tente novamente em instantes.");
    } finally {
      definirProcessando(null);
    }
  }

  async function recusarSugestao() {
    if (!sessao || !resultado) return;
    definirErro(null);
    definirProcessando("desfecho");
    try {
      await registrarDesfechoDaSugestao(resultado.sugestao_id, "recusada", sessao.token);
      definirResultado(null);
      definirAtividadesEditaveis([]);
      definirTopico("");
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível registrar a recusa. Tente novamente em instantes.");
    } finally {
      definirProcessando(null);
    }
  }

  return (
    <section className="template-da-missao" aria-label={`Template da missão ${missao.titulo}`}>
      <h3>Template da missão</h3>

      <form onSubmit={aoPedirEstrutura}>
        <Campo
          rotulo="O que você quer ensinar nesta missão?"
          valor={topico}
          aoAlterar={definirTopico}
        />
        <Botao tipo="submit" desabilitado={pedindo}>
          Pedir estrutura sugerida
        </Botao>
      </form>

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {resultado && (
        <div className="template-da-missao__resultado">
          {!resultado.disponivel && resultado.aviso && (
            <Aviso tipo="atencao">{resultado.aviso}</Aviso>
          )}

          {resultado.lacunas.length > 0 && (
            <section aria-label="Lacunas apontadas">
              <h4>O que falta nesta missão</h4>
              <ul>
                {resultado.lacunas.map((lacuna) => (
                  <li key={lacuna}>{lacuna}</li>
                ))}
              </ul>
            </section>
          )}

          {resultado.atividades.length > 0 && (
            <section aria-label="Atividades propostas">
              <h4>Estrutura proposta</h4>
              {atividadesEditaveis.map((atividade, indice) => (
                // Posicional: a proposta não tem identidade estável até o
                // Mestre aceitar, exatamente como as linhas de EtiquetasOds.
                // biome-ignore lint/suspicious/noArrayIndexKey: proposta sem id até gravar
                <div key={indice} className="template-da-missao__atividade">
                  <p className="template-da-missao__marca">Proposta</p>
                  {atividade.desplugada && <p>Atividade desplugada</p>}
                  <Campo
                    rotulo="Título"
                    valor={atividade.titulo}
                    aoAlterar={(valor) => alterarAtividade(indice, { titulo: valor })}
                  />
                  <div className="cg-campo">
                    <label>
                      Modalidade
                      <select
                        value={atividade.modalidade}
                        onChange={(evento) =>
                          alterarAtividade(indice, { modalidade: evento.target.value })
                        }
                      >
                        {Object.entries(ROTULO_DA_MODALIDADE).map(([valor, rotulo]) => (
                          <option key={valor} value={valor}>
                            {rotulo}
                          </option>
                        ))}
                      </select>
                    </label>
                  </div>
                  <div className="cg-campo">
                    <label>
                      Formato
                      <select
                        value={atividade.formato}
                        onChange={(evento) =>
                          alterarAtividade(indice, { formato: evento.target.value })
                        }
                      >
                        {Object.entries(ROTULO_DO_FORMATO).map(([valor, rotulo]) => (
                          <option key={valor} value={valor}>
                            {rotulo}
                          </option>
                        ))}
                      </select>
                    </label>
                  </div>
                  <Campo
                    rotulo="Natureza"
                    valor={atividade.natureza}
                    aoAlterar={(valor) => alterarAtividade(indice, { natureza: valor })}
                  />
                  <Campo
                    rotulo="Produção esperada"
                    valor={atividade.producao_esperada}
                    aoAlterar={(valor) =>
                      alterarAtividade(indice, { producao_esperada: valor })
                    }
                  />
                  <Botao
                    onClick={() => aceitarAtividade(indice)}
                    desabilitado={processando !== null}
                  >
                    Aceitar esta atividade
                  </Botao>
                </div>
              ))}
            </section>
          )}

          <section aria-label="Retomada e ODS sugeridos">
            <p>
              Retomada sugerida: {resultado.cadencia_de_retomada.join(", ")} dias do
              desbloqueio
            </p>
            <Botao
              variante="secundaria"
              onClick={usarCadenciaSugerida}
              desabilitado={processando !== null}
            >
              Usar esta cadência
            </Botao>

            {resultado.objetivo_ods !== null && (
              <>
                <p>{`ODS sugerido: ${resultado.objetivo_ods}`}</p>
                <Botao
                  variante="secundaria"
                  onClick={usarOdsSugerido}
                  desabilitado={processando !== null}
                >
                  Usar este ODS
                </Botao>
              </>
            )}
          </section>

          <Botao
            variante="secundaria"
            onClick={recusarSugestao}
            desabilitado={processando !== null}
          >
            Recusar sugestão
          </Botao>
        </div>
      )}
    </section>
  );
}
