import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import {
  CustomizacaoDoKit,
  type FormularioAberto,
  type KitAberto,
  lerMinhasCustomizacoes,
  type MinhasCustomizacoes,
  ultimoRegistroDoKit,
} from "comum/customizacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { descreverRecompensa } from "comum/trilha";
import { useCallback, useEffect, useState } from "react";
import { listarMinhasRecompensas, type RecompensaConquistada } from "../api/carteira";

function formatarData(valorIso: string): string {
  return new Date(valorIso).toLocaleDateString("pt-BR");
}

// As recompensas de marco conquistadas — o Mestre confirma a entrega, e
// nenhuma tela oferece comprá-las com pontos de qualquer natureza
// (`RF-05-45`, `RF-05-46`, `RN-05-07`, `RN-05-41`).
export function Conquistas() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [recompensas, definirRecompensas] = useState<RecompensaConquistada[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [customizacoes, definirCustomizacoes] = useState<MinhasCustomizacoes | null>(null);
  const [erroDasCustomizacoes, definirErroDasCustomizacoes] = useState(false);
  const [formularioAberto, definirFormularioAberto] = useState<FormularioAberto | null>(null);

  // As duas leituras saem juntas, mas a falha só das customizações não esconde
  // as conquistas: o cartão segue como antes, com um aviso único (design —
  // decisão 3).
  const lerCustomizacoes = useCallback(
    async (token: string, ehCancelado: () => boolean = () => false) => {
      try {
        const resultado = await lerMinhasCustomizacoes(token);
        if (ehCancelado()) return;
        definirCustomizacoes(resultado);
        definirErroDasCustomizacoes(false);
      } catch (erroCapturado) {
        if (ehCancelado()) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErroDasCustomizacoes(true);
      }
    },
    [tratarRecusaDeSessao],
  );

  useEffect(() => {
    if (!sessao) return;
    const token = sessao.token;
    let cancelado = false;

    async function carregarRecompensas() {
      definirErro(null);
      try {
        const resultado = await listarMinhasRecompensas(token);
        if (cancelado) return;
        definirRecompensas(resultado);
      } catch (erroCapturado) {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro(
          "Não foi possível carregar as suas conquistas agora. Tente de novo em instantes.",
        );
      }
    }

    carregarRecompensas();
    lerCustomizacoes(token, () => cancelado);
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao, lerCustomizacoes]);

  function kitDaRecompensa(recompensa: RecompensaConquistada): KitAberto | null {
    return (
      customizacoes?.kits_abertos.find(
        (kit) =>
          kit.recompensa_de_marco_id === recompensa.recompensa_de_marco_id &&
          kit.customizacao_aberta,
      ) ?? null
    );
  }

  return (
    <section className="cg-conquistas" aria-label="Minhas conquistas">
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {erroDasCustomizacoes && (
        <Aviso tipo="atencao">
          Não foi possível carregar a customização dos seus kits agora. Tente de novo em
          instantes.
        </Aviso>
      )}

      {recompensas === null && !erro && (
        <EstadoDaLista>Carregando as suas conquistas…</EstadoDaLista>
      )}
      {recompensas !== null && recompensas.length === 0 && (
        <EstadoDaLista>
          Você ainda não conquistou nenhuma recompensa de marco. Continue na sua trilha!
        </EstadoDaLista>
      )}
      {recompensas !== null && recompensas.length > 0 && (
        <ul className="cg-lista-de-conquistas">
          {recompensas.map((recompensa) => (
            <li key={recompensa.recompensa_de_marco_id} className="cg-cartao-de-conquista">
              {/* A mesma frase da tela da recompensa no percurso, e não
                  outra: "Quantidade conquistada: 1" não dizia se era o
                  livro, a camisa ou o kit (`RF-05-45`). */}
              <p>{descreverRecompensa(recompensa)}</p>
              {recompensa.entregue ? (
                <Aviso tipo="sucesso">
                  Entregue em{" "}
                  {recompensa.entregue_em ? formatarData(recompensa.entregue_em) : ""}
                </Aviso>
              ) : (
                <Aviso tipo="andamento">Aguardando o Mestre confirmar a entrega.</Aviso>
              )}
              {(() => {
                const kit = kitDaRecompensa(recompensa);
                if (kit === null || !sessao || customizacoes === null) return null;
                return (
                  <CustomizacaoDoKit
                    kit={kit}
                    ultimo={ultimoRegistroDoKit(kit, customizacoes.registros)}
                    token={sessao.token}
                    formularioAberto={formularioAberto}
                    abrirFormulario={definirFormularioAberto}
                    fecharFormulario={() => definirFormularioAberto(null)}
                    aoMudar={() => lerCustomizacoes(sessao.token)}
                  />
                );
              })()}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
