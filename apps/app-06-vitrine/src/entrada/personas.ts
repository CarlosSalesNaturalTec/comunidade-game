import {
  URL_DA_APP_01_AULA,
  URL_DA_APP_03_GESTAO,
  URL_DA_APP_05_GUERREIRO,
  URL_DA_APP_07_RESPONSAVEL,
  URL_DA_APP_08_APOIADOR,
  URL_DA_APP_09_MESTRE,
} from "../api/configuracao";
import { CAMINHO_DA_PARTICIPACAO } from "../navegacao/caminhos";

export type ChaveDePersona =
  | "guerreiro"
  | "responsavel"
  | "mestre"
  | "apoiador"
  | "gestao"
  | "aparelho-da-aula";

/** A orientação de quem **ainda não tem cadastro** (`RF-03-62`). O PRD-03 §5.9
 * escreve quatro: pré-cadastro para quem quer ser Apoiador, formulário de
 * participação para quem quer ser Mestre, e procurar a gestão no encontro para
 * responsável e Guerreiro(a). Gestão e aparelho da aula não recebem orientação
 * porque o PRD não lhes dá uma — Admin é ato do projeto e o aparelho da aula não
 * é pessoa que se cadastra. */
export interface OrientacaoSemCadastro {
  texto: string;
  /** Endereço da orientação, quando existe. O do Mestre é o formulário de
   * participação da própria vitrine (`RF-03-62`). */
  url?: string;
  rotuloDoLink?: string;
}

export interface Persona {
  chave: ChaveDePersona;
  rotulo: string;
  nomeDoDestino: string;
  url: string;
  orientacaoSemCadastro?: OrientacaoSemCadastro;
}

const PROCURAR_A_GESTAO: OrientacaoSemCadastro = {
  texto:
    "Entrar não cria cadastro. Quem ainda não tem cadastro procura a gestão no encontro, " +
    "que faz o cadastro pessoalmente.",
};

export const PERSONAS: Persona[] = [
  {
    chave: "guerreiro",
    rotulo: "Sou Guerreiro ou Guerreira",
    nomeDoDestino: "Minha Área",
    url: URL_DA_APP_05_GUERREIRO,
    orientacaoSemCadastro: PROCURAR_A_GESTAO,
  },
  {
    chave: "responsavel",
    rotulo: "Sou responsável por um Guerreiro ou Guerreira",
    nomeDoDestino: "Área dos responsáveis",
    url: URL_DA_APP_07_RESPONSAVEL,
    orientacaoSemCadastro: PROCURAR_A_GESTAO,
  },
  {
    chave: "mestre",
    rotulo: "Sou Mestre",
    nomeDoDestino: "Área do Mestre",
    url: URL_DA_APP_09_MESTRE,
    orientacaoSemCadastro: {
      texto:
        "Entrar não cria cadastro. Quem quer ser Mestre preenche o formulário de " +
        "solicitação de participação da vitrine, que um Admin avalia em até 7 dias.",
      url: CAMINHO_DA_PARTICIPACAO,
      rotuloDoLink: "Abrir o formulário de participação",
    },
  },
  {
    chave: "apoiador",
    rotulo: "Sou Apoiador",
    nomeDoDestino: "Área do Apoiador",
    url: URL_DA_APP_08_APOIADOR,
    orientacaoSemCadastro: {
      texto:
        "Entrar não cria cadastro. Quem quer ser Apoiador começa pelo pré-cadastro da " +
        "Área do Apoiador, que um Admin avalia em até 7 dias.",
      url: URL_DA_APP_08_APOIADOR,
      rotuloDoLink: "Ir ao pré-cadastro da Área do Apoiador",
    },
  },
  {
    chave: "gestao",
    rotulo: "Sou da gestão",
    nomeDoDestino: "Gestão",
    url: URL_DA_APP_03_GESTAO,
  },
  {
    chave: "aparelho-da-aula",
    rotulo: "Este é o aparelho da aula",
    nomeDoDestino: "Aula presencial",
    url: URL_DA_APP_01_AULA,
  },
];
