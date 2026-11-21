import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Avatar } from "comum/avatar";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import type { TipoDeRecurso } from "../recursos/api";
import { listarTiposDeRecurso } from "../recursos/api";
import { listarEntregasPendentes, type PendenciaDeEntrega, registrarEntrega } from "./api";

// A fila do Mestre em Minhas turmas: quem desbloqueou marco com recompensa
// declarada na comunidade dele e ainda não recebeu — nunca por autoria da
// trilha. O ponto de apoio não se escolhe: o núcleo tira o recurso da aula
// imediatamente anterior da comunidade (`RF-09-75`, `RF-09-76`, `RN-09-18`).
export function FilaDeEntregasPendentes() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [pendencias, definirPendencias] = useState<PendenciaDeEntrega[] | null>(null);
  const [tiposDeRecurso, definirTiposDeRecurso] = useState<TipoDeRecurso[]>([]);
  const [erro, definirErro] = useState<string | null>(null);
  const [confirmando, definirConfirmando] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const [listaDePendencias, tipos] = await Promise.all([
        listarEntregasPendentes(sessao.token),
        listarTiposDeRecurso(sessao.token),
      ]);
      definirPendencias(listaDePendencias);
      definirTiposDeRecurso(tipos);
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

    definirErro(null);
    definirConfirmando(chave);
    try {
      await registrarEntrega(
        pendencia.recompensa_de_marco_id,
        { guerreiro_id: pendencia.guerreiro_id },
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
      // de lastro, comunidade sem aula anterior, recompensa já entregue ou
      // marco não alcançado (`RN-09-18`, `RF-09-76`).
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
                  <Avatar avatar={pendencia.guerreiro_avatar} tamanho={32} />{" "}
                  <strong>{pendencia.guerreiro_nick}</strong> — {pendencia.trilha_nome} —{" "}
                  {pendencia.missao_titulo}
                </p>
                <p>
                  {pendencia.quantidade}{" "}
                  {tipoPorId.get(pendencia.tipo_de_recurso_id)?.nome ?? "recurso"}
                </p>

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
