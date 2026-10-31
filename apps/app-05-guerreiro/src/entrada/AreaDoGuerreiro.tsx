import { useSessao } from "comum/autenticacao";
import {
  Aviso,
  Botao,
  Cabecalho,
  type CaminhoDaTela,
  ListaDeCaminhos,
  Moldura,
} from "comum/react";
import { listarMinhasTrilhas } from "comum/trilha/api";
import { useEffect, useRef, useState } from "react";
import { DURACAO_DE_INATIVIDADE_EM_MINUTOS } from "../api/configuracao";
import { Carteira } from "../carteira/Carteira";
import { Coleta } from "../coleta/Coleta";
import { DesafiosEEquipes } from "../desafios/DesafiosEEquipes";
import { Trilha } from "../trilha/Trilha";

const UM_MINUTO_EM_MS = 60_000;
const EVENTOS_DE_ATIVIDADE = ["pointerdown", "keydown", "touchstart"] as const;

type Bloco = "carteira" | "trilha" | "desafios-e-equipes" | "coleta";

// Conteúdo da sessão aberta: o encerramento por saída e por inatividade, o
// bloco da trilha — inscrição, guia, conteúdo, sondagem, desbloqueio e
// progresso —, o bloco da carteira, catálogo, conquistas e ranking, o bloco
// dos desafios em aberto e das equipes de que participa e o bloco da coleta
// do território — acervo é fatia do Ciclo 02 (PRD-05 §3.2).
//
// A área **abre no bloco da trilha**, e é ele que diz o que fazer agora e o
// que a missão desbloqueia: o `RF-05-08` e as §§5.2, 10 e 12 do PRD-05 pedem
// a tela inicial na próxima missão, "sem que a criança precise procurar em
// menu". Até 2026-10-31 a área abria na coleta do território, e chegar à
// missão custava uma ida ao menu.
//
// Os quatro caminhos são **cartões em grade** — duas colunas no celular,
// quatro a partir do marco de `768` px —, com o glifo acima do rótulo em
// frase. A **ordem** é decisão do fundador de 2026-10-31 e não é o acaso de
// quando cada fatia acrescentou o bloco: carteira, trilha, desafios e
// equipes, coleta. O cartão do bloco aberto é anunciado como o atual, de modo
// que os cartões são navegação com item corrente — e não o menu que o
// `RF-05-08` proíbe.
export function AreaDoGuerreiro() {
  const { sessao, sair } = useSessao();
  const [avisando, definirAvisando] = useState(false);
  const [bloco, definirBloco] = useState<Bloco>("trilha");
  const referenciaDeReiniciar = useRef<() => void>(() => {});
  const proximaMissao = useProximaMissao(sessao?.token);

  useEffect(() => {
    const duracaoEmMs = DURACAO_DE_INATIVIDADE_EM_MINUTOS * 60_000;
    let timeoutDeAviso: ReturnType<typeof setTimeout>;
    let timeoutDeEncerramento: ReturnType<typeof setTimeout>;

    function reiniciar() {
      clearTimeout(timeoutDeAviso);
      clearTimeout(timeoutDeEncerramento);
      definirAvisando(false);
      timeoutDeAviso = setTimeout(
        () => definirAvisando(true),
        Math.max(duracaoEmMs - UM_MINUTO_EM_MS, 0),
      );
      timeoutDeEncerramento = setTimeout(() => {
        sair();
      }, duracaoEmMs);
    }
    referenciaDeReiniciar.current = reiniciar;

    function aoDetectarAtividade() {
      reiniciar();
    }

    reiniciar();
    for (const evento of EVENTOS_DE_ATIVIDADE) {
      window.addEventListener(evento, aoDetectarAtividade);
    }
    return () => {
      clearTimeout(timeoutDeAviso);
      clearTimeout(timeoutDeEncerramento);
      for (const evento of EVENTOS_DE_ATIVIDADE) {
        window.removeEventListener(evento, aoDetectarAtividade);
      }
    };
  }, [sair]);

  const caminhos: CaminhoDaTela[] = [
    {
      chave: "carteira",
      rotulo: "Minha carteira — seus pontos, badges e conquistas",
      glifo: "carteira",
      aoAcionar: () => definirBloco("carteira"),
    },
    {
      chave: "trilha",
      rotulo: "Trilha — o seu percurso e a próxima missão",
      glifo: "trilhas",
      conteudoExtra: proximaMissao ?? undefined,
      aoAcionar: () => definirBloco("trilha"),
    },
    {
      chave: "desafios-e-equipes",
      rotulo: "Desafios e equipes — o que está em aberto e com quem você joga",
      glifo: "desafios",
      aoAcionar: () => definirBloco("desafios-e-equipes"),
    },
    {
      chave: "coleta",
      rotulo: "Coleta do território — medir e registrar o que você vê na sua rua",
      glifo: "coleta",
      aoAcionar: () => definirBloco("coleta"),
    },
  ];

  return (
    <Moldura>
      <Cabecalho titulo="Minha Área" acao={{ rotulo: "Sair", aoAcionar: sair }} />
      {avisando && (
        <>
          <Aviso tipo="atencao">Você ainda está aí? Sua sessão vai fechar em 1 minuto.</Aviso>
          <Botao onClick={() => referenciaDeReiniciar.current()}>Continuar</Botao>
        </>
      )}

      <ListaDeCaminhos
        rotulo="Área do Guerreiro(a)"
        caminhos={caminhos}
        disposicao="grade"
        caminhoAtual={bloco}
      />

      {bloco === "carteira" && <Carteira />}
      {bloco === "trilha" && <Trilha />}
      {bloco === "desafios-e-equipes" && <DesafiosEEquipes />}
      {bloco === "coleta" && <Coleta />}
    </Moldura>
  );
}

// A próxima missão para o cartão da trilha, pelo dado que `GET /v1/eu/trilhas`
// já devolve — sem rota nova (`RF-05-08`, `RF-05-17`, design — decisão 5).
//
// A trilha de referência é a **primeira** da lista, a mesma que o bloco da
// trilha seleciona por padrão, para que o cartão e o bloco não discordem.
// Falhando a leitura, ou não havendo próxima missão, devolve `null` e o cartão
// fica só com o rótulo: a tela inicial nunca apresenta erro de rede por causa
// de um subtítulo de cartão, e quem ainda não se inscreveu encontra a escolha
// do poder dentro do bloco, não aqui.
function useProximaMissao(token: string | undefined): string | null {
  const [proximaMissao, definirProximaMissao] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    let descartado = false;
    listarMinhasTrilhas(token)
      .then((trilhas) => {
        if (descartado) return;
        const primeira = trilhas[0];
        if (!primeira?.proxima_missao_titulo) return;
        const posicao = primeira.proxima_missao_posicao;
        definirProximaMissao(
          posicao === null
            ? primeira.proxima_missao_titulo
            : `Missão ${posicao} — ${primeira.proxima_missao_titulo}`,
        );
      })
      .catch(() => {
        // Silêncio de propósito: o cartão recua ao rótulo sozinho.
      });
    return () => {
      descartado = true;
    };
  }, [token]);

  return proximaMissao;
}
