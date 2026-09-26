import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { eu as lerSessao } from "comum/autenticacao/api";
import {
  Aviso,
  type BadgeNaCarta,
  CartaDoPersonagem,
  cartaEstaCompleta,
  type DadosDaCarta,
  EstadoDaLista,
  type FamiliaDeBadge,
  type PoderComNivel,
} from "comum/react";
import { listarPoderesDoCatalogo, type PoderPublico } from "comum/trilha/api";
import { useEffect, useState } from "react";
import {
  type MinhaPosicaoNoRanking,
  obterMinhaPosicaoNoRanking,
  obterPortfolioDaCarta,
  obterProgressoDaCarta,
  type ProgressoDaTrilhaNaCarta,
} from "./api";

// A **carta do próprio Guerreiro(a)** em sessão, na variante Guerreiro(a) do
// documento 11 §8.2: avatar, nick, badges, poderes com níveis, desempenho e
// criações originais — e nada de imagem real, nome civil, rede social ou canal
// de contato, que a carta do `comum` nem tem campo para receber (`RF-05-50`,
// `RF-05-51`, invariantes 9 e 10).
//
// Promovida do App 05 ao `comum` porque as duas aplicações da Arena que
// apresentam personagem a montam da mesma forma (decisão do fundador de
// 2026-09-25). A carta é montada das leituras de `./api`, **sem rota nova**.
//
// Faltando qualquer coisa que a variante exige, **não se apresenta carta pela
// metade** (documento 11 §8.2): quem monta a tela diz em uma frase o que tem,
// e a carta não aparece.
//
// A identificação vem de `GET /v1/eu` e o desempenho do ranking logado da
// própria turma, que o núcleo recorta pelo **vínculo vigente**. Antes as duas
// vinham da `minha_posicao` do ranking, e a comunidade dele era adivinhada das
// **séries de coleta**: quem nunca abriu série não tinha carta — nem na Área,
// nem no desfecho da presença (`RF-01-76`, decisão do fundador de 2026-09-26).

const FAMILIAS: Record<string, FamiliaDeBadge> = {
  de_nivel: "de_nivel",
  de_conquista: "de_conquista",
  de_valores_e_causas: "de_valores_e_causas",
  de_territorio: "de_territorio",
  de_autoria: "de_autoria",
  de_protagonismo: "de_protagonismo",
};

function poderDaTrilha(poderes: PoderPublico[], item: ProgressoDaTrilhaNaCarta): string {
  const poder = poderes.find((candidato) =>
    candidato.trilhas.some((trilha) => trilha.id === item.trilha_id),
  );
  return poder?.nome ?? item.trilha_nome;
}

export function poderesComNivel(
  progresso: ProgressoDaTrilhaNaCarta[],
  poderes: PoderPublico[],
): PoderComNivel[] {
  const porPoder = new Map<string, number>();
  for (const item of progresso) {
    if (item.nivel_atual === null) continue;
    const poder = poderDaTrilha(poderes, item);
    porPoder.set(poder, Math.max(porPoder.get(poder) ?? 0, item.nivel_atual));
  }
  return [...porPoder].map(([poder, nivel]) => ({ poder, nivel }));
}

export function badgesDoProgresso(
  progresso: ProgressoDaTrilhaNaCarta[],
  poderes: PoderPublico[],
): BadgeNaCarta[] {
  return progresso.flatMap((item) =>
    item.badges.map((tipo) => ({
      familia: FAMILIAS[tipo] ?? "de_nivel",
      poder: poderDaTrilha(poderes, item),
    })),
  );
}

function desempenho(posicao: MinhaPosicaoNoRanking): string {
  return `${posicao.posicao}º na comunidade, com ${posicao.pontos_regulares} pontos`;
}

interface Props {
  /** A frase que substitui a carta quando a leitura não trouxe tudo o que a
   * variante exige. Cada aplicação diz a sua, porque o que oferecer em troca
   * depende da tela. */
  aviso: string;
}

export function CartaDoGuerreiro({ aviso }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [dados, definirDados] = useState<DadosDaCarta | null>(null);

  useEffect(() => {
    if (!sessao) return;
    const token = sessao.token;
    let cancelado = false;

    async function montar() {
      // Cada leitura que falta deixa o campo dela `undefined`, e é isso que a
      // carta lê para recusar a montagem incompleta.
      let identificacao: { nick?: string; avatar?: string } | undefined;
      let minhaPosicao: MinhaPosicaoNoRanking | undefined;
      let poderes: PoderPublico[] = [];
      let progresso: ProgressoDaTrilhaNaCarta[] | undefined;
      let criacoes: string[] | undefined;

      try {
        const [quemSou, catalogo] = await Promise.all([
          lerSessao(token),
          listarPoderesDoCatalogo().catch(() => [] as PoderPublico[]),
        ]);
        poderes = catalogo;
        identificacao = { nick: quemSou.nick, avatar: quemSou.avatar };
      } catch (erroCapturado) {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
      }

      try {
        minhaPosicao = (await obterMinhaPosicaoNoRanking(token)).minha_posicao;
      } catch (erroCapturado) {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        minhaPosicao = undefined;
      }

      try {
        progresso = await obterProgressoDaCarta(token);
      } catch {
        progresso = undefined;
      }

      try {
        criacoes = (await obterPortfolioDaCarta(token)).map(
          (item) => item.producao ?? "Criação em mídia",
        );
      } catch {
        criacoes = undefined;
      }

      if (cancelado) return;
      definirDados({
        variante: "guerreiro",
        avatar: identificacao?.avatar,
        nick: identificacao?.nick,
        desempenho: minhaPosicao && desempenho(minhaPosicao),
        poderes: progresso && poderesComNivel(progresso, poderes),
        badges: progresso && badgesDoProgresso(progresso, poderes),
        criacoes,
      });
    }

    montar();
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  if (dados === null) return <EstadoDaLista>Montando a sua carta…</EstadoDaLista>;

  // Tom de **falta**, não de coisa em curso: a montagem já terminou, e o
  // rótulo "Em andamento:" mandava esperar uma tela que não ia mudar
  // (`RF-04-67`, documento 15 §5).
  if (!cartaEstaCompleta(dados)) return <Aviso tipo="atencao">{aviso}</Aviso>;

  return <CartaDoPersonagem dados={dados} />;
}
