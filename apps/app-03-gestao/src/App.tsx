import { ProvedorDeSessao, useSessao } from "comum/autenticacao";
import { useState } from "react";
import { TelaDaAgenda } from "./agenda/TelaDaAgenda";
import { TelaDeEntrada } from "./autenticacao/TelaDeEntrada";
import { TelaDeChaves } from "./chaves/TelaDeChaves";
import { TelaDeComunidades } from "./comunidades/TelaDeComunidades";
import { TelaDeFilas } from "./filas/TelaDeFilas";
import { TelaDoPainelDoDia } from "./painel-do-dia/TelaDoPainelDoDia";
import { TelaDePersonas } from "./personas/TelaDePersonas";
import { TelaDePoderes } from "./poderes/TelaDePoderes";
import { TelaDePontosDeApoio } from "./pontos-de-apoio/TelaDePontosDeApoio";
import { TelaDeQuiz } from "./quiz/TelaDeQuiz";

type Area =
  | "comunidades"
  | "poderes"
  | "pontos-de-apoio"
  | "agenda"
  | "personas"
  | "filas"
  | "chaves"
  | "painel-do-dia"
  | "quiz";

const AREAS: { chave: Area; rotulo: string }[] = [
  { chave: "comunidades", rotulo: "Comunidades" },
  { chave: "poderes", rotulo: "Poderes" },
  { chave: "pontos-de-apoio", rotulo: "Pontos de Apoio" },
  { chave: "agenda", rotulo: "Agenda" },
  { chave: "personas", rotulo: "Personas" },
  { chave: "filas", rotulo: "Filas" },
  { chave: "chaves", rotulo: "Chaves" },
  { chave: "painel-do-dia", rotulo: "Painel do dia" },
  { chave: "quiz", rotulo: "Quiz ao Vivo" },
];

const CHAVES_DE_AREA = new Set<string>(AREAS.map((item) => item.chave));

// O caminho que a App 09 oferece para o painel do dia chega por parâmetro
// de URL, porque a navegação é entre aplicações — cada uma no seu endereço
// próprio, sem estado compartilhado (`RF-09-50`, documento 03 §1).
function areaInicialDaUrl(): Area {
  const area = new URLSearchParams(window.location.search).get("area");
  return area && CHAVES_DE_AREA.has(area) ? (area as Area) : "comunidades";
}

// Sem sessão aberta, só a entrada aparece — nenhum dado de gestão aparece
// antes disso (`RF-01-02`, `RN-01-32`, PRD-02 §4).
function Conteudo() {
  const { sessao, restaurando } = useSessao();
  const [area, definirArea] = useState<Area>(areaInicialDaUrl);

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
      {area === "poderes" && <TelaDePoderes />}
      {area === "pontos-de-apoio" && <TelaDePontosDeApoio />}
      {area === "agenda" && <TelaDaAgenda />}
      {area === "personas" && <TelaDePersonas />}
      {area === "filas" && <TelaDeFilas />}
      {area === "chaves" && <TelaDeChaves />}
      {area === "painel-do-dia" && <TelaDoPainelDoDia />}
      {area === "quiz" && <TelaDeQuiz />}
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
