import {
  CustomizacaoDoKit,
  type FormularioAberto,
  lerMinhasCustomizacoes,
  type MinhasCustomizacoes,
  ultimoRegistroDoKit,
} from "comum/customizacao";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { EscolhaDoPoder, GuiaDaTrilha } from "comum/trilha";
import { listarMinhasTrilhas, type TrilhaComProximaMissao } from "comum/trilha/api";
import { useCallback, useEffect, useState } from "react";
import { listarMinhasEquipes, type MinhaEquipe } from "../api/equipes";
import { useEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";

interface Props {
  /** A aula em curso, para separar as equipes daquele encontro das da
   * trilha (`RF-04-35`). */
  aulaId: string;
  token: string;
  aoVoltar: () => void;
}

const MENSAGEM_DE_FALHA =
  "Não foi possível carregar as suas trilhas agora. Tente de novo ou chame um Mestre ou Admin.";

// Distinta da frase de encontro sem programação declarada de propósito: não
// integrar equipe é outro fato, e dizer "o encontro não tem atividade" a
// quem só não entrou em equipe manda procurar o Mestre por nada
// (`RF-04-72`, `RF-04-35`).
const MENSAGEM_SEM_EQUIPE_NA_AULA =
  "Você ainda não está em nenhuma equipe deste encontro. Volte ao início e escolha Equipes " +
  "para entrar numa.";

// A mesma frase da App 05: a falha só da customização não esconde o percurso
// (`RF-04-80`, design — decisão 4).
const MENSAGEM_DE_FALHA_DA_CUSTOMIZACAO =
  "Não foi possível carregar a customização dos seus kits agora. Tente de novo em instantes.";

const MENSAGEM_SEM_ATIVIDADE_DA_EQUIPE =
  "A sua equipe deste encontro ainda não tem atividade declarada. Peça a um Mestre para " +
  "verificar.";

// O caminho das trilhas e missões no aparelho do encontro: o percurso do
// próprio Guerreiro(a) — as trilhas inscritas, a missão atual e a seguinte
// trancada com o motivo — sobre as telas promovidas a `comum/trilha`, mais
// as atividades das equipes dele naquela aula (`RF-04-72`, `RF-04-35`).
//
// Três atos individuais de partida acontecem aqui, por decisão do fundador
// de 2026-09-25: a **inscrição** em trilha, a **sondagem** que abre a
// trilha ao ser respondida e o **desafio de desbloqueio** (`RF-04-73`,
// `RF-04-74`). A **entrega individual** da produção NUNCA: a entrega desta
// aplicação é por equipe, no caminho das equipes (`RF-04-45`, `RF-05-74`).
//
// A **customização do kit recebido** também se registra aqui, pela própria
// criança, com o mesmo bloco da App 05 — registro, acompanhamento e
// cancelamento —, e vai à fila do cuidado do encontro (`RF-04-80`, PRD-04
// §5.13.1).
export function TelaDeTrilhasDoGuerreiro({ aulaId, token, aoVoltar }: Props) {
  const { semRede } = useEstadoDeRede();
  const [trilhas, definirTrilhas] = useState<TrilhaComProximaMissao[] | null>(null);
  const [equipes, definirEquipes] = useState<MinhaEquipe[] | null>(null);
  const [escolhidaId, definirEscolhidaId] = useState<string | null>(null);
  const [mostrarCatalogo, definirMostrarCatalogo] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [customizacoes, definirCustomizacoes] = useState<MinhasCustomizacoes | null>(null);
  const [erroDaCustomizacao, definirErroDaCustomizacao] = useState(false);

  // Leitura à parte das do percurso: a falha dela vira aviso único e não
  // derruba as trilhas; depois de registrar ou cancelar, só ela é lida de novo
  // (`RF-04-80`, design — decisão 4).
  const lerCustomizacoes = useCallback(async () => {
    try {
      definirCustomizacoes(await lerMinhasCustomizacoes(token));
      definirErroDaCustomizacao(false);
    } catch {
      definirErroDaCustomizacao(true);
    }
  }, [token]);

  // Nada é enfileirado aqui: sem rede o caminho simplesmente não abre, como
  // nos das equipes, do quiz e da troca (`RF-04-58`, `RF-04-68`).
  const carregar = useCallback(
    async (trilhaARecomporId: string | null = null) => {
      definirErro(null);
      try {
        const [minhasTrilhas, minhasEquipes] = await Promise.all([
          listarMinhasTrilhas(token),
          listarMinhasEquipes(token),
        ]);
        definirTrilhas(minhasTrilhas);
        definirEquipes(minhasEquipes);
        definirEscolhidaId((atual) => {
          const alvo = trilhaARecomporId ?? atual;
          if (alvo && minhasTrilhas.some((trilha) => trilha.id === alvo)) return alvo;
          // Uma inscrição só abre o percurso dela direto, sem lista no
          // caminho; mais de uma apresenta a lista primeiro.
          return minhasTrilhas.length === 1 ? minhasTrilhas[0].id : null;
        });
      } catch {
        definirErro(MENSAGEM_DE_FALHA);
      }
    },
    [token],
  );

  useEffect(() => {
    if (semRede) return;
    carregar();
    lerCustomizacoes();
  }, [carregar, lerCustomizacoes, semRede]);

  // Feita a inscrição, o percurso daquela trilha abre no mesmo atendimento
  // — na sondagem, porque é ela a próxima missão que o núcleo devolve
  // (`RF-04-74`, invariante 5).
  function aoInscrever(trilhaId: string) {
    definirMostrarCatalogo(false);
    carregar(trilhaId);
  }

  if (semRede) {
    return (
      <Moldura>
        <Cabecalho
          titulo="Este caminho precisa de rede"
          acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
        />
        <Aviso tipo="atencao">
          A rede está fora. As suas trilhas e missões voltam assim que ela voltar, e nada ficou
          guardado neste aparelho.
        </Aviso>
      </Moldura>
    );
  }

  if (erro) {
    return (
      <Moldura>
        <Cabecalho
          titulo="Trilhas e missões"
          acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
        />
        <Aviso tipo="erro">{erro}</Aviso>
      </Moldura>
    );
  }

  if (trilhas === null || equipes === null) {
    return (
      <Moldura>
        <Cabecalho
          titulo="Trilhas e missões"
          acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
        />
        <EstadoDaLista>Carregando as suas trilhas…</EstadoDaLista>
      </Moldura>
    );
  }

  // As atividades do encontro e, ao lado, os kits a customizar — nos três
  // estados do percurso (`RF-04-72`, `RF-04-80`, design — decisão 3).
  const blocosDoEncontro = (
    <>
      <AtividadesDaAula aulaId={aulaId} equipes={equipes} />
      <CustomizacaoDosKits
        customizacoes={customizacoes}
        falhou={erroDaCustomizacao}
        token={token}
        aoMudar={lerCustomizacoes}
      />
    </>
  );

  // Sem inscrição alguma, o catálogo de poderes do ciclo é o desfecho — não
  // um aviso de que inscrever-se acontece noutro lugar (`RF-04-74`, design
  // — decisão 6).
  if (trilhas.length === 0 || mostrarCatalogo) {
    return (
      <Moldura>
        <Cabecalho
          titulo="Trilhas e missões"
          subtitulo="Escolha um poder e inscreva-se numa trilha dele."
          acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
        />
        <EscolhaDoPoder aoInscrever={aoInscrever} inscricaoLigada />
        {blocosDoEncontro}
      </Moldura>
    );
  }

  const escolhida = trilhas.find((trilha) => trilha.id === escolhidaId) ?? null;

  if (escolhida === null) {
    return (
      <Moldura>
        <Cabecalho
          titulo="Trilhas e missões"
          subtitulo="Escolha a trilha que você quer abrir agora."
          acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
        />
        <section aria-label="Suas trilhas">
          <ul className="cg-trilha__lista-de-trilhas">
            {trilhas.map((trilha) => (
              <li key={trilha.id}>
                <Botao onClick={() => definirEscolhidaId(trilha.id)}>{trilha.nome}</Botao>
              </li>
            ))}
          </ul>
          <Botao variante="secundaria" onClick={() => definirMostrarCatalogo(true)}>
            Escolher outro poder
          </Botao>
        </section>
        {blocosDoEncontro}
      </Moldura>
    );
  }

  // Uma trilha só não tem para onde trocar — e é justamente nesse caso que a
  // lista de trilhas fica inalcançável. Então o rodapé do guia é o **único**
  // caminho ao catálogo de poderes e tem de oferecê-lo; com duas trilhas ou
  // mais a lista já o alcança, e repeti-lo no rodapé seria ruído
  // (`RF-04-74`, design — decisão 3).
  const temOutraTrilha = trilhas.length > 1;

  return (
    <Moldura>
      <Cabecalho titulo="Trilhas e missões" acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }} />
      <GuiaDaTrilha
        trilha={escolhida}
        aoAtualizarTrilhas={() => carregar(escolhida.id)}
        aoTrocarDeTrilha={temOutraTrilha ? () => definirEscolhidaId(null) : undefined}
        submissaoDoDesbloqueioLigada
        atividadesDoEncontro={blocosDoEncontro}
        aoEscolherOutroPoder={temOutraTrilha ? undefined : () => definirMostrarCatalogo(true)}
      />
    </Moldura>
  );
}

