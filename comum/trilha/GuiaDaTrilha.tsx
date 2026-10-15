import { type ReactNode, useCallback, useEffect, useState } from "react";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { Aviso } from "../react/Aviso";
import { BlocoRecolhivel } from "../react/BlocoRecolhivel";
import { Botao } from "../react/Botao";
import { EstadoDaLista } from "../react/EstadoDaLista";
import {
  type AtividadeDaMissaoPublica,
  type MissaoNoPercurso,
  obterMissaoNoPercurso,
  obterTrilhaPublica,
  type TrilhaComProximaMissao,
  type TrilhaPublicaComMissoes,
} from "./api";
import { Missao } from "./Missao";

interface Props {
  trilha: TrilhaComProximaMissao;
  aoAtualizarTrilhas: () => void;
  /** Ausente quando não há outra trilha para onde ir — a App 01 com uma
   * inscrição só não oferece a troca. */
  aoTrocarDeTrilha?: () => void;
  submissaoDoDesbloqueioLigada?: boolean;
  entregaDaProducao?: (dados: {
    missaoId: string;
    atividades: AtividadeDaMissaoPublica[];
  }) => ReactNode;
  /** A culminância da trilha, oferecida por quem a atende — a App 01 não a
   * liga: culminância está fora desta fatia (`RF-05-39`). */
  culminancia?: ReactNode;
  /** O grupo das atividades do encontro. Só a App 01 o tem; sem ele o grupo
   * inteiro desaparece, com a linha dele (`RF-04-72`). */
  atividadesDoEncontro?: ReactNode;
  /** O caminho ao catálogo de poderes, no rodapé. Quem monta a tela decide
   * se passa: só entra onde é o **único** caminho ao catálogo, porque quem
   * tem uma trilha só não alcança a lista de trilhas (`RF-04-74`,
   * design — decisão 3). */
  aoEscolherOutroPoder?: () => void;
}

const FALHA_DO_CONTEUDO =
  "Não foi possível carregar o conteúdo agora. Tente de novo em instantes.";

