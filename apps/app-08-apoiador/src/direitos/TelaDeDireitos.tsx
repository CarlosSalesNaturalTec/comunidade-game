import { useSessao } from "comum/autenticacao";
import { Cabecalho, Moldura } from "comum/react";

interface LinhaDeDado {
  dado: string;
  finalidade: string;
  baseLegal: string;
  retencao: string;
  quemAcessa: string;
}

const RETENCAO_DO_CADASTRO = "Enquanto durar o cadastro";
const BASE_LEGAL_CONSENTIMENTO = "Consentimento";

// A tabela do PRD-14 §11 — fonte única do que é exibido aqui; mudança na
// §11 exige mudar esta lista junto (mesmo precedente das Apps 03 e 09).
const DADOS: LinhaDeDado[] = [
  {
    dado: "Nome ou razão social",
    finalidade: "Identificar o Apoiador e o aporte",
    baseLegal: BASE_LEGAL_CONSENTIMENTO,
    retencao: RETENCAO_DO_CADASTRO,
    quemAcessa: "Gestão e público (nick)",
  },
  {
    dado: "E-mail",
    finalidade: "Dar acesso à aplicação e responder ao pedido",
    baseLegal: BASE_LEGAL_CONSENTIMENTO,
    retencao: RETENCAO_DO_CADASTRO,
    quemAcessa: "Gestão",
  },
  {
    dado: "WhatsApp",
    finalidade: "Contato da gestão com o Apoiador",
    baseLegal: BASE_LEGAL_CONSENTIMENTO,
    retencao: RETENCAO_DO_CADASTRO,
    quemAcessa: "Gestão",
  },
  {
    dado: "Comprovante de transferência",
    finalidade: "Provar o aporte e homologá-lo",
    baseLegal: "Obrigação legal",
    retencao: "Permanente, junto ao lançamento",
    quemAcessa: "Gestão",
  },
  {
    dado: "Documentos comprobatórios",
    finalidade: "Comprovar o apoio na página pública",
    baseLegal: BASE_LEGAL_CONSENTIMENTO,
    retencao: RETENCAO_DO_CADASTRO,
    quemAcessa: "Gestão e público",
  },
  {
    dado: "Avatar e nick",
    finalidade: "Identidade pública do Apoiador",
    baseLegal: BASE_LEGAL_CONSENTIMENTO,
    retencao: RETENCAO_DO_CADASTRO,
    quemAcessa: "Público",
  },
  {
    dado: "Perfil pessoa física ou jurídica",
    finalidade: "Definir a escada de valores e o recorte do painel",
    baseLegal: BASE_LEGAL_CONSENTIMENTO,
    retencao: RETENCAO_DO_CADASTRO,
    quemAcessa: "Gestão",
  },
  {
    dado: "Justificativa do vínculo",
    finalidade: "Aprovar o desafio direcionado",
    baseLegal: "Interesse legítimo",
    retencao: "Permanente, junto ao desafio",
    quemAcessa: "Gestão",
  },
  {
    dado: "Proposta registrada",
    finalidade: "Evolução da plataforma",
    baseLegal: BASE_LEGAL_CONSENTIMENTO,
    retencao: "90 dias após o retorno; permanente se adotada",
    quemAcessa: "Gestão",
  },
];

interface Props {
  /** Caminho de volta para a porta pública, só usado sem sessão. */
  aoVoltar?: () => void;
}

// Área de leitura: apresenta o destino e o uso de cada dado que o Apoiador
// coleta, na tabela do PRD-14 §11. Sem dado fiscal nem bancário, e sem
// escrita, exclusão ou exportação aqui — o pedido de acesso, correção ou
// exclusão é feito à gestão (`RF-14-58`). Existe sem sessão e durante a
// troca da senha provisória, porque a porta pública e a troca coletam
// dado antes de a navegação normal existir; `aoVoltar` cobre essas duas
// telas trancadas, sem abrir um caminho de contorno novo — a ação de sair
// só aparece na navegação normal, com sessão e sem `aoVoltar` (design —
// decisão 4).
export function TelaDeDireitos({ aoVoltar }: Props) {
  const { sessao, sair } = useSessao();

  return (
    <Moldura>
      <Cabecalho
        titulo="Direitos e dados"
        acao={
          aoVoltar
            ? { rotulo: "Voltar", aoAcionar: aoVoltar }
            : sessao
              ? { rotulo: "Sair", aoAcionar: sair }
              : undefined
        }
      />

      <table className="cg-tabela-de-direitos">
        <caption>
          O que a App 08 coleta, para quê, com que base legal, por quanto tempo e quem acessa
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
        <li>
          A plataforma não coleta CPF, CNPJ nem documento de identidade e não armazena chave
          nem conta.
        </li>
        <li>
          O pedido de acesso, correção ou exclusão de dado é feito à gestão. O comprovante do
          aporte já homologado permanece, por ser prova contábil do lançamento.
        </li>
      </ul>
    </Moldura>
  );
}
