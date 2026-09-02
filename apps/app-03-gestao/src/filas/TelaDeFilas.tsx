import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useId, useState } from "react";
import { AvaliacaoDaSolicitacao } from "./AvaliacaoDaSolicitacao";
import { AvaliacaoDeChave } from "./AvaliacaoDeChave";
import { AvaliacaoDeDados } from "./AvaliacaoDeDados";
import { AvaliacaoDeSugestao } from "./AvaliacaoDeSugestao";
import { AvaliacaoDoDesafioExtra } from "./AvaliacaoDoDesafioExtra";
import {
  listarSolicitacoesDeChave,
  listarSolicitacoesDeDados,
  listarSolicitacoesDeParticipacao,
  listarSolicitacoesDoResponsavel,
  listarSugestoes,
  type SolicitacaoDeChave,
  type SolicitacaoDeDados,
  type SolicitacaoDeParticipacao,
  type SolicitacaoDoResponsavel,
  type Sugestao,
} from "./api";
import { type ItemDeFila, ListaDeFilas } from "./ListaDeFilas";
import { TratamentoDaSolicitacaoDoResponsavel } from "./TratamentoDaSolicitacaoDoResponsavel";

// O filtro por natureza alcança as seis naturezas da fila, fechando o que
// a fatia anterior abriu só para participação (`RF-02-18`, `RF-02-23`,
// `RF-02-25`, `RF-02-27`, `RF-02-77`, `RF-02-87`).
type Natureza =
  | "participacao"
  | "dados"
  | "chave"
  | "sugestao"
  | "responsavel"
  | "desafio_extra";

const NATUREZAS: { chave: Natureza; rotulo: string }[] = [
  { chave: "participacao", rotulo: "Participação" },
  { chave: "dados", rotulo: "Dados" },
  { chave: "chave", rotulo: "Chave" },
  { chave: "sugestao", rotulo: "Sugestões" },
  { chave: "responsavel", rotulo: "Responsável" },
  { chave: "desafio_extra", rotulo: "Desafios extras" },
];

const MENSAGEM_VAZIA: Record<Natureza, string> = {
  participacao: "Nenhuma solicitação de participação por enquanto.",
  dados: "Nenhuma solicitação de dados por enquanto.",
  chave: "Nenhuma solicitação de chave por enquanto.",
  sugestao: "Nenhuma sugestão ou proposta por enquanto.",
  responsavel: "Nenhuma solicitação do responsável por enquanto.",
  desafio_extra: "Nenhum desafio extra aguardando aprovação por enquanto.",
};

const ROTULO_DO_TIPO_DA_SOLICITACAO_DO_RESPONSAVEL: Record<
  SolicitacaoDoResponsavel["tipo"],
  string
> = {
  acesso: "Acesso",
  correcao: "Correção",
  exclusao: "Exclusão",
  esclarecimento: "Esclarecimento",
};

const ROTULO_DA_PRETENSAO: Record<SolicitacaoDeParticipacao["pretensao"], string> = {
  mestre: "Mestre",
  apoiador: "Apoiador",
};

const ROTULO_DA_SITUACAO: Record<string, string> = {
  recebida: "Recebida",
  em_avaliacao: "Em avaliação",
  aceita: "Aceita",
  recusada: "Recusada",
};

const ROTULO_DA_SITUACAO_DA_SUGESTAO: Record<Sugestao["situacao"], string> = {
  recebida: "Recebida",
  em_avaliacao: "Em avaliação",
  adotada: "Adotada",
  nao_adotada: "Não adotada",
};

const ROTULO_DO_PAPEL: Record<string, string> = {
  guerreiro: "Guerreiro(a)",
  mestre: "Mestre",
  apoiador: "Apoiador",
  responsavel: "Responsável",
  admin: "Admin",
};

function normalizarParticipacao(item: SolicitacaoDeParticipacao): ItemDeFila {
  return {
    id: item.id,
    quem: item.nome_ou_razao_social,
    detalhe: ROTULO_DA_PRETENSAO[item.pretensao],
    situacaoRotulo: ROTULO_DA_SITUACAO[item.situacao],
    em_atraso: item.em_atraso,
    prazo: item.prazo,
  };
}

