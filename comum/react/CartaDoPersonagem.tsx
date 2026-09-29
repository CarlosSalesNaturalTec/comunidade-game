import { Avatar } from "../avatar/Avatar";
import type { AvatarDoGuerreiro } from "../avatar/objeto";
import { BadgeDaFamilia, type FamiliaDeBadge } from "./BadgeDaFamilia";
import { EmblemaDeNivel } from "./EmblemaDeNivel";
import { type CamadaDoTerritorio, TerritorioDaComunidade } from "./TerritorioDaComunidade";

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
// As quatro variantes do §8.2 entram aqui: **Guerreiro(a)**, **Comunidade
// Virtual**, **Mestre** e **Apoiador**.

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

/** A variante Comunidade Virtual do documento 11 §8.2: nome, território,
 * representação visual, séries ativas e número de Guerreiros e Guerreiras
 * vinculados. Nada aqui desce abaixo do bairro, e nenhum campo carrega
 * coletor — a tabela do §8.2 veda a granularidade que permita inferir
 * endereço de criança (`RN-03-09`, `RN-03-10`). */
export interface CartaDeComunidadeVirtual {
  variante: "comunidade-virtual";
  nome: string | undefined;
  /** A localização da comunidade — o "território" da tabela do §8.2. */
  territorio: string | undefined;
  /** Nulo é o que a lista devolve para a comunidade abaixo do piso: a carta
   * então não se apresenta, e a tela usa outra forma. */
  seriesAtivas: number | null | undefined;
  seriesAbertas: number | null | undefined;
  vinculados: number | undefined;
  /** Os insumos da representação visual (documento 11 §8.3). Lista vazia é
   * "território ainda vazio", que é diferente de `undefined`. */
  camadas: CamadaDoTerritorio[] | undefined;
  bairrosPublicados: number | undefined;
}

/** Quem é o adulto na carta, **e o que o valor é**. O nick é opcional para
 * Mestre e Apoiador: não havendo, vale o nome, e a carta o apresenta como
 * nome — nunca no lugar reservado ao nick (`RF-03-79`, `RN-03-36`, documento
 * 11 §8.2). NUNCA vale para Guerreiro(a), cuja variante só tem `nick`. */
export interface IdentificacaoDoAdulto {
  valor: string;
  tipo: "nick" | "nome";
}

export interface ArtefatoNaCarta {
  endereco: string;
  rotulo: string;
}

/** A variante **Mestre** do documento 11 §8.2: avatar, nick, áreas de
 * habilidade, artefatos comprobatórios, trilhas de autoria e o selo de quem
 * sustentou atividade sem recurso. A tabela não veda nada para esta variante
 * — o adulto aparece com a prova pública dele. */
export interface CartaDeMestre {
  variante: "mestre";
  avatar: string | null | undefined;
  identificacao: IdentificacaoDoAdulto | undefined;
  areasDeHabilidade: string[] | undefined;
  artefatos: ArtefatoNaCarta[] | undefined;
  trilhasDeAutoria: string[] | undefined;
  /** Quantas vezes sustentou atividade que estava sem recurso — o selo da
   * tabela do §8.2. */
  absorcoes: number | undefined;
}

/** A variante **Apoiador** do documento 11 §8.2: avatar, nick e total de
 * moedas em destaque, nível de sustento, selos, desafios propostos e
 * efetividade agregada. NUNCA exibe valor em reais nem dado de contato de
 * Guerreiro(a) (`RN-03-18`, `RN-03-26`). */
export interface CartaDeApoiador {
  variante: "apoiador";
  avatar: string | null | undefined;
  identificacao: IdentificacaoDoAdulto | undefined;
  /** Sempre em moedas da plataforma. A carta nunca recebe reais: o núcleo não
   * os envia (`RF-03-10`, `RN-03-18`). */
  totalEmMoedas: string | undefined;
  /** `true` abaixo do piso de 10 moedas, quando o avatar próprio não é
   * exibido (`RF-03-66`). A moldura e o resto da carta não mudam. */
  avatarPadrao: boolean | undefined;
  nivelDeSustento: number | undefined;
  nomeDoNivel: string | undefined;
  selos: string[] | undefined;
  desafiosPropostos: DesafioNaCarta[] | undefined;
  artefatos: ArtefatoNaCarta[] | undefined;
}

/** A efetividade **agregada** do `RF-03-80`: trilha, período e quantos
 * concluíram. Nunca quem concluiu (`RN-03-37`). */
export interface DesafioNaCarta {
  trilha: string;
  periodoInicio: string;
  periodoFim: string;
  concluiram: number;
  direcionado: boolean;
}