// As atividades da aula em curso, pelas equipes de que o Guerreiro(a) é
// integrante naquela aula — a equipe da trilha, sem `aula_id`, não é deste
// encontro (`RF-04-72`, `RF-04-35`).
function AtividadesDaAula({ aulaId, equipes }: { aulaId: string; equipes: MinhaEquipe[] }) {
  const doEncontro = equipes.filter((equipe) => equipe.aula_id === aulaId);

  return (
    <section aria-label="Atividades do encontro" className="cg-trilha__atividades-da-aula">
      <h2>Atividades do encontro</h2>
      {doEncontro.length === 0 ? (
        <Aviso tipo="andamento">{MENSAGEM_SEM_EQUIPE_NA_AULA}</Aviso>
      ) : (
        doEncontro.map((equipe) => (
          <div key={equipe.id}>
            <h3>{equipe.nome}</h3>
            {equipe.atividades.length === 0 ? (
              <Aviso tipo="atencao">{MENSAGEM_SEM_ATIVIDADE_DA_EQUIPE}</Aviso>
            ) : (
              <ul>
                {equipe.atividades.map((item) => (
                  <li key={item.atividade.id}>
                    <strong>{item.atividade.titulo}</strong> — {item.missao_titulo}
                    {item.corrente && " (a atividade do momento)"}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))
      )}
    </section>
  );
}

// Os kits recebidos com customização aberta, cada um com a situação e a ação
// do bloco da camada comum — o mesmo da App 05, para não divergir. Sem kit
// aberto a seção não se monta; um formulário aberto por vez (`RF-04-80`,
// design — decisões 1 e 3).
function CustomizacaoDosKits({
  customizacoes,
  falhou,
  token,
  aoMudar,
}: {
  customizacoes: MinhasCustomizacoes | null;
  falhou: boolean;
  token: string;
  aoMudar: () => Promise<void>;
}) {
  const [formularioAberto, definirFormularioAberto] = useState<FormularioAberto | null>(null);

  if (falhou) {
    return <Aviso tipo="atencao">{MENSAGEM_DE_FALHA_DA_CUSTOMIZACAO}</Aviso>;
  }
  const abertos = customizacoes?.kits_abertos.filter((kit) => kit.customizacao_aberta) ?? [];
  if (customizacoes === null || abertos.length === 0) return null;

  return (
    <section aria-label="Customização dos seus kits" className="cg-trilha__atividades-da-aula">
      <h2>Customização dos seus kits</h2>
      <ul>
        {abertos.map((kit) => (
          <li key={kit.entrega_de_recompensa_id}>
            <h3>
              {kit.tipo_de_recurso_nome} — {kit.trilha_nome}
            </h3>
            <CustomizacaoDoKit
              kit={kit}
              ultimo={ultimoRegistroDoKit(kit, customizacoes.registros)}
              token={token}
              formularioAberto={formularioAberto}
              abrirFormulario={definirFormularioAberto}
              fecharFormulario={() => definirFormularioAberto(null)}
              aoMudar={aoMudar}
            />
          </li>
        ))}
      </ul>
    </section>
  );
}