// A tela da missão, em **quatro grupos separados por linha muda**: o
// conteúdo com o ato da missão; a próxima missão com a bibliografia; as
// atividades do encontro; e o rodapé, com o caminho ao catálogo e o crédito
// da trilha (decisão do fundador de 2026-10-15).
//
// A linha é `border-top` do grupo de baixo, não elemento próprio — então
// **grupo sem conteúdo leva a sua linha embora** e nunca sobra separador
// entre dois grupos vizinhos (`estilos.css`, design — decisão 2). Por isso
// cada grupo é condicionado ao que tem dentro, e os grupos são irmãos
// consecutivos: nada se intromete entre eles.
//
// Abre direto na próxima missão do Guerreiro(a), sem procurar em menu. A
// missão seguinte, ainda trancada, e o motivo dela seguem apresentados, mas
// **recolhidos** (`RF-05-08`, `RF-05-10`, documento 15 §§6.1, 6.4).
// Alternar de trilha preserva o contexto de cada uma, porque a posição vem
// sempre do núcleo (`RF-05-17`).
//
// É este componente que busca a trilha publicada, e não a `Missao`: a
// bibliografia e o crédito saem da mesma resposta e caem em grupos
// diferentes, e um dono só precisa saber se o grupo do meio ficou vazio
// (design — decisão 1).
export function GuiaDaTrilha({
  trilha,
  aoAtualizarTrilhas,
  aoTrocarDeTrilha,
  submissaoDoDesbloqueioLigada,
  entregaDaProducao,
  culminancia,
  atividadesDoEncontro,
  aoEscolherOutroPoder,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [missaoAtual, definirMissaoAtual] = useState<MissaoNoPercurso | null>(null);
  const [missaoSeguinte, definirMissaoSeguinte] = useState<MissaoNoPercurso | null>(null);
  const [trilhaPublica, definirTrilhaPublica] = useState<TrilhaPublicaComMissoes | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [erroDoConteudo, definirErroDoConteudo] = useState<string | null>(null);

  const tratarErro = useCallback(
    (erroCapturado: unknown) => {
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
      if (
        erroCapturado &&
        typeof erroCapturado === "object" &&
        "codigo" in erroCapturado &&
        erroCapturado.codigo === "nao_encontrado"
      ) {
        return;
      }
      definirErro("Não foi possível carregar a missão agora. Tente de novo em instantes.");
    },
    [tratarRecusaDeSessao],
  );

  const carregar = useCallback(() => {
    if (!sessao || trilha.proxima_missao_posicao === null) return;
    definirErro(null);
    obterMissaoNoPercurso(trilha.id, trilha.proxima_missao_posicao, sessao.token)
      .then(definirMissaoAtual)
      .catch(tratarErro);
    obterMissaoNoPercurso(trilha.id, trilha.proxima_missao_posicao + 1, sessao.token)
      .then(definirMissaoSeguinte)
      .catch(() => definirMissaoSeguinte(null));
  }, [sessao, trilha, tratarErro]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  // A trilha publicada é buscada aqui, uma vez por trilha aberta. Trocar de
  // trilha limpa o que estava em tela antes de a nova resposta chegar, para
  // o crédito de uma trilha nunca aparecer sob o conteúdo de outra.
  useEffect(() => {
    let cancelado = false;
    definirTrilhaPublica(null);
    definirErroDoConteudo(null);
    obterTrilhaPublica(trilha.id)
      .then((resultado) => {
        if (!cancelado) definirTrilhaPublica(resultado);
      })
      .catch(() => {
        if (!cancelado) definirErroDoConteudo(FALHA_DO_CONTEUDO);
      });
    return () => {
      cancelado = true;
    };
  }, [trilha.id]);

  function aoDesbloquear() {
    aoAtualizarTrilhas();
  }

  const trilhaConcluida = trilha.proxima_missao_posicao === null;
  const missaoPublica = missaoAtual
    ? trilhaPublica?.missoes.find((item) => item.id === missaoAtual.id)
    : undefined;
  const bibliografia = missaoPublica?.bibliografia ?? [];
  const proximaTrancada = missaoSeguinte !== null && !missaoSeguinte.desbloqueada;

  // Cada grupo só existe se tiver conteúdo — é isso que impede a linha órfã.
  const temGrupoDoQueSeLeDepois =
    !trilhaConcluida && (proximaTrancada || bibliografia.length > 0);
  const temRodape = aoEscolherOutroPoder !== undefined || trilhaPublica !== null;

  return (
    <section aria-label={`Guia de ${trilha.nome}`} className="cg-trilha__guia">
      <header className="cg-trilha__cabecalho-do-guia">
        <h2>{trilha.nome}</h2>
        {aoTrocarDeTrilha && (
          <Botao variante="secundaria" onClick={aoTrocarDeTrilha}>
            Trocar de trilha
          </Botao>
        )}
      </header>

      {/* Grupo 1 — o conteúdo e o ato da missão, ou, na trilha inteira
          desbloqueada, a culminância. Não tem linha: é o primeiro. */}
      <div className="cg-trilha__grupo">
        {trilhaConcluida ? (
          <>
            <Aviso tipo="sucesso">
              Você já desbloqueou todas as missões desta trilha. Agora é hora da culminância!
            </Aviso>
            {culminancia}
          </>
        ) : (
          <>
            {erro && <Aviso tipo="erro">{erro}</Aviso>}
            {!erro && missaoAtual === null && (
              <EstadoDaLista>Carregando a missão…</EstadoDaLista>
            )}
            {missaoAtual && (
              <Missao
                missao={missaoAtual}
                missaoPublica={missaoPublica}
                erroDoConteudo={erroDoConteudo}
                aoDesbloquear={aoDesbloquear}
                submissaoDoDesbloqueioLigada={submissaoDoDesbloqueioLigada}
                entregaDaProducao={entregaDaProducao}
              />
            )}
          </>
        )}
      </div>

      {/* Grupo 2 — o que se lê depois: os dois recolhidos, lado a lado. */}
      {temGrupoDoQueSeLeDepois && (
        <div className="cg-trilha__grupo">
          {proximaTrancada && missaoSeguinte && (
            <BlocoRecolhivel titulo="Próxima missão" resumo="O que vem depois desta missão.">
              <p>
                A seguir: <strong>{missaoSeguinte.titulo}</strong> —{" "}
                {missaoSeguinte.motivo_do_bloqueio}
              </p>
            </BlocoRecolhivel>
          )}
          {bibliografia.length > 0 && (
            <BlocoRecolhivel titulo="Bibliografia" resumo="Onde ler mais sobre esta missão.">
              <ul className="cg-trilha__bibliografia">
                {bibliografia.map((item) => (
                  <li key={item.id}>
                    {item.titulo} — {item.capitulo}
                    {item.disponivel === true && " (disponível no seu ponto de apoio)"}
                    {item.disponivel === false && " (sem exemplar no seu ponto de apoio)"}
                  </li>
                ))}
              </ul>
            </BlocoRecolhivel>
          )}
        </div>
      )}

      {/* Grupo 3 — as atividades do encontro, de quem as tem. */}
      {atividadesDoEncontro && <div className="cg-trilha__grupo">{atividadesDoEncontro}</div>}

      {/* Grupo 4 — o rodapé: o caminho ao catálogo, quando é o único, e o
          crédito da trilha, que é metadado da obra. */}
      {temRodape && (
        <div className="cg-trilha__grupo">
          {aoEscolherOutroPoder && (
            <Botao variante="secundaria" onClick={aoEscolherOutroPoder}>
              Escolher outro poder
            </Botao>
          )}
          {trilhaPublica && (
            <BlocoRecolhivel
              titulo="Crédito e licença"
              resumo="Quem fez esta trilha e sob qual licença."
            >
              <p className="cg-trilha__credito">
                Crédito: {trilhaPublica.autor_nome ?? "Mestre autor"} — licença{" "}
                {trilhaPublica.licenca}
              </p>
            </BlocoRecolhivel>
          )}
        </div>
      )}
    </section>
  );
}
