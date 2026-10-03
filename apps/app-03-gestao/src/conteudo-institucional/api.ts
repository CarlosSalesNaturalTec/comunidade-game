import { chamarNucleo } from "comum/api";

export type SecaoInstitucional = "quem-somos" | "contatos" | "como-apoiar";

// A ordem é fixa e vem do núcleo; o rótulo é desta tela, porque é o que o
// Admin lê (`RF-02-80`, `RF-03-45`).
export const SECOES: { chave: SecaoInstitucional; rotulo: string }[] = [
  { chave: "quem-somos", rotulo: "Quem somos" },
  { chave: "contatos", rotulo: "Contatos" },
  { chave: "como-apoiar", rotulo: "Como apoiar" },
];

// O vídeo de apresentação só existe em "Quem somos" — o núcleo recusa o link
// nas outras duas seções (`RF-03-49`).
export const SECAO_COM_VIDEO: SecaoInstitucional = "quem-somos";

export interface SecaoPublicada {
  secao: SecaoInstitucional;
  texto: string | null;
  video_url: string | null;
  // Nulos enquanto a seção nunca foi publicada, e nulos também quando quem
  // gravou foi a semeadura da implantação, que não tem persona.
  autor_id: string | null;
  publicado_em: string | null;
}

// Leitura de Admin: a pública, sob `/vitrine`, omite o autor de propósito, e
// autor e data são justamente o que esta tela precisa apresentar
// (`RF-02-80`, `RF-03-45`).
export function lerConteudoInstitucional(token: string): Promise<SecaoPublicada[]> {
  return chamarNucleo<SecaoPublicada[]>("/v1/conteudo-institucional", { token });
}

export interface PublicarSecaoEntrada {
  texto: string;
  video_url?: string | null;
}

export function publicarSecao(
  secao: SecaoInstitucional,
  entrada: PublicarSecaoEntrada,
  token: string,
): Promise<SecaoPublicada> {
  return chamarNucleo<SecaoPublicada>(`/v1/conteudo-institucional/${secao}`, {
    metodo: "PUT",
    corpo: entrada,
    token,
  });
}
