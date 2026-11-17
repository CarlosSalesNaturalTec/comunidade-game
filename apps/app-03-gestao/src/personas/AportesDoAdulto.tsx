import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, type ColunaDaTabela, EstadoDaLista, Tabela } from "comum/react";
import { useEffect, useState } from "react";
import { formatarMoedas, formatarQuantidade } from "../recursos/formatacao";
import { type AporteDoProvedor, type AportesDoProvedor, lerAportesDoProvedor } from "./api";

interface Props {
  provedorId: string;
}

const FORMAS: Record<string, string> = {
  financeira: "Financeira",
  material: "Material",
  servico: "Serviço",
  absorcao: "Absorção",
};

const DESTINACOES: Record<string, string> = {
  lastro: "Lastro",
  ressarcimento: "Ressarcimento",
};

const ORIGENS_DA_ESCOLHA: Record<string, string> = {
  missao: "Missão do Apoiador",
  necessidade: "Necessidade publicada",
  valor_sugerido: "Valor sugerido",
  valor_livre: "Valor livre",
};

const REAIS = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

function formatarData(valor: string): string {
  const [ano, mes, dia] = valor.slice(0, 10).split("-");
  return `${dia}/${mes}/${ano}`;
}

// Os reais nunca saem sozinhos: sempre ao lado do equivalente em moedas,
// e só nesta ficha do Admin (`RN-02-34`, documento 04 §1).
function formatarValor(aporte: AporteDoProvedor): string {
  const moedas = formatarMoedas(aporte.valor_em_moedas);
  if (aporte.valor_de_origem === null) return moedas;
  return `${moedas} (${REAIS.format(Number(aporte.valor_de_origem))})`;
}

const COLUNAS: ColunaDaTabela<AporteDoProvedor>[] = [
  {
    chave: "data",
    rotulo: "Data",
    cabecalhoDeLinha: true,
    renderizar: (aporte) => formatarData(aporte.data_do_aporte),
  },
  {
    chave: "tipo",
    rotulo: "Tipo de recurso",
    renderizar: (aporte) => aporte.tipo_de_recurso_nome,
  },
  {
    chave: "quantidade",
    rotulo: "Quantidade",
    renderizar: (aporte) =>
      formatarQuantidade(aporte.quantidade, aporte.tipo_de_recurso_unidade),
  },
  { chave: "valor", rotulo: "Valor", renderizar: formatarValor },
  {
    chave: "ponto",
    rotulo: "Ponto de apoio",
    recolhida: true,
    renderizar: (aporte) => aporte.ponto_de_apoio_nome,
  },
  {
    chave: "forma",
    rotulo: "Forma",
    recolhida: true,
    renderizar: (aporte) => FORMAS[aporte.forma] ?? aporte.forma,
  },
  {
    chave: "destinacao",
    rotulo: "Destinação",
    recolhida: true,
    renderizar: (aporte) => DESTINACOES[aporte.destinacao] ?? aporte.destinacao,
  },
  {
    chave: "comprovante",
    rotulo: "Comprovante",
    renderizar: (aporte) => (aporte.tem_comprovante ? "Com comprovante" : "Sem comprovante"),
  },
];

// Seção de leitura: NEVER oferece baixar o comprovante, nem editar,
// estornar, homologar ou recusar aporte ou declaração (`RF-02-117`,
// `RN-02-01`). A declaração pendente não tem moedas ainda — a valoração só
// nasce na homologação, pela vigência da data do aporte (`RF-07-05`).
export function AportesDoAdulto({ provedorId }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [dados, definirDados] = useState<AportesDoProvedor | null>(null);
  const [falhou, definirFalhou] = useState(false);

  useEffect(() => {
    if (!sessao) return;
    let ativo = true;
    definirDados(null);
    definirFalhou(false);
    lerAportesDoProvedor(provedorId, sessao.token)
      .then((resposta) => {
        if (ativo) definirDados(resposta);
      })
      .catch((erro) => {
        if (!ativo) return;
        if (ehRecusaDeSessao(erro)) {
          tratarRecusaDeSessao();
          return;
        }
        definirFalhou(true);
      });
    return () => {
      ativo = false;
    };
  }, [sessao, provedorId, tratarRecusaDeSessao]);

  return (
    <section aria-label="Aportes">
      <h3>Aportes</h3>
      {falhou ? (
        <Aviso tipo="erro">
          Não foi possível carregar os aportes. Tente novamente em instantes.
        </Aviso>
      ) : dados === null ? (
        <EstadoDaLista>Carregando os aportes…</EstadoDaLista>
      ) : (
        <>
          <p>
            Poder Sustentador:{" "}
            <strong>{formatarMoedas(dados.poder_sustentador_em_moedas)}</strong>
          </p>
          {dados.aportes.length === 0 ? (
            <EstadoDaLista>Ainda não há aporte registrado.</EstadoDaLista>
          ) : (
            <Tabela
              legenda="Aportes homologados"
              colunas={COLUNAS}
              linhas={dados.aportes}
              chaveDaLinha={(aporte) => aporte.id}
            />
          )}
          {dados.declaracoes_pendentes.length > 0 && (
            <>
              <h4>Declarações pendentes</h4>
              <ul aria-label="Declarações pendentes">
                {dados.declaracoes_pendentes.map((declaracao) => (
                  <li key={declaracao.id}>
                    {formatarData(declaracao.registrado_em)} —{" "}
                    {REAIS.format(Number(declaracao.valor_declarado))} declarados —{" "}
                    {ORIGENS_DA_ESCOLHA[declaracao.origem_da_escolha] ??
                      declaracao.origem_da_escolha}
                    . Em moedas, só na homologação.
                  </li>
                ))}
              </ul>
            </>
          )}
        </>
      )}
    </section>
  );
}
