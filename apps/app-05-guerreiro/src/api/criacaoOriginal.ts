import { chamarNucleo, ErroDaApi, enviarParteComProgresso } from "comum/api";

export type TipoDeProducaoDaCriacaoOriginal =
  | "texto"
  | "imagem"
  | "link_externo"
  | "video"
  | "arquivo";
export type SituacaoDaCriacaoOriginal = "entregue" | "validada" | "devolvida";

export interface CriacaoOriginal {
  id: string;
  trilha_id: string;
  equipe_id: string | null;
  guerreiro_id: string | null;
  tipo: TipoDeProducaoDaCriacaoOriginal;
  producao: string | null;
  referencia: string | null;
  tamanho: number | null;
  situacao: SituacaoDaCriacaoOriginal;
  motivo_da_devolucao: string | null;
}

export interface EntregarCriacaoEntrada {
  equipe_id?: string;
  tipo: TipoDeProducaoDaCriacaoOriginal;
  producao?: string;
}

// A trilha da entrega é resolvida pelo núcleo a partir da culminância
// endereçada; a modalidade, a coerência do tipo e a substituição antes da
// validação já são dele (`RF-05-40`, `RF-05-41`, `RF-05-42`).
export function entregarCriacaoOriginal(
  idDaCulminancia: string,
  entrada: EntregarCriacaoEntrada,
  token: string,
): Promise<CriacaoOriginal> {
  return chamarNucleo<CriacaoOriginal>(`/v1/culminancias/${idDaCulminancia}/criacoes`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// A própria entrega do Guerreiro(a) naquela trilha, em qualquer situação —
// sustenta a entrega e a devolução ao reabrir a aplicação (`RF-05-40`,
// `RF-05-42`). `null` é "ainda não entregou nada nesta trilha".
export function obterMinhaCriacaoDaTrilha(
  trilhaId: string,
  token: string,
): Promise<CriacaoOriginal | null> {
  return chamarNucleo<CriacaoOriginal>(`/v1/eu/trilhas/${trilhaId}/criacao`, { token }).catch(
    (erro) => {
      if (erro instanceof ErroDaApi && erro.codigo === "nao_encontrado") {
        return null;
      }
      throw erro;
    },
  );
}

interface AbrirEnvioSaida {
  endereco_da_sessao: string;
}

// Abre a sessão retomável de envio da mídia da criação original —
// espelha `conteudos.abrirEnvio` da App 09 (`RF-05-40`).
export function abrirEnvio(
  idDaCriacao: string,
  tipoMime: string,
  tamanhoDeclarado: number,
  token: string,
): Promise<string> {
  return chamarNucleo<AbrirEnvioSaida>(`/v1/criacoes/${idDaCriacao}/arquivo`, {
    metodo: "POST",
    corpo: { tipo_mime: tipoMime, tamanho_declarado: tamanhoDeclarado },
    token,
  }).then((saida) => saida.endereco_da_sessao);
}

// Só depois desta chamada a criação passa a servir bytes.
export function confirmarEnvio(idDaCriacao: string, token: string): Promise<CriacaoOriginal> {
  return chamarNucleo<CriacaoOriginal>(`/v1/criacoes/${idDaCriacao}/arquivo`, {
    metodo: "PATCH",
    token,
  });
}

const TAMANHO_DA_PARTE = 5 * 1024 * 1024;

// Consulta o quanto a sessão já recebeu, sem enviar bytes — sustenta a
// retomada depois de recarregar a página no meio do envio.
export async function consultarProgressoDaSessao(
  enderecoDaSessao: string,
  tamanhoDoArquivo: number,
): Promise<number> {
  const resultado = await enviarParteComProgresso(
    enderecoDaSessao,
    new Blob([]),
    `bytes */${tamanhoDoArquivo}`,
    () => {},
  );
  return resultado.bytesRecebidos;
}

// Envia o arquivo em partes, retomando de `posicaoInicial`.
export async function enviarArquivo(
  enderecoDaSessao: string,
  arquivo: File,
  aoProgredir: (bytesEnviados: number, total: number) => void,
  posicaoInicial = 0,
): Promise<void> {
  let posicao = posicaoInicial;
  const total = arquivo.size;
  while (posicao < total) {
    const fim = Math.min(posicao + TAMANHO_DA_PARTE, total);
    const parte = arquivo.slice(posicao, fim);
    const resultado = await enviarParteComProgresso(
      enderecoDaSessao,
      parte,
      `bytes ${posicao}-${fim - 1}/${total}`,
      (bytesDaParte) => aoProgredir(posicao + bytesDaParte, total),
    );
    posicao = resultado.bytesRecebidos;
    aoProgredir(posicao, total);
  }
}

export interface CreditadoNoPortfolio {
  avatar: string | null;
  nick: string;
}

export interface ItemDoPortfolio {
  id: string;
  trilha_id: string;
  tipo: TipoDeProducaoDaCriacaoOriginal;
  producao: string | null;
  referencia: string | null;
  validado_em: string | null;
  autores: CreditadoNoPortfolio[];
  publica: boolean;
}

// As criações validadas do Guerreiro(a) em sessão, com a situação de
// exposição pública (`RF-05-43`, `RF-05-44`).
export function obterPortfolio(token: string): Promise<ItemDoPortfolio[]> {
  return chamarNucleo<ItemDoPortfolio[]>("/v1/eu/portfolio", { token });
}

export interface IntegranteDaEquipe {
  avatar: string | null;
  nick: string;
  papel: string | null;
}

export interface EquipeDaTrilha {
  id: string;
  aula_id: string | null;
  integrantes: IntegranteDaEquipe[];
}

// A equipe homologada da trilha de que o Guerreiro(a) participa — só
// consulta, nunca forma nem edita (`RN-05-12`).
export function obterMinhaEquipeDaTrilha(
  trilhaId: string,
  token: string,
): Promise<EquipeDaTrilha> {
  return chamarNucleo<EquipeDaTrilha>(`/v1/eu/trilhas/${trilhaId}/equipe`, { token });
}
