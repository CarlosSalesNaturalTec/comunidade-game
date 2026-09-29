/** O garfo da entrada: a chamada pergunta **o que a pessoa traz** e encaminha
 * conforme a resposta (documentos 02 §1 e 14 §§10, 11). São as sete
 * modalidades da tabela do documento 14 §10, cada uma com o comprobatório que
 * ela pede, e **só dois destinos**, os que já existem: o pré-cadastro da App 08
 * e o formulário de participação da vitrine.
 *
 * O garfo **só encaminha**: nenhum campo novo no formulário e nenhum atributo
 * novo no núcleo — quem traz material, serviço, conteúdo, código, divulgação ou
 * quer ensinar descreve isso na apresentação e nos links comprobatórios que o
 * `RF-03-28` já aceita (decisão do fundador, 2026-09-29; design — decisão 2). */
export type DestinoDaModalidade = "pre-cadastro" | "formulario";

export interface Modalidade {
  chave: string;
  rotulo: string;
  destino: DestinoDaModalidade;
  comprobatorio: string;
}

export const MODALIDADES: Modalidade[] = [
  {
    chave: "dinheiro",
    rotulo: "Dinheiro",
    destino: "pre-cadastro",
    comprobatorio: "Comprovante da transferência",
  },
  {
    chave: "insumo",
    rotulo: "Insumo, equipamento ou alimento",
    destino: "formulario",
    comprobatorio: "Descrição e foto do bem",
  },
  {
    chave: "servico",
    rotulo: "Serviço",
    destino: "formulario",
    comprobatorio: "O que faz e quando pode",
  },
  {
    chave: "conteudo",
    rotulo: "Conteúdo educacional",
    destino: "formulario",
    comprobatorio: "Amostra do material",
  },
  {
    chave: "codigo",
    rotulo: "Código",
    destino: "formulario",
    comprobatorio: "Repositório e portfólio",
  },
  {
    chave: "divulgacao",
    rotulo: "Divulgação",
    destino: "formulario",
    comprobatorio: "Alcance e mídia própria",
  },
  {
    chave: "ensinar",
    rotulo: "Quero ensinar",
    destino: "formulario",
    comprobatorio: "Artefatos da habilidade",
  },
];
