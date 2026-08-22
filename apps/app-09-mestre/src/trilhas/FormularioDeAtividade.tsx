import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import { type AtividadeDaMissao, criarAtividade } from "./api";

interface Props {
  idDaMissao: string;
  onSalvo: (atividade: AtividadeDaMissao) => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
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

// A natureza é lista aberta — texto livre, sem seletor fechado (`RF-09-69`,
// design — decisões).
export function FormularioDeAtividade({ idDaMissao, onSalvo, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDaModalidade = useId();
  const idDoFormato = useId();
  const [titulo, definirTitulo] = useState("");
  const [descricao, definirDescricao] = useState("");
  const [modalidade, definirModalidade] = useState("");
  const [formato, definirFormato] = useState("");
  const [natureza, definirNatureza] = useState("");
  const [producaoEsperada, definirProducaoEsperada] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!titulo.trim()) {
      definirErroDeCampo({ campo: "titulo", mensagem: "Informe o título da atividade." });
      return;
    }
    if (!modalidade) {
      definirErroDeCampo({ campo: "modalidade", mensagem: "Escolha a modalidade." });
      return;
    }
    if (!formato) {
      definirErroDeCampo({ campo: "formato", mensagem: "Escolha o formato." });
      return;
    }
    if (!natureza.trim()) {
      definirErroDeCampo({ campo: "natureza", mensagem: "Informe a natureza da atividade." });
      return;
    }
    if (!producaoEsperada.trim()) {
      definirErroDeCampo({
        campo: "producao_esperada",
        mensagem: "Descreva o que o Guerreiro(a) vai produzir.",
      });
      return;
    }

    if (!sessao) return;
    definirEnviando(true);
    try {
      const atividade = await criarAtividade(
        idDaMissao,
        {
          titulo,
          descricao: descricao.trim() ? descricao : undefined,
          modalidade,
          formato,
          natureza,
          producao_esperada: producaoEsperada,
        },
        sessao.token,
      );
      onSalvo(atividade);
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
        "Não foi possível acrescentar a atividade. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Nova atividade">
      <Campo
        rotulo="Título"
        valor={titulo}
        aoAlterar={definirTitulo}
        erro={erroDeCampo?.campo === "titulo" ? erroDeCampo.mensagem : null}
      />
      <Campo rotulo="Descrição" valor={descricao} aoAlterar={definirDescricao} />

      <div className="cg-campo">
        <label htmlFor={idDaModalidade}>Modalidade</label>
        <select
          id={idDaModalidade}
          value={modalidade}
          onChange={(evento) => definirModalidade(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "modalidade" || undefined}
        >
          <option value="">Selecione</option>
          {Object.entries(ROTULO_DA_MODALIDADE).map(([valor, rotulo]) => (
            <option key={valor} value={valor}>
              {rotulo}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "modalidade" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <div className="cg-campo">
        <label htmlFor={idDoFormato}>Formato</label>
        <select
          id={idDoFormato}
          value={formato}
          onChange={(evento) => definirFormato(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "formato" || undefined}
        >
          <option value="">Selecione</option>
          {Object.entries(ROTULO_DO_FORMATO).map(([valor, rotulo]) => (
            <option key={valor} value={valor}>
              {rotulo}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "formato" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <Campo
        rotulo="Natureza"
        valor={natureza}
        aoAlterar={definirNatureza}
        erro={erroDeCampo?.campo === "natureza" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Produção esperada"
        valor={producaoEsperada}
        aoAlterar={definirProducaoEsperada}
        erro={erroDeCampo?.campo === "producao_esperada" ? erroDeCampo.mensagem : null}
      />

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Acrescentar atividade
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
