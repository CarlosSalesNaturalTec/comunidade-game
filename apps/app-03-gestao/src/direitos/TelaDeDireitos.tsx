import { useSessao } from "comum/autenticacao";
import { Cabecalho, Moldura } from "comum/react";

interface LinhaDeDado {
  dado: string;
  finalidade: string;
  baseLegal: string;
  retencao: string;
  quemAcessa: string;
}

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
  const { sair } = useSessao();

  return (
    <Moldura>
      <Cabecalho titulo="Direitos e dados" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      <table className="cg-tabela-de-direitos">
        <caption>
          O que a gestão coleta, para quê, com que base legal, por quanto tempo e quem acessa
        </caption>
        <thead>
          <tr>
            <th scope="col">Dado coletado</th>
            <th scope="col">Finalidade</th>
            <th scope="col">Base legal</th>
            <th scope="col">Retenção</th>
            <th scope="col">Quem acessa</th>
          </tr>
        </thead>
        <tbody>
          {DADOS.map((linha) => (
            <tr key={linha.dado}>
              <th scope="row">{linha.dado}</th>
              <td>{linha.finalidade}</td>
              <td>{linha.baseLegal}</td>
              <td>{linha.retencao}</td>
              <td>{linha.quemAcessa}</td>
            </tr>
          ))}
        </tbody>
      </table>

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
