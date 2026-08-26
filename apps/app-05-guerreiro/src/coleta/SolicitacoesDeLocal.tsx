import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import {
  listarMinhasSolicitacoes,
  type SolicitacaoDeLocal,
  solicitarLocal,
} from "../api/coleta";

const ROTULO_DA_SITUACAO: Record<SolicitacaoDeLocal["situacao"], string> = {
  recebida: "Recebida — aguardando resposta",
  aprovada: "Aprovada",
  recusada: "Recusada",
};

export interface ContextoDeNovoPedido {
  desafioId: string;
  comunidadeId: string;
  nivel: string;
}

interface Props {
  contexto: ContextoDeNovoPedido | null;
}

// Solicitação do local que falta e acompanhamento da situação até o
// desfecho — o pedido nunca cria local sozinho (`RF-05-32`, PRD-05 §5.4).
export function SolicitacoesDeLocal({ contexto }: Props) {
  const { sessao } = useSessao();
  const [solicitacoes, definirSolicitacoes] = useState<SolicitacaoDeLocal[] | null>(null);
  const [rotulo, definirRotulo] = useState("");
  const [justificativa, definirJustificativa] = useState("");
  const [enviando, definirEnviando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [sucesso, definirSucesso] = useState(false);

  useEffect(() => {
    if (!sessao) return;
    listarMinhasSolicitacoes(sessao.token)
      .then((pagina) => definirSolicitacoes(pagina.itens))
      .catch(() => definirSolicitacoes([]));
  }, [sessao]);

  async function aoEnviar() {
    if (!sessao || !contexto) return;
    definirEnviando(true);
    definirErro(null);
    try {
      const nova = await solicitarLocal(
        {
          comunidadeId: contexto.comunidadeId,
          desafioDeColetaId: contexto.desafioId,
          nivel: contexto.nivel,
          rotulo,
          justificativa,
        },
        sessao.token,
      );
      definirSolicitacoes((atual) => [nova, ...(atual ?? [])]);
      definirRotulo("");
      definirJustificativa("");
      definirSucesso(true);
    } catch {
      definirErro("Não foi possível enviar o seu pedido agora. Tente de novo em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <section aria-label="Solicitações de local">
      {contexto && (
        <div className="cg-solicitar-local">
          <h2>Pedir local que falta</h2>
          <p>
            Esse pedido não cria o local sozinho — quem decide é o Mestre da trilha ou um
            Admin.
          </p>
          <Campo rotulo="Nome do local" valor={rotulo} aoAlterar={definirRotulo} />
          <Campo
            rotulo="Por que esse local é importante?"
            valor={justificativa}
            aoAlterar={definirJustificativa}
          />
          {erro && <Aviso tipo="erro">{erro}</Aviso>}
          {sucesso && <Aviso tipo="sucesso">Seu pedido foi enviado!</Aviso>}
          <Botao
            desabilitado={!rotulo.trim() || !justificativa.trim() || enviando}
            onClick={aoEnviar}
          >
            Enviar pedido
          </Botao>
        </div>
      )}

      <h2>Meus pedidos</h2>
      {solicitacoes === null && <EstadoDaLista>Carregando os seus pedidos…</EstadoDaLista>}
      {solicitacoes !== null && solicitacoes.length === 0 && (
        <EstadoDaLista>Você ainda não fez nenhum pedido de local.</EstadoDaLista>
      )}
      {solicitacoes !== null && solicitacoes.length > 0 && (
        <ul className="cg-lista-de-solicitacoes">
          {solicitacoes.map((solicitacao) => (
            <li key={solicitacao.id} className="cg-cartao-de-solicitacao">
              <p className="cg-cartao-de-solicitacao__titulo">{solicitacao.rotulo}</p>
              <p>{ROTULO_DA_SITUACAO[solicitacao.situacao]}</p>
              {solicitacao.situacao === "recusada" && solicitacao.motivo_da_recusa && (
                <p>Motivo: {solicitacao.motivo_da_recusa}</p>
              )}
              {solicitacao.situacao === "aprovada" && (
                <p>O local já está disponível para abrir série.</p>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
