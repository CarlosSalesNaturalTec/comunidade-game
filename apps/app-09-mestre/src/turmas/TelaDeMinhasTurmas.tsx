import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { URL_DA_APP_03 } from "../api/configuracao";
import { FilaDeEntregasPendentes } from "../recompensas/FilaDeEntregasPendentes";
import { type AtividadeDoMestre, type AulaDaTurma, listarMinhasTurmas } from "./api";
import { TelaDaAula } from "./TelaDaAula";

const ROTULO_DA_SITUACAO: Record<string, string> = {
  prevista: "Prevista",
  pendente_de_lastro: "Pendente de lastro",
  confirmada: "Confirmada",
  realizada: "Realizada",
  // A pendente que chegou ao fim do horário (`RF-07-55`).
  realizada_sem_lastro: "Realizada sem lastro",
  cancelada: "Cancelada",
};

function formatarPeriodo(inicioEm: string, fimEm: string): string {
  const formatador = new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  });
  return `${formatador.format(new Date(inicioEm))} – ${formatador.format(new Date(fimEm))}`;
}

// Só a aula cuja janela contém o instante atual oferece o caminho para o
// painel do dia — aula futura, já realizada ou cancelada não tem encontro a
// acompanhar (`RF-09-50`, decisão do fundador, 2026-08-25).
function aulaEmAndamento(aula: AulaDaTurma): boolean {
  const agora = Date.now();
  return (
    aula.situacao !== "cancelada" &&
    agora >= new Date(aula.inicio_em).getTime() &&
    agora <= new Date(aula.fim_em).getTime()
  );
}

// A área Minhas turmas: as aulas das comunidades do Mestre e as atividades
// on-line de que ele é autor. As presenciais não têm seção própria: aparecem
// dentro da aula, no lançamento do resultado. Nenhum Guerreiro(a) aparece por
// imagem real (`RF-09-42`, `RF-09-73`, `RN-09-08`, `RN-09-18`).
export function TelaDeMinhasTurmas() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [aulas, definirAulas] = useState<AulaDaTurma[] | null>(null);
  const [atividadesPresenciais, definirAtividadesPresenciais] = useState<AtividadeDoMestre[]>(
    [],
  );
  const [atividadesOnLine, definirAtividadesOnLine] = useState<AtividadeDoMestre[]>([]);
  const [erro, definirErro] = useState<string | null>(null);
  const [aulaAberta, definirAulaAberta] = useState<AulaDaTurma | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const turmas = await listarMinhasTurmas(sessao.token);
      // A aula cancelada já não vem do núcleo (`RF-09-42`, decisão do
      // fundador, 2026-11-20).
      definirAulas(turmas.itens);
      definirAtividadesPresenciais(turmas.atividades_presenciais);
      definirAtividadesOnLine(turmas.atividades_on_line);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar as suas turmas. Tente novamente em instantes.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  if (aulaAberta) {
    return (
      <TelaDaAula
        aula={aulaAberta}
        atividadesPresenciais={atividadesPresenciais}
        aoVoltar={() => definirAulaAberta(null)}
      />
    );
  }

  return (
    <Moldura>
      <Cabecalho titulo="Minhas turmas" />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      <section aria-label="Aulas">
        <h2>Aulas</h2>
        {aulas === null && <EstadoDaLista>Carregando as suas turmas…</EstadoDaLista>}
        {aulas !== null && aulas.length === 0 && (
          <EstadoDaLista>Nenhuma aula agendada nas suas comunidades.</EstadoDaLista>
        )}
        {aulas !== null && aulas.length > 0 && (
          <ul className="lista-de-turmas" aria-label="Minhas aulas">
            {aulas.map((aula) => (
              <li key={aula.id} className="lista-de-turmas__item">
                <div className="lista-de-turmas__linha">
                  <span>{formatarPeriodo(aula.inicio_em, aula.fim_em)}</span>
                  <span>{ROTULO_DA_SITUACAO[aula.situacao] ?? aula.situacao}</span>
                </div>
                <Botao variante="secundaria" onClick={() => definirAulaAberta(aula)}>
                  Presença e ocorrência
                </Botao>
                {aulaEmAndamento(aula) && URL_DA_APP_03 && (
                  <a
                    className="cg-botao cg-botao--secundaria"
                    href={`${URL_DA_APP_03}/?area=painel-do-dia`}
                  >
                    Painel do dia
                  </a>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section aria-label="Atividades on-line">
        <h2>Atividades on-line</h2>
        {atividadesOnLine.length === 0 && (
          <EstadoDaLista>Nenhuma atividade on-line sua.</EstadoDaLista>
        )}
        {atividadesOnLine.length > 0 && (
          <ul className="lista-de-turmas" aria-label="Atividades on-line">
            {atividadesOnLine.map((atividade) => (
              <li key={atividade.id} className="lista-de-turmas__item">
                <span>{atividade.titulo}</span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <FilaDeEntregasPendentes />
    </Moldura>
  );
}