function normalizarDados(item: SolicitacaoDeDados): ItemDeFila {
  return {
    id: item.id,
    quem: item.solicitante,
    detalhe: item.instituicao,
    situacaoRotulo: ROTULO_DA_SITUACAO[item.situacao],
    em_atraso: item.em_atraso,
    prazo: item.prazo,
  };
}

function normalizarChave(item: SolicitacaoDeChave): ItemDeFila {
  return {
    id: item.id,
    quem: item.solicitante,
    detalhe: item.o_que_pretende_construir,
    situacaoRotulo: ROTULO_DA_SITUACAO[item.situacao],
    em_atraso: item.em_atraso,
    prazo: item.prazo,
  };
}

function normalizarSugestao(item: Sugestao): ItemDeFila {
  return {
    id: item.id,
    quem: ROTULO_DO_PAPEL[item.papel_do_autor] ?? item.papel_do_autor,
    detalhe: item.texto,
    situacaoRotulo: ROTULO_DA_SITUACAO_DA_SUGESTAO[item.situacao],
    em_atraso: item.em_atraso,
    prazo: item.prazo,
  };
}

function normalizarSolicitacaoDoResponsavel(item: SolicitacaoDoResponsavel): ItemDeFila {
  return {
    id: item.id,
    quem: item.nick_do_responsavel ?? item.responsavel_id,
    detalhe: `${ROTULO_DO_TIPO_DA_SOLICITACAO_DO_RESPONSAVEL[item.tipo]} — ${
      item.nick_do_guerreiro ?? item.guerreiro_id
    }`,
    situacaoRotulo: ROTULO_DA_SITUACAO[item.situacao],
    em_atraso: item.em_atraso,
    prazo: item.prazo,
  };
}

type Selecionada =
  | { natureza: "participacao"; item: SolicitacaoDeParticipacao }
  | { natureza: "dados"; item: SolicitacaoDeDados }
  | { natureza: "chave"; item: SolicitacaoDeChave }
  | { natureza: "sugestao"; item: Sugestao }
  | { natureza: "responsavel"; item: SolicitacaoDoResponsavel };

