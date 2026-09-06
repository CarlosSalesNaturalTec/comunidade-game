import type { ColunaDaTabela } from "comum/react";
import { Cabecalho, Moldura, Tabela } from "comum/react";

interface LinhaDeDado {
  dado: string;
  finalidade: string;
  baseLegal: string;
  retencao: string;
  quemAcessa: string;
}

const COLUNAS: ColunaDaTabela<LinhaDeDado>[] = [
  {
    chave: "dado",
    rotulo: "Dado coletado",
    cabecalhoDeLinha: true,
    renderizar: (l) => l.dado,
  },
  { chave: "finalidade", rotulo: "Finalidade", renderizar: (l) => l.finalidade },
  {
    chave: "baseLegal",
    rotulo: "Base legal",
    recolhida: true,
    renderizar: (l) => l.baseLegal,
  },
  {
    chave: "retencao",
    rotulo: "Retenção",
    recolhida: true,
    renderizar: (l) => l.retencao,
  },
  {
    chave: "quemAcessa",
    rotulo: "Quem acessa",
    recolhida: true,
    renderizar: (l) => l.quemAcessa,
  },
];

const RETENCAO_DO_VINCULO = "Enquanto durar o vínculo";
const RETENCAO_DA_FILA = "Enquanto durar a fila";

// A tabela do PRD-02 §11 — fonte única do que é exibido aqui; mudança na
// §11 exige mudar esta lista junto (design — risco 1).
const DADOS: LinhaDeDado[] = [
  {
    dado: "Cadastro do Guerreiro(a)",
    finalidade: "Identificação e operação",
    baseLegal: "Consentimento",
    retencao: RETENCAO_DO_VINCULO,
    quemAcessa: "Gestão e responsável",
  },
  {
    dado: "Presença e resultado de atividade",
    finalidade: "Registro da participação",
    baseLegal: "Consentimento",
    retencao: RETENCAO_DO_VINCULO,
    quemAcessa: "Gestão e responsável",
  },
  {
    dado: "Infração e pontuação negativa",
    finalidade: "Aplicação do Código de Conduta",
    baseLegal: "Interesse público",
    retencao: RETENCAO_DO_VINCULO,
    quemAcessa: "Gestão e responsável",
  },
  {
    dado: "Contato do responsável",
    finalidade: "Canal oficial com a família",
    baseLegal: "Consentimento",
    retencao: RETENCAO_DO_VINCULO,
    quemAcessa: "Gestão",
  },
  {
    dado: "Artefatos comprobatórios de adulto",
    finalidade: "Provar habilidade ou apoio",
    baseLegal: "Consentimento",
    retencao: RETENCAO_DO_VINCULO,
    quemAcessa: "Gestão e visitante",
  },
  {
    dado: "Solicitação de participação",
    finalidade: "Avaliar quem pede para participar",
    baseLegal: "Consentimento",
    retencao: RETENCAO_DA_FILA,
    quemAcessa: "Gestão",
  },
  {
    dado: "Solicitação de dados",
    finalidade: "Avaliar e registrar a entrega",
    baseLegal: "Consentimento",
    retencao: RETENCAO_DA_FILA,
    quemAcessa: "Gestão",
  },
  {
    dado: "Auditoria das ações de gestão",
    finalidade: "Rastreabilidade",
    baseLegal: "Interesse público",
    retencao: "Permanente",
    quemAcessa: "Admin",
  },
];

// Área de leitura: apresenta o destino e o uso de cada dado que a gestão
// coleta, na tabela do PRD-02 §11, mais os pontos que a §11 declara em
// prosa. Nenhuma escrita, exclusão ou exportação aqui (`RF-02-64`).
export function TelaDeDireitos() {
  return (
    <Moldura variante="densa">
      <Cabecalho titulo="Direitos e dados" />

      <Tabela
        legenda="O que a gestão coleta, para quê, com que base legal, por quanto tempo e quem acessa"
        colunas={COLUNAS}
        linhas={DADOS}
        chaveDaLinha={(linha) => linha.dado}
      />

      <ul>
        <li>A gestão não vê a imagem do Guerreiro(a): aqui só aparecem o avatar e o nick.</li>
        <li>O responsável exerce os direitos de acesso, correção e exclusão pela App 07.</li>
        <li>
          O registro de dado do território é despersonalizado quando revogado — nunca apagado.
        </li>
        <li>
          O registro de infração fica restrito à gestão e ao responsável do Guerreiro(a).
        </li>
      </ul>
    </Moldura>
  );
}
