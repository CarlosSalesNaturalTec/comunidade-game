import { useSessao } from "comum/autenticacao";
import type { FamiliaDeBadge, FatoDaArena } from "comum/react";
import {
  Aviso,
  BadgeDaFamilia,
  EmblemaDeNivel,
  EstadoDaLista,
  RetornoDeConquista,
} from "comum/react";
import { listarPoderesDoCatalogo, type PoderPublico } from "comum/trilha/api";
import { useEffect, useState } from "react";
import { obterProgresso, type ProgressoDaTrilha } from "../api/trilha";
import { fatosDoProgresso } from "./fatosDoProgresso";

// Nível e quanto falta para o próximo, por trilha, mais pontos e badges —
// nível é percurso, nunca saldo de pontos, e nenhuma ação daqui lança
// resultado, presença ou mérito (`RF-05-15`, `RF-05-16`, `RN-05-03`,
// `RN-05-04`, `RN-05-06`).
//
// O nível aparece pelo **emblema contável** do documento 15 §8.2 e o badge
// pela **silhueta da família** do §8.3, com o glifo do poder — nunca só o
// numeral, nunca só o texto: o emblema existe para ser contado por uma criança
// de 6 anos.

// O `TipoDeBadge` do núcleo devolve o tipo como texto; as seis famílias da
// camada comum o cobrem, e as duas que o núcleo ainda não emite — de conquista
// e de território — seguem como pendência no documento 09 §1. Tipo que o
// núcleo venha a acrescentar sem silhueta não quebra a tela: cai na família de
// nível, que é a do badge que todo percurso rende.
const FAMILIAS: Record<string, FamiliaDeBadge> = {
  de_nivel: "de_nivel",
  de_conquista: "de_conquista",
  de_valores_e_causas: "de_valores_e_causas",
  de_territorio: "de_territorio",
  de_autoria: "de_autoria",
  de_protagonismo: "de_protagonismo",
};

function familiaDoBadge(tipo: string): FamiliaDeBadge {
  return FAMILIAS[tipo] ?? "de_nivel";
}

/** O nome do poder da trilha, que a moldura do emblema carrega (documento 15
 * §8.2). O catálogo é leitura pública, e a App 05 já o consome no filtro do
 * ranking; sem ele, a moldura leva o nome da trilha — o emblema é sempre de
 * uma trilha ou de um poder, nunca global. */
function nomeDoPoder(poderes: PoderPublico[], item: ProgressoDaTrilha): string {
  const poder = poderes.find((candidato) =>
    candidato.trilhas.some((trilha) => trilha.id === item.trilha_id),
  );
  return poder?.nome ?? item.trilha_nome;
}

export function Progresso() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [progresso, definirProgresso] = useState<ProgressoDaTrilha[] | null>(null);
  // Qual fato aconteceu em cada trilha desde a última leitura desta sessão
  // (documento 11 §8.5). Computado **junto com** a leitura, e não a cada
  // renderização: a marca do que já se viu é consumida uma vez, senão a
  // segunda renderização já não acharia fato nenhum.
  const [fatos, definirFatos] = useState<Record<string, FatoDaArena>>({});
  const [poderes, definirPoderes] = useState<PoderPublico[]>([]);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    let cancelado = false;
    obterProgresso(sessao.token)
      .then((resultado) => {
        if (cancelado) return;
        definirFatos(fatosDoProgresso(resultado));
        definirProgresso(resultado);
      })
      .catch((erroCapturado) => {
        if (cancelado) return;
        if (
          erroCapturado &&
          typeof erroCapturado === "object" &&
          "codigo" in erroCapturado &&
          (erroCapturado.codigo === "sessao_ausente" ||
            erroCapturado.codigo === "sessao_invalida")
        ) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro(
          "Não foi possível carregar o seu progresso agora. Tente de novo em instantes.",
        );
      });
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  // O catálogo é acessório ao progresso: falhar nele não tira o progresso da
  // tela, só faz a moldura levar o nome da trilha.
  useEffect(() => {
    let cancelado = false;
    listarPoderesDoCatalogo()
      .then((resultado) => {
        if (!cancelado) definirPoderes(resultado);
      })
      .catch(() => {
        if (!cancelado) definirPoderes([]);
      });
    return () => {
      cancelado = true;
    };
  }, []);

  if (erro) return <Aviso tipo="erro">{erro}</Aviso>;
  if (progresso === null) return <EstadoDaLista>Carregando o seu progresso…</EstadoDaLista>;
  if (progresso.length === 0) {
    return <EstadoDaLista>Você ainda não está inscrito em nenhuma trilha.</EstadoDaLista>;
  }

  return (
    <section aria-label="Meu progresso">
      <h2>Meu progresso</h2>
      <ul className="cg-trilha__progresso">
        {progresso.map((item) => {
          const poder = nomeDoPoder(poderes, item);
          // O núcleo emite um badge por nível alcançado, e dois badges de
          // nível da mesma trilha são indistinguíveis: a posição na lista é o
          // único identificador que a leitura dá, e ela só cresce ao fim.
          const badges = item.badges.map((tipo, indice) => ({
            chave: `${indice}-${tipo}`,
            familia: familiaDoBadge(tipo),
          }));
          return (
            <li key={item.trilha_id} className="cg-trilha__progresso-item">
              <h3>{item.trilha_nome}</h3>
              {/* O retorno acompanha o fato, e o nível continua legível pelo
                  emblema contável com ou sem movimento (documento 15 §§5, 6).
                  Sem fato novo, `fato` é `null` e nada anima. */}
              <RetornoDeConquista fato={fatos[item.trilha_id] ?? null}>
                {item.nivel_atual === null ? (
                  <p>Nível: ainda sem nível</p>
                ) : (
                  <EmblemaDeNivel nivel={item.nivel_atual} poder={poder} />
                )}
              </RetornoDeConquista>
              <p>
                Faltam {item.obrigatorias_totais - item.obrigatorias_desbloqueadas} de{" "}
                {item.obrigatorias_totais} missões obrigatórias para o próximo nível
              </p>
              <p>Pontos: {item.pontos_regulares}</p>
              {badges.length > 0 && (
                <ul className="cg-trilha__badges">
                  {badges.map((badge) => (
                    <li key={badge.chave}>
                      <BadgeDaFamilia familia={badge.familia} poder={poder} />
                    </li>
                  ))}
                </ul>
              )}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
