import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { type ReactNode, useEffect, useState } from "react";
import { lerMinhaPresenca } from "../api/presencas";

type Conferencia = "conferindo" | "tem" | "naoTem" | "falhou";

interface Props {
  aulaId: string;
  tokenDoGuerreiro: string;
  /** Leva ao caminho Presença, encerrando a sessão aberta aqui
   * (`RF-04-67`, `RF-04-28`). */
  aoRegistrarPresenca: () => void;
  aoVoltar: () => void;
  children: ReactNode;
}

// A falha de camada não é falta de presença: quem não conseguiu perguntar
// não descobriu nada sobre a criança, e dizer "registre a presença" seria a
// sexta falha silenciosa deste caminho (`RN-04-36`, invariante 25).
const MENSAGEM_DE_FALHA =
  "Não foi possível conferir a presença agora. Tente de novo ou chame um Mestre ou Admin.";

// Formar equipe, jogar o quiz e trocar recompensa exigem presença registrada
// no encontro (`RF-04-68`, `RN-04-40`, e a decisão do fundador de 2026-09-23
// que estende a exigência ao quiz e à troca). O núcleo também recusa a
// formação sem presença; esta guarda existe para que a criança saiba o que
// falta antes de chegar à tela das equipes.
export function GuardaDePresenca({
  aulaId,
  tokenDoGuerreiro,
  aoRegistrarPresenca,
  aoVoltar,
  children,
}: Props) {
  const [conferencia, definirConferencia] = useState<Conferencia>("conferindo");

  useEffect(() => {
    let ativo = true;
    definirConferencia("conferindo");
    lerMinhaPresenca(aulaId, tokenDoGuerreiro)
      .then((presenca) => {
        if (ativo) definirConferencia(presenca.presente ? "tem" : "naoTem");
      })
      .catch(() => {
        if (ativo) definirConferencia("falhou");
      });
    return () => {
      ativo = false;
    };
  }, [aulaId, tokenDoGuerreiro]);

  if (conferencia === "tem") return <>{children}</>;

  if (conferencia === "conferindo") {
    return (
      <Moldura>
        <Cabecalho titulo="Conferindo a presença…" />
      </Moldura>
    );
  }

  if (conferencia === "falhou") {
    return (
      <Moldura>
        <Cabecalho
          titulo="Não deu para conferir"
          acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
        />
        <Aviso tipo="erro">{MENSAGEM_DE_FALHA}</Aviso>
      </Moldura>
    );
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Registre a presença primeiro"
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />
      <Aviso tipo="atencao">
        Para entrar numa equipe você precisa registrar a presença do dia. É rapidinho: vá no
        caminho Presença, diga o seu nick e olhe para a câmera.
      </Aviso>
      <Botao onClick={aoRegistrarPresenca}>Registrar a presença</Botao>
    </Moldura>
  );
}
