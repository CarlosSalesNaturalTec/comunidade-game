import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo, MarcaDeGravacao } from "comum/react";
import { useState } from "react";
import {
  declararDesafioDeDesbloqueio,
  type MissaoDaTrilha,
  type PerguntaDoDesbloqueioEntrada,
  type TipoDeDesafioDeDesbloqueio,
} from "./api";

interface Props {
  missao: MissaoDaTrilha;
  onAtualizada: (missao: MissaoDaTrilha) => void;
}

const TOTAL_DE_ALTERNATIVAS = 4;

function perguntaVazia(): PerguntaDoDesbloqueioEntrada {
  return { enunciado: "", alternativas: ["", "", "", ""], alternativa_correta: 1 };
}

// O Mestre autor monta o desafio de desbloqueio — quiz ou prático — que
// abre a missão seguinte para o Guerreiro(a). O quiz tem quantas perguntas
// ele quiser, cada uma com quatro alternativas; declarar de novo substitui
// o anterior, e a missão sem desafio segue publicável (`RF-09-26`,
// `RF-09-117`, `RF-09-118`, `RN-09-43`).
export function DesafioDeDesbloqueio({ missao, onAtualizada }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [tipo, definirTipo] = useState<TipoDeDesafioDeDesbloqueio>(
    missao.tipo_do_desafio_de_desbloqueio ?? "quiz",
  );
  const [enunciado, definirEnunciado] = useState(
    missao.desafio_de_desbloqueio_enunciado ?? "",
  );
  const [perguntas, definirPerguntas] = useState<PerguntaDoDesbloqueioEntrada[]>(
    missao.perguntas_do_desbloqueio?.length
      ? missao.perguntas_do_desbloqueio.map((pergunta) => ({
          enunciado: pergunta.enunciado,
          alternativas: [...pergunta.alternativas],
          alternativa_correta: pergunta.alternativa_correta,
        }))
      : [perguntaVazia()],
  );
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [gravadoEm, definirGravadoEm] = useState<Date | null>(null);

  function alterarPergunta(indice: number, mudanca: Partial<PerguntaDoDesbloqueioEntrada>) {
    definirPerguntas(
      perguntas.map((pergunta, posicao) =>
        posicao === indice ? { ...pergunta, ...mudanca } : pergunta,
      ),
    );
  }

  function alterarAlternativa(indice: number, posicao: number, valor: string) {
    const alternativas = [...perguntas[indice].alternativas];
    alternativas[posicao] = valor;
    alterarPergunta(indice, { alternativas });
  }

  async function declarar() {
    if (!sessao) return;
    if (tipo === "quiz" && perguntas.length === 0) {
      definirErro("O quiz precisa de ao menos uma pergunta.");
      return;
    }
    definirErro(null);
    definirEnviando(true);
    try {
      const atualizada = await declararDesafioDeDesbloqueio(
        missao.id,
        {
          tipo,
          enunciado: tipo === "pratico" ? enunciado : null,
          perguntas: tipo === "quiz" ? perguntas : null,
        },
        sessao.token,
      );
      definirGravadoEm(new Date());
      onAtualizada(atualizada);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível declarar o desafio. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <section className="desafio-de-desbloqueio" aria-label={`Desafio de ${missao.titulo}`}>
      <p>Esse desafio é que abre a missão seguinte para o Guerreiro(a).</p>

      {missao.tipo_do_desafio_de_desbloqueio === undefined && (
        <Aviso tipo="andamento">Esta missão ainda não tem desafio de desbloqueio.</Aviso>
      )}

      <div className="desafio-de-desbloqueio__tipo">
        <label>
          <input
            type="radio"
            name={`tipo-${missao.id}`}
            checked={tipo === "quiz"}
            onChange={() => definirTipo("quiz")}
          />
          Quiz
        </label>
        <label>
          <input
            type="radio"
            name={`tipo-${missao.id}`}
            checked={tipo === "pratico"}
            onChange={() => definirTipo("pratico")}
          />
          Desafio prático
        </label>
      </div>

      {tipo === "pratico" && (
        <Campo rotulo="Enunciado" valor={enunciado} aoAlterar={definirEnunciado} />
      )}

      {tipo === "quiz" && (
        <>
          <p className="desafio-de-desbloqueio__corte">
            Passa quem acerta ao menos 60% das perguntas.
          </p>

          {perguntas.map((pergunta, indice) => (
            <fieldset
              // biome-ignore lint/suspicious/noArrayIndexKey: a pergunta só existe pela posição enquanto não foi gravada
              key={indice}
              className="desafio-de-desbloqueio__pergunta"
            >
              <legend>Pergunta {indice + 1}</legend>

              <Campo
                rotulo={`Enunciado da pergunta ${indice + 1}`}
                valor={pergunta.enunciado}
                aoAlterar={(valor) => alterarPergunta(indice, { enunciado: valor })}
              />

              {Array.from({ length: TOTAL_DE_ALTERNATIVAS }, (_, posicao) => (
                // biome-ignore lint/suspicious/noArrayIndexKey: a lista tem tamanho fixo e não é reordenada
                <div key={posicao} className="desafio-de-desbloqueio__alternativa">
                  <input
                    type="radio"
                    name={`alternativa-correta-${missao.id}-${indice}`}
                    checked={pergunta.alternativa_correta === posicao + 1}
                    onChange={() =>
                      alterarPergunta(indice, { alternativa_correta: posicao + 1 })
                    }
                    aria-label={`Alternativa ${posicao + 1} da pergunta ${indice + 1} é a correta`}
                  />
                  <Campo
                    rotulo={`Alternativa ${posicao + 1} da pergunta ${indice + 1}`}
                    valor={pergunta.alternativas[posicao]}
                    aoAlterar={(valor) => alterarAlternativa(indice, posicao, valor)}
                  />
                </div>
              ))}

              <Botao
                variante="secundaria"
                onClick={() =>
                  definirPerguntas(perguntas.filter((_, posicao) => posicao !== indice))
                }
              >
                Remover pergunta {indice + 1}
              </Botao>
            </fieldset>
          ))}

          <Botao
            variante="secundaria"
            onClick={() => definirPerguntas([...perguntas, perguntaVazia()])}
          >
            Acrescentar pergunta
          </Botao>
        </>
      )}

      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Botao onClick={declarar} desabilitado={enviando}>
        {enviando ? "Salvando…" : "Declarar desafio"}
      </Botao>
      <MarcaDeGravacao instante={gravadoEm} />
    </section>
  );
}
