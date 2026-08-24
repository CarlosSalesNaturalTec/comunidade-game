import { useSessao } from "comum/autenticacao";
import { Cabecalho, Moldura } from "comum/react";
import { useState } from "react";
import { TelaDeEntradaDoGuerreiro } from "../entrada/TelaDeEntradaDoGuerreiro";
import { TelaDeEquipes } from "../equipes/TelaDeEquipes";

type Caminho = "inicio" | "trilhas";

interface Props {
  tokenDeTrabalho: string;
  aulaId: string;
}

// Os dois caminhos do PRD-04 §6.1 — onboarding e trilhas. O onboarding
// entra desabilitado: depende da câmera, fora do recorte desta fatia
// (`RF-04-01`, proposal — decisão 1).
export function TelaInicial({ tokenDeTrabalho, aulaId }: Props) {
  const { sessao: sessaoDoGuerreiro, sair: sairDoGuerreiro } = useSessao();
  const [caminho, definirCaminho] = useState<Caminho>("inicio");

  // Fim de cada atendimento: a sessão do Guerreiro(a) é limpa e a tela
  // volta ao início, sem dado do atendimento anterior (`RF-04-28`, design
  // — decisão 2).
  function voltarAoInicio() {
    sairDoGuerreiro();
    definirCaminho("inicio");
  }

  if (caminho === "trilhas") {
    if (!sessaoDoGuerreiro) {
      return (
        <TelaDeEntradaDoGuerreiro
          tokenDeTrabalho={tokenDeTrabalho}
          aoVoltar={() => definirCaminho("inicio")}
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
        <button type="button" className="cg-caminho" disabled>
          Onboarding — cadastro e presença por nick e foto (em breve)
        </button>
        <button type="button" className="cg-caminho" onClick={() => definirCaminho("trilhas")}>
          Trilhas — entrar com o nick e trabalhar em equipe
        </button>
      </div>
    </Moldura>
  );
}
