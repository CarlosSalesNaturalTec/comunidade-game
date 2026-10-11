import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { useId, useState } from "react";
import type { AtividadeAvulsa } from "../atividades/api";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import type { PainelDoDia } from "../painel-do-dia/api";
import { DESFECHOS, type Desfecho, lancarResultadosDaAtividadeAvulsa } from "./api";

interface Props {
  aulaId: string;
  atividade: AtividadeAvulsa;
  presencas: PainelDoDia["presencas"];
  equipes: PainelDoDia["equipes"];
  onLancado: () => void;
}

interface LinhaDoParticipante {
  producao: string;
  desfecho: Desfecho | "";
}

// A avulsa não entra na programação do encontro: o ato por atividade grava
// Resultado e nada mais (`RF-02-112`, `RF-02-34`).
const LINHA_DO_QUE_NAO_FAZ =
  "Este lançamento não converte reserva em baixa nem passa a aula a realizada — " +
  "isso é do lançamento da atividade da aula.";

const DADO_COLETADO = "o resultado da atividade avulsa do Guerreiro(a)";

// A recusa do núcleo chega em linguagem do domínio; a tela a reescreve no
// que a pessoa precisa fazer (`RN-02-33`).
function recusaEmLinguagemSimples(erro: ErroDaApi): string {
  if (erro.campo === "guerreiro_id") {
    return (
      "Alguém desta lista já recebeu Resultado nesta atividade. " +
      "O Resultado não se repete nem se corrige — confira quem já foi lançado."
    );
  }
  if (erro.campo === "equipe_id") {
    return `Não foi possível lançar por equipe: ${erro.message}`;
  }
  return erro.message;
}

