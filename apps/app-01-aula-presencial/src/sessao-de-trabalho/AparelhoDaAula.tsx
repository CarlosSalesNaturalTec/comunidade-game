import { ErroDaApi } from "comum/api";
import { ProvedorDeSessao, useSessao } from "comum/autenticacao";
import { andamentoDosModelos, precarregarModelos } from "comum/biometria";
import { useNarracao, useNarrarAoEntrar } from "comum/narracao";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useRef, useState } from "react";
import { type AulaVigente, listarAulasVigentes } from "../api/aulas";
import { listarCatalogoAvulso } from "../api/catalogoAvulso";
import { buscarNomeDaComunidade } from "../api/comunidades";
import { TelaInicial } from "../inicio/TelaInicial";
import {
  apagarEstadoDoPin,
  buscarVerificadorDoPin,
  estadoDoPinDe,
  guardarVerificadorDoPin,
} from "../pin/pinDeConfirmacao";
import { ProvedorDeEstadoDeRede, useEstadoDeRede } from "./EstadoDeRede";
import { TelaDeEntradaDeTrabalho } from "./TelaDeEntradaDeTrabalho";

// A sessão do Guerreiro(a) — um atendimento, não a aula inteira — vive
// aninhada dentro da sessão de trabalho, cada uma na própria chave de
// `sessionStorage` (design — decisão 1).
const CHAVE_DE_SESSAO_DO_GUERREIRO = "app-01:sessao-guerreiro";
const CHAVE_DA_AULA_ESCOLHIDA = "app-01:sessao-trabalho:aula";

const MENSAGEM_DE_RECUSA_DO_GUERREIRO =
  "Esta tela é para abrir o aparelho — só Mestre ou Admin. Guerreiros e Guerreiras entram na tela seguinte, pelo nick.";

const MENSAGEM_DE_TROCA_SEM_REDE =
  "A troca exige rede. Verifique a conexão do aparelho e tente abrir de novo.";

const MENSAGEM_DE_FALHA_DA_PRECARGA =
  "Não foi possível carregar os modelos de reconhecimento facial.";

// A biblioteca não informa bytes: o andamento só se lê perguntando quantos
// modelos já carregaram. Daí a leitura periódica, e daí o andamento ser de
// cinco passos (`RF-04-75`, design — decisão 5).
const ESPERA_ENTRE_LEITURAS_DO_ANDAMENTO_MS = 300;

interface OpcaoDeComunidade {
  aula: AulaVigente;
  nomeDaComunidade: string;
}

export function AparelhoDaAula() {
  return (
    <ProvedorDeEstadoDeRede>
      <ConviteParaIniciarANarracao />
      <AvisoDeOperacaoSemConexao />
      <PrecargaDosModelos />
      <ConteudoDoAparelho />
    </ProvedorDeEstadoDeRede>
  );
}

// O navegador não fala antes de um gesto da pessoa: este é o gesto. Aparece
// depois de carregada e antes da primeira fala, em qualquer tela, e sai da
// tela assim que a narração está armada. Com a narração **desligada** não há
// o que armar, e sem síntese no navegador não há o que oferecer — nos dois
// casos ele não é apresentado, e nenhum erro é anunciado (documento 15 §5.1,
// design — decisão 6).
function ConviteParaIniciarANarracao() {
  const { ligada, armada, disponivel, armarNarracao } = useNarracao();
  if (!ligada || armada || !disponivel) return null;
  return (
    <div className="cg-narracao-convite">
      <Botao variante="secundaria" onClick={armarNarracao}>
        Iniciar a narração das telas
      </Botao>
    </div>
  );
}

