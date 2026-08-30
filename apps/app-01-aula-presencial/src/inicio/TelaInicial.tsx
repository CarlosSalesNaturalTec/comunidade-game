import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useState } from "react";
import { TelaDeEntradaDoGuerreiro } from "../entrada/TelaDeEntradaDoGuerreiro";
import { TelaDeEquipes } from "../equipes/TelaDeEquipes";
import { FluxoDeOnboarding } from "../onboarding/FluxoDeOnboarding";
import { TelaDeCaptura } from "../onboarding/TelaDeCaptura";
import { CHAVE_DA_PARTIDA_DE_QUIZ, TelaDaPartida } from "../quiz/TelaDaPartida";
import { TelaDaProgramacao } from "../trilhas/TelaDaProgramacao";
import { TelaDeTroca } from "../troca/TelaDeTroca";

type Caminho = "inicio" | "onboarding" | "trilhas" | "troca" | "quiz";

interface Props {
  tokenDeTrabalho: string;
  personaIdDeTrabalho: string;
  /** Só o Mestre, na sessão de trabalho, homologa a equipe da trilha ali
   * mesmo (`RF-04-62`, `RN-04-18`). */
  papelDeTrabalho: string;
  aulaId: string;
  /** Relê `GET /v1/aulas/vigentes`, para que a janela da aula seja
   * conferida a cada volta ao início (`RF-04-05`, design — decisão 3). */
  aoVoltarAoInicio: () => void;
  /** Só o Mestre da sessão de trabalho abre e fecha o momento de troca
   * (`RF-04-49`, decisão do fundador de 2026-08-25). */
  podeAbrirMomentoDeTroca: boolean;
  momentoDeTrocaAberto: boolean;
  abrindoMomentoDeTroca: boolean;
  erroDeAberturaDaTroca: string | null;
  aoAbrirMomentoDeTroca: () => void;
  aoFecharMomentoDeTroca: () => void;
}

