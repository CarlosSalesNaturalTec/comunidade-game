import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo, MarcaDeGravacao } from "comum/react";
import { useState } from "react";
import {
  abrirEnvioDaImagemDaPergunta,
  confirmarEnvioDaImagemDaPergunta,
  declararDesafioDeDesbloqueio,
  enviarArquivo,
  FORMATOS_DA_IMAGEM_DA_PERGUNTA,
  FORMATOS_DA_IMAGEM_DA_PERGUNTA_EM_PORTUGUES,
  type MissaoDaTrilha,
  type PerguntaDoDesbloqueioEntrada,
  TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA,
  type TipoDeDesafioDeDesbloqueio,
} from "./api";

interface Props {
  missao: MissaoDaTrilha;
  onAtualizada: (missao: MissaoDaTrilha) => void;
}

const TOTAL_DE_ALTERNATIVAS = 4;

// A pergunta ganha `id` só depois de gravada — e é o id que endereça o
// envio da imagem. Enquanto ela existe apenas na tela, não há o que anexar
// (`RF-09-119`).
interface PerguntaEmEdicao extends PerguntaDoDesbloqueioEntrada {
  id?: string;
}

function perguntaVazia(): PerguntaEmEdicao {
  return { enunciado: "", alternativas: ["", "", "", ""], alternativa_correta: 1 };
}

function comoEdicao(missao: MissaoDaTrilha): PerguntaEmEdicao[] {
  return missao.perguntas_do_desbloqueio?.length
    ? missao.perguntas_do_desbloqueio.map((pergunta) => ({
        id: pergunta.id,
        enunciado: pergunta.enunciado,
        alternativas: [...pergunta.alternativas],
        alternativa_correta: pergunta.alternativa_correta,
        imagem_referencia: pergunta.imagem_referencia ?? null,
      }))
    : [perguntaVazia()];
}

function emMegabytes(bytes: number): string {
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
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
  const [perguntas, definirPerguntas] = useState<PerguntaEmEdicao[]>(comoEdicao(missao));
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [gravadoEm, definirGravadoEm] = useState<Date | null>(null);
  // O erro e o progresso do envio são **por pergunta**: a recusa de uma
  // imagem nunca apaga nem esconde o que o Mestre escreveu nas outras.
  const [erroDaImagem, definirErroDaImagem] = useState<Record<number, string>>({});
  const [progressoDaImagem, definirProgressoDaImagem] = useState<
    Record<number, { enviados: number; total: number }>
  >({});

  function alterarPergunta(indice: number, mudanca: Partial<PerguntaEmEdicao>) {
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

  // Anexar e trocar são a mesma operação: o envio confirmado sobrescreve a
  // referência daquela pergunta. O teto e os formatos são conferidos aqui
  // **e** no núcleo — aqui para o Mestre saber na hora, lá porque é o
  // núcleo que decide (`RF-09-119`).
  async function anexarImagem(indice: number, arquivo: File) {
    const pergunta = perguntas[indice];
    if (!sessao) return;
    if (!pergunta.id) {
      definirErroDaImagem({
        ...erroDaImagem,
        [indice]: "Grave o desafio antes de anexar a imagem desta pergunta.",
      });
      return;
    }
    if (!FORMATOS_DA_IMAGEM_DA_PERGUNTA.includes(arquivo.type)) {
      definirErroDaImagem({
        ...erroDaImagem,
        [indice]:
          `O arquivo é ${arquivo.type || "de formato desconhecido"}. ` +
          `Os formatos aceitos são ${FORMATOS_DA_IMAGEM_DA_PERGUNTA_EM_PORTUGUES}.`,
      });
      return;
    }
    if (arquivo.size > TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA) {
      definirErroDaImagem({
        ...erroDaImagem,
        [indice]:
          `A imagem tem ${emMegabytes(arquivo.size)} e o limite é ` +
          `${emMegabytes(TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA)}.`,
      });
      return;
    }

    definirErroDaImagem({ ...erroDaImagem, [indice]: "" });
    try {
      const endereco = await abrirEnvioDaImagemDaPergunta(
        pergunta.id,
        arquivo.type,
        arquivo.size,
        sessao.token,
      );
      await enviarArquivo(endereco, arquivo, (enviados, total) =>
        definirProgressoDaImagem((atual) => ({ ...atual, [indice]: { enviados, total } })),
      );
      const confirmada = await confirmarEnvioDaImagemDaPergunta(pergunta.id, sessao.token);
      alterarPergunta(indice, { imagem_referencia: confirmada.imagem_referencia ?? null });
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDaImagem({
        ...erroDaImagem,
        [indice]:
          erroCapturado instanceof ErroDaApi
            ? erroCapturado.message
            : "Não foi possível enviar a imagem. Tente novamente em instantes.",
      });
    } finally {
      definirProgressoDaImagem((atual) => {
        const { [indice]: _, ...resto } = atual;
        return resto;
      });
    }
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
      definirPerguntas(comoEdicao(atualizada));
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

              <div className="desafio-de-desbloqueio__imagem">
                <label htmlFor={`imagem-${missao.id}-${indice}`}>
                  Imagem da pergunta {indice + 1} (opcional)
                </label>
                <p className="desafio-de-desbloqueio__limite">
                  Até {emMegabytes(TAMANHO_TETO_DA_IMAGEM_DA_PERGUNTA)}, em{" "}
                  {FORMATOS_DA_IMAGEM_DA_PERGUNTA_EM_PORTUGUES}.
                </p>
                <input
                  id={`imagem-${missao.id}-${indice}`}
                  type="file"
                  accept={FORMATOS_DA_IMAGEM_DA_PERGUNTA.join(",")}
                  onChange={(evento) => {
                    const escolhido = evento.target.files?.[0];
                    if (escolhido) anexarImagem(indice, escolhido);
                  }}
                />
                {progressoDaImagem[indice] && (
                  <p role="status">
                    Enviado{" "}
                    {Math.round(
                      (progressoDaImagem[indice].enviados / progressoDaImagem[indice].total) *
                        100,
                    )}
                    % de {emMegabytes(progressoDaImagem[indice].total)}
                  </p>
                )}
                {pergunta.imagem_referencia && (
                  <>
                    <p className="desafio-de-desbloqueio__com-imagem">
                      Esta pergunta tem imagem.
                    </p>
                    <Botao
                      variante="secundaria"
                      onClick={() => alterarPergunta(indice, { imagem_referencia: null })}
                    >
                      Remover imagem da pergunta {indice + 1}
                    </Botao>
                  </>
                )}
                {erroDaImagem[indice] && <Aviso tipo="erro">{erroDaImagem[indice]}</Aviso>}
              </div>

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
