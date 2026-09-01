import { ProvedorDeSessao, useSessao } from "comum/autenticacao";
import { useEffect, useState } from "react";
import { TelaDoModoAssistido } from "./assistido/TelaDoModoAssistido";
import { TelaDeEntrada } from "./autenticacao/TelaDeEntrada";
import { TelaDeTrocaDeSenha } from "./autenticacao/TelaDeTrocaDeSenha";
import { ProvedorDeDireitos } from "./direitos/ContextoDeDireitos";
import { TelaDeVinculados } from "./vinculados/TelaDeVinculados";

const MENSAGEM_DE_RECUSA_DE_OUTRO_PAPEL =
  "Esta área é só para responsáveis. Quem ainda não tem cadastro deve procurar a gestão no " +
  "encontro.";

// Responsável usa a área inteira; Admin e Mestre entram só para o modo
// assistido — a única exceção à recusa de qualquer papel que não seja
// responsável (`RF-13-01`, `RF-13-35`, `RN-01-32`).
const PAPEIS_ADMITIDOS = new Set(["responsavel", "admin", "mestre"]);

// A App 07 é inteiramente autenticada: sem sessão, só a entrada aparece, e
// a senha provisória tranca todas as demais telas até a troca, sem caminho
// de contorno (`RF-13-01`, `RF-13-02`, `RN-13-01`, `RN-13-02`).
function Conteudo() {
  const { sessao, restaurando, trocaDeSenhaPendente, sair } = useSessao();
  const [recusadoComoOutroPapel, definirRecusadoComoOutroPapel] = useState(false);
  // Contador, não booleano: cada acionamento do aviso precisa reabrir a
  // transparência mesmo que o vinculado já esteja nela (`RF-13-41`).
  const [pedidoDeTransparencia, definirPedidoDeTransparencia] = useState(0);

  useEffect(() => {
    if (sessao && !PAPEIS_ADMITIDOS.has(sessao.papel)) {
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
    return (
      <ProvedorDeDireitos
        irParaTransparencia={() => definirPedidoDeTransparencia((n) => n + 1)}
      >
        <TelaDeTrocaDeSenha />
      </ProvedorDeDireitos>
    );
  }

  if (!sessao) {
    return <TelaDeEntrada />;
  }

  // Admin e Mestre alcançam só o modo assistido — nada da evolução, das
  // solicitações, da transparência ou do histórico de acessos do
  // vinculado (`RF-13-35`, `RF-13-36`, `RF-13-38`, design — decisão 7).
  if (sessao.papel === "admin" || sessao.papel === "mestre") {
    return <TelaDoModoAssistido />;
  }

  return <TelaDeVinculados pedidoDeTransparencia={pedidoDeTransparencia} />;
}

function App() {
  return (
    <ProvedorDeSessao>
      <Conteudo />
    </ProvedorDeSessao>
  );
}

export default App;
