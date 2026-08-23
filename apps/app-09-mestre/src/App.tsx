import { ProvedorDeSessao, useSessao } from "comum/autenticacao";
import { Botao } from "comum/react";
import { useEffect, useState } from "react";
import { TelaDeEntrada } from "./autenticacao/TelaDeEntrada";
import { TelaDeAutoria } from "./autoria/TelaDeAutoria";
import { TelaDoBancoDeQuiz } from "./quiz/TelaDoBancoDeQuiz";
import { TelaDeMinhasTurmas } from "./turmas/TelaDeMinhasTurmas";

const MENSAGEM_DE_RECUSA_DO_GUERREIRO =
  "Esta área é só para Mestres. Guerreiros e Guerreiras entram pelo aplicativo delas.";

// A App 09 é inteiramente autenticada: sem sessão, só a entrada aparece, e
// o Guerreiro(a) nunca alcança a autoria — o papel vem do núcleo, não de
// escolha na tela (`RF-01-02`, `RN-01-32`, PRD-09 §4).
type Area = "autoria" | "turmas" | "quiz";

function Conteudo() {
  const { sessao, restaurando, sair } = useSessao();
  const [recusadoComoGuerreiro, definirRecusadoComoGuerreiro] = useState(false);
  const [area, definirArea] = useState<Area>("autoria");

  useEffect(() => {
    if (sessao?.papel === "guerreiro") {
      definirRecusadoComoGuerreiro(true);
      sair();
    }
  }, [sessao, sair]);

  if (restaurando) {
    return null;
  }

  if (recusadoComoGuerreiro) {
    return <TelaDeEntrada mensagemDeRecusa={MENSAGEM_DE_RECUSA_DO_GUERREIRO} />;
  }

  if (!sessao) {
    return <TelaDeEntrada />;
  }

  return (
    <>
      <nav className="cg-navegacao-de-area" aria-label="Áreas do Mestre">
        <Botao
          variante={area === "autoria" ? "primaria" : "secundaria"}
          onClick={() => definirArea("autoria")}
        >
          Minhas trilhas
        </Botao>
        <Botao
          variante={area === "turmas" ? "primaria" : "secundaria"}
          onClick={() => definirArea("turmas")}
        >
          Minhas turmas
        </Botao>
        <Botao
          variante={area === "quiz" ? "primaria" : "secundaria"}
          onClick={() => definirArea("quiz")}
        >
          Banco do Quiz
        </Botao>
      </nav>
      {area === "autoria" && <TelaDeAutoria />}
      {area === "turmas" && <TelaDeMinhasTurmas />}
      {area === "quiz" && <TelaDoBancoDeQuiz />}
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