// Os cinco modelos da biometria somam ~10 MB e, sem isto, seriam buscados na
// **primeira criança diante da câmera**, com a turma entrando pela porta. A
// pré-carga os traz assim que a sessão de trabalho abre, **ao fundo**: nenhuma
// tela, caminho ou botão espera por ela, porque a aula não pode travar na
// porta (`RF-04-75`, documento 03 §§3.2, 3.4).
//
// Repete o desenho do efeito que busca o verificador do PIN: desiste sem rede
// e tenta de novo quando ela volta — sala com rede intermitente é o caso
// normal, não a exceção.
function PrecargaDosModelos() {
  const { sessao } = useSessao();
  const { semRede } = useEstadoDeRede();
  const [andamento, definirAndamento] = useState<{ carregados: number; total: number } | null>(
    null,
  );
  const [falhou, definirFalhou] = useState(false);
  // Em `ref`, e não em estado: reavaliar o efeito não pode disparar uma
  // segunda carga sobre a primeira.
  const situacao = useRef<"ocioso" | "carregando" | "pronto">("ocioso");

  useEffect(() => {
    if (situacao.current !== "ocioso") return;
    if (!sessao || sessao.papel === "guerreiro") return;
    if (semRede) return;

    situacao.current = "carregando";
    definirFalhou(false);
    definirAndamento(andamentoDosModelos());
    let cancelado = false;
    const relogio = setInterval(() => {
      if (!cancelado) definirAndamento(andamentoDosModelos());
    }, ESPERA_ENTRE_LEITURAS_DO_ANDAMENTO_MS);

    precarregarModelos().then((conseguiu) => {
      clearInterval(relogio);
      if (cancelado) return;
      // Falhou volta a `ocioso`: a volta da rede tenta de novo.
      situacao.current = conseguiu ? "pronto" : "ocioso";
      definirAndamento(null);
      definirFalhou(!conseguiu);
    });

    return () => {
      cancelado = true;
      clearInterval(relogio);
    };
  }, [sessao, semRede]);

  if (andamento) {
    return (
      <Aviso tipo="andamento">
        {`Carregando modelos de reconhecimento facial (${andamento.carregados} de ${andamento.total})`}
      </Aviso>
    );
  }
  if (falhou) return <FalhaDaPrecarga />;
  return null;
}

// A falha é **dita, e não interrompe**. Por isso não é `Aviso`: os dois tipos
// vermelhos dele — `erro` e `atencao` — são `role="alert"`, e o fundador fixou
// em 2026-10-02 que não interromper vem antes do vermelho. Sem cor, a frase
// inteira carrega a informação, e o documento 15 §5 fica satisfeito sem
// precisar de rótulo. A narração é pedida à mão, já que não vem do `Aviso`
// (`RF-04-75`, design — decisão 4).
function FalhaDaPrecarga() {
  useNarrarAoEntrar(MENSAGEM_DE_FALHA_DA_PRECARGA);
  return <EstadoDaLista>{MENSAGEM_DE_FALHA_DA_PRECARGA}</EstadoDaLista>;
}

// Aparece em toda tela enquanto durar a queda — o Mestre na porta precisa
// saber sem sair da tela em que está (`RF-04-23`, `RF-04-24`).
function AvisoDeOperacaoSemConexao() {
  const { semRede } = useEstadoDeRede();
  if (!semRede) return null;
  return (
    <Aviso tipo="atencao">
      Operando sem conexão. A presença continua sendo registrada — ela entra na fila e
      sincroniza sozinha quando a rede voltar. Cadastro novo, entrada por reconhecimento e o
      assistente de trilhas ficam indisponíveis até lá.
    </Aviso>
  );
}

