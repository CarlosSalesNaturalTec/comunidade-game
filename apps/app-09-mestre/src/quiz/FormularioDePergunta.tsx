import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import type { TrilhaDoMestre } from "../trilhas/api";
import { cadastrarPergunta, type PerguntaDeQuiz } from "./api";

interface Props {
  trilhas: TrilhaDoMestre[];
  onSalvo: (pergunta: PerguntaDeQuiz) => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const TOTAL_DE_ALTERNATIVAS = 4;

// Exatamente quatro alternativas e a correta declarada — a mesma exigência
// que `cadastrar_pergunta` já aplica, repetida aqui só para poupar a
// viagem ao núcleo com um envio incompleto (`RF-09-36`, `RF-09-37`,
// `RF-09-39`).
export function FormularioDePergunta({ trilhas, onSalvo, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDaTrilha = useId();
  const idDaMissao = useId();
  const idDaCorreta = useId();
  const [enunciado, definirEnunciado] = useState("");
  const [alternativas, definirAlternativas] = useState<string[]>(
    Array(TOTAL_DE_ALTERNATIVAS).fill(""),
  );
  const [alternativaCorreta, definirAlternativaCorreta] = useState("");
  const [trilhaId, definirTrilhaId] = useState("");
  const [missaoId, definirMissaoId] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  const trilhaSelecionada = trilhas.find((trilha) => trilha.id === trilhaId) ?? null;
  const missoesDaTrilha = trilhaSelecionada?.missoes ?? [];

  function alterarAlternativa(indice: number, valor: string) {
    definirAlternativas((atual) => atual.map((a, i) => (i === indice ? valor : a)));
  }

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!enunciado.trim()) {
      definirErroDeCampo({ campo: "enunciado", mensagem: "Informe o enunciado da pergunta." });
      return;
    }
    if (!trilhaId) {
      definirErroDeCampo({ campo: "trilha_id", mensagem: "Escolha a trilha." });
      return;
    }
    if (!missaoId) {
      definirErroDeCampo({ campo: "missao_id", mensagem: "Escolha a missão." });
      return;
    }
    if (alternativas.some((alternativa) => !alternativa.trim())) {
      definirErroDeCampo({
        campo: "alternativas",
        mensagem: "Preencha as quatro alternativas.",
      });
      return;
    }
    if (!alternativaCorreta) {
      definirErroDeCampo({
        campo: "alternativa_correta",
        mensagem: "Indique qual alternativa é a correta.",
      });
      return;
    }

    if (!sessao) return;
    definirEnviando(true);
    try {
      const pergunta = await cadastrarPergunta(
        {
          enunciado,
          alternativas,
          alternativa_correta: Number(alternativaCorreta),
          missao_id: missaoId,
        },
        sessao.token,
      );
      onSalvo(pergunta);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa(
        "Não foi possível cadastrar a pergunta. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Nova pergunta">
      <Campo
        rotulo="Enunciado"
        valor={enunciado}
        aoAlterar={definirEnunciado}
        erro={erroDeCampo?.campo === "enunciado" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDaTrilha}>Trilha</label>
        <select
          id={idDaTrilha}
          value={trilhaId}
          onChange={(evento) => {
            definirTrilhaId(evento.target.value);
            definirMissaoId("");
          }}
          aria-invalid={erroDeCampo?.campo === "trilha_id" || undefined}
        >
          <option value="">Selecione uma trilha</option>
          {trilhas.map((trilha) => (
            <option key={trilha.id} value={trilha.id}>
              {trilha.nome}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "trilha_id" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <div className="cg-campo">
        <label htmlFor={idDaMissao}>Missão</label>
        <select
          id={idDaMissao}
          value={missaoId}
          onChange={(evento) => definirMissaoId(evento.target.value)}
          disabled={!trilhaId}
          aria-invalid={erroDeCampo?.campo === "missao_id" || undefined}
        >
          <option value="">Selecione uma missão</option>
          {missoesDaTrilha.map((missao) => (
            <option key={missao.id} value={missao.id}>
              {missao.titulo}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "missao_id" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <fieldset>
        <legend>Alternativas</legend>
        {alternativas.map((alternativa, indice) => (
          <Campo
            // biome-ignore lint/suspicious/noArrayIndexKey: a posição é o identificador da alternativa
            key={indice}
            rotulo={`Alternativa ${indice + 1}`}
            valor={alternativa}
            aoAlterar={(valor) => alterarAlternativa(indice, valor)}
            erro={
              erroDeCampo?.campo === "alternativas" && indice === 0
                ? erroDeCampo.mensagem
                : null
            }
          />
        ))}
      </fieldset>

      <div className="cg-campo">
        <label htmlFor={idDaCorreta}>Alternativa correta</label>
        <select
          id={idDaCorreta}
          value={alternativaCorreta}
          onChange={(evento) => definirAlternativaCorreta(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "alternativa_correta" || undefined}
        >
          <option value="">Selecione a correta</option>
          {alternativas.map((_, indice) => (
            <option
              // biome-ignore lint/suspicious/noArrayIndexKey: a posição é o identificador da alternativa
              key={indice}
              value={indice + 1}
            >
              Alternativa {indice + 1}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "alternativa_correta" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Cadastrar pergunta
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