export type DadosDaCarta =
  | CartaDeGuerreiro
  | CartaDeComunidadeVirtual
  | CartaDeMestre
  | CartaDeApoiador;

function guerreiroEstaCompleto(dados: CartaDeGuerreiro): boolean {
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

function comunidadeEstaCompleta(dados: CartaDeComunidadeVirtual): boolean {
  return (
    dados.nome !== undefined &&
    dados.nome.trim().length > 0 &&
    dados.territorio !== undefined &&
    dados.territorio.trim().length > 0 &&
    dados.seriesAtivas !== undefined &&
    dados.seriesAtivas !== null &&
    dados.vinculados !== undefined &&
    dados.camadas !== undefined
  );
}

function identificacaoEstaCompleta(identificacao: IdentificacaoDoAdulto | undefined): boolean {
  return identificacao !== undefined && identificacao.valor.trim().length > 0;
}

function mestreEstaCompleto(dados: CartaDeMestre): boolean {
  return (
    identificacaoEstaCompleta(dados.identificacao) &&
    dados.areasDeHabilidade !== undefined &&
    dados.artefatos !== undefined &&
    dados.trilhasDeAutoria !== undefined &&
    dados.absorcoes !== undefined
  );
}

function apoiadorEstaCompleto(dados: CartaDeApoiador): boolean {
  return (
    identificacaoEstaCompleta(dados.identificacao) &&
    dados.totalEmMoedas !== undefined &&
    dados.nivelDeSustento !== undefined &&
    dados.selos !== undefined &&
    dados.desafiosPropostos !== undefined &&
    dados.artefatos !== undefined
  );
}

/** `true` quando a leitura trouxe tudo o que a tabela do documento 11 §8.2
 * exige **daquela** variante. A decisão é por variante porque cada linha da
 * tabela exige campos próprios. */
export function cartaEstaCompleta(dados: DadosDaCarta): boolean {
  switch (dados.variante) {
    case "guerreiro":
      return guerreiroEstaCompleto(dados);
    case "comunidade-virtual":
      return comunidadeEstaCompleta(dados);
    case "mestre":
      return mestreEstaCompleto(dados);
    case "apoiador":
      return apoiadorEstaCompleto(dados);
  }
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
  if (dados.variante === "comunidade-virtual") return <CartaDeComunidade dados={dados} />;
  if (dados.variante === "mestre") return <CartaDoMestre dados={dados} />;
  if (dados.variante === "apoiador") return <CartaDoApoiador dados={dados} />;

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

function CartaDeComunidade({ dados }: { dados: CartaDeComunidadeVirtual }) {
  const { nome, territorio, seriesAtivas, seriesAbertas, vinculados, camadas = [] } = dados;
  return (
    <article
      className="cg-carta"
      data-variante={dados.variante}
      aria-label={`Carta de ${nome}`}
    >
      <TerritorioDaComunidade
        nome={nome ?? ""}
        bairrosPublicados={dados.bairrosPublicados ?? 0}
        camadas={camadas}
        seriesAbertas={seriesAbertas ?? null}
        seriesAtivas={seriesAtivas ?? null}
      />
      <p className="cg-carta__nick">{nome}</p>
      <p className="cg-carta__desempenho">{territorio}</p>

      <p className="cg-carta__rotulo">Séries ativas</p>
      <p className="cg-carta__vazio">{seriesAtivas}</p>

      <p className="cg-carta__rotulo">Guerreiros e Guerreiras vinculados</p>
      <p className="cg-carta__vazio">{vinculados}</p>
    </article>
  );
}

/** O que identifica o adulto na carta. O `data-tipo` carrega se aquilo é nick
 * ou nome, para que a superfície nunca apresente um no lugar do outro
 * (`RF-03-79`, `RN-03-36`). */
function IdentificacaoNaCarta({ identificacao }: { identificacao: IdentificacaoDoAdulto }) {
  return (
    <p className="cg-carta__nick" data-tipo={identificacao.tipo}>
      {identificacao.valor}
    </p>
  );
}

function ArtefatosNaCarta({ artefatos }: { artefatos: ArtefatoNaCarta[] }) {
  return (
    <>
      <p className="cg-carta__rotulo">Prova pública</p>
      {artefatos.length === 0 ? (
        <p className="cg-carta__vazio">Nenhum comprobatório declarado ainda.</p>
      ) : (
        <ul className="cg-carta__artefatos">
          {artefatos.map((artefato) => (
            <li key={artefato.endereco}>
              {/* A prova é link declarado, nunca anexo de arquivo
                  (`RN-02-01`, documento 02 §1). */}
              <a href={artefato.endereco} rel="noreferrer noopener" target="_blank">
                {artefato.rotulo}
              </a>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}

function CartaDoMestre({ dados }: { dados: CartaDeMestre }) {
  const {
    avatar,
    identificacao,
    areasDeHabilidade = [],
    artefatos = [],
    trilhasDeAutoria = [],
    absorcoes = 0,
  } = dados;
  const identidade = identificacao as IdentificacaoDoAdulto;

  return (
    <article
      className="cg-carta"
      data-variante={dados.variante}
      aria-label={`Carta de ${identidade.valor}`}
    >
      <div className="cg-carta__avatar">
        {/* Avatar ausente vira o avatar padrão do projeto (documento 15
            §7.3), e isso não é carta incompleta. */}
        <Avatar avatar={avatar ?? null} tamanho={96} />
      </div>
      <IdentificacaoNaCarta identificacao={identidade} />

      <p className="cg-carta__rotulo">Áreas de habilidade</p>
      {areasDeHabilidade.length === 0 ? (
        <p className="cg-carta__vazio">Nenhuma trilha publicada ainda.</p>
      ) : (
        <ul className="cg-carta__areas">
          {areasDeHabilidade.map((area) => (
            <li key={area}>{area}</li>
          ))}
        </ul>
      )}

      <p className="cg-carta__rotulo">Trilhas de autoria</p>
      {trilhasDeAutoria.length === 0 ? (
        <p className="cg-carta__vazio">Nenhuma trilha publicada ainda.</p>
      ) : (
        <ul className="cg-carta__trilhas">
          {trilhasDeAutoria.map((trilha) => (
            <li key={trilha}>{trilha}</li>
          ))}
        </ul>
      )}

      <ArtefatosNaCarta artefatos={artefatos} />

      <p className="cg-carta__rotulo">Sustentou atividade sem recurso</p>
      <p className="cg-carta__vazio">{absorcoes === 1 ? "1 vez" : `${absorcoes} vezes`}</p>
    </article>
  );
}

function CartaDoApoiador({ dados }: { dados: CartaDeApoiador }) {
  const {
    avatar,
    identificacao,
    totalEmMoedas,
    avatarPadrao = false,
    nivelDeSustento = 0,
    nomeDoNivel,
    selos = [],
    desafiosPropostos = [],
    artefatos = [],
  } = dados;
  const identidade = identificacao as IdentificacaoDoAdulto;

  return (
    <article
      className="cg-carta"
      // A moldura é **a mesma** de todo Apoiador: avatar centralizado em
      // proporção fixa, nick abaixo e o total em destaque. É o que impede a
      // marca maior de dominar a página (`RF-03-56`, documento 11 §8.2).
      data-variante={dados.variante}
      data-avatar-padrao={avatarPadrao ? "sim" : "nao"}
      aria-label={`Carta de ${identidade.valor}`}
    >
      <div className="cg-carta__avatar">
        <Avatar avatar={avatar ?? null} tamanho={96} />
      </div>
      <IdentificacaoNaCarta identificacao={identidade} />

      {/* Sempre em moedas da plataforma, nunca em reais (`RN-03-18`). */}
      <p className="cg-carta__moedas">{totalEmMoedas} moedas</p>

      <p className="cg-carta__rotulo">Nível de sustento</p>
      <p className="cg-carta__vazio">
        {nomeDoNivel ? `${nivelDeSustento} — ${nomeDoNivel}` : nivelDeSustento}
      </p>

      <p className="cg-carta__rotulo">Selos</p>
      {selos.length === 0 ? (
        <p className="cg-carta__vazio">Nenhum selo ainda.</p>
      ) : (
        <ul className="cg-carta__selos">
          {selos.map((selo) => (
            <li key={selo}>{selo}</li>
          ))}
        </ul>
      )}

      <p className="cg-carta__rotulo">Desafios propostos</p>
      {desafiosPropostos.length === 0 ? (
        <p className="cg-carta__vazio">Nenhum desafio publicado ainda.</p>
      ) : (
        <ul className="cg-carta__desafios">
          {desafiosPropostos.map((desafio) => (
            // Trilha, período e contagem — nunca quem concluiu
            // (`RF-03-80`, `RN-03-37`).
            <li key={`${desafio.trilha}-${desafio.periodoInicio}`}>
              {desafio.trilha} — de {desafio.periodoInicio} a {desafio.periodoFim} —{" "}
              {desafio.concluiram === 1 ? "1 concluiu" : `${desafio.concluiram} concluíram`}
            </li>
          ))}
        </ul>
      )}

      <ArtefatosNaCarta artefatos={artefatos} />
    </article>
  );
}
