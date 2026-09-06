import { ProvedorDeSessao, useSessao } from "comum/autenticacao";
import { NavegacaoDeAreas } from "comum/react";
import { useEffect, useState } from "react";
import { TelaDeEntrada } from "./autenticacao/TelaDeEntrada";
import { TelaDeAutoria } from "./autoria/TelaDeAutoria";
import { TelaDeCriacoesAValidar } from "./criacoesOriginais/TelaDeCriacoesAValidar";
import { TelaDeDesafiosExtras } from "./desafiosExtras/TelaDeDesafiosExtras";
import { ProvedorDeDireitos } from "./direitos/ContextoDeDireitos";
import { TelaDeDireitos } from "./direitos/TelaDeDireitos";
import { TelaDoPerfil } from "./perfil/TelaDoPerfil";
import { TelaDePropostas } from "./propostas/TelaDePropostas";
import { TelaDoBancoDeQuiz } from "./quiz/TelaDoBancoDeQuiz";
import { TelaDeRecursos } from "./recursos/TelaDeRecursos";
import { TelaDeResponsaveis } from "./responsaveis/TelaDeResponsaveis";
import { listarSolicitacoesAbertasDeTodasAsComunidades } from "./territorio/api";
import { TelaDeTerritorio } from "./territorio/TelaDeTerritorio";
import { TelaDeDesbloqueiosPendentes } from "./turmas/TelaDeDesbloqueiosPendentes";
import { TelaDeMinhasTurmas } from "./turmas/TelaDeMinhasTurmas";

const MENSAGEM_DE_RECUSA_DO_GUERREIRO =
  "Esta área é só para Mestres. Guerreiros e Guerreiras entram pelo aplicativo delas.";

// A App 09 é inteiramente autenticada: sem sessão, só a entrada aparece, e
// o Guerreiro(a) nunca alcança a autoria — o papel vem do núcleo, não de
// escolha na tela (`RF-01-02`, `RN-01-32`, PRD-09 §4).
type Area =
  | "autoria"
  | "turmas"
  | "quiz"
  | "desbloqueios"
  | "criacoes"
  | "territorio"
  | "desafiosExtras"
  | "propostas"
  | "recursos"
  | "responsaveis"
  | "perfil"
  | "direitos";

function Conteudo() {
  const { sessao, restaurando, sair } = useSessao();
  const [recusadoComoGuerreiro, definirRecusadoComoGuerreiro] = useState(false);
  const [area, definirArea] = useState<Area>("autoria");
  const [contagemDeSolicitacoes, definirContagemDeSolicitacoes] = useState(0);

  useEffect(() => {
    if (sessao?.papel === "guerreiro") {
      definirRecusadoComoGuerreiro(true);
      sair();
    }
  }, [sessao, sair]);

  // O alerta fica fora da área de território, para o Mestre saber que há
  // pedido parado sem precisar entrar nela; refeito a cada troca de área,
  // inclusive ao sair do território depois de avaliar (`RF-09-54`).
  // biome-ignore lint/correctness/useExhaustiveDependencies: `area` dispara a releitura de propósito, não é lida no corpo
  useEffect(() => {
    if (!sessao) return;
    let cancelado = false;
    listarSolicitacoesAbertasDeTodasAsComunidades(sessao.token)
      .then((grupos) => {
        if (cancelado) return;
        const total = grupos.reduce((soma, grupo) => soma + grupo.solicitacoes.length, 0);
        definirContagemDeSolicitacoes(total);
      })
      .catch(() => {});
    return () => {
      cancelado = true;
    };
  }, [sessao, area]);

  if (restaurando) {
    return null;
  }

  if (recusadoComoGuerreiro) {
    return <TelaDeEntrada mensagemDeRecusa={MENSAGEM_DE_RECUSA_DO_GUERREIRO} />;
  }

  if (!sessao) {
    return <TelaDeEntrada />;
  }

  const areas = [
    { chave: "autoria", rotulo: "Minhas trilhas" },
    { chave: "turmas", rotulo: "Minhas turmas" },
    { chave: "quiz", rotulo: "Banco do Quiz" },
    { chave: "desbloqueios", rotulo: "Desafios a julgar" },
    { chave: "criacoes", rotulo: "Criações a validar" },
    {
      chave: "territorio",
      rotulo: "Território",
      conteudoExtra: contagemDeSolicitacoes > 0 && (
        <span className="cg-navegacao-de-areas__alerta">
          {" "}
          ({contagemDeSolicitacoes} solicitação(ões) de novo local em aberto)
        </span>
      ),
    },
    { chave: "desafiosExtras", rotulo: "Desafios extras" },
    { chave: "propostas", rotulo: "Propostas" },
    { chave: "recursos", rotulo: "Recursos" },
    { chave: "responsaveis", rotulo: "Responsáveis" },
    { chave: "perfil", rotulo: "Meu perfil" },
    { chave: "direitos", rotulo: "Direitos e dados" },
  ];

  return (
    <ProvedorDeDireitos irParaDireitos={() => definirArea("direitos")}>
      <NavegacaoDeAreas
        rotulo="Áreas do Mestre"
        areas={areas}
        areaAtual={area}
        aoSelecionarArea={(chave) => definirArea(chave as Area)}
        aoSair={sair}
      />
      {area === "autoria" && <TelaDeAutoria />}
      {area === "turmas" && <TelaDeMinhasTurmas />}
      {area === "quiz" && <TelaDoBancoDeQuiz />}
      {area === "desbloqueios" && <TelaDeDesbloqueiosPendentes />}
      {area === "criacoes" && <TelaDeCriacoesAValidar />}
      {area === "territorio" && (
        <TelaDeTerritorio onContagemAtualizada={definirContagemDeSolicitacoes} />
      )}
      {area === "desafiosExtras" && <TelaDeDesafiosExtras />}
      {area === "propostas" && <TelaDePropostas />}
      {area === "recursos" && <TelaDeRecursos />}
      {area === "responsaveis" && <TelaDeResponsaveis />}
      {area === "perfil" && <TelaDoPerfil />}
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
