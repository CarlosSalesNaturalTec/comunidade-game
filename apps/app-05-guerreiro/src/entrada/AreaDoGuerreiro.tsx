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
import { type ReactNode, useEffect, useRef, useState } from "react";
import { DURACAO_DE_INATIVIDADE_EM_MINUTOS } from "../api/configuracao";
import { Carteira } from "../carteira/Carteira";
import { Coleta } from "../coleta/Coleta";
import { DesafiosEEquipes } from "../desafios/DesafiosEEquipes";
import { Trilha } from "../trilha/Trilha";

const UM_MINUTO_EM_MS = 60_000;
const EVENTOS_DE_ATIVIDADE = ["pointerdown", "keydown", "touchstart"] as const;

type Caminho = "menu" | "trilha" | "carteira" | "desafios-e-equipes" | "coleta";

// Conteúdo da sessão aberta: o encerramento por saída e por inatividade, o
// bloco da trilha — inscrição, guia, conteúdo, sondagem, desbloqueio e
// progresso —, o bloco da carteira, catálogo, conquistas e ranking, o bloco
// dos desafios em aberto e das equipes de que participa e o bloco da coleta
// do território — acervo é fatia do Ciclo 02 (PRD-05 §3.2).
//
// A área **abre no menu dos caminhos**, e nenhum conteúdo de bloco aparece
// antes de a criança acionar um deles. Quem diz o que fazer agora é o cartão
// da Trilha, que nomeia a próxima missão e vem primeiro — é o que sustenta o
// `RF-05-08` depois de ele ser reenunciado. Até 2026-10-31 a área abria no
// bloco da trilha, com os caminhos em grade convivendo com o conteúdo na
// mesma tela.
//
// Acionado um caminho, o bloco ocupa a tela sozinho e o cabeçalho dele traz
// **Voltar** — o idioma que a tela inicial da App 01 já usa. O Voltar é um
// único retorno ao menu, e não um passo atrás: o estado interno do bloco é
// desmontado junto com ele, de modo que voltar de Progresso, de Retomadas ou
// do histórico de uma série dá no mesmo lugar.
//
// A **ordem** é decisão do fundador de 2026-10-31 e não é o acaso de quando
// cada fatia acrescentou o bloco: trilha, carteira, desafios e equipes,
// coleta — e **sair** por último, cartão igual aos demais. A saída existe só
// aqui: a tela de conteúdo tem Voltar e mais nada, porque o cabeçalho tem uma
// única fatia de ação.
export function AreaDoGuerreiro() {
  const { sessao, sair } = useSessao();
  const [avisando, definirAvisando] = useState(false);
  const [caminho, definirCaminho] = useState<Caminho>("menu");
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

  // O aviso de inatividade acompanha **as duas** telas: a sessão da criança
  // nunca fecha sem aviso por ela estar dentro de um bloco (`RF-05-71`).
  const avisoDeInatividade = avisando && (
    <>
      <Aviso tipo="atencao">Você ainda está aí? Sua sessão vai fechar em 1 minuto.</Aviso>
      <Botao onClick={() => referenciaDeReiniciar.current()}>Continuar</Botao>
    </>
  );

  if (caminho !== "menu") {
    const { titulo, conteudo } = TELAS[caminho];
    return (
      <Moldura>
        <Cabecalho
          titulo={titulo}
          acao={{ rotulo: "Voltar", aoAcionar: () => definirCaminho("menu") }}
        />
        {avisoDeInatividade}
        {conteudo}
      </Moldura>
    );
  }

  const caminhos: CaminhoDaTela[] = [
    {
      chave: "trilha",
      rotulo: "Trilha — o seu percurso e a próxima missão",
      glifo: "trilhas",
      conteudoExtra: proximaMissao ?? undefined,
      aoAcionar: () => definirCaminho("trilha"),
    },
    {
      chave: "carteira",
      rotulo: "Minha carteira — seus pontos, badges e conquistas",
      glifo: "carteira",
      aoAcionar: () => definirCaminho("carteira"),
    },
    {
      chave: "desafios-e-equipes",
      rotulo: "Desafios e equipes — o que está em aberto e com quem você joga",
      glifo: "desafios",
      aoAcionar: () => definirCaminho("desafios-e-equipes"),
    },
    {
      chave: "coleta",
      rotulo: "Coleta do território — medir e registrar o que você vê na sua rua",
      glifo: "coleta",
      aoAcionar: () => definirCaminho("coleta"),
    },
    {
      chave: "sair",
      rotulo: "Sair",
      glifo: "encerrar",
      aoAcionar: sair,
    },
  ];

  // Sem rótulo, a lista é o contêiner dos cartões e não declara marco de
  // navegação: aqui os caminhos **são** a tela, e o marco não distinguiria
  // nada — além de o cartão de sair ser ação, não destino.
  return (
    <Moldura>
      <Cabecalho titulo="Minha Área" />
      {avisoDeInatividade}
      <ListaDeCaminhos caminhos={caminhos} />
    </Moldura>
  );
}

const TELAS: Record<Exclude<Caminho, "menu">, { titulo: string; conteudo: ReactNode }> = {
  trilha: { titulo: "Trilha", conteudo: <Trilha /> },
  carteira: { titulo: "Minha carteira", conteudo: <Carteira /> },
  "desafios-e-equipes": {
    titulo: "Desafios e equipes",
    conteudo: <DesafiosEEquipes />,
  },
  coleta: { titulo: "Coleta do território", conteudo: <Coleta /> },
};

// A próxima missão para o cartão da trilha, pelo dado que `GET /v1/eu/trilhas`
// já devolve — sem rota nova (`RF-05-08`, `RF-05-17`).
//
// A trilha de referência é a **primeira** da lista, a mesma que o bloco da
// trilha seleciona por padrão, para que o cartão e o bloco não discordem.
// Falhando a leitura, ou não havendo próxima missão, devolve `null` e o cartão
// fica só com o rótulo: o menu nunca apresenta erro de rede por causa de um
// subtítulo de cartão, e quem ainda não se inscreveu encontra a escolha do
// poder dentro do bloco, não aqui.
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
