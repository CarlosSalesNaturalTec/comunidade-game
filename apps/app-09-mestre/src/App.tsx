import { ProvedorDeSessao, useSessao } from "comum/autenticacao";
import { useEffect, useState } from "react";
import { TelaDeEntrada } from "./autenticacao/TelaDeEntrada";
import { TelaDeAutoria } from "./autoria/TelaDeAutoria";

const MENSAGEM_DE_RECUSA_DO_GUERREIRO =
  "Esta área é só para Mestres. Guerreiros e Guerreiras entram pelo aplicativo delas.";

// A App 09 é inteiramente autenticada: sem sessão, só a entrada aparece, e
// o Guerreiro(a) nunca alcança a autoria — o papel vem do núcleo, não de
// escolha na tela (`RF-01-02`, `RN-01-32`, PRD-09 §4).
function Conteudo() {
  const { sessao, restaurando, sair } = useSessao();
  const [recusadoComoGuerreiro, definirRecusadoComoGuerreiro] = useState(false);

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

  return <TelaDeAutoria />;
}

function App() {
  return (
    <ProvedorDeSessao>
      <Conteudo />
    </ProvedorDeSessao>
  );
}

export default App;
