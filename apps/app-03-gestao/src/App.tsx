import { ProvedorDeSessao, useSessao } from "./autenticacao/ContextoDeSessao";
import { TelaDeEntrada } from "./autenticacao/TelaDeEntrada";
import { TelaDeComunidades } from "./comunidades/TelaDeComunidades";

// Sem sessão aberta, só a entrada aparece — nenhum dado de gestão aparece
// antes disso (`RF-01-02`, `RN-01-32`, PRD-02 §4).
function Conteudo() {
  const { sessao, restaurando } = useSessao();

  if (restaurando) {
    return null;
  }

  if (!sessao) {
    return <TelaDeEntrada />;
  }

  return <TelaDeComunidades />;
}

function App() {
  return (
    <ProvedorDeSessao>
      <Conteudo />
    </ProvedorDeSessao>
  );
}

export default App;
