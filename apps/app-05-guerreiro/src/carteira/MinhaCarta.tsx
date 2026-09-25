import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
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
import { type ItemDoRankingDaTurma, listarRankingDaTurma } from "../api/carteira";
import { listarMinhasSeries } from "../api/coleta";
import { obterPortfolio } from "../api/criacaoOriginal";
import { obterProgresso, type ProgressoDaTrilha } from "../api/trilha";

// A **carta do próprio Guerreiro(a)** na Área dele, na variante Guerreiro(a) do
// documento 11 §8.2: avatar, nick, badges, poderes com níveis, desempenho e
// criações originais — e nada de imagem real, nome civil, rede social ou canal
// de contato, que a carta do `comum` nem tem campo para receber (`RF-05-50`,
// `RF-05-51`, invariantes 9 e 10).
//
// A carta é montada das **leituras que a Área já consome**, sem rota nova:
//
// | O que a variante exige | De onde vem                                        |
// | ---------------------- | -------------------------------------------------- |
// | Avatar e nick          | `minha_posicao` do ranking logado da turma          |
// | Desempenho             | posição e pontos da mesma `minha_posicao`           |
// | Poderes com níveis     | `GET /v1/eu/progresso` cruzado com o catálogo       |
// | Badges                 | `GET /v1/eu/progresso`                              |
// | Criações originais      | `GET /v1/eu/portfolio`                             |
//
// O ranking é a única leitura logada que devolve ao Guerreiro(a) o **próprio**
// avatar e nick — `GET /v1/eu` devolve papel, permissões e a autorização de
// divulgação, e nunca os dois, pendência registrada no documento 09 §1. Ele é
// segmentado por comunidade, e a comunidade vem das séries de coleta do
// Guerreiro(a), o mesmo caminho que a tela do ranking já usa.
//
// Faltando qualquer coisa que a variante exige, **não se apresenta carta pela
// metade** (documento 11 §8.2): a Área diz em uma frase o que tem, e a carta
// não aparece.

const FAMILIAS: Record<string, FamiliaDeBadge> = {
  de_nivel: "de_nivel",
  de_conquista: "de_conquista",
  de_valores_e_causas: "de_valores_e_causas",
  de_territorio: "de_territorio",
  de_autoria: "de_autoria",
  de_protagonismo: "de_protagonismo",
};

function poderDaTrilha(poderes: PoderPublico[], item: ProgressoDaTrilha): string {
  const poder = poderes.find((candidato) =>
    candidato.trilhas.some((trilha) => trilha.id === item.trilha_id),
  );
  return poder?.nome ?? item.trilha_nome;
}

function poderesComNivel(
  progresso: ProgressoDaTrilha[],
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

function badgesDoProgresso(
  progresso: ProgressoDaTrilha[],
  poderes: PoderPublico[],
): BadgeNaCarta[] {
  return progresso.flatMap((item) =>
    item.badges.map((tipo) => ({
      familia: FAMILIAS[tipo] ?? "de_nivel",
      poder: poderDaTrilha(poderes, item),
    })),
  );
}

function desempenho(posicao: ItemDoRankingDaTurma): string {
  return `${posicao.posicao}º na comunidade, com ${posicao.pontos_regulares} pontos`;
}

export function MinhaCarta() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [dados, definirDados] = useState<DadosDaCarta | null>(null);

  useEffect(() => {
    if (!sessao) return;
    const token = sessao.token;
    let cancelado = false;

    async function montar() {
      // Cada leitura que falta deixa o campo dela `undefined`, e é isso que a
      // carta lê para recusar a montagem incompleta.
      let minhaPosicao: ItemDoRankingDaTurma | undefined;
      let poderes: PoderPublico[] = [];
      let progresso: ProgressoDaTrilha[] | undefined;
      let criacoes: string[] | undefined;

      try {
        const [series, catalogo] = await Promise.all([
          listarMinhasSeries(token),
          listarPoderesDoCatalogo().catch(() => [] as PoderPublico[]),
        ]);
        poderes = catalogo;
        const comunidade = series.itens[0]?.comunidade_virtual_id;
        if (comunidade !== undefined) {
          minhaPosicao = (await listarRankingDaTurma(comunidade, token)).minha_posicao;
        }
      } catch (erroCapturado) {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
      }

      try {
        progresso = await obterProgresso(token);
      } catch {
        progresso = undefined;
      }

      try {
        criacoes = (await obterPortfolio(token)).map(
          (item) => item.producao ?? "Criação em mídia",
        );
      } catch {
        criacoes = undefined;
      }

      if (cancelado) return;
      definirDados({
        variante: "guerreiro",
        avatar: minhaPosicao?.avatar,
        nick: minhaPosicao?.nick,
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

  if (!cartaEstaCompleta(dados)) {
    return (
      <Aviso tipo="andamento">
        A sua carta aparece aqui quando o seu percurso tiver tudo o que ela mostra — avatar,
        apelido, poderes, badges e criações. Suas conquistas seguem nas abas abaixo.
      </Aviso>
    );
  }

  return (
    <div className="cg-minha-carta">
      <CartaDoPersonagem dados={dados} />
    </div>
  );
}