function ConteudoDoAparelho() {
  const { sessao, restaurando, sair } = useSessao();
  const [recusadoComoGuerreiro, definirRecusadoComoGuerreiro] = useState(false);
  const [aulasVigentes, definirAulasVigentes] = useState<AulaVigente[] | null>(null);
  const [aulaEscolhidaId, definirAulaEscolhidaId] = useState<string | null>(() =>
    sessionStorage.getItem(CHAVE_DA_AULA_ESCOLHIDA),
  );
  const [opcoesDeComunidade, definirOpcoesDeComunidade] = useState<OpcaoDeComunidade[] | null>(
    null,
  );
  // Estado do próprio aparelho, em memória e nascendo fechado: recarregar a
  // página fecha o momento, e o Mestre o reabre (`RF-04-49`, design —
  // decisão 2).
  const [momentoDeTrocaAberto, definirMomentoDeTrocaAberto] = useState(false);
  const [abrindoMomentoDeTroca, definirAbrindoMomentoDeTroca] = useState(false);
  const [erroDeAberturaDaTroca, definirErroDeAberturaDaTroca] = useState<string | null>(null);
  const [semPinCadastrado, definirSemPinCadastrado] = useState(false);
  const { semRede } = useEstadoDeRede();

  useEffect(() => {
    if (sessao?.papel === "guerreiro") {
      definirRecusadoComoGuerreiro(true);
      sair();
    }
  }, [sessao, sair]);

  // O verificador do PIN de quem abriu a sessão de trabalho chega com ela e
  // sai com ela — é o que deixa confirmar sem rede. O PIN nunca vem. Sem PIN
  // cadastrado, o aparelho abre mesmo assim e avisa (`RN-04-38`, PRD-04 §5.1,
  // design — decisão 7).
  useEffect(() => {
    if (restaurando) return;
    if (!sessao || sessao.papel === "guerreiro") {
      apagarEstadoDoPin();
      definirSemPinCadastrado(false);
      return;
    }
    const guardado = estadoDoPinDe(sessao.persona_id);
    if (guardado?.verificador) {
      definirSemPinCadastrado(false);
      return;
    }
    if (semRede) return;
    let cancelado = false;
    buscarVerificadorDoPin(sessao.token)
      .then((verificador) => {
        if (cancelado) return;
        guardarVerificadorDoPin(sessao.persona_id, verificador);
        definirSemPinCadastrado(false);
      })
      .catch((erro) => {
        if (cancelado) return;
        if (erro instanceof ErroDaApi && erro.codigo === "pin_nao_cadastrado") {
          guardarVerificadorDoPin(sessao.persona_id, null);
          definirSemPinCadastrado(true);
        }
      });
    return () => {
      cancelado = true;
    };
  }, [sessao, restaurando, semRede]);

  // Relida ao abrir a sessão de trabalho e a cada volta à tela inicial —
  // `voltarAoInicio`, em `TelaInicial`, chama esta mesma função de novo
  // (`RF-04-02`, `RF-04-05`, design — decisão 3).
  const consultarAulasVigentes = useCallback(async () => {
    const pagina = await listarAulasVigentes();
    definirAulasVigentes(pagina.itens);
  }, []);

  useEffect(() => {
    if (sessao && sessao.papel !== "guerreiro") {
      consultarAulasVigentes();
    }
  }, [sessao, consultarAulasVigentes]);

  // A aula escolhida saiu das vigentes: a sessão de trabalho encerra, sem
  // esperar o adulto perceber (`RF-04-05`, `RN-04-29`, design — decisão 3).
  useEffect(() => {
    if (aulasVigentes === null || aulaEscolhidaId === null) return;
    const aindaVigente = aulasVigentes.some((aula) => aula.id === aulaEscolhidaId);
    if (!aindaVigente) {
      sessionStorage.removeItem(CHAVE_DA_AULA_ESCOLHIDA);
      definirAulaEscolhidaId(null);
      sair();
    }
  }, [aulasVigentes, aulaEscolhidaId, sair]);

  const escolherAula = useCallback((aula: AulaVigente) => {
    sessionStorage.setItem(CHAVE_DA_AULA_ESCOLHIDA, aula.id);
    definirAulaEscolhidaId(aula.id);
    definirOpcoesDeComunidade(null);
  }, []);

  // Abrir é ler o catálogo: só o Mestre chega aqui, e o momento só abre com
  // resposta do núcleo — falha de rede mantém fechado (`RF-04-57`, design —
  // decisão 3).
  const abrirMomentoDeTroca = useCallback(async () => {
    if (!sessao) return;
    definirErroDeAberturaDaTroca(null);
    definirAbrindoMomentoDeTroca(true);
    try {
      await listarCatalogoAvulso(sessao.token);
      definirMomentoDeTrocaAberto(true);
    } catch {
      definirErroDeAberturaDaTroca(MENSAGEM_DE_TROCA_SEM_REDE);
    } finally {
      definirAbrindoMomentoDeTroca(false);
    }
  }, [sessao]);

  const fecharMomentoDeTroca = useCallback(() => {
    definirMomentoDeTrocaAberto(false);
  }, []);

  // A saída do aparelho, oferecida só na tela inicial e confirmada ali pelo
  // PIN de quem o abriu: derruba a sessão de trabalho, a aula escolhida, o
  // momento de troca e o verificador do PIN, e a tela volta à abertura do
  // aparelho — que só reabre por login Google (`RF-04-71`, `RF-04-05`,
  // `RN-04-38`, `RN-04-41`). O estado do PIN sai aqui, e não só pelo efeito
  // que o apaga quando a sessão cai, para que a ordem não dependa de quando o
  // núcleo responder ao encerramento.
  const encerrarSessaoDeTrabalho = useCallback(() => {
    sessionStorage.removeItem(CHAVE_DA_AULA_ESCOLHIDA);
    definirAulaEscolhidaId(null);
    definirMomentoDeTrocaAberto(false);
    apagarEstadoDoPin();
    definirSemPinCadastrado(false);
    sair();
  }, [sair]);

  // Uma aula vigente dispensa a pergunta; mais de uma pergunta só uma vez
  // (`RF-04-03`). Sem sessão de trabalho não há aula a escolher: encerrada a
  // sessão, a escolha NEVER volta sozinha (`RF-04-71`).
  useEffect(() => {
    if (!sessao) return;
    if (aulasVigentes === null || aulaEscolhidaId !== null) return;
    if (aulasVigentes.length === 0) return;
    if (aulasVigentes.length === 1) {
      escolherAula(aulasVigentes[0]);
      return;
    }
    let cancelado = false;
    Promise.all(
      aulasVigentes.map(async (aula) => ({
        aula,
        nomeDaComunidade: await buscarNomeDaComunidade(aula.comunidade_virtual_id),
      })),
    ).then((opcoes) => {
      if (!cancelado) definirOpcoesDeComunidade(opcoes);
    });
    return () => {
      cancelado = true;
    };
  }, [sessao, aulasVigentes, aulaEscolhidaId, escolherAula]);

  if (restaurando) {
    return null;
  }

  if (recusadoComoGuerreiro) {
    return <TelaDeEntradaDeTrabalho mensagemDeRecusa={MENSAGEM_DE_RECUSA_DO_GUERREIRO} />;
  }

  if (!sessao) {
    return <TelaDeEntradaDeTrabalho />;
  }

  if (aulasVigentes === null) {
    return (
      <Moldura>
        <EstadoDaLista>Consultando as aulas do momento…</EstadoDaLista>
      </Moldura>
    );
  }

  if (aulasVigentes.length === 0) {
    return (
      <Moldura>
        <Cabecalho titulo="Comunidade Game — Aula" />
        <Aviso tipo="atencao">
          Não há aula agendada para agora. O aparelho só abre dentro da janela de uma aula.
        </Aviso>
      </Moldura>
    );
  }

  if (aulaEscolhidaId === null) {
    return (
      <Moldura>
        <Cabecalho
          titulo="Comunidade Game — Aula"
          subtitulo="Mais de uma aula está acontecendo agora. Em qual comunidade este aparelho está?"
        />
        {opcoesDeComunidade === null ? (
          <EstadoDaLista>Carregando as comunidades…</EstadoDaLista>
        ) : (
          <ul className="cg-caminhos">
            {opcoesDeComunidade.map((opcao) => (
              <li key={opcao.aula.id}>
                <button
                  type="button"
                  className="cg-caminho"
                  onClick={() => escolherAula(opcao.aula)}
                >
                  {opcao.nomeDaComunidade}
                </button>
              </li>
            ))}
          </ul>
        )}
      </Moldura>
    );
  }

  return (
    <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO_DO_GUERREIRO}>
      {semPinCadastrado && (
        <Aviso tipo="atencao">
          Você ainda não tem PIN de confirmação. Sem ele, não dá para confirmar a identidade de
          quem o reconhecimento não identificou. O Mestre cadastra o PIN na App 09, e o Admin,
          na App 03.
        </Aviso>
      )}
      <TelaInicial
        tokenDeTrabalho={sessao.token}
        personaIdDeTrabalho={sessao.persona_id}
        papelDeTrabalho={sessao.papel}
        aulaId={aulaEscolhidaId}
        aoVoltarAoInicio={consultarAulasVigentes}
        podeAbrirMomentoDeTroca={sessao.papel === "mestre"}
        momentoDeTrocaAberto={momentoDeTrocaAberto}
        abrindoMomentoDeTroca={abrindoMomentoDeTroca}
        erroDeAberturaDaTroca={erroDeAberturaDaTroca}
        aoAbrirMomentoDeTroca={abrirMomentoDeTroca}
        aoFecharMomentoDeTroca={fecharMomentoDeTroca}
        aoEncerrarSessaoDeTrabalho={encerrarSessaoDeTrabalho}
      />
    </ProvedorDeSessao>
  );
}
