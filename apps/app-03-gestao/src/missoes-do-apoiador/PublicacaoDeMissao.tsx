import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import type { NecessidadeDeRecurso } from "../recursos/api";
import {
  type FamiliaDeSelo,
  type MissaoDoApoiador,
  type NivelDeNecessidade,
  publicarMissao,
} from "./api";

interface Props {
  necessidades: NecessidadeDeRecurso[];
  nomeDoTipoDeRecurso: (id: string) => string;
  onPublicada: (missao: MissaoDoApoiador) => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const NIVEIS: { valor: NivelDeNecessidade; rotulo: string }[] = [
  { valor: "existir", rotulo: "Existir" },
  { valor: "acontecer", rotulo: "Acontecer" },
  { valor: "reconhecer", rotulo: "Reconhecer" },
  { valor: "permanecer", rotulo: "Permanecer" },
];

const FAMILIAS: { valor: FamiliaDeSelo; rotulo: string }[] = [
  { valor: "frente", rotulo: "De frente" },
  { valor: "modalidade", rotulo: "De modalidade" },
  { valor: "ato", rotulo: "De ato" },
  { valor: "multiplicacao", rotulo: "De multiplicação" },
];

const MENSAGEM_DE_FALHA = "Não foi possível publicar a missão. Tente novamente em instantes.";

// A publicação da missão a partir de uma necessidade de recurso em aberto —
// só Admin, e a recusa por faltar necessidade por trás aparece em
// linguagem simples, sem erro cru (`RF-02-102`, `RF-02-103`, `RN-02-31`).
export function PublicacaoDeMissao({ necessidades, nomeDoTipoDeRecurso, onPublicada }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDaNecessidade = useId();
  const idDoNivel = useId();
  const idDaFamilia = useId();

  const [necessidadeChave, definirNecessidadeChave] = useState("");
  const [nivelDeNecessidade, definirNivelDeNecessidade] =
    useState<NivelDeNecessidade>("acontecer");
  const [titulo, definirTitulo] = useState("");
  const [oQueSePede, definirOQueSePede] = useState("");
  const [quantidade, definirQuantidade] = useState("");
  const [prazo, definirPrazo] = useState("");
  const [seloNome, definirSeloNome] = useState("");
  const [seloFamilia, definirSeloFamilia] = useState<FamiliaDeSelo>("frente");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  function aoSelecionarNecessidade(chave: string) {
    definirNecessidadeChave(chave);
    definirErroDeCampo(null);
  }

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    const necessidade = necessidades.find(
      (item) => `${item.aula_id}::${item.tipo_de_recurso_id}` === necessidadeChave,
    );
    if (!necessidade) {
      definirErroDeCampo({ campo: "aula_id", mensagem: "Escolha a necessidade de origem." });
      return;
    }
    if (!titulo.trim()) {
      definirErroDeCampo({ campo: "titulo", mensagem: "Informe o título." });
      return;
    }
    if (!oQueSePede.trim()) {
      definirErroDeCampo({ campo: "o_que_se_pede", mensagem: "Informe o que se pede." });
      return;
    }
    if (!quantidade.trim() || Number(quantidade) <= 0) {
      definirErroDeCampo({
        campo: "quantidade",
        mensagem: "Informe uma quantidade maior que zero.",
      });
      return;
    }
    if (!prazo) {
      definirErroDeCampo({ campo: "prazo", mensagem: "Informe o prazo." });
      return;
    }
    if (!seloNome.trim()) {
      definirErroDeCampo({ campo: "selo_nome", mensagem: "Informe o selo que rende." });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      const missao = await publicarMissao(
        {
          aulaId: necessidade.aula_id,
          tipoDeRecursoId: necessidade.tipo_de_recurso_id,
          nivelDeNecessidade,
          titulo,
          oQueSePede,
          quantidade,
          prazo,
          seloNome,
          seloFamilia,
        },
        sessao.token,
      );
      onPublicada(missao);
      definirTitulo("");
      definirOQueSePede("");
      definirQuantidade("");
      definirPrazo("");
      definirSeloNome("");
      definirNecessidadeChave("");
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa(MENSAGEM_DE_FALHA);
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Publicar missão">
      <div className="cg-campo">
        <label htmlFor={idDaNecessidade}>Necessidade de origem</label>
        <select
          id={idDaNecessidade}
          value={necessidadeChave}
          onChange={(evento) => aoSelecionarNecessidade(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "aula_id" || undefined}
        >
          <option value="">Escolha a necessidade</option>
          {necessidades.map((necessidade) => (
            <option
              key={`${necessidade.aula_id}::${necessidade.tipo_de_recurso_id}`}
              value={`${necessidade.aula_id}::${necessidade.tipo_de_recurso_id}`}
            >
              {nomeDoTipoDeRecurso(necessidade.tipo_de_recurso_id)} — falta{" "}
              {necessidade.quantidade_faltante}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "aula_id" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <div className="cg-campo">
        <label htmlFor={idDoNivel}>Nível de necessidade</label>
        <select
          id={idDoNivel}
          value={nivelDeNecessidade}
          onChange={(evento) =>
            definirNivelDeNecessidade(evento.target.value as NivelDeNecessidade)
          }
        >
          {NIVEIS.map((item) => (
            <option key={item.valor} value={item.valor}>
              {item.rotulo}
            </option>
          ))}
        </select>
      </div>

      <Campo
        rotulo="Título"
        valor={titulo}
        aoAlterar={definirTitulo}
        erro={erroDeCampo?.campo === "titulo" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor="o-que-se-pede">O que se pede</label>
        <textarea
          id="o-que-se-pede"
          value={oQueSePede}
          onChange={(evento) => definirOQueSePede(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "o_que_se_pede" || undefined}
        />
        {erroDeCampo?.campo === "o_que_se_pede" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <Campo
        rotulo="Valor da missão, em moedas"
        tipo="number"
        valor={quantidade}
        aoAlterar={definirQuantidade}
        erro={erroDeCampo?.campo === "quantidade" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Prazo"
        tipo="date"
        valor={prazo}
        aoAlterar={definirPrazo}
        erro={erroDeCampo?.campo === "prazo" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Selo que rende"
        valor={seloNome}
        aoAlterar={definirSeloNome}
        erro={erroDeCampo?.campo === "selo_nome" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDaFamilia}>Família do selo</label>
        <select
          id={idDaFamilia}
          value={seloFamilia}
          onChange={(evento) => definirSeloFamilia(evento.target.value as FamiliaDeSelo)}
        >
          {FAMILIAS.map((item) => (
            <option key={item.valor} value={item.valor}>
              {item.rotulo}
            </option>
          ))}
        </select>
      </div>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Publicar missão
      </Botao>
    </form>
  );
}
