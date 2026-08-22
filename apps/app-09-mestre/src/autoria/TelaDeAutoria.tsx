import { useSessao } from "comum/autenticacao";
import { Cabecalho, Moldura } from "comum/react";

// Esqueleto da área autenticada — a autoria de trilha, missão e atividade
// entra na fatia seguinte (PRD-09 §6.1).
export function TelaDeAutoria() {
  const { sair } = useSessao();

  return (
    <Moldura>
      <Cabecalho
        titulo="Comunidade Game — Mestre"
        acao={{ rotulo: "Sair", aoAcionar: sair }}
      />
    </Moldura>
  );
}
