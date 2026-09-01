import { chamarNucleo } from "comum/api";

export interface DocumentoDoApoiador {
  id: string;
  endereco: string;
  rotulo: string;
  publicado: boolean;
}

export interface DeclararDocumentoEntrada {
  endereco: string;
  rotulo: string;
}

// A prova do apoio, sempre link declarado — nunca anexo de arquivo. Nasce
// pendente e só o Admin, anexando ao cadastro, publica (`RF-14-18`,
// `RF-14-19`, `RN-14-12`).
export function declararDocumento(
  entrada: DeclararDocumentoEntrada,
  token: string,
): Promise<DocumentoDoApoiador> {
  return chamarNucleo<DocumentoDoApoiador>("/v1/eu/apoiador/documentos", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// O que o Apoiador declarou e o que já está publicado na página dele
// (`RF-14-20`).
export function listarMeusDocumentos(token: string): Promise<DocumentoDoApoiador[]> {
  return chamarNucleo<DocumentoDoApoiador[]>("/v1/eu/apoiador/documentos", { token });
}
