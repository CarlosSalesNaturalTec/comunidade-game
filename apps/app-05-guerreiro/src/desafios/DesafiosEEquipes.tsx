import { Botao } from "comum/react";
import { useState } from "react";
import { MeusDesafios } from "./MeusDesafios";
import { MinhasEquipes } from "./MinhasEquipes";

type Tela = "desafios" | "equipes";

const ABAS: { tela: Tela; rotulo: string }[] = [
  { tela: "desafios", rotulo: "Desafios" },
  { tela: "equipes", rotulo: "Minhas equipes" },
];

// O bloco dos desafios em aberto e das equipes de que participa, na Área
// do Guerreiro(a) — duas telas de leitura, no molde da `Carteira`
// (`RF-05-19`, `RF-05-22`, design — decisão 6).
export function DesafiosEEquipes() {
  const [tela, definirTela] = useState<Tela>("desafios");

  return (
    <div className="cg-desafios-e-equipes">
      <nav className="cg-desafios-e-equipes__abas" aria-label="Desafios e equipes">
        {ABAS.map((aba) => (
          <Botao
            key={aba.tela}
            variante={tela === aba.tela ? "primaria" : "secundaria"}
            onClick={() => definirTela(aba.tela)}
          >
            {aba.rotulo}
          </Botao>
        ))}
      </nav>

      {tela === "desafios" && <MeusDesafios />}
      {tela === "equipes" && <MinhasEquipes />}
    </div>
  );
}
