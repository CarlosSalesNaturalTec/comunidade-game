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
const RETENCAO_PERMANENTE_COM_LICENCA = "Permanente, sob CC BY-SA";
const RETENCAO_PERMANENTE_COM_AUTORIA = "Permanente, com autoria";
const BASE_LEGAL_CONSENTIMENTO = "Consentimento";

// A tabela do PRD-09 §11 — fonte única do que é exibido aqui; mudança na
// §11 exige mudar esta lista junto (mesmo precedente da App 03, design —
// Decisions).
const DADOS: LinhaDeDado[] = [
  {
    dado: "Artefatos comprobatórios do Mestre",
    finalidade: "Provar habilidade",
    baseLegal: BASE_LEGAL_CONSENTIMENTO,
    retencao: RETENCAO_DO_VINCULO,
    quemAcessa: "Gestão e visitante",
  },
  {
    dado: "Conteúdo autoral do Mestre",
    finalidade: "Ensinar nas trilhas",
    baseLegal: BASE_LEGAL_CONSENTIMENTO,
    retencao: RETENCAO_PERMANENTE_COM_LICENCA,
    quemAcessa: "Público",
  },
  {
    dado: "Presença e resultado de atividade",
    finalidade: "Registro da participação",
    baseLegal: BASE_LEGAL_CONSENTIMENTO,
    retencao: RETENCAO_DO_VINCULO,
    quemAcessa: "Gestão e responsável",
  },
  {
    dado: "Pontuação negativa e motivo",
    finalidade: "Aplicação do Código de Conduta",
    baseLegal: "Interesse público",
    retencao: RETENCAO_DO_VINCULO,
    quemAcessa: "Gestão e responsável",
  },
  {
    dado: "Criação original do Guerreiro(a)",
    finalidade: "Autoria, portfólio e culminância",
    baseLegal: BASE_LEGAL_CONSENTIMENTO,
    retencao: RETENCAO_PERMANENTE_COM_AUTORIA,
    quemAcessa: "Gestão e responsável",
  },
  {
    dado: "Contato do responsável",
    finalidade: "Canal oficial com a família",
    baseLegal: BASE_LEGAL_CONSENTIMENTO,
    retencao: RETENCAO_DO_VINCULO,
    quemAcessa: "Gestão",
  },
];

// Área de leitura: apresenta o destino e o uso de cada dado que o Mestre
// coleta, na tabela do PRD-09 §11, mais os pontos que a §11 declara em
// prosa. Nenhuma escrita, exclusão ou exportação aqui (`RF-09-68`).
export function TelaDeDireitos() {
  const { sair } = useSessao();

  return (
    <Moldura>
      <Cabecalho titulo="Direitos e dados" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      <table className="cg-tabela-de-direitos">
        <caption>
          O que a App 09 coleta, para quê, com que base legal, por quanto tempo e quem acessa
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
        <li>Você não vê a imagem real do Guerreiro(a) em nenhuma tela desta aplicação.</li>
        <li>
          A criação original validada só vai à vitrine com autorização do responsável — sem
          ela, continua creditada dentro da plataforma.
        </li>
        <li>
          A pontuação negativa fica restrita à gestão e ao responsável do Guerreiro(a), nunca
          em rota pública, ranking ou vitrine.
        </li>
        <li>
          O pedido de acesso, correção ou exclusão de dado chega pela App 07 e é tratado pela
          gestão.
        </li>
      </ul>
    </Moldura>
  );
}
