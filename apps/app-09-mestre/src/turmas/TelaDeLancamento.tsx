import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo, CampoDeDataHora } from "comum/react";
import { type FormEvent, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import type { AtividadeDoMestre, AulaDaTurma, DesfechoDoResultado } from "./api";
import { lancarResultadosDaAtividade } from "./api";

interface Props {
  aula: AulaDaTurma;
  atividade: AtividadeDoMestre;
  aoVoltar: () => void;
}

interface LinhaDoParticipante {
  guerreiroId: string;
  producao: string;
  desfecho: DesfechoDoResultado;
  momentoDoFato: string;
}

const ROTULO_DO_DESFECHO: Record<DesfechoDoResultado, string> = {
  realizada: "Realizada",
  realizada_com_merito: "Realizada com mérito",
  merito_extra_por_auxilio: "Mérito extra por auxílio aos colegas",
};

function linhaVazia(): LinhaDoParticipante {
  return { guerreiroId: "", producao: "", desfecho: "realizada", momentoDoFato: "" };
}

// O lançamento da atividade que o Mestre propôs, com todos os participantes
// num só envio — a equipe inteira, preservando o desfecho de cada um
// (`RF-09-43`, `RF-09-44`, `RF-09-74`).
export function TelaDeLancamento({ aula, atividade, aoVoltar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [linhas, definirLinhas] = useState<LinhaDoParticipante[]>([linhaVazia()]);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [confirmado, definirConfirmado] = useState(false);

  function atualizarLinha(indice: number, mudanca: Partial<LinhaDoParticipante>) {
    definirLinhas((atual) =>
      atual.map((linha, i) => (i === indice ? { ...linha, ...mudanca } : linha)),
    );
  }

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErro(null);
    definirConfirmado(false);

    if (!sessao) return;
    definirEnviando(true);
    try {
      await lancarResultadosDaAtividade(
        atividade.id,
        aula.id,
        linhas.map((linha) => ({
          guerreiro_id: linha.guerreiroId,
          producao: linha.producao,
          desfecho: linha.desfecho,
          momento_do_fato: linha.momentoDoFato,
        })),
        sessao.token,
      );
      definirConfirmado(true);
      definirLinhas([linhaVazia()]);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      // A recusa chega em linguagem simples, sem código nem jargão (`RN-09-16`).
      if (erroCapturado instanceof ErroDaApi) {
        definirErro(erroCapturado.message);
        return;
      }
      definirErro("Não foi possível registrar o lançamento. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <main className="cg-moldura">
      <header className="cg-cabecalho">
        <div className="cg-cabecalho__texto">
          <h1>Lançar: {atividade.titulo}</h1>
        </div>
        <Botao variante="secundaria" onClick={aoVoltar}>
          Voltar
        </Botao>
      </header>

      <AvisoDeColeta dado="o resultado da atividade de cada participante" />
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {confirmado && <Aviso tipo="sucesso">Lançamento registrado.</Aviso>}

      <form onSubmit={aoSubmeter} aria-label="Lançamento da atividade">
        {linhas.map((linha, indice) => (
          // biome-ignore lint/suspicious/noArrayIndexKey: a lista é reordenada só por remoção no fim
          <fieldset key={indice} className="lancamento__participante">
            <legend>Participante {indice + 1}</legend>
            <Campo
              rotulo="Identificador do Guerreiro(a)"
              valor={linha.guerreiroId}
              aoAlterar={(valor) => atualizarLinha(indice, { guerreiroId: valor })}
            />
            <Campo
              rotulo="Produção"
              valor={linha.producao}
              aoAlterar={(valor) => atualizarLinha(indice, { producao: valor })}
            />
            <CampoDeDataHora
              rotulo="Momento do fato"
              valor={linha.momentoDoFato}
              aoAlterar={(valor) => atualizarLinha(indice, { momentoDoFato: valor })}
            />
            <div className="cg-campo">
              <label htmlFor={`desfecho-${indice}`}>Desfecho</label>
              <select
                id={`desfecho-${indice}`}
                value={linha.desfecho}
                onChange={(evento) =>
                  atualizarLinha(indice, {
                    desfecho: evento.target.value as DesfechoDoResultado,
                  })
                }
              >
                {Object.entries(ROTULO_DO_DESFECHO).map(([valor, rotulo]) => (
                  <option key={valor} value={valor}>
                    {rotulo}
                  </option>
                ))}
              </select>
            </div>
            {linhas.length > 1 && (
              <Botao
                variante="secundaria"
                onClick={() => definirLinhas((atual) => atual.filter((_, i) => i !== indice))}
              >
                Remover participante
              </Botao>
            )}
          </fieldset>
        ))}

        <Botao
          variante="secundaria"
          onClick={() => definirLinhas((atual) => [...atual, linhaVazia()])}
        >
          Adicionar participante
        </Botao>

        <Botao tipo="submit" desabilitado={enviando}>
          Lançar
        </Botao>
      </form>
    </main>
  );
}
