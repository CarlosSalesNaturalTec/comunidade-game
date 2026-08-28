import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { useId, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import type { AtividadePrevista, PainelDoDia } from "../painel-do-dia/api";
import { DESFECHOS, type Desfecho, lancarAtividadeRealizada } from "./api";

interface Props {
  aulaId: string;
  presencas: PainelDoDia["presencas"];
  atividadesPrevistas: AtividadePrevista[];
  onLancado: () => void;
}

interface LinhaDoParticipante {
  producao: string;
  desfecho: Desfecho;
}

const MENSAGEM_DE_SUCESSO =
  "Lançamento gravado: a aula passou a realizada e as reservas viraram baixa.";

const DADO_COLETADO = "o resultado da atividade do Guerreiro(a)";

// Um único ato por aula, com todos os participantes juntos — sem campo de
// valor de pontuação, que vem da tabela do documento 11 §5 (`RF-02-34`,
// `RF-02-39`, `RN-02-21`).
export function LancamentoDaAtividade({
  aulaId,
  presencas,
  atividadesPrevistas,
  onLancado,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoSeletorDeAtividade = useId();
  const [atividadeId, definirAtividadeId] = useState(atividadesPrevistas[0]?.id ?? "");
  const [linhas, definirLinhas] = useState<Record<string, LinhaDoParticipante>>({});
  const [participanteSemProducao, definirParticipanteSemProducao] = useState<string | null>(
    null,
  );
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [gravado, definirGravado] = useState(false);

  function linhaDe(guerreiroId: string): LinhaDoParticipante {
    return linhas[guerreiroId] ?? { producao: "", desfecho: "realizada" };
  }

  function atualizarLinha(guerreiroId: string, parcial: Partial<LinhaDoParticipante>) {
    definirLinhas((atual) => ({
      ...atual,
      [guerreiroId]: { ...linhaDe(guerreiroId), ...parcial },
    }));
  }

  async function aoSubmeter() {
    definirParticipanteSemProducao(null);
    definirErroDeRecusa(null);

    if (!atividadeId) {
      definirErroDeRecusa("Escolha a atividade lançada.");
      return;
    }
    const semProducao = presencas.find(
      (presenca) => !linhaDe(presenca.guerreiro_id).producao.trim(),
    );
    if (semProducao) {
      definirParticipanteSemProducao(semProducao.guerreiro_id);
      return;
    }
    if (!sessao) return;

    const agora = new Date().toISOString();
    definirEnviando(true);
    try {
      await lancarAtividadeRealizada(
        aulaId,
        presencas.map((presenca) => ({
          guerreiro_id: presenca.guerreiro_id,
          atividade_id: atividadeId,
          momento_do_fato: agora,
          producao: linhaDe(presenca.guerreiro_id).producao,
          desfecho: linhaDe(presenca.guerreiro_id).desfecho,
        })),
        sessao.token,
      );
      definirGravado(true);
      onLancado();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDeRecusa(
        erro instanceof ErroDaApi
          ? erro.message
          : "Não foi possível lançar a atividade realizada. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  if (gravado) {
    return <Aviso tipo="sucesso">{MENSAGEM_DE_SUCESSO}</Aviso>;
  }

  if (presencas.length === 0) {
    return <p role="status">Ninguém registrou presença ainda — nada a lançar.</p>;
  }

  if (atividadesPrevistas.length === 0) {
    return <p role="status">Nenhuma atividade prevista para este encontro.</p>;
  }

  return (
    <section aria-label="Lançar atividade realizada" className="cg-lancamento-da-atividade">
      <AvisoDeColeta dado={DADO_COLETADO} />

      <div className="cg-campo">
        <label htmlFor={idDoSeletorDeAtividade}>Atividade lançada</label>
        <select
          id={idDoSeletorDeAtividade}
          value={atividadeId}
          onChange={(evento) => definirAtividadeId(evento.target.value)}
        >
          {atividadesPrevistas.map((atividade) => (
            <option key={atividade.id} value={atividade.id}>
              {atividade.missao_titulo} — {atividade.titulo}
            </option>
          ))}
        </select>
      </div>

      <ul>
        {presencas.map((presenca) => (
          <li key={presenca.guerreiro_id}>
            <span>{presenca.nick}</span>
            <select
              aria-label={`Desfecho de ${presenca.nick}`}
              value={linhaDe(presenca.guerreiro_id).desfecho}
              onChange={(evento) =>
                atualizarLinha(presenca.guerreiro_id, {
                  desfecho: evento.target.value as Desfecho,
                })
              }
            >
              {DESFECHOS.map((desfecho) => (
                <option key={desfecho.valor} value={desfecho.valor}>
                  {desfecho.rotulo}
                </option>
              ))}
            </select>
            <Campo
              rotulo={`O que ${presenca.nick} produziu`}
              valor={linhaDe(presenca.guerreiro_id).producao}
              aoAlterar={(valor) => atualizarLinha(presenca.guerreiro_id, { producao: valor })}
              erro={
                participanteSemProducao === presenca.guerreiro_id
                  ? "Informe o que este Guerreiro(a) produziu."
                  : null
              }
            />
          </li>
        ))}
      </ul>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao onClick={aoSubmeter} desabilitado={enviando}>
        Lançar atividade realizada
      </Botao>
    </section>
  );
}
