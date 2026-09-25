import { type SessaoAberta, useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Icone, Moldura } from "comum/react";
import { useState } from "react";
import { TelaDeMedicaoDoLimiar } from "../bancada/TelaDeMedicaoDoLimiar";
import { AreaDetalhadaDeDireitos } from "../direitos/AreaDetalhadaDeDireitos";
import { GuardaDePresenca } from "../entrada/GuardaDePresenca";
import { TelaDeEntradaDoGuerreiro } from "../entrada/TelaDeEntradaDoGuerreiro";
import { TelaDeEquipes } from "../equipes/TelaDeEquipes";
import { FilaDePresencaPendente } from "../fila/FilaDePresencaPendente";
import { contarFilaDePresenca } from "../fila/filaDePresenca";
import { useSincronizacaoDaFilaDePresenca } from "../fila/sincronizacao";
import { FluxoDeOnboarding } from "../onboarding/FluxoDeOnboarding";
import { TelaDeCaptura } from "../onboarding/TelaDeCaptura";
import {
  conferirPinNoAparelho,
  FORMATO_DO_PIN,
  MENSAGEM_DE_PIN_BLOQUEADO,
  MENSAGEM_DE_PIN_ERRADO,
  MENSAGEM_DE_PIN_NAO_CADASTRADO,
  MENSAGEM_SEM_VERIFICADOR_NO_APARELHO,
  situacaoDoPinNoAparelho,
} from "../pin/pinDeConfirmacao";
import { CHAVE_DA_PARTIDA_DE_QUIZ, TelaDaPartida } from "../quiz/TelaDaPartida";
import { useEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";
import { TelaDaProgramacao } from "../trilhas/TelaDaProgramacao";
import { TelaDeTroca } from "../troca/TelaDeTroca";

type Caminho =
  | "inicio"
  | "onboarding"
  | "presenca"
  | "equipes"
  | "troca"
  | "quiz"
  | "medicao"
  | "encerramento";

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
  /** Derruba a sessão de trabalho do aparelho, já com o PIN de quem a abriu
   * conferido nesta tela (`RF-04-71`, `RN-04-41`). */
  aoEncerrarSessaoDeTrabalho: () => void;
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
  aoEncerrarSessaoDeTrabalho,
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
  // O PIN da bancada vale para a abertura daquela vez: voltar ao início o
  // devolve ao zero, e a bancada seguinte pede de novo (`RN-04-41`).
  const [pinDaMedicaoConferido, definirPinDaMedicaoConferido] = useState(false);

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
    definirPinDaMedicaoConferido(false);
    sessionStorage.removeItem(CHAVE_DA_PARTIDA_DE_QUIZ);
    aoVoltarAoInicio();
  }

  // Encerrar a sessão de trabalho, já com o PIN conferido: o atendimento em
  // curso sai antes, para que nada dele sobreviva ao encerramento
  // (`RF-04-71`, `RF-04-28`).
  function encerrarSessaoDeTrabalho() {
    sairDoGuerreiro();
    sessionStorage.removeItem(CHAVE_DA_PARTIDA_DE_QUIZ);
    definirCaminho("inicio");
    aoEncerrarSessaoDeTrabalho();
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
    // O PIN vem antes: a medição grava o limiar que decide se o
    // reconhecimento confere neste ponto de apoio, e a sessão de trabalho
    // sozinha não prova que o adulto responsável está aqui. A câmera não chega
    // a ser preparada — a tela da bancada não monta — enquanto ele não
    // conferir (`RF-04-63`, `RF-04-66`, `RN-04-41`, design — decisão 6).
    if (!pinDaMedicaoConferido) {
      return (
        <PedidoDePinDoAparelho
          titulo="Medição do limiar"
          subtitulo="Quem abriu o aparelho confirma com o próprio PIN antes de a bancada abrir."
          rotuloDaAcao="Abrir a bancada de medição"
          aoConferir={() => definirPinDaMedicaoConferido(true)}
          aoVoltar={voltarAoInicio}
        />
      );
    }
    return (
      <TelaDeMedicaoDoLimiar
        alcance="operador"
        tokenDeTrabalho={tokenDeTrabalho}
        aulaId={aulaId}
        aoVoltar={voltarAoInicio}
      />
    );
  }

  // O encerramento da sessão de trabalho, alcançado só daqui: a tela inicial é
  // a que aparece entre um atendimento e o seguinte, e fora dela quem está com
  // o aparelho é uma criança no meio do dela (`RF-04-71`, `RF-04-28`, design —
  // decisão 2).
  if (caminho === "encerramento") {
    const aguardandoNaFila = contarFilaDePresenca(aulaId);
    return (
      <PedidoDePinDoAparelho
        titulo="Encerrar a sessão de trabalho"
        subtitulo="Quem abriu o aparelho confirma com o próprio PIN. Depois de encerrada, a sessão só reabre pelo login Google."
        rotuloDaAcao="Encerrar a sessão de trabalho"
        aviso={aguardandoNaFila > 0 ? avisoDaFilaPendente(aguardandoNaFila) : null}
        fraseDaAlternativa={MENSAGEM_DE_FECHAR_A_ABA}
        aoConferir={encerrarSessaoDeTrabalho}
        aoVoltar={() => definirCaminho("inicio")}
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
      <Cabecalho
        titulo="Comunidade Game — Aula"
        subtitulo="O que você quer fazer?"
        acao={{
          rotulo: "Encerrar a sessão de trabalho",
          aoAcionar: () => definirCaminho("encerramento"),
        }}
      />
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

// A saída que não depende do PIN, e a única que sobra com ele bloqueado: a
// sessão de trabalho vive em `sessionStorage` e não sobrevive ao fechamento da
// aba. Sem esta frase, PIN bloqueado deixaria o aparelho sem saída alguma
// (`RN-04-41`, design — decisão 3).
const MENSAGEM_DE_FECHAR_A_ABA =
  "Fechar a aba do navegador encerra a sessão de trabalho deste aparelho.";

// A fila é anunciada pela contagem, e o aviso diz o que falta para ela entrar
// na aula. Nada se perde: ela fica no aparelho (`RF-04-23`, `RF-04-25`,
// design — decisão 5).
function avisoDaFilaPendente(quantas: number): string {
  const presencas = quantas === 1 ? "1 presença aguarda" : `${quantas} presenças aguardam`;
  return (
    `${presencas} sincronização na fila deste aparelho. A sincronização exige o aparelho ` +
    "aberto nesta mesma aula: a fila continua guardada aqui e entra assim que alguém " +
    "reabrir."
  );
}

interface PropsDoPedidoDePin {
  titulo: string;
  subtitulo: string;
  rotuloDaAcao: string;
  /** O que a tela precisa dizer antes de pedir o PIN — hoje, a fila local de
   * presença pendente no encerramento (`RF-04-71`, `RF-04-23`). */
  aviso?: string | null;
  /** Acrescentada à recusa quando o ato tem alternativa fora do PIN: o
   * encerramento a tem — fechar a aba —, e a bancada não (design — decisão 3). */
  fraseDaAlternativa?: string;
  aoConferir: () => void;
  aoVoltar: () => void;
}

// O pedido do PIN de quem abriu o aparelho, comum ao encerramento da sessão de
// trabalho e à bancada de medição: a mesma conferência no aparelho, o mesmo
// contador de cinco erros e a mesma redação de recusa da confirmação de
// identidade (`RN-04-41`, `RN-04-38`, design — decisão 1). Nenhum dos dois atos
// fala com o núcleo para conferir PIN: a exigência é da tela.
function PedidoDePinDoAparelho({
  titulo,
  subtitulo,
  rotuloDaAcao,
  aviso,
  fraseDaAlternativa,
  aoConferir,
  aoVoltar,
}: PropsDoPedidoDePin) {
  // O PIN vive só neste estado, limpo a cada tentativa, e nunca é gravado no
  // aparelho (`RN-04-38`).
  const [pin, definirPin] = useState("");
  const [emAndamento, definirEmAndamento] = useState(false);
  // Lida ao abrir e atualizada pelo quinto erro: é ela que decide se a tela
  // pede o PIN, passa sem ele ou recusa de saída.
  const [situacao, definirSituacao] = useState(situacaoDoPinNoAparelho);
  const [erro, definirErro] = useState<string | null>(null);

  function comAlternativa(frase: string): string {
    return fraseDaAlternativa ? `${frase} ${fraseDaAlternativa}` : frase;
  }

  async function conferir() {
    definirErro(null);
    const digitado = pin;
    definirPin("");
    definirEmAndamento(true);
    try {
      const desfecho = await conferirPinNoAparelho(digitado);
      if (desfecho === "confere") {
        aoConferir();
        return;
      }
      if (desfecho === "pin_errado") {
        definirErro(MENSAGEM_DE_PIN_ERRADO);
        return;
      }
      // Bloqueado e sem verificador tiram o campo da tela: não há dígito que
      // resolva nenhum dos dois.
      definirSituacao(desfecho);
    } finally {
      definirEmAndamento(false);
    }
  }

  if (situacao === "bloqueado" || situacao === "sem_verificador") {
    return (
      <Moldura>
        <Cabecalho titulo={titulo} acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }} />
        <Aviso tipo="erro">
          {comAlternativa(
            situacao === "bloqueado"
              ? MENSAGEM_DE_PIN_BLOQUEADO
              : MENSAGEM_SEM_VERIFICADOR_NO_APARELHO,
          )}
        </Aviso>
      </Moldura>
    );
  }

  const semPinCadastrado = situacao === "sem_pin_cadastrado";

  return (
    <Moldura>
      <Cabecalho
        titulo={titulo}
        subtitulo={subtitulo}
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />
      {aviso && <Aviso tipo="atencao">{aviso}</Aviso>}
      {semPinCadastrado ? (
        // Sem PIN cadastrado o ato passa, com o aviso que o aparelho já
        // apresenta: trancar a saída e o diagnóstico por uma configuração que
        // se resolve na App 09 deixaria o encontro pior do que está
        // (`RN-04-41`, `RN-04-38`, design — decisão 4).
        <Aviso tipo="atencao">{MENSAGEM_DE_PIN_NAO_CADASTRADO}</Aviso>
      ) : (
        <Campo
          rotulo="PIN de quem abriu o aparelho"
          tipo="password"
          valor={pin}
          aoAlterar={(valor) => definirPin(valor.replace(/\D/g, "").slice(0, 4))}
          focoInicial
        />
      )}
      <Botao
        onClick={semPinCadastrado ? aoConferir : conferir}
        desabilitado={emAndamento || (!semPinCadastrado && !FORMATO_DO_PIN.test(pin))}
      >
        {emAndamento ? "Conferindo…" : rotuloDaAcao}
      </Botao>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
    </Moldura>
  );
}
