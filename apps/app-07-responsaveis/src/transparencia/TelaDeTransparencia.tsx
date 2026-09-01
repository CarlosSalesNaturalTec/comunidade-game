import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { abrirSolicitacao } from "../solicitacoes/api";
import type { GuerreiroVinculado } from "../vinculados/api";
import {
  type AcessoDoResponsavel,
  type ItemDoCatalogoDeDados,
  listarAcessosDoVinculado,
  listarDadosDoVinculado,
} from "./api";

interface Props {
  guerreiro: GuerreiroVinculado;
}

const FORMATADOR_DE_DATA_HORA = new Intl.DateTimeFormat("pt-BR", {
  dateStyle: "short",
  timeStyle: "short",
});

function formatarDataHora(momentoISO: string): string {
  return FORMATADOR_DE_DATA_HORA.format(new Date(momentoISO));
}

function LinhaDeAcesso({
  acesso,
  guerreiroId,
}: {
  acesso: AcessoDoResponsavel;
  guerreiroId: string;
}) {
  const { sessao } = useSessao();
  const [aberto, definirAberto] = useState(false);
  const [texto, definirTexto] = useState(
    `Sobre o acesso de ${acesso.autor_nome ?? "alguém da gestão"} em ` +
      `${formatarDataHora(acesso.momento)}: `,
  );
  const [confirmacao, definirConfirmacao] = useState<{ id: string; prazo: string } | null>(
    null,
  );
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function enviar() {
    if (!sessao || !texto.trim()) return;
    definirEnviando(true);
    definirErro(null);
    try {
      const resposta = await abrirSolicitacao(
        guerreiroId,
        "esclarecimento",
        texto,
        sessao.token,
      );
      definirConfirmacao({ id: resposta.id, prazo: resposta.prazo });
    } catch {
      definirErro("Não foi possível registrar o esclarecimento. Tente novamente.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <li>
      {formatarDataHora(acesso.momento)} — {acesso.autor_nome ?? "gestão"} (
      {acesso.papel_do_autor}){" — "}
      {acesso.entidade_afetada}
      {!aberto && !confirmacao && (
        <Botao variante="secundaria" onClick={() => definirAberto(true)}>
          Pedir esclarecimento
        </Botao>
      )}
      {aberto && !confirmacao && (
        <div className="cg-campo">
          <label htmlFor={`esclarecimento-${acesso.id}`}>O que você quer entender</label>
          <textarea
            id={`esclarecimento-${acesso.id}`}
            value={texto}
            onChange={(evento) => definirTexto(evento.target.value)}
          />
          <Botao onClick={enviar} desabilitado={enviando || !texto.trim()}>
            Enviar esclarecimento
          </Botao>
          {erro && <Aviso tipo="erro">{erro}</Aviso>}
        </div>
      )}
      {confirmacao && (
        <Aviso tipo="sucesso">
          Esclarecimento registrado — protocolo {confirmacao.id}, prazo de resposta em{" "}
          {formatarDataHora(confirmacao.prazo)}.
        </Aviso>
      )}
    </li>
  );
}

// A transparência do vinculado: o que o núcleo guarda, com finalidade e
// prazo (`RF-13-29`, `RN-13-20`); e o histórico de quem acessou, com o
// esclarecimento aberto direto da linha, sem sair da tela (`RF-13-30`,
// `RF-13-31`). Tela de leitura: nenhuma escrita, exclusão ou exportação —
// o pedido continua sendo a solicitação (PRD-13 §§10, 11).
export function TelaDeTransparencia({ guerreiro }: Props) {
  const { sessao } = useSessao();
  const [dados, definirDados] = useState<ItemDoCatalogoDeDados[] | null>(null);
  const [acessos, definirAcessos] = useState<AcessoDoResponsavel[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  const carregar = useCallback(() => {
    if (!sessao) return;
    definirErro(null);
    Promise.all([
      listarDadosDoVinculado(guerreiro.id, sessao.token),
      listarAcessosDoVinculado(guerreiro.id, sessao.token),
    ])
      .then(([listaDeDados, listaDeAcessos]) => {
        definirDados(listaDeDados);
        definirAcessos(listaDeAcessos);
      })
      .catch(() => definirErro("Não foi possível carregar a transparência. Tente novamente."));
  }, [guerreiro.id, sessao]);

  useEffect(() => {
    definirDados(null);
    definirAcessos(null);
    carregar();
  }, [carregar]);

  if (erro) {
    return <Aviso tipo="erro">{erro}</Aviso>;
  }

  if (dados === null || acessos === null) {
    return <EstadoDaLista>Carregando…</EstadoDaLista>;
  }

  return (
    <section aria-label={`Transparência de ${guerreiro.nick}`}>
      <section>
        <h2>O que a plataforma guarda</h2>
        <table>
          <thead>
            <tr>
              <th>Dado</th>
              <th>Finalidade</th>
              <th>Prazo</th>
              <th>Situação</th>
            </tr>
          </thead>
          <tbody>
            {dados.map((item) => (
              <tr key={item.dado} aria-label={item.dado}>
                <td>{item.dado}</td>
                <td>{item.finalidade}</td>
                <td>{item.prazo}</td>
                <td>
                  {item.restrito_a_gestao
                    ? "Restrito à gestão"
                    : item.guardado
                      ? "Guardado hoje"
                      : "Não guardado hoje"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h2>Histórico de acessos</h2>
        {acessos.length === 0 && (
          <EstadoDaLista>Nenhum acesso registrado ainda.</EstadoDaLista>
        )}
        {acessos.length > 0 && (
          <ul aria-label={`Acessos a ${guerreiro.nick}`}>
            {acessos.map((acesso) => (
              <LinhaDeAcesso key={acesso.id} acesso={acesso} guerreiroId={guerreiro.id} />
            ))}
          </ul>
        )}
      </section>
    </section>
  );
}
