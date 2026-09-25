import { Avatar } from "../avatar/Avatar";
import type { AvatarDoGuerreiro } from "../avatar/objeto";
import { BadgeDaFamilia, type FamiliaDeBadge } from "./BadgeDaFamilia";
import { EmblemaDeNivel } from "./EmblemaDeNivel";

// A **carta do personagem** — o átomo da interface comum às oito aplicações
// (documento 15 §8.1). Os valores dela vêm do temperamento e dos tokens, em
// `estilos.css`: superfície de carta, borda de 1 px, raio que a aplicação
// declara — `4` px na Operação e `12` na Arena —, avatar quadrado recortado em
// círculo ocupando **metade da largura** e nick na família de destaque.
//
// O que cada variante exibe é do documento 11 §8.2, e a carta exibe **só**
// aquilo: não há aqui campo de imagem real, de nome civil, de rede social nem
// de canal de contato, e é por não existir que nenhuma tela os põe na carta
// (invariantes 9 e 10).
//
// **Carta pela metade não se apresenta.** A leitura que não devolve o que a
// tabela do §8.2 exige daquela variante não vira carta incompleta: vira outra
// forma de apresentação, escolhida por quem monta a tela. Quem decide é
// `cartaEstaCompleta`, e a carta devolve `null` quando a resposta é não — a
// mesma decisão do fundador registrada no documento 09 §1 para a lista de
// comunidades da App 03.
//
// Só a variante **Guerreiro(a)** entra aqui. Mestre, Apoiador e Comunidade
// Virtual têm tabela de exibição própria no §8.2 e rotas de outras aplicações,
// e entram na fatia da aplicação que as exibe.

export interface BadgeNaCarta {
  familia: FamiliaDeBadge;
  poder?: string;
}

export interface PoderComNivel {
  poder: string;
  nivel: number;
}

/** A variante Guerreiro(a) do documento 11 §8.2. Cada campo aceita
 * `undefined` para dizer "a leitura não trouxe isto" — e é o que torna a carta
 * incompleta. O `avatar` é a exceção: ausente ou vazio, o documento 15 §7.3
 * manda desenhar o **avatar padrão do projeto**, e isso não é falta. */
export interface CartaDeGuerreiro {
  variante: "guerreiro";
  avatar: string | AvatarDoGuerreiro | null | undefined;
  nick: string | undefined;
  badges: BadgeNaCarta[] | undefined;
  poderes: PoderComNivel[] | undefined;
  /** O desempenho do Guerreiro(a), em uma frase — posição e pontos, por
   * exemplo. O §8.2 o exige da variante. */
  desempenho: string | undefined;
  /** As criações originais, uma linha por criação. Lista vazia é "ainda
   * nenhuma", que é diferente de `undefined`. */
  criacoes: string[] | undefined;
}

export type DadosDaCarta = CartaDeGuerreiro;

/** `true` quando a leitura trouxe tudo o que a tabela do documento 11 §8.2
 * exige da variante. */
export function cartaEstaCompleta(dados: DadosDaCarta): boolean {
  return (
    dados.nick !== undefined &&
    dados.nick.trim().length > 0 &&
    dados.badges !== undefined &&
    dados.poderes !== undefined &&
    dados.desempenho !== undefined &&
    dados.desempenho.trim().length > 0 &&
    dados.criacoes !== undefined
  );
}

interface Props {
  dados: DadosDaCarta;
}

/** A posição é o único identificador que a leitura dá: o núcleo emite um badge
 * por nível alcançado, e dois badges de nível do mesmo poder são de fato
 * indistinguíveis. A lista só cresce ao fim, nunca se reordena, e por isso a
 * chave por posição é estável. */
function comChave<T>(itens: T[], nome: (item: T) => string): { chave: string; item: T }[] {
  return itens.map((item, indice) => ({ chave: `${indice}-${nome(item)}`, item }));
}

export function CartaDoPersonagem({ dados }: Props) {
  if (!cartaEstaCompleta(dados)) return null;

  const { avatar, nick, badges = [], poderes = [], desempenho, criacoes = [] } = dados;
  const badgesNaOrdem = comChave(badges, (badge) => `${badge.familia}-${badge.poder ?? ""}`);
  const criacoesNaOrdem = comChave(criacoes, (criacao) => criacao);

  return (
    <article
      className="cg-carta"
      data-variante={dados.variante}
      aria-label={`Carta de ${nick}`}
    >
      <div className="cg-carta__avatar">
        <Avatar avatar={avatar ?? null} tamanho={96} />
      </div>
      <p className="cg-carta__nick">{nick}</p>

      <p className="cg-carta__desempenho">{desempenho}</p>

      <p className="cg-carta__rotulo">Poderes</p>
      {poderes.length === 0 ? (
        <p className="cg-carta__vazio">Nenhum poder com nível ainda.</p>
      ) : (
        <ul className="cg-carta__poderes">
          {poderes.map((item) => (
            <li key={item.poder}>
              <EmblemaDeNivel nivel={item.nivel} poder={item.poder} />
            </li>
          ))}
        </ul>
      )}

      <p className="cg-carta__rotulo">Badges</p>
      {badges.length === 0 ? (
        <p className="cg-carta__vazio">Nenhum badge ainda.</p>
      ) : (
        <ul className="cg-carta__badges">
          {badgesNaOrdem.map(({ chave, item }) => (
            <li key={chave}>
              <BadgeDaFamilia familia={item.familia} poder={item.poder} />
            </li>
          ))}
        </ul>
      )}

      <p className="cg-carta__rotulo">Criações originais</p>
      {criacoes.length === 0 ? (
        <p className="cg-carta__vazio">Nenhuma criação original validada ainda.</p>
      ) : (
        <ul className="cg-carta__criacoes">
          {criacoesNaOrdem.map(({ chave, item }) => (
            <li key={chave}>{item}</li>
          ))}
        </ul>
      )}
    </article>
  );
}