// Os dois caminhos do PRD-04 §6.1 — onboarding e trilhas. O onboarding
// entra em estado operante nesta fatia: cadastro do Guerreiro(a), do
// responsável, o termo e a captura da imagem (`RF-04-01`, `RF-04-07`).
export function TelaInicial({
  tokenDeTrabalho,
  personaIdDeTrabalho,
  papelDeTrabalho,
  aulaId,
  aoVoltarAoInicio,
  podeAbrirMomentoDeTroca,
  momentoDeTrocaAberto,
  abrindoMomentoDeTroca,
  erroDeAberturaDaTroca,
  aoAbrirMomentoDeTroca,
  aoFecharMomentoDeTroca,
}: Props) {
  const { sessao: sessaoDoGuerreiro, sair: sairDoGuerreiro } = useSessao();
  const [caminho, definirCaminho] = useState<Caminho>("inicio");
  // Só a sessão aberta por confirmação presencial autoriza o recadastro da
  // imagem — nunca a de reconhecimento, que já provou que a imagem serve
  // (`RF-04-22`, design — decisão 4).
  const [viaDeEntrada, definirViaDeEntrada] = useState<
    "reconhecimento" | "confirmacao" | null
  >(null);
  const [mostrarRecadastro, definirMostrarRecadastro] = useState(false);
  // A equipe escolhida no caminho das trilhas — estado deste aparelho, que
  // morre com a volta ao início, nunca gravado no núcleo (`RF-04-35`,
  // documento 02 §5).
  const [equipeEscolhidaId, definirEquipeEscolhidaId] = useState<string | null>(null);

  // Fim de cada atendimento: a sessão do Guerreiro(a) é limpa e a tela
  // volta ao início, sem dado do atendimento anterior (`RF-04-28`, design
  // — decisão 2). O desmonte da tela de cadastro, sozinho, já descarta o
  // que ela tinha em estado.
  function voltarAoInicio() {
    sairDoGuerreiro();
    definirCaminho("inicio");
    definirViaDeEntrada(null);
    definirMostrarRecadastro(false);
    definirEquipeEscolhidaId(null);
    sessionStorage.removeItem(CHAVE_DA_PARTIDA_DE_QUIZ);
    aoVoltarAoInicio();
  }

  if (caminho === "onboarding") {
    return (
      <FluxoDeOnboarding
        tokenDeTrabalho={tokenDeTrabalho}
        personaIdDeTrabalho={personaIdDeTrabalho}
        aulaId={aulaId}
        aoConcluir={voltarAoInicio}
        aoVoltar={voltarAoInicio}
      />
    );
  }

  if (caminho === "trilhas" || caminho === "troca" || caminho === "quiz") {
    if (!sessaoDoGuerreiro) {
      return (
        <TelaDeEntradaDoGuerreiro
          tokenDeTrabalho={tokenDeTrabalho}
          aulaId={aulaId}
          aoVoltar={voltarAoInicio}
          aoAbrirSessao={definirViaDeEntrada}
        />
      );
    }
    if (caminho === "troca") {
      return (
        <TelaDeTroca
          tokenDeTrabalho={tokenDeTrabalho}
          aulaId={aulaId}
          tokenDoGuerreiro={sessaoDoGuerreiro.token}
          guerreiroId={sessaoDoGuerreiro.persona_id}
          aoConcluir={voltarAoInicio}
          aoVoltar={voltarAoInicio}
        />
      );
    }
    if (caminho === "quiz") {
      return (
        <TelaDaPartida
          aulaId={aulaId}
          tokenDoGuerreiro={sessaoDoGuerreiro.token}
          aoVoltar={voltarAoInicio}
        />
      );
    }
    if (mostrarRecadastro) {
      return (
        <TelaDeCaptura
          tokenDeTrabalho={tokenDeTrabalho}
          guerreiroId={sessaoDoGuerreiro.persona_id}
          aoConcluir={() => definirMostrarRecadastro(false)}
          aoVoltar={() => definirMostrarRecadastro(false)}
        />
      );
    }
    if (equipeEscolhidaId) {
      return (
        <TelaDaProgramacao
          equipeId={equipeEscolhidaId}
          token={sessaoDoGuerreiro.token}
          aoVoltar={() => definirEquipeEscolhidaId(null)}
          podeHomologarEquipeDaTrilha={papelDeTrabalho === "mestre"}
          tokenDeTrabalho={tokenDeTrabalho}
        />
      );
    }
    return (
      <TelaDeEquipes
        aulaId={aulaId}
        token={sessaoDoGuerreiro.token}
        aoVoltar={voltarAoInicio}
        podeRecadastrarImagem={viaDeEntrada === "confirmacao"}
        aoRecadastrarImagem={() => definirMostrarRecadastro(true)}
        aoEscolherEquipe={definirEquipeEscolhidaId}
      />
    );
  }

  return (
    <Moldura>
      <Cabecalho titulo="Comunidade Game — Aula" subtitulo="O que você quer fazer?" />
      <div className="cg-caminhos">
        <button
          type="button"
          className="cg-caminho"
          onClick={() => definirCaminho("onboarding")}
        >
          Onboarding — cadastro do Guerreiro(a) e presença do dia
        </button>
        <button type="button" className="cg-caminho" onClick={() => definirCaminho("trilhas")}>
          Trilhas — entrar com o nick e trabalhar em equipe
        </button>
        <button type="button" className="cg-caminho" onClick={() => definirCaminho("quiz")}>
          Quiz ao Vivo — entrar com o nick e responder pela equipe
        </button>
        {momentoDeTrocaAberto && (
          <button type="button" className="cg-caminho" onClick={() => definirCaminho("troca")}>
            Troca por recompensa avulsa — entregar uma recompensa do encontro
          </button>
        )}
      </div>
      {podeAbrirMomentoDeTroca && (
        <div className="cg-momento-de-troca">
          <Botao
            variante="secundaria"
            onClick={momentoDeTrocaAberto ? aoFecharMomentoDeTroca : aoAbrirMomentoDeTroca}
            desabilitado={abrindoMomentoDeTroca}
          >
            {momentoDeTrocaAberto
              ? "Fechar o momento de troca"
              : abrindoMomentoDeTroca
                ? "Abrindo…"
                : "Abrir o momento de troca"}
          </Botao>
          {erroDeAberturaDaTroca && <Aviso tipo="erro">{erroDeAberturaDaTroca}</Aviso>}
        </div>
      )}
    </Moldura>
  );
}
