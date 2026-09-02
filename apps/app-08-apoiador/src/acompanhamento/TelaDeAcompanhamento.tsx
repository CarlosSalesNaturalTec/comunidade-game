import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, EstadoDaLista, Moldura } from "comum/react";
import { type FormEvent, useCallback, useEffect, useState } from "react";
import {
  type CoberturaPublicaDeOds,
  type CriacaoPublica,
  type Favoritos,
  favoritarGuerreiroPeloNick,
  listarCoberturaPublicaDeOds,
  listarCriacoesPublicas,
  listarGuerreirosPublicos,
  listarMeusFavoritos,
  listarPoderesPublicos,
  type Novidade,
  type PoderPublico,
  removerFavorito,
} from "./api";

const MENSAGEM_DE_RECUSA_DO_FAVORITO =
  "Não encontramos esse nick com divulgação autorizada. Confira o nick exato com a família.";

function formatarData(iso: string): string {
  const data = new Date(iso);
  return Number.isNaN(data.getTime())
    ? iso
    : data.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric" });
}

const DESCRICAO_DA_NOVIDADE: Record<Novidade["tipo"], (novidade: Novidade) => string> = {
  criacao_original: () => "Publicou uma criação original",
  badge: () => "Ganhou um badge novo",
  nivel: (novidade) => `Alcançou o nível ${novidade.nivel_valor ?? ""}`.trim(),
  trilha: (novidade) => `Publicou a trilha "${novidade.trilha_nome ?? ""}"`.trim(),
};

function ListaDeNovidades({ novidades }: { novidades: Novidade[] }) {
  if (novidades.length === 0) return null;
  return (
    <ul>
      {novidades.map((novidade, indice) => (
        // biome-ignore lint/suspicious/noArrayIndexKey: novidade é derivada, sem id próprio.
        <li key={`${novidade.tipo}-${novidade.data}-${indice}`}>
          {DESCRICAO_DA_NOVIDADE[novidade.tipo](novidade)} — {formatarData(novidade.data)}
        </li>
      ))}
    </ul>
  );
}