export function TelaDeFilas() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const idDoFiltro = useId();
  const [natureza, definirNatureza] = useState<Natureza>("participacao");
  const [participacoes, definirParticipacoes] = useState<SolicitacaoDeParticipacao[] | null>(
    null,
  );
  const [dados, definirDados] = useState<SolicitacaoDeDados[] | null>(null);
  const [chaves, definirChaves] = useState<SolicitacaoDeChave[] | null>(null);
  const [sugestoes, definirSugestoes] = useState<Sugestao[] | null>(null);
  const [solicitacoesDoResponsavel, definirSolicitacoesDoResponsavel] = useState<
    SolicitacaoDoResponsavel[] | null
  >(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [selecionada, definirSelecionada] = useState<Selecionada | null>(null);

  const ehAdmin = sessao?.papel === "admin";

  const carregar = useCallback(async () => {
    if (!sessao || !ehAdmin) return;
    try {
      if (natureza === "participacao") {
        const pagina = await listarSolicitacoesDeParticipacao(sessao.token);
        definirParticipacoes(pagina.itens);
      } else if (natureza === "dados") {
        const pagina = await listarSolicitacoesDeDados(sessao.token);
        definirDados(pagina.itens);
      } else if (natureza === "chave") {
        const pagina = await listarSolicitacoesDeChave(sessao.token);
        definirChaves(pagina.itens);
      } else if (natureza === "sugestao") {
        const pagina = await listarSugestoes(sessao.token);
        definirSugestoes(pagina.itens);
      } else if (natureza === "responsavel") {
        const itens = await listarSolicitacoesDoResponsavel(sessao.token);
        definirSolicitacoesDoResponsavel(itens);
      }
      // "desafio_extra" carrega as próprias listas dentro de
      // `AvaliacaoDoDesafioExtra` — não uma seleção sobre `ListaDeFilas`
      // (design — decisão 7).
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar a fila. Tente novamente em instantes.");
    }
  }, [sessao, ehAdmin, natureza, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  function selecionarNatureza(novaNatureza: Natureza) {
    definirNatureza(novaNatureza);
    definirSelecionada(null);
  }

  function aoSelecionarId(id: string) {
    if (natureza === "participacao") {
      const item = participacoes?.find((solicitacao) => solicitacao.id === id);
      if (item) definirSelecionada({ natureza: "participacao", item });
    } else if (natureza === "dados") {
      const item = dados?.find((solicitacao) => solicitacao.id === id);
      if (item) definirSelecionada({ natureza: "dados", item });
    } else if (natureza === "chave") {
      const item = chaves?.find((solicitacao) => solicitacao.id === id);
      if (item) definirSelecionada({ natureza: "chave", item });
    } else if (natureza === "sugestao") {
      const item = sugestoes?.find((sugestao) => sugestao.id === id);
      if (item) definirSelecionada({ natureza: "sugestao", item });
    } else if (natureza === "responsavel") {
      const item = solicitacoesDoResponsavel?.find((solicitacao) => solicitacao.id === id);
      if (item) definirSelecionada({ natureza: "responsavel", item });
    }
  }

  const itensDaListaAtual: ItemDeFila[] | null =
    natureza === "participacao"
      ? (participacoes?.map(normalizarParticipacao) ?? null)
      : natureza === "dados"
        ? (dados?.map(normalizarDados) ?? null)
        : natureza === "chave"
          ? (chaves?.map(normalizarChave) ?? null)
          : natureza === "sugestao"
            ? (sugestoes?.map(normalizarSugestao) ?? null)
            : natureza === "responsavel"
              ? (solicitacoesDoResponsavel?.map(normalizarSolicitacaoDoResponsavel) ?? null)
              : null;

  return (
    <Moldura>
      <Cabecalho titulo="Filas" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {!ehAdmin && (
        <Aviso tipo="atencao">
          Esta área é do Admin. Fale com um Admin da comunidade se precisar avaliar uma
          solicitação.
        </Aviso>
      )}

      {ehAdmin && (
        <>
          {erro && <Aviso tipo="erro">{erro}</Aviso>}

          <div className="cg-campo">
            <label htmlFor={idDoFiltro}>Natureza</label>
            <select
              id={idDoFiltro}
              value={natureza}
              onChange={(evento) => selecionarNatureza(evento.target.value as Natureza)}
            >
              {NATUREZAS.map((item) => (
                <option key={item.chave} value={item.chave}>
                  {item.rotulo}
                </option>
              ))}
            </select>
          </div>

          {selecionada?.natureza === "participacao" && (
            <AvaliacaoDaSolicitacao
              solicitacao={selecionada.item}
              onFechar={() => definirSelecionada(null)}
              onAvaliado={(atualizada) => {
                definirSelecionada({ natureza: "participacao", item: atualizada });
                carregar();
              }}
            />
          )}
          {selecionada?.natureza === "dados" && (
            <AvaliacaoDeDados
              solicitacao={selecionada.item}
              onFechar={() => definirSelecionada(null)}
              onAvaliado={(atualizada) => {
                definirSelecionada({ natureza: "dados", item: atualizada });
                carregar();
              }}
            />
          )}
          {selecionada?.natureza === "chave" && (
            <AvaliacaoDeChave
              solicitacao={selecionada.item}
              onFechar={() => definirSelecionada(null)}
              onAvaliado={(atualizada) => {
                definirSelecionada({ natureza: "chave", item: atualizada });
                carregar();
              }}
            />
          )}
          {selecionada?.natureza === "sugestao" && (
            <AvaliacaoDeSugestao
              sugestao={selecionada.item}
              onFechar={() => definirSelecionada(null)}
              onAvaliado={(atualizada) => {
                definirSelecionada({ natureza: "sugestao", item: atualizada });
                carregar();
              }}
            />
          )}
          {selecionada?.natureza === "responsavel" && (
            <TratamentoDaSolicitacaoDoResponsavel
              solicitacao={selecionada.item}
              onFechar={() => definirSelecionada(null)}
              onTratada={(atualizada) => {
                definirSelecionada({ natureza: "responsavel", item: atualizada });
                carregar();
              }}
            />
          )}
          {natureza === "desafio_extra" && <AvaliacaoDoDesafioExtra />}
          {!selecionada && natureza !== "desafio_extra" && (
            <ListaDeFilas
              itens={itensDaListaAtual}
              mensagemVazia={MENSAGEM_VAZIA[natureza]}
              aoSelecionar={aoSelecionarId}
            />
          )}
        </>
      )}
    </Moldura>
  );
}
