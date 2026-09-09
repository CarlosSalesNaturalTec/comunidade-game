import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import {
  cadastrarTipoDeRecurso,
  type NaturezaDoRecurso,
  ROTULO_DA_NATUREZA_DO_RECURSO,
} from "../recursos/api";

interface Props {
  onSalvo: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const RECUSA_POR_PAPEL = "Só o Admin cadastra tipo de recurso do catálogo.";

function hoje(): string {
  return new Date().toISOString().slice(0, 10);
}

// O tipo e a primeira vigência do valor de referência num ato só, porque é
// assim que o núcleo os grava (`RF-02-107`, `RF-07-01`, `RF-07-02`). A
// vigência nasce em hoje, que é o caso corrente — cadastrar com data
// adiante é legítimo e o tipo só aparece na lista naquele dia
// (design — decisão 4, riscos).
export function FormularioDeTipoDeRecurso({ onSalvo, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDaNatureza = useId();
  const idDoComprovante = useId();
  const [nome, definirNome] = useState("");
  const [natureza, definirNatureza] = useState<NaturezaDoRecurso>("consumivel");
  const [unidade, definirUnidade] = useState("");
  const [valorEmMoedas, definirValorEmMoedas] = useState("");
  const [vigenciaInicio, definirVigenciaInicio] = useState(hoje);
  const [exigeComprovante, definirExigeComprovante] = useState(false);
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    // Campo obrigatório em falta é apontado no campo, sem chamar o núcleo e
    // sem gravar nada (`RF-02-107`).
    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome do tipo de recurso." });
      return;
    }
    if (!unidade.trim()) {
      definirErroDeCampo({ campo: "unidade", mensagem: "Informe a unidade." });
      return;
    }
    if (!valorEmMoedas.trim()) {
      definirErroDeCampo({
        campo: "valor_em_moedas",
        mensagem: "Informe o valor de referência em moedas.",
      });
      return;
    }
    if (!vigenciaInicio) {
      definirErroDeCampo({
        campo: "vigencia_inicio",
        mensagem: "Informe o início da vigência.",
      });
      return;
    }

    if (!sessao) return;

    definirEnviando(true);
    try {
      await cadastrarTipoDeRecurso(
        {
          nome,
          natureza,
          unidade,
          valor_em_moedas: valorEmMoedas,
          vigencia_inicio: vigenciaInicio,
          exige_comprovante: exigeComprovante,
        },
        sessao.token,
      );
      onSalvo();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "permissao_negada") {
        definirErroDeRecusa(RECUSA_POR_PAPEL);
        return;
      }
      // A recusa do núcleo — natureza fora das quatro, valor negativo ou
      // com mais de duas casas — volta com o campo que a originou e é
      // apresentada nele (`RN-07-04`).
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa(
        "Não foi possível cadastrar o tipo de recurso. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Novo tipo de recurso">
      <Campo
        rotulo="Nome"
        valor={nome}
        aoAlterar={definirNome}
        erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDaNatureza}>Natureza</label>
        <select
          id={idDaNatureza}
          value={natureza}
          onChange={(evento) => definirNatureza(evento.target.value as NaturezaDoRecurso)}
          aria-invalid={erroDeCampo?.campo === "natureza" || undefined}
        >
          {Object.entries(ROTULO_DA_NATUREZA_DO_RECURSO).map(([valor, rotulo]) => (
            <option key={valor} value={valor}>
              {rotulo}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "natureza" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <Campo
        rotulo="Unidade"
        valor={unidade}
        aoAlterar={definirUnidade}
        erro={erroDeCampo?.campo === "unidade" ? erroDeCampo.mensagem : null}
      />

      <Campo
        rotulo="Valor de referência em moedas"
        valor={valorEmMoedas}
        aoAlterar={definirValorEmMoedas}
        erro={erroDeCampo?.campo === "valor_em_moedas" ? erroDeCampo.mensagem : null}
      />

      <Campo
        rotulo="Início da vigência"
        tipo="date"
        valor={vigenciaInicio}
        aoAlterar={definirVigenciaInicio}
        erro={erroDeCampo?.campo === "vigencia_inicio" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDoComprovante}>
          <input
            id={idDoComprovante}
            type="checkbox"
            checked={exigeComprovante}
            onChange={(evento) => definirExigeComprovante(evento.target.checked)}
          />{" "}
          Este tipo exige comprovante
        </label>
        <p>Marque para que o aporte deste tipo sem comprovante seja recusado.</p>
      </div>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Cadastrar
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