// Os mesmos dados do painel público, sem token de sessão e sem recorte
// adicional (`RF-14-48`, `RN-14-24`, design — decisões 9 e 10).
function PainelPublico() {
  const [guerreiros, definirGuerreiros] = useState<
    { avatar: string | null; nick: string }[] | null
  >(null);
  const [poderes, definirPoderes] = useState<PoderPublico[] | null>(null);
  const [criacoes, definirCriacoes] = useState<CriacaoPublica[] | null>(null);
  const [cobertura, definirCobertura] = useState<CoberturaPublicaDeOds[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      listarGuerreirosPublicos(),
      listarPoderesPublicos(),
      listarCriacoesPublicas(),
      listarCoberturaPublicaDeOds(),
    ])
      .then(([paginaDeGuerreiros, listaDePoderes, paginaDeCriacoes, listaDeCobertura]) => {
        definirGuerreiros(paginaDeGuerreiros.itens);
        definirPoderes(listaDePoderes);
        definirCriacoes(paginaDeCriacoes.itens);
        definirCobertura(listaDeCobertura);
      })
      .catch(() =>
        definirErro("Não foi possível carregar o painel público. Tente novamente."),
      );
  }, []);

  const carregando = guerreiros === null && !erro;

  return (
    <section aria-label="Painel público">
      <h2>Painel público</h2>
      <p>O mesmo que qualquer visitante da vitrine vê — sem nenhum recorte a mais.</p>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {carregando && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {guerreiros && (
        <>
          <h3>Guerreiros e Guerreiras</h3>
          {guerreiros.length === 0 ? (
            <EstadoDaLista>Nenhum Guerreiro(a) com divulgação autorizada ainda.</EstadoDaLista>
          ) : (
            <ul>
              {guerreiros.map((guerreiro) => (
                <li key={guerreiro.nick}>{guerreiro.nick}</li>
              ))}
            </ul>
          )}
        </>
      )}
      {poderes && (
        <>
          <h3>Poderes</h3>
          {poderes.length === 0 ? (
            <EstadoDaLista>Nenhum poder publicado ainda.</EstadoDaLista>
          ) : (
            <ul>
              {poderes.map((poder) => (
                <li key={poder.id}>
                  {poder.nome} — {poder.trilhas.length} trilha(s)
                </li>
              ))}
            </ul>
          )}
        </>
      )}
      {criacoes && (
        <>
          <h3>Criações</h3>
          {criacoes.length === 0 ? (
            <EstadoDaLista>Nenhuma criação publicada ainda.</EstadoDaLista>
          ) : (
            <ul>
              {criacoes.map((criacao, indice) => (
                // biome-ignore lint/suspicious/noArrayIndexKey: a criação pública não leva id.
                <li key={indice}>
                  {criacao.producao} —{" "}
                  {criacao.autores.map((autor) => autor.nick).join(", ") ||
                    "sem autoria exibível"}
                </li>
              ))}
            </ul>
          )}
        </>
      )}
      {cobertura && (
        <>
          <h3>Cobertura de ODS</h3>
          {cobertura.length === 0 ? (
            <EstadoDaLista>Nenhuma cobertura agregada ainda.</EstadoDaLista>
          ) : (
            <ul>
              {cobertura.map((linha) => (
                <li key={linha.comunidade_id}>
                  {linha.comunidade_nome} — ODS {linha.objetivos.join(", ")}
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </section>
  );
}

// O favorito é leitura, nunca canal — nick exato, recusa indistinta e
// remoção a qualquer tempo (`RF-14-49` a `RF-14-55`, `RN-14-23` a
// `RN-14-25`, `RN-14-27`).
function BlocoDeFavoritos() {
  const { sessao } = useSessao();
  const [favoritos, definirFavoritos] = useState<Favoritos | null>(null);
  const [erroDeLeitura, definirErroDeLeitura] = useState<string | null>(null);
  const [nick, definirNick] = useState("");
  const [enviando, definirEnviando] = useState(false);
  const [erroDeFavoritar, definirErroDeFavoritar] = useState<string | null>(null);

  const carregarFavoritos = useCallback(() => {
    if (!sessao) return;
    listarMeusFavoritos(sessao.token)
      .then(definirFavoritos)
      .catch(() =>
        definirErroDeLeitura("Não foi possível carregar os favoritos. Tente novamente."),
      );
  }, [sessao]);

  useEffect(() => {
    carregarFavoritos();
  }, [carregarFavoritos]);

  async function aoFavoritar(evento: FormEvent) {
    evento.preventDefault();
    if (!sessao) return;
    definirEnviando(true);
    definirErroDeFavoritar(null);
    try {
      await favoritarGuerreiroPeloNick(sessao.token, nick);
      definirNick("");
      carregarFavoritos();
    } catch (erro) {
      if (erro instanceof ErroDaApi && erro.status === 404) {
        definirErroDeFavoritar(MENSAGEM_DE_RECUSA_DO_FAVORITO);
      } else {
        definirErroDeFavoritar("Não foi possível favoritar agora. Tente novamente.");
      }
    } finally {
      definirEnviando(false);
    }
  }

  async function aoRemover(favoritoId: string) {
    if (!sessao) return;
    await removerFavorito(sessao.token, favoritoId);
    carregarFavoritos();
  }

  const semNenhumFavorito =
    favoritos !== null && favoritos.guerreiros.length === 0 && favoritos.mestres.length === 0;

  return (
    <section aria-label="Favoritos">
      <h2>Favoritos</h2>
      <form onSubmit={aoFavoritar}>
        <Campo rotulo="Nick exato do Guerreiro(a)" valor={nick} aoAlterar={definirNick} />
        <p>
          O nick é cedido pela família — a plataforma não lista, sugere nem completa nick
          nenhum.
        </p>
        {erroDeFavoritar && <Aviso tipo="erro">{erroDeFavoritar}</Aviso>}
        <Botao tipo="submit" desabilitado={enviando || nick.trim().length === 0}>
          Favoritar
        </Botao>
      </form>

      <p>
        As novidades ficam em destaque por 30 dias, e esse destaque existe só dentro desta
        aplicação — sem e-mail nem aviso fora dela.
      </p>

      {erroDeLeitura && <Aviso tipo="erro">{erroDeLeitura}</Aviso>}
      {favoritos === null && !erroDeLeitura && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {semNenhumFavorito && (
        <EstadoDaLista>
          Você ainda não favoritou ninguém. Use o nick exato para favoritar um Guerreiro(a).
        </EstadoDaLista>
      )}
      {favoritos && favoritos.guerreiros.length > 0 && (
        <ul>
          {favoritos.guerreiros.map((favorito) => (
            <li key={favorito.id}>
              {favorito.nick}
              <ListaDeNovidades novidades={favorito.novidades} />
              <Botao variante="secundaria" onClick={() => aoRemover(favorito.id)}>
                Remover
              </Botao>
            </li>
          ))}
        </ul>
      )}
      {favoritos && favoritos.mestres.length > 0 && (
        <ul>
          {favoritos.mestres.map((favorito) => (
            <li key={favorito.id}>
              {favorito.nome}
              <ListaDeNovidades novidades={favorito.novidades} />
              <Botao variante="secundaria" onClick={() => aoRemover(favorito.id)}>
                Remover
              </Botao>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export function TelaDeAcompanhamento() {
  return (
    <Moldura>
      <Cabecalho titulo="Acompanhamento" />
      <PainelPublico />
      <BlocoDeFavoritos />
    </Moldura>
  );
}
