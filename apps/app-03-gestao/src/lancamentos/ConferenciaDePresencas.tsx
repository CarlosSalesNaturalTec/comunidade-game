import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { useEffect, useId, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import type { PainelDoDia } from "../painel-do-dia/api";
import { type GuerreiroDaLista, listarGuerreiros } from "../personas/api";
import { anularPresenca, confirmarPresenca } from "./api";

interface Props {
  aulaId: string;
  comunidadeVirtualId: string | null;
  presencas: PainelDoDia["presencas"];
  onAlterado: () => void;
}

const DADO_COLETADO = "a presença do Guerreiro(a) no encontro";

const ROTULO_DO_MODO: Record<string, string> = {
  reconhecimento: "reconhecimento",
  confirmacao: "confirmada",
};

interface AnulacaoConcluida {
  guerreiroId: string;
  nick: string;
  motivo: string;
}

// Presença já registrada não some quando anulada — fica marcada, com o
// motivo, e o par (aula, guerreiro) volta a aceitar o registro correto
// (`RF-02-36`, `RN-02-12`). Nenhuma imagem real de Guerreiro(a) aparece: a
// representação é o avatar e o nick (`RN-02-22`).
export function ConferenciaDePresencas({
  aulaId,
  comunidadeVirtualId,
  presencas,
  onAlterado,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoSeletor = useId();
  const [guerreiros, definirGuerreiros] = useState<GuerreiroDaLista[]>([]);
  const [guerreiroFaltanteId, definirGuerreiroFaltanteId] = useState("");
  const [erroDeConfirmacao, definirErroDeConfirmacao] = useState<string | null>(null);
  const [motivosDaAnulacao, definirMotivosDaAnulacao] = useState<Record<string, string>>({});
  const [erroDaAnulacao, definirErroDaAnulacao] = useState<{
    presencaId: string;
    mensagem: string;
  } | null>(null);
  const [anulacoesConcluidas, definirAnulacoesConcluidas] = useState<AnulacaoConcluida[]>([]);
  const [enviando, definirEnviando] = useState(false);

  useEffect(() => {
    if (!sessao) return;
    listarGuerreiros(sessao.token)
      .then((pagina) => definirGuerreiros(pagina.itens))
      .catch(() => definirGuerreiros([]));
  }, [sessao]);

  const idsPresentes = new Set(presencas.map((presenca) => presenca.guerreiro_id));
  const faltantes = guerreiros.filter(
    (guerreiro) =>
      guerreiro.comunidade_virtual_id === comunidadeVirtualId &&
      !idsPresentes.has(guerreiro.id),
  );

  async function confirmarQueFaltou() {
    definirErroDeConfirmacao(null);
    if (!guerreiroFaltanteId) {
      definirErroDeConfirmacao("Escolha quem chegou.");
      return;
    }
    if (!sessao) return;
    definirEnviando(true);
    try {
      await confirmarPresenca(
        aulaId,
        {
          guerreiro_id: guerreiroFaltanteId,
          modo: "confirmacao",
          momento_do_fato: new Date().toISOString(),
        },
        sessao.token,
      );
      definirGuerreiroFaltanteId("");
      onAlterado();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDeConfirmacao(
        erro instanceof ErroDaApi
          ? erro.message
          : "Não foi possível confirmar a presença. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  async function anular(presenca: PainelDoDia["presencas"][number]) {
    definirErroDaAnulacao(null);
    const motivo = motivosDaAnulacao[presenca.id] ?? "";
    if (!motivo.trim()) {
      definirErroDaAnulacao({ presencaId: presenca.id, mensagem: "Informe o motivo." });
      return;
    }
    if (!sessao) return;
    definirEnviando(true);
    try {
      await anularPresenca(aulaId, presenca.id, motivo, sessao.token);
      definirAnulacoesConcluidas((atual) => [
        ...atual,
        { guerreiroId: presenca.guerreiro_id, nick: presenca.nick, motivo },
      ]);
      onAlterado();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDaAnulacao({
        presencaId: presenca.id,
        mensagem:
          erro instanceof ErroDaApi
            ? erro.message
            : "Não foi possível anular a presença. Tente novamente em instantes.",
      });
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <section aria-label="Conferência de presenças">
      <AvisoDeColeta dado={DADO_COLETADO} />
      <h2>Presenças</h2>
      {presencas.length === 0 && <p role="status">Ninguém registrou presença ainda.</p>}
      {presencas.length > 0 && (
        <ul>
          {presencas.map((presenca) => (
            <li key={presenca.id}>
              <span>{presenca.nick}</span> — {ROTULO_DO_MODO[presenca.modo] ?? presenca.modo}
              <Campo
                rotulo={`Motivo da anulação de ${presenca.nick}`}
                valor={motivosDaAnulacao[presenca.id] ?? ""}
                aoAlterar={(valor) =>
                  definirMotivosDaAnulacao((atual) => ({ ...atual, [presenca.id]: valor }))
                }
                erro={
                  erroDaAnulacao?.presencaId === presenca.id ? erroDaAnulacao.mensagem : null
                }
              />
              <Botao
                variante="secundaria"
                onClick={() => anular(presenca)}
                desabilitado={enviando}
              >
                Anular presença
              </Botao>
            </li>
          ))}
        </ul>
      )}

      {anulacoesConcluidas.length > 0 && (
        <ul aria-label="Presenças anuladas">
          {anulacoesConcluidas.map((anulacao) => (
            <li key={anulacao.guerreiroId}>
              Presença de {anulacao.nick} anulada — {anulacao.motivo}
            </li>
          ))}
        </ul>
      )}

      <h2>Registrar a presença que faltou</h2>
      {faltantes.length === 0 && (
        <p role="status">Todos os Guerreiros e Guerreiras da comunidade já têm presença.</p>
      )}
      {faltantes.length > 0 && (
        <div className="cg-campo">
          <label htmlFor={idDoSeletor}>Quem chegou</label>
          <select
            id={idDoSeletor}
            value={guerreiroFaltanteId}
            onChange={(evento) => definirGuerreiroFaltanteId(evento.target.value)}
          >
            <option value="">Selecione</option>
            {faltantes.map((guerreiro) => (
              <option key={guerreiro.id} value={guerreiro.id}>
                {guerreiro.nick}
              </option>
            ))}
          </select>
          <Botao onClick={confirmarQueFaltou} desabilitado={enviando}>
            Confirmar presença
          </Botao>
        </div>
      )}
      {erroDeConfirmacao && <Aviso tipo="erro">{erroDeConfirmacao}</Aviso>}
    </section>
  );
}
