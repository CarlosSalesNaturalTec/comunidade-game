import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import type { GuerreiroVinculado } from "../vinculados/api";
import {
  type EvolucaoDoGuerreiro,
  listarOcorrencias,
  type OcorrenciaDaEvolucao,
  obterEvolucao,
} from "./api";

interface Props {
  guerreiro: GuerreiroVinculado;
}

const FORMATADOR_DE_DATA = new Intl.DateTimeFormat("pt-BR", { dateStyle: "short" });

function formatarData(momentoISO: string): string {
  return FORMATADOR_DE_DATA.format(new Date(momentoISO));
}

// O painel do vinculado: presença, atividades, pontos, poderes, badges,
// nível como percurso e criações validadas (`RF-13-07`, `RF-13-08`,
// `RF-13-10`), mais as ocorrências de conduta, buscadas à parte
// (`RF-13-09`). Nem esta tela nem o núcleo que ela chama chegam perto de
// consulta ao assistente, transcrição de apoio escolar ou dado de outra
// criança (`RF-13-11`, `RF-13-12`, `RN-13-20`).
export function TelaDeEvolucao({ guerreiro }: Props) {
  const { sessao } = useSessao();
  const [evolucao, definirEvolucao] = useState<EvolucaoDoGuerreiro | null>(null);
  const [ocorrencias, definirOcorrencias] = useState<OcorrenciaDaEvolucao[] | null>(null);
  const [vinculoEncerrado, definirVinculoEncerrado] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    definirEvolucao(null);
    definirOcorrencias(null);
    definirVinculoEncerrado(false);
    definirErro(null);

    Promise.all([
      obterEvolucao(guerreiro.id, sessao.token),
      listarOcorrencias(guerreiro.id, sessao.token),
    ])
      .then(([evolucaoRecebida, ocorrenciasRecebidas]) => {
        definirEvolucao(evolucaoRecebida);
        definirOcorrencias(ocorrenciasRecebidas);
      })
      .catch((erroRecebido) => {
        // O vínculo pode ter terminado entre a lista e o painel — a tela diz
        // isso em texto simples, nunca com o erro cru do núcleo (design —
        // riscos, `RN-13-04`).
        if (erroRecebido instanceof ErroDaApi && erroRecebido.status === 403) {
          definirVinculoEncerrado(true);
          return;
        }
        definirErro("Não foi possível carregar a evolução. Tente novamente.");
      });
  }, [guerreiro.id, sessao]);

  if (vinculoEncerrado) {
    return (
      <Aviso tipo="atencao">
        O vínculo com {guerreiro.nick} não está mais vigente. Procure a gestão no encontro.
      </Aviso>
    );
  }

  if (erro) {
    return <Aviso tipo="erro">{erro}</Aviso>;
  }

  if (evolucao === null || ocorrencias === null) {
    return <EstadoDaLista>Carregando…</EstadoDaLista>;
  }

  return (
    <section aria-label={`Evolução de ${guerreiro.nick}`}>
      <section>
        <h2>Trilhas</h2>
        {evolucao.trilhas.length === 0 && (
          <EstadoDaLista>Nenhuma trilha em andamento ainda.</EstadoDaLista>
        )}
        {evolucao.trilhas.map((trilha) => (
          <article key={trilha.trilha_id} className="cg-cartao-de-trilha">
            <h3>{trilha.trilha_nome}</h3>
            <p>Nível: {trilha.nivel_atual ?? "ainda sem nível"}</p>
            <p>
              Percurso: {trilha.obrigatorias_desbloqueadas} de {trilha.obrigatorias_totais}{" "}
              missões obrigatórias
            </p>
            {trilha.badges.length > 0 && <p>Badges: {trilha.badges.join(", ")}</p>}
          </article>
        ))}
      </section>

      <section>
        <h2>Presença</h2>
        {evolucao.presencas.length === 0 && (
          <EstadoDaLista>Nenhuma presença registrada ainda.</EstadoDaLista>
        )}
        {evolucao.presencas.length > 0 && (
          <ul>
            {evolucao.presencas.map((presenca) => (
              <li key={`${presenca.aula_id}-${presenca.momento_do_fato}`}>
                {formatarData(presenca.momento_do_fato)}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section>
        <h2>Atividades realizadas</h2>
        {evolucao.atividades.length === 0 && (
          <EstadoDaLista>Nenhuma atividade realizada ainda.</EstadoDaLista>
        )}
        {evolucao.atividades.length > 0 && (
          <ul>
            {evolucao.atividades.map((atividade) => (
              <li key={atividade.atividade_id}>
                {atividade.atividade_titulo} — {formatarData(atividade.momento_do_fato)}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section>
        <h2>Poderes</h2>
        {evolucao.pontos_por_poder.length === 0 && (
          <EstadoDaLista>Nenhum ponto de poder ainda.</EstadoDaLista>
        )}
        {evolucao.pontos_por_poder.length > 0 && (
          <ul>
            {evolucao.pontos_por_poder.map((item) => (
              <li key={item.poder_id}>
                {item.poder_nome}: {item.total} pontos
              </li>
            ))}
          </ul>
        )}
      </section>

      <section>
        <h2>Criações validadas</h2>
        {evolucao.criacoes_validadas.length === 0 && (
          <EstadoDaLista>Nenhuma criação validada ainda.</EstadoDaLista>
        )}
        {evolucao.criacoes_validadas.length > 0 && (
          <ul>
            {evolucao.criacoes_validadas.map((criacao) => (
              <li key={`${criacao.trilha_id}-${criacao.validado_em}`}>
                {criacao.trilha_titulo} — {formatarData(criacao.validado_em)}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section>
        <h2>Ocorrências de conduta</h2>
        {ocorrencias.length === 0 && (
          <EstadoDaLista>Nenhuma ocorrência de conduta registrada.</EstadoDaLista>
        )}
        {ocorrencias.length > 0 && (
          <ul>
            {/* O motivo apagado pelo expurgo do ciclo não recebe texto
             * substituto — só a data aparece (`RN-13-21`, design — riscos). */}
            {ocorrencias.map((ocorrencia) => (
              <li key={ocorrencia.id}>
                {formatarData(ocorrencia.momento_do_fato)}
                {ocorrencia.motivo && ` — ${ocorrencia.motivo}`}
              </li>
            ))}
          </ul>
        )}
      </section>
    </section>
  );
}
