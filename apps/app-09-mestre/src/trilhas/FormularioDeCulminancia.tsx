import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import {
  type CulminanciaDaTrilha,
  declararCulminancia,
  type ModalidadeDaCulminancia,
} from "./api";

interface Props {
  idDaTrilha: string;
  culminancia: CulminanciaDaTrilha | null;
  onSalvo: (culminancia: CulminanciaDaTrilha) => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const ROTULO_DA_MODALIDADE: Record<ModalidadeDaCulminancia, string> = {
  individual: "Individual",
  em_equipe: "Em equipe",
};

// A culminância é a especificação da criação original esperada — uma por
// trilha; declarar de novo substitui a anterior, nunca cria uma segunda
// (`RF-09-29`, `RF-09-30`).
export function FormularioDeCulminancia({
  idDaTrilha,
  culminancia,
  onSalvo,
  onCancelar,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDaModalidade = useId();
  const [descricao, definirDescricao] = useState(culminancia?.descricao ?? "");
  const [modalidade, definirModalidade] = useState<ModalidadeDaCulminancia | "">(
    culminancia?.modalidade ?? "",
  );
  const [criterioDeValidacao, definirCriterioDeValidacao] = useState(
    culminancia?.criterio_de_validacao ?? "",
  );
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!descricao.trim()) {
      definirErroDeCampo({
        campo: "descricao",
        mensagem: "Descreva a criação original esperada.",
      });
      return;
    }
    if (!modalidade) {
      definirErroDeCampo({ campo: "modalidade", mensagem: "Escolha a modalidade." });
      return;
    }
    if (!criterioDeValidacao.trim()) {
      definirErroDeCampo({
        campo: "criterio_de_validacao",
        mensagem: "Informe o critério de validação.",
      });
      return;
    }

    if (!sessao) return;
    definirEnviando(true);
    try {
      const declarada = await declararCulminancia(
        idDaTrilha,
        { descricao, modalidade, criterio_de_validacao: criterioDeValidacao },
        sessao.token,
      );
      onSalvo(declarada);
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
        "Não foi possível gravar a culminância. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Culminância da trilha">
      <Campo
        rotulo="Descrição da criação esperada"
        valor={descricao}
        aoAlterar={definirDescricao}
        erro={erroDeCampo?.campo === "descricao" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDaModalidade}>Modalidade</label>
        <select
          id={idDaModalidade}
          value={modalidade}
          onChange={(evento) =>
            definirModalidade(evento.target.value as ModalidadeDaCulminancia)
          }
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

      <Campo
        rotulo="Critério de validação"
        valor={criterioDeValidacao}
        aoAlterar={definirCriterioDeValidacao}
        erro={erroDeCampo?.campo === "criterio_de_validacao" ? erroDeCampo.mensagem : null}
      />

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        {culminancia ? "Salvar culminância" : "Declarar culminância"}
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
