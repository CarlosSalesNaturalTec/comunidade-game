import { ErroDaApi } from "comum/api";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import {
  confirmarEntregaNoEncontro,
  listarEntregasPendentesDoEncontro,
  type PendenciaDeEntrega,
} from "../api/entregasPendentes";

interface Props {
  tokenDeTrabalho: string;
  aulaId: string;
  aoVoltar: () => void;
}

function chaveDaPendencia(pendencia: PendenciaDeEntrega): string {
  return `${pendencia.recompensa_de_marco_id}-${pendencia.guerreiro_id}`;
}

// A fila do **encontro**: só quem tem presença registrada nesta aula e
// conquistou marco com recompensa que ainda não recebeu. Sem seletor de ponto
// de apoio — o recurso sai do ponto de apoio que a aula declara
// obrigatoriamente —, e sem valor em moedas ou em reais (`RF-09-75`,
// `RF-09-76`, `RF-01-71`, invariantes 12 e 16).
//
// Tudo vai sob o `tokenDeTrabalho`: quem confirma é o Mestre que abriu o
// aparelho, e é a persona dele que o núcleo grava como autora (`RF-07-13`,
// `RN-02-17`).
export function TelaDeEntregasDoEncontro({ tokenDeTrabalho, aulaId, aoVoltar }: Props) {
  const [pendencias, definirPendencias] = useState<PendenciaDeEntrega[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [confirmando, definirConfirmando] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    try {
      definirPendencias(await listarEntregasPendentesDoEncontro(aulaId, tokenDeTrabalho));
    } catch (erroCapturado) {
      definirPendencias([]);
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível carregar as entregas do encontro. Tente novamente em instantes.",
      );
    }
  }, [aulaId, tokenDeTrabalho]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  // Confirmada a entrega, a fila é **relida** do núcleo, nunca remendada
  // aqui: o mesmo par pode ter sido entregue na App 09 enquanto esta tela
  // estava aberta, e quem sabe disso é o núcleo (design — Risks).
  async function confirmar(pendencia: PendenciaDeEntrega) {
    const chave = chaveDaPendencia(pendencia);
    definirErro(null);
    definirConfirmando(chave);
    try {
      await confirmarEntregaNoEncontro(
        pendencia.recompensa_de_marco_id,
        { guerreiro_id: pendencia.guerreiro_id, aula_id: aulaId },
        tokenDeTrabalho,
      );
      await carregar();
    } catch (erroCapturado) {
      // A recusa do núcleo já vem em linguagem simples — falta de lastro no
      // ponto de apoio da aula, quantidade esgotada, presença ausente. A tela
      // a apresenta como ela vem, sem recalcular saldo por conta própria.
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível confirmar a entrega. Tente novamente em instantes.",
      );
    } finally {
      definirConfirmando(null);
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Entregas pendentes do encontro"
        subtitulo="Quem chegou hoje e já conquistou a recompensa. O item sai do ponto de apoio desta aula."
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {pendencias === null && (
        <EstadoDaLista>Carregando as entregas do encontro…</EstadoDaLista>
      )}
      {pendencias !== null && pendencias.length === 0 && (
        <EstadoDaLista>Nenhuma entrega pendente neste encontro.</EstadoDaLista>
      )}
      {pendencias !== null && pendencias.length > 0 && (
        <ul className="cg-entregas-do-encontro" aria-label="Entregas pendentes do encontro">
          {pendencias.map((pendencia) => {
            const chave = chaveDaPendencia(pendencia);
            return (
              <li key={chave} className="cg-entrega-do-encontro">
                <p>
                  <strong>{pendencia.guerreiro_nick}</strong> ({pendencia.guerreiro_avatar}) —{" "}
                  {pendencia.trilha_nome} — {pendencia.missao_titulo}
                </p>
                <p>
                  {pendencia.quantidade} {pendencia.tipo_de_recurso_unidade} de{" "}
                  {pendencia.tipo_de_recurso_nome}
                  {pendencia.quantidade_esgotada &&
                    " — quantidade declarada já esgotada nas entregas anteriores"}
                </p>
                <Botao
                  onClick={() => confirmar(pendencia)}
                  desabilitado={confirmando !== null}
                >
                  {confirmando === chave ? "Confirmando…" : "Confirmar entrega"}
                </Botao>
              </li>
            );
          })}
        </ul>
      )}
    </Moldura>
  );
}
