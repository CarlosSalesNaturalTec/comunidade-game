import { ProvedorDeSessao, useSessao } from "comum/autenticacao";
import { Botao } from "comum/react";
import { useEffect, useState } from "react";
import { TelaDeEntrada } from "./autenticacao/TelaDeEntrada";
import { TelaDeTrocaDeSenha } from "./autenticacao/TelaDeTrocaDeSenha";
import { TelaDeAcompanhamento } from "./desafiosExtras/TelaDeAcompanhamento";
import { TelaDeProposta } from "./desafiosExtras/TelaDeProposta";
import { TelaDeComprobatorios } from "./documentos/TelaDeComprobatorios";
import { TelaDeIdentidadePublica } from "./identidade/TelaDeIdentidadePublica";
import { TelaDePreCadastro } from "./preCadastro/TelaDePreCadastro";

const MENSAGEM_DE_RECUSA_DE_OUTRO_PAPEL =
  "Esta área é só para Apoiadores. Quem ainda não tem cadastro pode pedir participação pelo " +
  "pré-cadastro da vitrine.";

// A App 08 é inteiramente autenticada: sem sessão, nenhuma tela do Apoiador
// aparece — só a porta pública, tela padrão, e a entrada de quem já tem
// cadastro, a um clique dela; a senha provisória tranca todas as demais
// telas até a troca, sem caminho de contorno (`RF-01-02`, `RN-01-32`,
// `RF-14-01`, `RF-14-09`, PRD-14 §4, design — decisão 1).
type Area = "identidade" | "documentos" | "propor" | "acompanhar";
type TelaSemSessao = "porta" | "entrada";

function Conteudo() {
  const { sessao, restaurando, trocaDeSenhaPendente, sair } = useSessao();
  const [recusadoComoOutroPapel, definirRecusadoComoOutroPapel] = useState(false);
  const [area, definirArea] = useState<Area>("propor");
  const [telaSemSessao, definirTelaSemSessao] = useState<TelaSemSessao>("porta");

  useEffect(() => {
    if (sessao && sessao.papel !== "apoiador") {
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
    return telaSemSessao === "entrada" ? (
      <TelaDeEntrada aoVoltar={() => definirTelaSemSessao("porta")} />
    ) : (
      <TelaDePreCadastro aoIrParaEntrada={() => definirTelaSemSessao("entrada")} />
    );
  }

  return (
    <>
      <nav className="cg-navegacao-de-area" aria-label="Áreas do Apoiador">
        <Botao
          variante={area === "identidade" ? "primaria" : "secundaria"}
          onClick={() => definirArea("identidade")}
        >
          Identidade pública
        </Botao>
        <Botao
          variante={area === "documentos" ? "primaria" : "secundaria"}
          onClick={() => definirArea("documentos")}
        >
          Documentos comprobatórios
        </Botao>
        <Botao
          variante={area === "propor" ? "primaria" : "secundaria"}
          onClick={() => definirArea("propor")}
        >
          Propor desafio extra
        </Botao>
        <Botao
          variante={area === "acompanhar" ? "primaria" : "secundaria"}
          onClick={() => definirArea("acompanhar")}
        >
          Meus desafios
        </Botao>
      </nav>
      {area === "identidade" && <TelaDeIdentidadePublica />}
      {area === "documentos" && <TelaDeComprobatorios />}
      {area === "propor" && <TelaDeProposta />}
      {area === "acompanhar" && <TelaDeAcompanhamento />}
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
