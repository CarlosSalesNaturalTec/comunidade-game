import { ProvedorDeSessao, useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { type AulaVigente, listarAulasVigentes } from "../api/aulas";
import { listarCatalogoAvulso } from "../api/catalogoAvulso";
import { buscarNomeDaComunidade } from "../api/comunidades";
import { TelaInicial } from "../inicio/TelaInicial";
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

interface OpcaoDeComunidade {
  aula: AulaVigente;
  nomeDaComunidade: string;
}

export function AparelhoDaAula() {
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

  useEffect(() => {
    if (sessao?.papel === "guerreiro") {
      definirRecusadoComoGuerreiro(true);
      sair();
    }
  }, [sessao, sair]);

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

  // Uma aula vigente dispensa a pergunta; mais de uma pergunta só uma vez
  // (`RF-04-03`).
  useEffect(() => {
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
  }, [aulasVigentes, aulaEscolhidaId, escolherAula]);

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
      <TelaInicial
        tokenDeTrabalho={sessao.token}
        personaIdDeTrabalho={sessao.persona_id}
        aulaId={aulaEscolhidaId}
        aoVoltarAoInicio={consultarAulasVigentes}
        podeAbrirMomentoDeTroca={sessao.papel === "mestre"}
        momentoDeTrocaAberto={momentoDeTrocaAberto}
        abrindoMomentoDeTroca={abrindoMomentoDeTroca}
        erroDeAberturaDaTroca={erroDeAberturaDaTroca}
        aoAbrirMomentoDeTroca={abrirMomentoDeTroca}
        aoFecharMomentoDeTroca={fecharMomentoDeTroca}
      />
    </ProvedorDeSessao>
  );
}
