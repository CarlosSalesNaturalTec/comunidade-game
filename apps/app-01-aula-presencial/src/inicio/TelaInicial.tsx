import { useSessao } from "comum/autenticacao";
import { Cabecalho, Moldura } from "comum/react";
import { useState } from "react";
import { TelaDeEntradaDoGuerreiro } from "../entrada/TelaDeEntradaDoGuerreiro";
import { TelaDeEquipes } from "../equipes/TelaDeEquipes";
import { TelaDeCadastro } from "../onboarding/TelaDeCadastro";

type Caminho = "inicio" | "onboarding" | "trilhas";

interface Props {
  tokenDeTrabalho: string;
  aulaId: string;
  /** Relê `GET /v1/aulas/vigentes`, para que a janela da aula seja
   * conferida a cada volta ao início (`RF-04-05`, design — decisão 3). */
  aoVoltarAoInicio: () => void;
}

// Os dois caminhos do PRD-04 §6.1 — onboarding e trilhas. O onboarding
// entra em estado operante nesta fatia: cadastro do encontro, sem câmera
// nem consentimento (`RF-04-01`, `RF-04-07`).
export function TelaInicial({ tokenDeTrabalho, aulaId, aoVoltarAoInicio }: Props) {
  const { sessao: sessaoDoGuerreiro, sair: sairDoGuerreiro } = useSessao();
  const [caminho, definirCaminho] = useState<Caminho>("inicio");

  // Fim de cada atendimento: a sessão do Guerreiro(a) é limpa e a tela
  // volta ao início, sem dado do atendimento anterior (`RF-04-28`, design
  // — decisão 2). O desmonte da tela de cadastro, sozinho, já descarta o
  // que ela tinha em estado.
  function voltarAoInicio() {
    sairDoGuerreiro();
    definirCaminho("inicio");
    aoVoltarAoInicio();
  }

  if (caminho === "onboarding") {
    return (
      <TelaDeCadastro
        tokenDeTrabalho={tokenDeTrabalho}
        aulaId={aulaId}
        aoConcluir={voltarAoInicio}
        aoVoltar={voltarAoInicio}
      />
    );
  }

  if (caminho === "trilhas") {
    if (!sessaoDoGuerreiro) {
      return (
        <TelaDeEntradaDoGuerreiro
          tokenDeTrabalho={tokenDeTrabalho}
          aoVoltar={voltarAoInicio}
        />
      );
    }
    return (
      <TelaDeEquipes
        aulaId={aulaId}
        token={sessaoDoGuerreiro.token}
        aoVoltar={voltarAoInicio}
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
      </div>
    </Moldura>
  );
}
