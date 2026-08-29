import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type ChangeEvent, type FormEvent, useId, useState } from "react";
import { absorverNecessidade, type NecessidadeDeRecurso, type TipoDeRecurso } from "./api";

interface Props {
  necessidade: NecessidadeDeRecurso;
  tipo: TipoDeRecurso | null;
  nomeDoTipoDeRecurso: string;
  nomeDoPontoDeApoio: string;
  onConcluida: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const NATUREZAS_COM_DESEMBOLSO = new Set(["consumivel", "duravel", "financeiro"]);
const MENSAGEM_DE_FALHA =
  "Não foi possível registrar a absorção. Tente novamente em instantes.";

function hoje(): string {
  return new Date().toISOString().slice(0, 10);
}

// O ato de confirmação a partir da própria necessidade — tipo, ponto de
// apoio e aula herdados, sem formulário livre (`RF-09-57`, `RF-09-58`,
// `RN-09-13`, design — decisão 3). Nenhum campo de provedor, homologação ou
// destinação: a absorção não os escolhe.
export function AbsorcaoDaNecessidade({
  necessidade,
  tipo,
  nomeDoTipoDeRecurso,
  nomeDoPontoDeApoio,
  onConcluida,
  onCancelar,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoComprovante = useId();

  const [quantidade, definirQuantidade] = useState(necessidade.quantidade_faltante);
  const [valorDeOrigem, definirValorDeOrigem] = useState("");
  const [comprovante, definirComprovante] = useState<File | undefined>(undefined);
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  const exigeValorDeOrigem = tipo !== null && NATUREZAS_COM_DESEMBOLSO.has(tipo.natureza);
  const valorPorUnidade = tipo ? Number(tipo.valor_em_moedas) : null;
  const equivalenteEmMoedas =
    valorPorUnidade !== null && quantidade
      ? (Number(quantidade) * valorPorUnidade).toFixed(2)
      : null;

  function aoEscolherArquivo(evento: ChangeEvent<HTMLInputElement>) {
    definirComprovante(evento.target.files?.[0]);
  }

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!quantidade.trim() || Number(quantidade) <= 0) {
      definirErroDeCampo({
        campo: "quantidade",
        mensagem: "Informe uma quantidade maior que zero.",
      });
      return;
    }
    if (exigeValorDeOrigem && !valorDeOrigem.trim()) {
      definirErroDeCampo({
        campo: "valor_de_origem",
        mensagem: "Informe o valor de origem em reais.",
      });
      return;
    }
    if (tipo?.exige_comprovante && !comprovante) {
      definirErroDeCampo({
        campo: "comprovante",
        mensagem: "Este tipo de recurso exige o comprovante.",
      });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      await absorverNecessidade(
        {
          tipoDeRecursoId: necessidade.tipo_de_recurso_id,
          quantidade,
          pontoDeApoioId: necessidade.ponto_de_apoio_id,
          dataDoAporte: hoje(),
          aulaId: necessidade.aula_id,
          valorDeOrigem: exigeValorDeOrigem ? valorDeOrigem : undefined,
          comprovante,
        },
        sessao.token,
      );
      onConcluida();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      if (erro instanceof ErroDaApi) {
        definirErroDeRecusa(erro.message);
        return;
      }
      definirErroDeRecusa(MENSAGEM_DE_FALHA);
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form
      onSubmit={aoSubmeter}
      aria-label="Absorver necessidade"
      className="absorcao-da-necessidade"
    >
      <p>
        {nomeDoTipoDeRecurso} · {nomeDoPontoDeApoio}
      </p>
      <p>O aporte nasce em seu nome e marcado como ressarcível.</p>

      <Campo
        rotulo="Quantidade"
        valor={quantidade}
        aoAlterar={definirQuantidade}
        erro={erroDeCampo?.campo === "quantidade" ? erroDeCampo.mensagem : null}
      />

      {exigeValorDeOrigem && (
        <>
          <Campo
            rotulo="Valor de origem (reais)"
            valor={valorDeOrigem}
            aoAlterar={definirValorDeOrigem}
            erro={erroDeCampo?.campo === "valor_de_origem" ? erroDeCampo.mensagem : null}
          />
          {equivalenteEmMoedas !== null && (
            <p className="absorcao-da-necessidade__equivalente">
              Equivalente: {equivalenteEmMoedas} moedas
            </p>
          )}
        </>
      )}

      {!exigeValorDeOrigem && equivalenteEmMoedas !== null && (
        <p className="absorcao-da-necessidade__equivalente">{equivalenteEmMoedas} moedas</p>
      )}

      {tipo?.exige_comprovante && (
        <div className="cg-campo">
          <label htmlFor={idDoComprovante}>Comprovante</label>
          <input
            id={idDoComprovante}
            type="file"
            accept="application/pdf,image/jpeg,image/png"
            onChange={aoEscolherArquivo}
            aria-invalid={erroDeCampo?.campo === "comprovante" || undefined}
          />
          {erroDeCampo?.campo === "comprovante" && (
            <p role="alert" className="cg-campo__erro">
              {erroDeCampo.mensagem}
            </p>
          )}
        </div>
      )}

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Confirmar absorção
      </Botao>
      <Botao variante="secundaria" desabilitado={enviando} onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
