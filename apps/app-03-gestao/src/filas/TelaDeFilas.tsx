import { Aviso, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useId, useState } from "react";
import { ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { AvaliacaoDaSolicitacao } from "./AvaliacaoDaSolicitacao";
import { listarSolicitacoesDeParticipacao, type SolicitacaoDeParticipacao } from "./api";
import { ListaDeFilas } from "./ListaDeFilas";

// O filtro por natureza nasce servindo só participação; a lista e a
// apresentação do atraso não mudam de forma quando as outras três
// naturezas entrarem (design — decisão 5, `RF-02-18`, `RF-02-25`).
type Natureza = "participacao";

const NATUREZAS: { chave: Natureza; rotulo: string }[] = [
  { chave: "participacao", rotulo: "Participação" },
];

export function TelaDeFilas() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const idDoFiltro = useId();
  const [natureza, definirNatureza] = useState<Natureza>("participacao");
  const [solicitacoes, definirSolicitacoes] = useState<SolicitacaoDeParticipacao[] | null>(
    null,
  );
  const [erro, definirErro] = useState<string | null>(null);
  const [selecionada, definirSelecionada] = useState<SolicitacaoDeParticipacao | null>(null);

  const ehAdmin = sessao?.papel === "admin";

  const carregar = useCallback(async () => {
    if (!sessao || !ehAdmin) return;
    try {
      const pagina = await listarSolicitacoesDeParticipacao(sessao.token);
      definirSolicitacoes(pagina.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar a fila. Tente novamente em instantes.");
    }
  }, [sessao, ehAdmin, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  return (
    <Moldura>
      <Cabecalho titulo="Filas" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {!ehAdmin && (
        <Aviso tipo="atencao">
          Esta área é do Admin. Fale com um Admin da comunidade se precisar avaliar uma
          solicitação.
        </Aviso>
      )}

      {ehAdmin && (
        <>
          {erro && <Aviso tipo="erro">{erro}</Aviso>}

          <div className="cg-campo">
            <label htmlFor={idDoFiltro}>Natureza</label>
            <select
              id={idDoFiltro}
              value={natureza}
              onChange={(evento) => definirNatureza(evento.target.value as Natureza)}
            >
              {NATUREZAS.map((item) => (
                <option key={item.chave} value={item.chave}>
                  {item.rotulo}
                </option>
              ))}
            </select>
          </div>

          {selecionada ? (
            <AvaliacaoDaSolicitacao
              solicitacao={selecionada}
              onFechar={() => definirSelecionada(null)}
              onAvaliado={(atualizada) => {
                definirSelecionada(atualizada);
                carregar();
              }}
            />
          ) : (
            <ListaDeFilas solicitacoes={solicitacoes} aoSelecionar={definirSelecionada} />
          )}
        </>
      )}
    </Moldura>
  );
}
