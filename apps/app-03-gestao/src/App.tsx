import { useState } from "react";
import { TelaDaAgenda } from "./agenda/TelaDaAgenda";
import { ProvedorDeSessao, useSessao } from "./autenticacao/ContextoDeSessao";
import { TelaDeEntrada } from "./autenticacao/TelaDeEntrada";
import { TelaDeChaves } from "./chaves/TelaDeChaves";
import { TelaDeComunidades } from "./comunidades/TelaDeComunidades";
import { TelaDeFilas } from "./filas/TelaDeFilas";
import { TelaDePersonas } from "./personas/TelaDePersonas";
import { TelaDePontosDeApoio } from "./pontos-de-apoio/TelaDePontosDeApoio";

type Area = "comunidades" | "pontos-de-apoio" | "agenda" | "personas" | "filas" | "chaves";

const AREAS: { chave: Area; rotulo: string }[] = [
  { chave: "comunidades", rotulo: "Comunidades" },
  { chave: "pontos-de-apoio", rotulo: "Pontos de Apoio" },
  { chave: "agenda", rotulo: "Agenda" },
  { chave: "personas", rotulo: "Personas" },
  { chave: "filas", rotulo: "Filas" },
  { chave: "chaves", rotulo: "Chaves" },
];

// Sem sessão aberta, só a entrada aparece — nenhum dado de gestão aparece
// antes disso (`RF-01-02`, `RN-01-32`, PRD-02 §4).
function Conteudo() {
  const { sessao, restaurando } = useSessao();
  const [area, definirArea] = useState<Area>("comunidades");

  if (restaurando) {
    return null;
  }

  if (!sessao) {
    return <TelaDeEntrada />;
  }

  return (
    <>
      <nav className="cg-navegacao" aria-label="Áreas da gestão">
        {AREAS.map((item) => (
          <button
            key={item.chave}
            type="button"
            className="cg-navegacao__item"
            aria-current={area === item.chave || undefined}
            onClick={() => definirArea(item.chave)}
          >
            {item.rotulo}
          </button>
        ))}
      </nav>

      {area === "comunidades" && <TelaDeComunidades />}
      {area === "pontos-de-apoio" && <TelaDePontosDeApoio />}
      {area === "agenda" && <TelaDaAgenda />}
      {area === "personas" && <TelaDePersonas />}
      {area === "filas" && <TelaDeFilas />}
      {area === "chaves" && <TelaDeChaves />}
    </>
  );
}

function App() {
  return (
    <ProvedorDeSessao>
      <Conteudo />
    </ProvedorDeSessao>
  );
}

export default App;
