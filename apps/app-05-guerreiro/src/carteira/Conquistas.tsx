import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import {
  cancelarCustomizacao,
  type KitAberto,
  lerMinhasCustomizacoes,
  type MinhasCustomizacoes,
  RegistroDaCustomizacao,
  type RegistroDeCustomizacao,
} from "comum/customizacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { descreverRecompensa } from "comum/trilha";
import { type ReactNode, useCallback, useEffect, useState } from "react";
import { listarMinhasRecompensas, type RecompensaConquistada } from "../api/carteira";

function formatarData(valorIso: string): string {
  return new Date(valorIso).toLocaleDateString("pt-BR");
}

/** O registro mais recente do kit, pela data em que foi registrado — é ele
 * que decide a ação do cartão (design — decisão 3). */
function ultimoRegistroDoKit(
  kit: KitAberto,
  registros: RegistroDeCustomizacao[],
): RegistroDeCustomizacao | null {
  const doKit = registros.filter(
    (registro) => registro.entrega_de_recompensa_id === kit.entrega_de_recompensa_id,
  );
  if (doKit.length === 0) return kit.pendente;
  return doKit.reduce((maisRecente, registro) =>
    registro.registrado_em > maisRecente.registrado_em ? registro : maisRecente,
  );
}

interface FormularioAberto {
  entregaId: string;
  registroId: string | null;
}

// A customização do kit aberto, no próprio cartão da conquista: a situação do
// último registro e a ação que cabe — registrar, retomar o envio, aguardar a
// aula e cancelar, ler o motivo e enviar de novo (`RF-05-102`, `RF-05-103`,
// resposta do fundador de 2026-11-13).
function CustomizacaoDoKit({
  kit,
  ultimo,
  token,
  formularioAberto,
  abrirFormulario,
  fecharFormulario,
  aoMudar,
}: {
  kit: KitAberto;
  ultimo: RegistroDeCustomizacao | null;
  token: string;
  formularioAberto: FormularioAberto | null;
  abrirFormulario: (formulario: FormularioAberto) => void;
  fecharFormulario: () => void;
  aoMudar: () => Promise<void>;
}) {
  const [erro, definirErro] = useState<string | null>(null);
  const [cancelando, definirCancelando] = useState(false);
  const entregaId = kit.entrega_de_recompensa_id;

  if (formularioAberto?.entregaId === entregaId) {
    return (
      <RegistroDaCustomizacao
        entregaDeRecompensaId={entregaId}
        registroIdInicial={formularioAberto.registroId}
        token={token}
        aoConcluir={async () => {
          fecharFormulario();
          await aoMudar();
        }}
        aoCancelar={fecharFormulario}
      />
    );
  }

  async function cancelar(registroId: string) {
    definirErro(null);
    definirCancelando(true);
    try {
      await cancelarCustomizacao(registroId, token);
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível cancelar agora. Tente de novo em instantes.",
      );
    } finally {
      definirCancelando(false);
    }
    await aoMudar();
  }

  const registrarNovo = (rotulo: string) => (
    <Botao
      variante="secundaria"
      onClick={() => abrirFormulario({ entregaId, registroId: null })}
    >
      {rotulo}
    </Botao>
  );

  let conteudo: ReactNode;
  if (ultimo === null || ultimo.situacao === "cancelado" || ultimo.situacao === "expirado") {
    conteudo = registrarNovo("Registrar a customização");
  } else if (ultimo.situacao === "pendente" && !ultimo.tem_midia) {
    conteudo = (
      <>
        <p>Falta enviar a foto ou o vídeo da sua customização.</p>
        <Botao onClick={() => abrirFormulario({ entregaId, registroId: ultimo.id })}>
          Enviar a foto ou o vídeo
        </Botao>
        <Botao
          variante="secundaria"
          onClick={() => cancelar(ultimo.id)}
          desabilitado={cancelando}
        >
          Cancelar
        </Botao>
      </>
    );
  } else if (ultimo.situacao === "pendente") {
    conteudo = (
      <>
        <Aviso tipo="andamento">
          Aguardando a aula: mostre o kit ao Mestre no encontro. Se não for apresentado até o
          fim do ciclo, este registro expira.
        </Aviso>
        <Botao
          variante="secundaria"
          onClick={() => cancelar(ultimo.id)}
          desabilitado={cancelando}
        >
          Cancelar
        </Botao>
      </>
    );
  } else if (ultimo.situacao === "reprovado") {
    conteudo = (
      <>
        <Aviso tipo="atencao">O Mestre pediu um ajuste: {ultimo.motivo_do_julgamento}</Aviso>
        {registrarNovo("Enviar de novo")}
      </>
    );
  } else {
    conteudo = (
      <>
        <Aviso tipo="sucesso">Aprovado pelo Mestre.</Aviso>
        {registrarNovo("Registrar a customização")}
      </>
    );
  }

  return (
    <div className="cg-cartao-de-conquista__customizacao">
      {conteudo}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
    </div>
  );
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
