import { ProvedorDeSessao, useSessao } from "comum/autenticacao";
import { useEffect, useState } from "react";
import { TelaDeEntrada } from "./autenticacao/TelaDeEntrada";
import { TelaDeTrocaDeSenha } from "./autenticacao/TelaDeTrocaDeSenha";
import { TelaDeVinculados } from "./vinculados/TelaDeVinculados";

const MENSAGEM_DE_RECUSA_DE_OUTRO_PAPEL =
  "Esta área é só para responsáveis. Quem ainda não tem cadastro deve procurar a gestão no " +
  "encontro.";

// A App 07 é inteiramente autenticada: sem sessão, só a entrada aparece, e
// a senha provisória tranca todas as demais telas até a troca, sem caminho
// de contorno (`RF-13-01`, `RF-13-02`, `RN-13-01`, `RN-13-02`).
function Conteudo() {
  const { sessao, restaurando, trocaDeSenhaPendente, sair } = useSessao();
  const [recusadoComoOutroPapel, definirRecusadoComoOutroPapel] = useState(false);

  useEffect(() => {
    if (sessao && sessao.papel !== "responsavel") {
      definirRecusadoComoOutroPapel(true);
      sair();
    }
  }, [sessao, sair]);

  if (restaurando) {
    return null;
  }

  if (recusadoComoOutroPapel) {
    return <TelaDeEntrada mensagemDeRecusa={MENSAGEM_DE_RECUSA_DE_OUTRO_PAPEL} />;
  }

  if (trocaDeSenhaPendente) {
    return <TelaDeTrocaDeSenha />;
  }

  if (!sessao) {
    return <TelaDeEntrada />;
  }

  return <TelaDeVinculados />;
}

function App() {
  return (
    <ProvedorDeSessao>
      <Conteudo />
    </ProvedorDeSessao>
  );
}

export default App;
