import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import type { PontoDeApoioDaLista } from "../pontos-de-apoio/api";
import { tombarItem } from "./api";

interface Props {
  pontosDeApoio: PontoDeApoioDaLista[];
  onTombado: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const RECUSA_POR_PAPEL = "Só o Admin tomba item patrimonial.";
const MENSAGEM_DE_FALHA = "Não foi possível tombar o exemplar. Tente novamente em instantes.";

// Oferecido só ao Admin. A recusa do núcleo ao número de tombo repetido no
// mesmo ponto de apoio é traduzida em linguagem simples, sem apagar o que
// foi digitado — os campos só se limpam quando `onTombado` fecha o
// formulário (`RF-02-52`, `RN-02-21`).
export function FormularioDeTombamento({ pontosDeApoio, onTombado, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoPontoDeApoio = useId();
  const [titulo, definirTitulo] = useState("");
  const [numeroDeTombo, definirNumeroDeTombo] = useState("");
  const [pontoDeApoioId, definirPontoDeApoioId] = useState(pontosDeApoio[0]?.id ?? "");
  const [estadoDeConservacao, definirEstadoDeConservacao] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!titulo.trim()) {
      definirErroDeCampo({ campo: "titulo", mensagem: "Informe o título." });
      return;
    }
    if (!numeroDeTombo.trim()) {
      definirErroDeCampo({
        campo: "numero_de_tombo",
        mensagem: "Informe o número de tombo.",
      });
      return;
    }
    if (!pontoDeApoioId) {
      definirErroDeCampo({
        campo: "ponto_de_apoio_id",
        mensagem: "Escolha o ponto de apoio.",
      });
      return;
    }
    if (!estadoDeConservacao.trim()) {
      definirErroDeCampo({
        campo: "estado_de_conservacao",
        mensagem: "Informe o estado de conservação.",
      });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      await tombarItem(
        {
          titulo,
          numero_de_tombo: numeroDeTombo,
          ponto_de_apoio_id: pontoDeApoioId,
          estado_de_conservacao: estadoDeConservacao,
        },
        sessao.token,
      );
      onTombado();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "permissao_negada") {
        definirErroDeRecusa(RECUSA_POR_PAPEL);
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
    <form onSubmit={aoSubmeter} aria-label="Tombar exemplar">
      <Campo
        rotulo="Título"
        valor={titulo}
        aoAlterar={definirTitulo}
        erro={erroDeCampo?.campo === "titulo" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Número de tombo"
        valor={numeroDeTombo}
        aoAlterar={definirNumeroDeTombo}
        erro={erroDeCampo?.campo === "numero_de_tombo" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDoPontoDeApoio}>Ponto de apoio</label>
        <select
          id={idDoPontoDeApoio}
          value={pontoDeApoioId}
          onChange={(evento) => definirPontoDeApoioId(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "ponto_de_apoio_id" || undefined}
        >
          <option value="">Selecione</option>
          {pontosDeApoio.map((ponto) => (
            <option key={ponto.id} value={ponto.id}>
              {ponto.nome}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "ponto_de_apoio_id" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <Campo
        rotulo="Estado de conservação"
        valor={estadoDeConservacao}
        aoAlterar={definirEstadoDeConservacao}
        erro={erroDeCampo?.campo === "estado_de_conservacao" ? erroDeCampo.mensagem : null}
      />

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Tombar
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
