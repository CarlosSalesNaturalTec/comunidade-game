import { useCallback, useEffect, useState } from "react";
import { ErroDaApi, ehRecusaDeSessao } from "../api/cliente";
import { Aviso } from "../react/Aviso";
import { Botao } from "../react/Botao";
import { EstadoDaLista } from "../react/EstadoDaLista";
import { EstrelaDePonto } from "../react/EstrelaDePonto";
import { Icone } from "../react/Icone";
import type {
  HistoricoDePontuacao as Historico,
  LancamentoDePontuacao,
  LerHistorico,
} from "./api";

// O histórico de pontuação com os saldos, o mesmo nas Apps 09, 03 e 05 —
// cada uma só muda a função de leitura (`RF-09-144`, `RF-02-116`,
// `RF-05-104`, design — decisão 7). Ponto regular e ponto extra têm cada um
// a sua estrela e o seu rótulo, e nunca se somam (documento 15 §9,
// invariante 24). A recusa do núcleo aparece como ele a declarou, nunca como
// lista vazia (invariante 25).

const ROTULO_DA_ORIGEM: Record<LancamentoDePontuacao["origem"], string> = {
  resultado: "Atividade realizada",
  merito_do_resultado: "Mérito na atividade",
  criacao_original: "Criação original validada",
  partida_de_quiz: "Partida de quiz",
  registro_de_coleta: "Registro de coleta",
  estorno_de_coleta: "Registro de coleta invalidado",
  desafio_pratico: "Desafio prático cumprido",
  ocorrencia_de_conduta: "Ocorrência de conduta",
  presenca: "Presença na aula",
  estorno_de_presenca: "Presença anulada",
  cuidado_do_bem: "Cuidado com o bem recebido",
  proposta_adotada: "Proposta adotada",
  troca: "Troca por recompensa",
  saldo_anterior: "Saldo anterior ao histórico",
};

const FORMATO_DA_DATA = new Intl.DateTimeFormat("pt-BR", {
  day: "2-digit",
  month: "2-digit",
  year: "numeric",
  hour: "2-digit",
  minute: "2-digit",
});

function comSinal(valor: number): string {
  return valor > 0 ? `+${valor}` : `${valor}`;
}

function descreverValor(lancamento: LancamentoDePontuacao): string {
  if (lancamento.conta === "regular") {
    return `${comSinal(lancamento.valor)} pontos`;
  }
  if (lancamento.origem === "saldo_anterior") {
    return `${lancamento.valor_no_acumulado ?? 0} acumulados, ${lancamento.valor} disponíveis`;
  }
  const acumulado = lancamento.valor_no_acumulado ?? 0;
  if (acumulado === lancamento.valor) {
    return `${comSinal(lancamento.valor)} pontos extras`;
  }
  if (acumulado === 0) {
    return `${comSinal(lancamento.valor)} no saldo disponível`;
  }
  return `${comSinal(acumulado)} no acumulado, ${comSinal(lancamento.valor)} no saldo disponível`;
}

interface Props {
  ler: LerHistorico;
  /** Recusa de sessão volta à entrada, como em toda tela da aplicação. */
  aoRecusarSessao?: () => void;
}

export function HistoricoDePontuacao({ ler, aoRecusarSessao }: Props) {
  const [historico, definirHistorico] = useState<Historico | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [carregando, definirCarregando] = useState(false);

  const tratarErro = useCallback(
    (erroCapturado: unknown) => {
      if (ehRecusaDeSessao(erroCapturado)) {
        aoRecusarSessao?.();
        return;
      }
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível carregar o histórico agora. Tente de novo em instantes.",
      );
    },
    [aoRecusarSessao],
  );

  useEffect(() => {
    let cancelado = false;
    definirErro(null);
    definirHistorico(null);
    ler(null)
      .then((pagina) => {
        if (!cancelado) definirHistorico(pagina);
      })
      .catch((erroCapturado) => {
        if (!cancelado) tratarErro(erroCapturado);
      });
    return () => {
      cancelado = true;
    };
  }, [ler, tratarErro]);

  async function carregarMais() {
    if (!historico?.proximo_cursor) return;
    definirCarregando(true);
    try {
      const pagina = await ler(historico.proximo_cursor);
      definirHistorico({
        ...pagina,
        itens: [...historico.itens, ...pagina.itens],
      });
    } catch (erroCapturado) {
      tratarErro(erroCapturado);
    } finally {
      definirCarregando(false);
    }
  }

  if (erro) return <Aviso tipo="erro">{erro}</Aviso>;
  if (historico === null) return <EstadoDaLista>Carregando o histórico…</EstadoDaLista>;

  const { regular, extra } = historico.saldos;

  return (
    <section className="cg-historico-de-pontuacao" aria-label="Histórico de pontuação">
      <h2>Saldos</h2>
      <div className="cg-historico-de-pontuacao__saldos">
        <div>
          <h3>
            <EstrelaDePonto tamanho={16} /> Pontos
          </h3>
          {regular.length === 0 ? (
            <p>Nenhum ponto ainda.</p>
          ) : (
            <ul>
              {regular.map((saldo) => (
                <li key={saldo.trilha_id ?? saldo.poder_id ?? saldo.nome}>
                  {saldo.nome}: {saldo.total} pontos
                </li>
              ))}
            </ul>
          )}
        </div>
        <div>
          <h3>
            <Icone glifo="ponto-extra" tamanho={16} /> Pontos extras
          </h3>
          <ul>
            <li>Acumulado: {extra.acumulado}</li>
            <li>Saldo disponível: {extra.saldo_disponivel}</li>
          </ul>
        </div>
      </div>

      <h2>Como chegou aqui</h2>
      {historico.itens.length === 0 ? (
        <EstadoDaLista>Ainda não há lançamento de pontuação.</EstadoDaLista>
      ) : (
        <ol className="cg-historico-de-pontuacao__lista">
          {historico.itens.map((lancamento) => (
            <li key={lancamento.id} className="cg-historico-de-pontuacao__item">
              <span className="cg-historico-de-pontuacao__data">
                {FORMATO_DA_DATA.format(new Date(lancamento.registrado_em))}
              </span>{" "}
              <strong>{ROTULO_DA_ORIGEM[lancamento.origem]}</strong>
              {lancamento.detalhe && <> — {lancamento.detalhe}</>}
              {lancamento.nome_da_trilha_ou_poder && (
                <> ({lancamento.nome_da_trilha_ou_poder})</>
              )}
              <span className="cg-historico-de-pontuacao__valor">
                {" "}
                {lancamento.conta === "regular" ? (
                  <EstrelaDePonto tamanho={16} />
                ) : (
                  <Icone glifo="ponto-extra" tamanho={16} />
                )}{" "}
                {descreverValor(lancamento)}
              </span>
              {lancamento.motivo && (
                <p className="cg-historico-de-pontuacao__motivo">
                  Motivo: {lancamento.motivo}
                </p>
              )}
            </li>
          ))}
        </ol>
      )}
      {historico.proximo_cursor && (
        <Botao variante="secundaria" onClick={carregarMais} desabilitado={carregando}>
          {carregando ? "Carregando…" : "Carregar mais"}
        </Botao>
      )}
    </section>
  );
}
