import { type SessaoAberta, useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Icone, Moldura } from "comum/react";
import { useState } from "react";
import { TelaDeMedicaoDoLimiar } from "../bancada/TelaDeMedicaoDoLimiar";
import { AreaDetalhadaDeDireitos } from "../direitos/AreaDetalhadaDeDireitos";
import { GuardaDePresenca } from "../entrada/GuardaDePresenca";
import { TelaDeEntradaDoGuerreiro } from "../entrada/TelaDeEntradaDoGuerreiro";
import { TelaDeEquipes } from "../equipes/TelaDeEquipes";
import { FilaDePresencaPendente } from "../fila/FilaDePresencaPendente";
import { useSincronizacaoDaFilaDePresenca } from "../fila/sincronizacao";
import { FluxoDeOnboarding } from "../onboarding/FluxoDeOnboarding";
import { TelaDeCaptura } from "../onboarding/TelaDeCaptura";
import { CHAVE_DA_PARTIDA_DE_QUIZ, TelaDaPartida } from "../quiz/TelaDaPartida";
import { useEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";
import { TelaDaProgramacao } from "../trilhas/TelaDaProgramacao";
import { TelaDeTroca } from "../troca/TelaDeTroca";

type Caminho = "inicio" | "onboarding" | "presenca" | "equipes" | "troca" | "quiz" | "medicao";

interface Props {
  tokenDeTrabalho: string;
  personaIdDeTrabalho: string;
  /** Só o Mestre, na sessão de trabalho, homologa a equipe da trilha ali
   * mesmo (`RF-04-62`, `RN-04-18`). */
  papelDeTrabalho: string;
  aulaId: string;
  /** Relê `GET /v1/aulas/vigentes`, para que a janela da aula seja
   * conferida a cada volta ao início (`RF-04-05`, design — decisão 3). */
  aoVoltarAoInicio: () => void;
  /** Só o Mestre da sessão de trabalho abre e fecha o momento de troca
   * (`RF-04-49`, decisão do fundador de 2026-08-25). */
  podeAbrirMomentoDeTroca: boolean;
  momentoDeTrocaAberto: boolean;
  abrindoMomentoDeTroca: boolean;
  erroDeAberturaDaTroca: string | null;
  aoAbrirMomentoDeTroca: () => void;
  aoFecharMomentoDeTroca: () => void;
}

// Os três caminhos do PRD-04 §6.1 — onboarding, presença e equipes. A
// presença termina no registro e volta ao início; as equipes abrem por nick
// e imagem ou PIN, sem registrar presença, e só para quem já a tem
// (`RF-04-01`, `RF-04-67`, `RF-04-68`).
//
// Cada caminho leva o glifo da camada comum ao lado do rótulo que já tem —
// nunca no lugar dele: é o que a criança reconhece antes de ler a frase
// inteira, e o rótulo segue sendo o nome acessível do botão (documento 15
// §§5, 11.1, decisão do fundador de 2026-09-25).
export function TelaInicial({
  tokenDeTrabalho,
  personaIdDeTrabalho,
  papelDeTrabalho,
  aulaId,
  aoVoltarAoInicio,
  podeAbrirMomentoDeTroca,
  momentoDeTrocaAberto,
  abrindoMomentoDeTroca,
  erroDeAberturaDaTroca,
  aoAbrirMomentoDeTroca,
  aoFecharMomentoDeTroca,
}: Props) {
  const { sessao: sessaoDoGuerreiro, sair: sairDoGuerreiro } = useSessao();
  const { semRede } = useEstadoDeRede();
  const { itens: itensDaFila, tentarDeNovo } = useSincronizacaoDaFilaDePresenca(
    aulaId,
    tokenDeTrabalho,
  );
  const [caminho, definirCaminho] = useState<Caminho>("inicio");
  // Só a sessão aberta por confirmação presencial autoriza o recadastro da
  // imagem — nunca a de reconhecimento, que já provou que a imagem serve
  // (`RF-04-22`, design — decisão 4).
  const [viaDeEntrada, definirViaDeEntrada] = useState<
    "reconhecimento" | "confirmacao" | null
  >(null);
  const [mostrarRecadastro, definirMostrarRecadastro] = useState(false);
  // A equipe escolhida no caminho das trilhas — estado deste aparelho, que
  // morre com a volta ao início, nunca gravado no núcleo (`RF-04-35`,
  // documento 02 §5).
  const [equipeEscolhidaId, definirEquipeEscolhidaId] = useState<string | null>(null);
  // Alcançável do aviso discreto, de qualquer estado de rede — é texto da
  // própria aplicação, sem chamada ao núcleo (`RF-04-26`, design — decisão
  // 10).
  const [mostrarDireitos, definirMostrarDireitos] = useState(false);

  // Fim de cada atendimento: a sessão do Guerreiro(a) é limpa e a tela
  // volta ao início, sem dado do atendimento anterior (`RF-04-28`, design
  // — decisão 2). O desmonte da tela de cadastro, sozinho, já descarta o
  // que ela tinha em estado.
  function voltarAoInicio() {
    sairDoGuerreiro();
    definirCaminho("inicio");
    definirViaDeEntrada(null);
    definirMostrarRecadastro(false);
    definirEquipeEscolhidaId(null);
    sessionStorage.removeItem(CHAVE_DA_PARTIDA_DE_QUIZ);
    aoVoltarAoInicio();
  }

  // Recusado o caminho por falta de presença, a sessão aberta aqui não
  // sobrevive ao encaminhamento: o atendimento seguinte começa limpo
  // (`RF-04-67`, `RF-04-28`).
  function irRegistrarPresenca() {
    sairDoGuerreiro();
    definirViaDeEntrada(null);
    definirEquipeEscolhidaId(null);
    definirMostrarRecadastro(false);
    definirCaminho("presenca");
  }

  // As telas do caminho, já com a sessão do Guerreiro(a) aberta e a
  // presença conferida pela guarda.
  function conteudoDoCaminho(sessaoDoGuerreiro: SessaoAberta) {
    if (caminho === "troca") {
      return (
        <TelaDeTroca
          tokenDeTrabalho={tokenDeTrabalho}
          aulaId={aulaId}
          tokenDoGuerreiro={sessaoDoGuerreiro.token}
          guerreiroId={sessaoDoGuerreiro.persona_id}
          aoConcluir={voltarAoInicio}
          aoVoltar={voltarAoInicio}
        />
      );
    }
    if (caminho === "quiz") {
      return (
        <TelaDaPartida
          aulaId={aulaId}
          tokenDoGuerreiro={sessaoDoGuerreiro.token}
          aoVoltar={voltarAoInicio}
        />
      );
    }
    if (mostrarRecadastro) {
      return (
        <TelaDeCaptura
          tokenDeTrabalho={tokenDeTrabalho}
          guerreiroId={sessaoDoGuerreiro.persona_id}
          aoConcluir={() => definirMostrarRecadastro(false)}
          aoVoltar={() => definirMostrarRecadastro(false)}
        />
      );
    }
    if (equipeEscolhidaId) {
      return (
        <TelaDaProgramacao
          equipeId={equipeEscolhidaId}
          token={sessaoDoGuerreiro.token}
          aoVoltar={() => definirEquipeEscolhidaId(null)}
          podeHomologarEquipeDaTrilha={papelDeTrabalho === "mestre"}
          tokenDeTrabalho={tokenDeTrabalho}
        />
      );
    }
    return (
      <TelaDeEquipes
        aulaId={aulaId}
        token={sessaoDoGuerreiro.token}
        aoVoltar={voltarAoInicio}
        podeRecadastrarImagem={viaDeEntrada === "confirmacao"}
        aoRecadastrarImagem={() => definirMostrarRecadastro(true)}
        aoEscolherEquipe={definirEquipeEscolhidaId}
      />
    );
  }

  if (mostrarDireitos) {
    return <AreaDetalhadaDeDireitos aoVoltar={() => definirMostrarDireitos(false)} />;
  }

  if (caminho === "onboarding") {
    // Sem rede não há como abrir o cadastro: nenhum campo é sequer
    // oferecido, e nenhum dado chega a ser coletado (`RF-04-24`,
    // `RN-04-12`).
    if (semRede) {
      return (
        <Moldura>
          <Cabecalho
            titulo="Onboarding indisponível sem rede"
            acao={{ rotulo: "Voltar", aoAcionar: voltarAoInicio }}
          />
          <Aviso tipo="atencao">
            O cadastro de um novo Guerreiro(a) exige rede. Nenhum dado foi coletado — assim que
            a rede voltar, tente de novo.
          </Aviso>
        </Moldura>
      );
    }
    return (
      <FluxoDeOnboarding
        tokenDeTrabalho={tokenDeTrabalho}
        personaIdDeTrabalho={personaIdDeTrabalho}
        aulaId={aulaId}
        aoConcluir={voltarAoInicio}
        aoVoltar={voltarAoInicio}
      />
    );
  }

  // O caminho do diagnóstico: alcança só quem opera, porque fora do
  // onboarding a aplicação não tem como saber que existe termo assinado de
  // um Guerreiro(a) (`RN-04-33`, design — decisão 3).
  if (caminho === "medicao") {
    return (
      <TelaDeMedicaoDoLimiar
        alcance="operador"
        tokenDeTrabalho={tokenDeTrabalho}
        aulaId={aulaId}
        aoVoltar={voltarAoInicio}
      />
    );
  }

  // O caminho Presença começa e termina na entrada: registrada a presença, a
  // própria tela avisa e volta ao início (`RF-04-67`).
  if (caminho === "presenca") {
    return (
      <TelaDeEntradaDoGuerreiro
        tokenDeTrabalho={tokenDeTrabalho}
        aulaId={aulaId}
        caminho="presenca"
        aoVoltar={voltarAoInicio}
        aoAbrirSessao={definirViaDeEntrada}
      />
    );
  }

  if (caminho === "equipes" || caminho === "troca" || caminho === "quiz") {
    if (!sessaoDoGuerreiro) {
      return (
        <TelaDeEntradaDoGuerreiro
          tokenDeTrabalho={tokenDeTrabalho}
          aulaId={aulaId}
          caminho={caminho}
          aoVoltar={voltarAoInicio}
          aoAbrirSessao={definirViaDeEntrada}
        />
      );
    }
    // A guarda confere a presença assim que a sessão abre e, faltando,
    // não deixa chegar às telas do caminho (`RF-04-68`, `RN-04-40`).
    return (
      <GuardaDePresenca
        aulaId={aulaId}
        tokenDoGuerreiro={sessaoDoGuerreiro.token}
        aoRegistrarPresenca={irRegistrarPresenca}
        aoVoltar={voltarAoInicio}
      >
        {conteudoDoCaminho(sessaoDoGuerreiro)}
      </GuardaDePresenca>
    );
  }

  return (
    <Moldura>
      <Cabecalho titulo="Comunidade Game — Aula" subtitulo="O que você quer fazer?" />
      <div className="cg-caminhos">
        <button
          type="button"
          className="cg-caminho"
          onClick={() => definirCaminho("onboarding")}
        >
          <Icone glifo="onboarding" />
          Onboarding — cadastro do Guerreiro(a) e presença do dia
        </button>
        <button
          type="button"
          className="cg-caminho"
          onClick={() => definirCaminho("presenca")}
        >
          <Icone glifo="presenca" />
          Presença — entrar com o nick e registrar a presença de hoje
        </button>
        <button type="button" className="cg-caminho" onClick={() => definirCaminho("equipes")}>
          <Icone glifo="equipes" />
          Equipes — formar a equipe e trabalhar a trilha
        </button>
        <button type="button" className="cg-caminho" onClick={() => definirCaminho("quiz")}>
          <Icone glifo="quiz" />
          Quiz ao Vivo — entrar com o nick e responder pela equipe
        </button>
        <button type="button" className="cg-caminho" onClick={() => definirCaminho("medicao")}>
          <Icone glifo="medicao" />
          Medição do limiar — calibrar o reconhecimento facial deste ponto de apoio
        </button>
        {momentoDeTrocaAberto && (
          <button type="button" className="cg-caminho" onClick={() => definirCaminho("troca")}>
            <Icone glifo="troca" />
            Troca por recompensa avulsa — entregar uma recompensa do encontro
          </button>
        )}
      </div>
      {podeAbrirMomentoDeTroca && (
        <div className="cg-momento-de-troca">
          <Botao
            variante="secundaria"
            onClick={momentoDeTrocaAberto ? aoFecharMomentoDeTroca : aoAbrirMomentoDeTroca}
            desabilitado={abrindoMomentoDeTroca}
          >
            {momentoDeTrocaAberto
              ? "Fechar o momento de troca"
              : abrindoMomentoDeTroca
                ? "Abrindo…"
                : "Abrir o momento de troca"}
          </Botao>
          {erroDeAberturaDaTroca && <Aviso tipo="erro">{erroDeAberturaDaTroca}</Aviso>}
        </div>
      )}
      {(papelDeTrabalho === "mestre" || papelDeTrabalho === "admin") && (
        <FilaDePresencaPendente itens={itensDaFila} aoTentarDeNovo={tentarDeNovo} />
      )}
      <p className="cg-aviso-de-coleta">
        A gente guarda alguns dados para o encontro funcionar.{" "}
        <button type="button" className="cg-link" onClick={() => definirMostrarDireitos(true)}>
          Veja o que a gente coleta e para quê
        </button>
        .
      </p>
    </Moldura>
  );
}
