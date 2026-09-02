import { ProvedorDeSessao, useSessao } from "comum/autenticacao";
import { Botao } from "comum/react";
import { useEffect, useState } from "react";
import { TelaDeAcompanhamento as TelaDePainelEFavoritos } from "./acompanhamento/TelaDeAcompanhamento";
import { TelaDeDeclaracaoDeAporte } from "./aportes/TelaDeDeclaracaoDeAporte";
import { TelaDeMeusAportes } from "./aportes/TelaDeMeusAportes";
import { TelaDeNecessidadesEmAberto } from "./aportes/TelaDeNecessidadesEmAberto";
import { TelaDeSituacaoDasDeclaracoes } from "./aportes/TelaDeSituacaoDasDeclaracoes";
import { TelaDeEntrada } from "./autenticacao/TelaDeEntrada";
import { TelaDeTrocaDeSenha } from "./autenticacao/TelaDeTrocaDeSenha";
import { TelaDeAcompanhamento } from "./desafiosExtras/TelaDeAcompanhamento";
import { TelaDeProposta } from "./desafiosExtras/TelaDeProposta";
import { ProvedorDeDireitos } from "./direitos/ContextoDeDireitos";
import { TelaDeDireitos } from "./direitos/TelaDeDireitos";
import { TelaDeComprobatorios } from "./documentos/TelaDeComprobatorios";
import { TelaDeEfetividade } from "./efetividade/TelaDeEfetividade";
import { TelaDeIdentidadePublica } from "./identidade/TelaDeIdentidadePublica";
import { TelaDeMissoes } from "./missoes/TelaDeMissoes";
import { TelaDePreCadastro } from "./preCadastro/TelaDePreCadastro";
import { TelaDePropostas } from "./propostas/TelaDePropostas";
import { TelaDeSustento } from "./sustento/TelaDeSustento";

const MENSAGEM_DE_RECUSA_DE_OUTRO_PAPEL =
  "Esta área é só para Apoiadores. Quem ainda não tem cadastro pode pedir participação pelo " +
  "pré-cadastro da vitrine.";

// A App 08 é inteiramente autenticada: sem sessão, nenhuma tela do Apoiador
// aparece — só a porta pública, tela padrão, e a entrada de quem já tem
// cadastro, a um clique dela; a senha provisória tranca todas as demais
// telas até a troca, sem caminho de contorno (`RF-01-02`, `RN-01-32`,
// `RF-14-01`, `RF-14-09`, PRD-14 §4, design — decisão 1).
type Area =
  | "identidade"
  | "documentos"
  | "propor"
  | "acompanhar"
  | "efetividade"
  | "meus-aportes"
  | "necessidades"
  | "missoes"
  | "sustento"
  | "declarar-aporte"
  | "situacao-de-declaracoes"
  | "painel-e-favoritos"
  | "propostas"
  | "direitos";
type TelaSemSessao = "porta" | "entrada" | "direitos";

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
    return (
      <ProvedorDeDireitos irParaDireitos={() => {}}>
        <TelaDeTrocaDeSenha />
      </ProvedorDeDireitos>
    );
  }

  if (!sessao) {
    return (
      <ProvedorDeDireitos irParaDireitos={() => definirTelaSemSessao("direitos")}>
        {telaSemSessao === "direitos" ? (
          <TelaDeDireitos aoVoltar={() => definirTelaSemSessao("porta")} />
        ) : telaSemSessao === "entrada" ? (
          <TelaDeEntrada aoVoltar={() => definirTelaSemSessao("porta")} />
        ) : (
          <TelaDePreCadastro aoIrParaEntrada={() => definirTelaSemSessao("entrada")} />
        )}
      </ProvedorDeDireitos>
    );
  }

  return (
    <ProvedorDeDireitos irParaDireitos={() => definirArea("direitos")}>
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
        <Botao
          variante={area === "efetividade" ? "primaria" : "secundaria"}
          onClick={() => definirArea("efetividade")}
        >
          Efetividade
        </Botao>
        <Botao
          variante={area === "meus-aportes" ? "primaria" : "secundaria"}
          onClick={() => definirArea("meus-aportes")}
        >
          Meus aportes
        </Botao>
        <Botao
          variante={area === "necessidades" ? "primaria" : "secundaria"}
          onClick={() => definirArea("necessidades")}
        >
          Necessidades em aberto
        </Botao>
        <Botao
          variante={area === "missoes" ? "primaria" : "secundaria"}
          onClick={() => definirArea("missoes")}
        >
          Missões
        </Botao>
        <Botao
          variante={area === "sustento" ? "primaria" : "secundaria"}
          onClick={() => definirArea("sustento")}
        >
          Sustento
        </Botao>
        <Botao
          variante={area === "declarar-aporte" ? "primaria" : "secundaria"}
          onClick={() => definirArea("declarar-aporte")}
        >
          Declarar aporte
        </Botao>
        <Botao
          variante={area === "situacao-de-declaracoes" ? "primaria" : "secundaria"}
          onClick={() => definirArea("situacao-de-declaracoes")}
        >
          Situação das declarações
        </Botao>
        <Botao
          variante={area === "painel-e-favoritos" ? "primaria" : "secundaria"}
          onClick={() => definirArea("painel-e-favoritos")}
        >
          Acompanhamento
        </Botao>
        <Botao
          variante={area === "propostas" ? "primaria" : "secundaria"}
          onClick={() => definirArea("propostas")}
        >
          Propostas
        </Botao>
        <Botao
          variante={area === "direitos" ? "primaria" : "secundaria"}
          onClick={() => definirArea("direitos")}
        >
          Direitos e dados
        </Botao>
      </nav>
      {area === "identidade" && <TelaDeIdentidadePublica />}
      {area === "documentos" && <TelaDeComprobatorios />}
      {area === "propor" && <TelaDeProposta />}
      {area === "acompanhar" && <TelaDeAcompanhamento />}
      {area === "efetividade" && <TelaDeEfetividade />}
      {area === "meus-aportes" && <TelaDeMeusAportes />}
      {area === "necessidades" && <TelaDeNecessidadesEmAberto />}
      {area === "missoes" && <TelaDeMissoes />}
      {area === "sustento" && <TelaDeSustento />}
      {area === "declarar-aporte" && <TelaDeDeclaracaoDeAporte />}
      {area === "situacao-de-declaracoes" && <TelaDeSituacaoDasDeclaracoes />}
      {area === "painel-e-favoritos" && <TelaDePainelEFavoritos />}
      {area === "propostas" && <TelaDePropostas />}
      {area === "direitos" && <TelaDeDireitos />}
    </ProvedorDeDireitos>
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
