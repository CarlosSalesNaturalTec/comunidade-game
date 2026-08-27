import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { useState } from "react";
import {
  declararDesafioDeDesbloqueio,
  type MissaoDaTrilha,
  type TipoDeDesafioDeDesbloqueio,
} from "./api";

interface Props {
  missao: MissaoDaTrilha;
  onAtualizada: (missao: MissaoDaTrilha) => void;
}

const TOTAL_DE_ALTERNATIVAS = 4;

// O Mestre autor monta o desafio de desbloqueio — quiz ou prático — que
// abre a missão seguinte para o Guerreiro(a); declarar de novo substitui o
// anterior, e a missão sem desafio segue publicável (`RF-09-26`,
// `RF-09-117`).
export function DesafioDeDesbloqueio({ missao, onAtualizada }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [tipo, definirTipo] = useState<TipoDeDesafioDeDesbloqueio>(
    missao.tipo_do_desafio_de_desbloqueio ?? "quiz",
  );
  const [enunciado, definirEnunciado] = useState(
    missao.desafio_de_desbloqueio_enunciado ?? "",
  );
  const [alternativas, definirAlternativas] = useState<string[]>(
    missao.desafio_de_desbloqueio_alternativas ?? ["", "", "", ""],
  );
  const [alternativaCorreta, definirAlternativaCorreta] = useState(
    missao.desafio_de_desbloqueio_alternativa_correta ?? 1,
  );
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  function alterarAlternativa(indice: number, valor: string) {
    const novas = [...alternativas];
    novas[indice] = valor;
    definirAlternativas(novas);
  }

  async function declarar() {
    if (!sessao) return;
    definirErro(null);
    definirEnviando(true);
    try {
      const atualizada = await declararDesafioDeDesbloqueio(
        missao.id,
        {
          tipo,
          enunciado,
          alternativas: tipo === "quiz" ? alternativas : null,
          alternativa_correta: tipo === "quiz" ? alternativaCorreta : null,
        },
        sessao.token,
      );
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
      <h4>Desafio de desbloqueio</h4>
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

      <Campo rotulo="Enunciado" valor={enunciado} aoAlterar={definirEnunciado} />

      {tipo === "quiz" && (
        <fieldset>
          <legend>Alternativas</legend>
          {Array.from({ length: TOTAL_DE_ALTERNATIVAS }, (_, indice) => (
            // biome-ignore lint/suspicious/noArrayIndexKey: a lista tem tamanho fixo e não é reordenada
            <div key={indice} className="desafio-de-desbloqueio__alternativa">
              <input
                type="radio"
                name={`alternativa-correta-${missao.id}`}
                checked={alternativaCorreta === indice + 1}
                onChange={() => definirAlternativaCorreta(indice + 1)}
                aria-label={`Alternativa ${indice + 1} é a correta`}
              />
              <Campo
                rotulo={`Alternativa ${indice + 1}`}
                valor={alternativas[indice]}
                aoAlterar={(valor) => alterarAlternativa(indice, valor)}
              />
            </div>
          ))}
        </fieldset>
      )}

      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Botao onClick={declarar} desabilitado={enviando}>
        {enviando ? "Salvando…" : "Declarar desafio"}
      </Botao>
    </section>
  );
}
