import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import type { PontoDeApoioDaLista, TipoDeRecurso } from "../recursos/api";
import { listarMeusPontosDeApoio, listarTiposDeRecurso } from "../recursos/api";
import { listarEntregasPendentes, type PendenciaDeEntrega, registrarEntrega } from "./api";

// A fila do Mestre em Minhas turmas: quem desbloqueou marco com recompensa
// declarada na comunidade dele e ainda não recebeu — nunca por autoria da
// trilha (`RF-09-75`, `RF-09-76`, `RN-09-18`).
export function FilaDeEntregasPendentes() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [pendencias, definirPendencias] = useState<PendenciaDeEntrega[] | null>(null);
  const [tiposDeRecurso, definirTiposDeRecurso] = useState<TipoDeRecurso[]>([]);
  const [pontosDeApoio, definirPontosDeApoio] = useState<PontoDeApoioDaLista[]>([]);
  const [pontoEscolhidoPorPendencia, definirPontoEscolhidoPorPendencia] = useState<
    Record<string, string>
  >({});
  const [erro, definirErro] = useState<string | null>(null);
  const [confirmando, definirConfirmando] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const [listaDePendencias, tipos, pontos] = await Promise.all([
        listarEntregasPendentes(sessao.token),
        listarTiposDeRecurso(sessao.token),
        listarMeusPontosDeApoio(sessao.token),
      ]);
      definirPendencias(listaDePendencias);
      definirTiposDeRecurso(tipos);
      definirPontosDeApoio(pontos);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro(
        "Não foi possível carregar as entregas pendentes. Tente novamente em instantes.",
      );
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const tipoPorId = new Map(tiposDeRecurso.map((tipo) => [tipo.id, tipo]));

  function chaveDaPendencia(pendencia: PendenciaDeEntrega): string {
    return `${pendencia.recompensa_de_marco_id}-${pendencia.guerreiro_id}`;
  }

  async function confirmar(pendencia: PendenciaDeEntrega) {
    if (!sessao) return;
    const chave = chaveDaPendencia(pendencia);
    const pontoDeApoioId = pontoEscolhidoPorPendencia[chave];
    if (!pontoDeApoioId) {
      definirErro("Escolha o ponto de apoio de onde a recompensa vai sair.");
      return;
    }

    definirErro(null);
    definirConfirmando(chave);
    try {
      await registrarEntrega(
        pendencia.recompensa_de_marco_id,
        { guerreiro_id: pendencia.guerreiro_id, ponto_de_apoio_id: pontoDeApoioId },
        sessao.token,
      );
      definirPendencias(
        (atual) => atual?.filter((item) => chaveDaPendencia(item) !== chave) ?? atual,
      );
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      // A entrega recusada pelo núcleo já vem em linguagem simples — falta
      // de lastro, quantidade esgotada ou marco não alcançado (`RN-09-18`).
      if (erroCapturado instanceof ErroDaApi) {
        definirErro(erroCapturado.message);
        return;
      }
      definirErro("Não foi possível confirmar a entrega. Tente novamente em instantes.");
    } finally {
      definirConfirmando(null);
    }
  }

  return (
    <section aria-label="Entregas pendentes">
      <h2>Entregas pendentes</h2>

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {pendencias === null && <EstadoDaLista>Carregando entregas pendentes…</EstadoDaLista>}
      {pendencias !== null && pendencias.length === 0 && (
        <EstadoDaLista>Nenhuma entrega pendente na sua comunidade.</EstadoDaLista>
      )}
      {pendencias !== null && pendencias.length > 0 && (
        <ul className="fila-de-entregas-pendentes" aria-label="Entregas pendentes">
          {pendencias.map((pendencia) => {
            const chave = chaveDaPendencia(pendencia);
            return (
              <li key={chave} className="fila-de-entregas-pendentes__item">
                <p>
                  <strong>{pendencia.guerreiro_nick}</strong> ({pendencia.guerreiro_avatar}) —{" "}
                  {pendencia.trilha_nome} — {pendencia.missao_titulo}
                </p>
                <p>
                  {pendencia.quantidade}{" "}
                  {tipoPorId.get(pendencia.tipo_de_recurso_id)?.nome ?? "recurso"}
                  {pendencia.quantidade_esgotada &&
                    " — quantidade declarada já esgotada nas entregas anteriores"}
                </p>

                <div className="cg-campo">
                  <label htmlFor={`ponto-de-apoio-${chave}`}>Ponto de apoio</label>
                  <select
                    id={`ponto-de-apoio-${chave}`}
                    value={pontoEscolhidoPorPendencia[chave] ?? ""}
                    onChange={(evento) =>
                      definirPontoEscolhidoPorPendencia((atual) => ({
                        ...atual,
                        [chave]: evento.target.value,
                      }))
                    }
                  >
                    <option value="">Selecione</option>
                    {pontosDeApoio.map((ponto) => (
                      <option key={ponto.id} value={ponto.id}>
                        {ponto.nome}
                      </option>
                    ))}
                  </select>
                </div>

                <Botao
                  onClick={() => confirmar(pendencia)}
                  desabilitado={confirmando === chave}
                >
                  Confirmar entrega
                </Botao>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
