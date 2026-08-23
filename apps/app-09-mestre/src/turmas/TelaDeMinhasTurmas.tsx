import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { type AtividadeDoMestre, type AulaDaTurma, listarMinhasTurmas } from "./api";
import { TelaDaAula } from "./TelaDaAula";
import { TelaDeLancamento } from "./TelaDeLancamento";

const ROTULO_DA_SITUACAO: Record<string, string> = {
  prevista: "Prevista",
  pendente_de_lastro: "Pendente de lastro",
  confirmada: "Confirmada",
  realizada: "Realizada",
  cancelada: "Cancelada",
};

function formatarPeriodo(inicioEm: string, fimEm: string): string {
  const formatador = new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  });
  return `${formatador.format(new Date(inicioEm))} – ${formatador.format(new Date(fimEm))}`;
}

interface SelecaoDeLancamento {
  aula: AulaDaTurma;
  atividade: AtividadeDoMestre;
}

// A área Minhas turmas: as aulas das comunidades do Mestre e as atividades
// de que ele é autor, separadas pelo formato — presencial do encontro e
// on-line entre encontros. Nenhum Guerreiro(a) aparece por imagem real
// (`RF-09-42`, `RF-09-73`, `RN-09-08`, `RN-09-18`).
export function TelaDeMinhasTurmas() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const [aulas, definirAulas] = useState<AulaDaTurma[] | null>(null);
  const [atividadesPresenciais, definirAtividadesPresenciais] = useState<AtividadeDoMestre[]>(
    [],
  );
  const [atividadesOnLine, definirAtividadesOnLine] = useState<AtividadeDoMestre[]>([]);
  const [erro, definirErro] = useState<string | null>(null);
  const [aulaAberta, definirAulaAberta] = useState<AulaDaTurma | null>(null);
  const [lancamentoAberto, definirLancamentoAberto] = useState<SelecaoDeLancamento | null>(
    null,
  );

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const turmas = await listarMinhasTurmas(sessao.token);
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

  if (lancamentoAberto) {
    return (
      <TelaDeLancamento
        aula={lancamentoAberto.aula}
        atividade={lancamentoAberto.atividade}
        aoVoltar={() => definirLancamentoAberto(null)}
      />
    );
  }

  if (aulaAberta) {
    return (
      <TelaDaAula
        aula={aulaAberta}
        atividadesPresenciais={atividadesPresenciais}
        aoVoltar={() => definirAulaAberta(null)}
        aoAbrirLancamento={(atividade) =>
          definirLancamentoAberto({ aula: aulaAberta, atividade })
        }
      />
    );
  }

  return (
    <Moldura>
      <Cabecalho titulo="Minhas turmas" acao={{ rotulo: "Sair", aoAcionar: sair }} />

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
              </li>
            ))}
          </ul>
        )}
      </section>

      <section aria-label="Atividades presenciais">
        <h2>Atividades presenciais</h2>
        <p>Abra uma aula acima para lançar o resultado ou a ocorrência de uma delas.</p>
        {atividadesPresenciais.length === 0 && (
          <EstadoDaLista>Nenhuma atividade presencial sua.</EstadoDaLista>
        )}
        {atividadesPresenciais.length > 0 && (
          <ul className="lista-de-turmas" aria-label="Atividades presenciais">
            {atividadesPresenciais.map((atividade) => (
              <li key={atividade.id} className="lista-de-turmas__item">
                <span>{atividade.titulo}</span>
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
    </Moldura>
  );
}
