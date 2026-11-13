import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useEffect, useId, useState } from "react";
import {
  alterarTipoDeRecurso,
  listarPrecosDeReferencia,
  type NaturezaDoRecurso,
  type PrecoDeReferencia,
  ROTULO_DA_NATUREZA_DO_RECURSO,
  registrarPrecoDeReferencia,
  registrarValorDeReferencia,
  type TipoDeRecurso,
} from "../recursos/api";

interface Props {
  tipo: TipoDeRecurso;
  onSalvo: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const RECUSA_POR_PAPEL = "Só o Admin altera tipo de recurso do catálogo.";

function hoje(): string {
  return new Date().toISOString().slice(0, 10);
}

function precoVigente(precos: PrecoDeReferencia[], data: string): PrecoDeReferencia | null {
  return (
    precos.find(
      (preco) =>
        preco.vigencia_inicio <= data &&
        (preco.vigencia_fim === null || preco.vigencia_fim > data),
    ) ?? null
  );
}

// Componente próprio, e não o formulário de cadastro em modo de edição: o
// cadastro grava tipo e primeira vigência num ato só, e a edição não. Altera
// nome, unidade e exige comprovante; a natureza aparece só como leitura. As
// duas réguas mudam por **vigência nova**, opcional cada uma — a edição que
// só corrige o nome não abre vigência alguma (`RF-02-113`, `RF-07-51`,
// `RF-07-02`, `RF-07-43`, design — decisão 8).
export function EdicaoDeTipoDeRecurso({ tipo, onSalvo, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoComprovante = useId();
  const [nome, definirNome] = useState(tipo.nome);
  const [unidade, definirUnidade] = useState(tipo.unidade);
  const [exigeComprovante, definirExigeComprovante] = useState(tipo.exige_comprovante);
  const [novoValor, definirNovoValor] = useState("");
  const [inicioDoValor, definirInicioDoValor] = useState(hoje);
  const [novoPreco, definirNovoPreco] = useState("");
  const [inicioDoPreco, definirInicioDoPreco] = useState(hoje);
  const [preco, definirPreco] = useState<PrecoDeReferencia | null | undefined>(undefined);
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  useEffect(() => {
    if (!sessao) return;
    listarPrecosDeReferencia(tipo.id, sessao.token)
      .then((precos) => definirPreco(precoVigente(precos, hoje())))
      .catch(() => definirPreco(null));
  }, [sessao, tipo.id]);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome do tipo de recurso." });
      return;
    }
    if (!unidade.trim()) {
      definirErroDeCampo({ campo: "unidade", mensagem: "Informe a unidade." });
      return;
    }
    if (novoValor.trim() && !inicioDoValor) {
      definirErroDeCampo({ campo: "vigencia_do_valor", mensagem: "Informe o início." });
      return;
    }
    if (novoPreco.trim() && !inicioDoPreco) {
      definirErroDeCampo({ campo: "vigencia_do_preco", mensagem: "Informe o início." });
      return;
    }

    if (!sessao) return;

    // Cada escrita aponta o campo do formulário que a originou.
    let campoEmCurso = "";
    definirEnviando(true);
    try {
      const alteracao: { nome?: string; unidade?: string; exige_comprovante?: boolean } = {};
      if (nome !== tipo.nome) alteracao.nome = nome;
      if (unidade !== tipo.unidade) alteracao.unidade = unidade;
      if (exigeComprovante !== tipo.exige_comprovante) {
        alteracao.exige_comprovante = exigeComprovante;
      }
      if (Object.keys(alteracao).length > 0) {
        campoEmCurso = "";
        await alterarTipoDeRecurso(tipo.id, alteracao, sessao.token);
      }
      if (novoValor.trim()) {
        campoEmCurso = "valor_em_moedas";
        await registrarValorDeReferencia(
          tipo.id,
          { valor_em_moedas: novoValor, vigencia_inicio: inicioDoValor },
          sessao.token,
        );
      }
      if (novoPreco.trim()) {
        campoEmCurso = "preco_em_pontos_extras";
        await registrarPrecoDeReferencia(
          tipo.id,
          { preco_em_pontos_extras: Number(novoPreco), vigencia_inicio: inicioDoPreco },
          sessao.token,
        );
      }
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
      // A recusa do núcleo — nome ou unidade em branco, valor com mais de
      // duas casas, preço fracionário ou abaixo do piso — volta com o campo
      // e é apresentada nele.
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao") {
        const campo =
          erro.campo === "vigencia_inicio"
            ? campoEmCurso === "valor_em_moedas"
              ? "vigencia_do_valor"
              : "vigencia_do_preco"
            : (erro.campo ?? campoEmCurso);
        if (campo) {
          definirErroDeCampo({ campo, mensagem: erro.message });
          return;
        }
      }
      definirErroDeRecusa(
        "Não foi possível alterar o tipo de recurso. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  const erroEm = (campo: string) =>
    erroDeCampo?.campo === campo ? erroDeCampo.mensagem : null;
  const rotuloDaNatureza =
    ROTULO_DA_NATUREZA_DO_RECURSO[tipo.natureza as NaturezaDoRecurso] ?? tipo.natureza;

  return (
    <form onSubmit={aoSubmeter} aria-label="Editar tipo de recurso">
      <Campo rotulo="Nome" valor={nome} aoAlterar={definirNome} erro={erroEm("nome")} />

      <p>
        Natureza: <strong>{rotuloDaNatureza}</strong> — a natureza não se altera.
      </p>

      <Campo
        rotulo="Unidade"
        valor={unidade}
        aoAlterar={definirUnidade}
        erro={erroEm("unidade")}
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
        <p>Vale para o aporte registrado daqui em diante, nunca para o já gravado.</p>
      </div>

      <fieldset>
        <legend>Valor de referência em moedas</legend>
        <p>
          Vigente: {tipo.valor_em_moedas ?? "—"} moedas. Informe um valor só para abrir
          vigência nova: a atual se encerra no dia de início da nova, sem ser reescrita.
        </p>
        <Campo
          rotulo="Novo valor em moedas"
          valor={novoValor}
          aoAlterar={definirNovoValor}
          erro={erroEm("valor_em_moedas")}
        />
        <Campo
          rotulo="Início da vigência do valor"
          tipo="date"
          valor={inicioDoValor}
          aoAlterar={definirInicioDoValor}
          erro={erroEm("vigencia_do_valor")}
        />
      </fieldset>

      <fieldset>
        <legend>Preço de referência em pontos extras</legend>
        <p>
          Vigente:{" "}
          {preco === undefined
            ? "carregando…"
            : preco === null
              ? "nenhum"
              : `${preco.preco_em_pontos_extras} pontos extras`}
          . Informe um preço só para abrir vigência nova: a atual se encerra no dia de início
          da nova, sem ser reescrita.
        </p>
        <Campo
          rotulo="Novo preço em pontos extras"
          tipo="number"
          valor={novoPreco}
          aoAlterar={definirNovoPreco}
          erro={erroEm("preco_em_pontos_extras")}
        />
        <Campo
          rotulo="Início da vigência do preço"
          tipo="date"
          valor={inicioDoPreco}
          aoAlterar={definirInicioDoPreco}
          erro={erroEm("vigencia_do_preco")}
        />
      </fieldset>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Salvar alterações
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
