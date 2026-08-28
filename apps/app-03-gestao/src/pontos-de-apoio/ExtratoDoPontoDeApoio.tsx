import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, CampoDeDataHora, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useId, useState } from "react";
import { listarTiposDeRecurso, type TipoDeRecurso } from "../recursos/api";
import { AjusteDeLancamento } from "./AjusteDeLancamento";
import { type LancamentoDoExtrato, listarLancamentos, type PontoDeApoioDaLista } from "./api";

interface Props {
  pontoDeApoio: PontoDeApoioDaLista;
  onVoltar: () => void;
}

const MENSAGEM_DE_FALHA = "Não foi possível carregar o extrato. Tente novamente em instantes.";

// O extrato do livro-razão de um ponto de apoio, com o ajuste sobre cada
// lançamento — sem caminho de edição nem de remoção (`RF-02-40`,
// `RN-02-12`).
export function ExtratoDoPontoDeApoio({ pontoDeApoio, onVoltar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoTipo = useId();
  const [tipos, definirTipos] = useState<TipoDeRecurso[]>([]);
  const [tipoDeRecursoId, definirTipoDeRecursoId] = useState("");
  const [periodoInicio, definirPeriodoInicio] = useState("");
  const [periodoFim, definirPeriodoFim] = useState("");
  const [lancamentos, definirLancamentos] = useState<LancamentoDoExtrato[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    listarTiposDeRecurso(sessao.token)
      .then(definirTipos)
      .catch(() => definirTipos([]));
  }, [sessao]);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const pagina = await listarLancamentos(pontoDeApoio.id, sessao.token, {
        periodoInicio: periodoInicio || undefined,
        periodoFim: periodoFim || undefined,
        tipoDeRecursoId: tipoDeRecursoId || undefined,
      });
      definirLancamentos(pagina.itens);
      definirErro(null);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro(MENSAGEM_DE_FALHA);
    }
  }, [
    pontoDeApoio.id,
    sessao,
    periodoInicio,
    periodoFim,
    tipoDeRecursoId,
    tratarRecusaDeSessao,
  ]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  return (
    <section aria-label={`Extrato de ${pontoDeApoio.nome}`}>
      <h2>Extrato — {pontoDeApoio.nome}</h2>

      <div className="cg-campo">
        <label htmlFor={idDoTipo}>Tipo de recurso</label>
        <select
          id={idDoTipo}
          value={tipoDeRecursoId}
          onChange={(evento) => definirTipoDeRecursoId(evento.target.value)}
        >
          <option value="">Todos</option>
          {tipos.map((tipo) => (
            <option key={tipo.id} value={tipo.id}>
              {tipo.nome}
            </option>
          ))}
        </select>
      </div>

      <CampoDeDataHora
        rotulo="Período — de"
        valor={periodoInicio}
        aoAlterar={definirPeriodoInicio}
      />
      <CampoDeDataHora
        rotulo="Período — até"
        valor={periodoFim}
        aoAlterar={definirPeriodoFim}
      />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {lancamentos === null && !erro && <EstadoDaLista>Carregando o extrato…</EstadoDaLista>}

      {lancamentos !== null && lancamentos.length === 0 && (
        <EstadoDaLista>Nenhum lançamento registrado neste ponto de apoio.</EstadoDaLista>
      )}

      {lancamentos !== null && lancamentos.length > 0 && (
        <ul>
          {lancamentos.map((lancamento) => (
            <li key={lancamento.id}>
              <span>{lancamento.natureza}</span> — {lancamento.quantidade} (
              {lancamento.valor_em_moedas} moedas)
              {lancamento.lancamento_original_id && (
                <span> — ajusta {lancamento.lancamento_original_id}</span>
              )}
              {lancamento.motivo_do_ajuste && <span> — {lancamento.motivo_do_ajuste}</span>}
              <AjusteDeLancamento lancamento={lancamento} onAjustado={carregar} />
            </li>
          ))}
        </ul>
      )}

      <Botao variante="secundaria" onClick={onVoltar}>
        Voltar
      </Botao>
    </section>
  );
}