export function LancamentoDaAtividadeAvulsa({
  aulaId,
  atividade,
  presencas,
  equipes,
  onLancado,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDaEquipe = useId();
  const idDoDesfechoDaEquipe = useId();

  const porEquipe = atividade.modalidade !== "individual";
  const equipesDaAula = equipes;

  const [linhas, definirLinhas] = useState<Record<string, LinhaDoParticipante>>({});
  const [equipeId, definirEquipeId] = useState("");
  const [desfechoDaEquipe, definirDesfechoDaEquipe] = useState<Desfecho | "">("");
  const [producaoDaEquipe, definirProducaoDaEquipe] = useState("");
  const [falta, definirFalta] = useState<string | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [gravado, definirGravado] = useState(false);

  const nicksPresentes = new Set(presencas.map((presenca) => presenca.nick));
  const equipeEscolhida = equipesDaAula.find((equipe) => equipe.id === equipeId) ?? null;
  const foraDaEquipe =
    equipeEscolhida?.integrantes
      .filter((integrante) => !nicksPresentes.has(integrante.nick))
      .map((integrante) => integrante.nick) ?? [];

  function linhaDe(guerreiroId: string): LinhaDoParticipante {
    return linhas[guerreiroId] ?? { producao: "", desfecho: "" };
  }

  function atualizarLinha(guerreiroId: string, parcial: Partial<LinhaDoParticipante>) {
    definirLinhas((atual) => ({
      ...atual,
      [guerreiroId]: { ...linhaDe(guerreiroId), ...parcial },
    }));
  }

  async function aoSubmeter() {
    definirFalta(null);
    definirErroDeRecusa(null);
    if (!sessao) return;

    const agora = new Date().toISOString();
    let declaracao: Parameters<typeof lancarResultadosDaAtividadeAvulsa>[2];

    if (porEquipe) {
      if (!equipeId) {
        definirFalta("Escolha a equipe que realizou a atividade.");
        return;
      }
      if (!desfechoDaEquipe) {
        definirFalta("Escolha o desfecho da equipe.");
        return;
      }
      if (!producaoDaEquipe.trim()) {
        definirFalta("Informe o que a equipe produziu.");
        return;
      }
      declaracao = {
        equipe: {
          equipe_id: equipeId,
          momento_do_fato: agora,
          producao: producaoDaEquipe,
          desfecho: desfechoDaEquipe,
        },
      };
    } else {
      const semDesfecho = presencas.find(
        (presenca) => !linhaDe(presenca.guerreiro_id).desfecho,
      );
      if (semDesfecho) {
        definirFalta(`Escolha o desfecho de ${semDesfecho.nick}.`);
        return;
      }
      const semProducao = presencas.find(
        (presenca) => !linhaDe(presenca.guerreiro_id).producao.trim(),
      );
      if (semProducao) {
        definirFalta(`Informe o que ${semProducao.nick} produziu.`);
        return;
      }
      declaracao = {
        participantes: presencas.map((presenca) => ({
          guerreiro_id: presenca.guerreiro_id,
          momento_do_fato: agora,
          producao: linhaDe(presenca.guerreiro_id).producao,
          desfecho: linhaDe(presenca.guerreiro_id).desfecho as Desfecho,
        })),
      };
    }

    definirEnviando(true);
    try {
      await lancarResultadosDaAtividadeAvulsa(atividade.id, aulaId, declaracao, sessao.token);
      definirGravado(true);
      onLancado();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDeRecusa(
        erro instanceof ErroDaApi
          ? recusaEmLinguagemSimples(erro)
          : "Não foi possível lançar a atividade avulsa. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  if (gravado) {
    return (
      <Aviso tipo="sucesso">
        Resultado da atividade "{atividade.titulo}" gravado. A aula segue como estava.
      </Aviso>
    );
  }

  return (
    <section aria-label={`Lançar a atividade avulsa ${atividade.titulo}`}>
      <h3>{atividade.titulo}</h3>
      <p role="status">{LINHA_DO_QUE_NAO_FAZ}</p>
      <AvisoDeColeta dado={DADO_COLETADO} />

      {porEquipe ? (
        <>
          <div className="cg-campo">
            <label htmlFor={idDaEquipe}>Equipe que realizou</label>
            <select
              id={idDaEquipe}
              value={equipeId}
              onChange={(evento) => definirEquipeId(evento.target.value)}
            >
              <option value="">Escolha uma equipe</option>
              {equipesDaAula.map((equipe) => (
                <option key={equipe.id} value={equipe.id}>
                  {equipe.nome}
                </option>
              ))}
            </select>
          </div>

          {equipesDaAula.length === 0 && (
            <p role="status">Nenhuma equipe formada neste encontro ainda.</p>
          )}

          {foraDaEquipe.length > 0 && (
            <p role="status">
              Fica de fora por não ter presença nesta aula: {foraDaEquipe.join(", ")}.
            </p>
          )}

          <div className="cg-campo">
            <label htmlFor={idDoDesfechoDaEquipe}>Desfecho da equipe</label>
            <select
              id={idDoDesfechoDaEquipe}
              value={desfechoDaEquipe}
              onChange={(evento) =>
                definirDesfechoDaEquipe(evento.target.value as Desfecho | "")
              }
            >
              <option value="">Escolha o desfecho</option>
              {DESFECHOS.map((desfecho) => (
                <option key={desfecho.valor} value={desfecho.valor}>
                  {desfecho.rotulo}
                </option>
              ))}
            </select>
          </div>

          <Campo
            rotulo="O que a equipe produziu"
            valor={producaoDaEquipe}
            aoAlterar={definirProducaoDaEquipe}
          />
        </>
      ) : presencas.length === 0 ? (
        <p role="status">Ninguém registrou presença ainda — nada a lançar.</p>
      ) : (
        <ul>
          {presencas.map((presenca) => (
            <li key={presenca.guerreiro_id}>
              <span>{presenca.nick}</span>
              <select
                aria-label={`Desfecho de ${presenca.nick}`}
                value={linhaDe(presenca.guerreiro_id).desfecho}
                onChange={(evento) =>
                  atualizarLinha(presenca.guerreiro_id, {
                    desfecho: evento.target.value as Desfecho | "",
                  })
                }
              >
                <option value="">Escolha o desfecho</option>
                {DESFECHOS.map((desfecho) => (
                  <option key={desfecho.valor} value={desfecho.valor}>
                    {desfecho.rotulo}
                  </option>
                ))}
              </select>
              <Campo
                rotulo={`O que ${presenca.nick} produziu`}
                valor={linhaDe(presenca.guerreiro_id).producao}
                aoAlterar={(valor) =>
                  atualizarLinha(presenca.guerreiro_id, { producao: valor })
                }
              />
            </li>
          ))}
        </ul>
      )}

      {falta && <Aviso tipo="erro">{falta}</Aviso>}
      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao onClick={aoSubmeter} desabilitado={enviando}>
        Lançar atividade avulsa
      </Botao>
    </section>
  );
}
