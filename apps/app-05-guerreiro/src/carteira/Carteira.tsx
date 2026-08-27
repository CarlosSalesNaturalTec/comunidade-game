import { Botao } from "comum/react";
import { useState } from "react";
import { CatalogoAvulso } from "./CatalogoAvulso";
import { Conquistas } from "./Conquistas";
import { MinhaCarteira } from "./MinhaCarteira";
import { Portfolio } from "./Portfolio";
import { RankingDaTurma } from "./RankingDaTurma";

type Tela = "carteira" | "catalogo" | "conquistas" | "ranking" | "portfolio";

const ABAS: { tela: Tela; rotulo: string }[] = [
  { tela: "carteira", rotulo: "Carteira" },
  { tela: "catalogo", rotulo: "Catálogo" },
  { tela: "conquistas", rotulo: "Conquistas" },
  { tela: "ranking", rotulo: "Ranking" },
  { tela: "portfolio", rotulo: "Portfólio" },
];

// O bloco da carteira, catálogo, conquistas, ranking e portfólio na Área
// do Guerreiro(a) — cinco telas, todas de leitura à entrada, sem sondagem
// periódica (`RF-05-45`, `RF-05-52`, `RF-05-82`, `RF-05-83`, `RF-05-43`,
// `RF-05-44`, proposal — What Changes).
export function Carteira() {
  const [tela, definirTela] = useState<Tela>("carteira");

  return (
    <div className="cg-carteira">
      <nav className="cg-carteira__abas" aria-label="Minhas conquistas">
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

      {tela === "carteira" && <MinhaCarteira />}
      {tela === "catalogo" && <CatalogoAvulso />}
      {tela === "conquistas" && <Conquistas />}
      {tela === "ranking" && <RankingDaTurma />}
      {tela === "portfolio" && <Portfolio />}
    </div>
  );
}
