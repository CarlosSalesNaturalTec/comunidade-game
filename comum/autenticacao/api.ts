import { chamarNucleo } from "../api/cliente";
import type { Papel } from "../api/tipos";

interface AberturaDeSessao {
  token: string;
  expira_em: string;
  papel: Papel;
}

export function loginSocial(idToken: string): Promise<AberturaDeSessao> {
  return chamarNucleo<AberturaDeSessao>("/v1/sessoes/social", {
    metodo: "POST",
    corpo: { id_token: idToken },
  });
}

// Usuário e senha criados pela gestão — o segundo caminho de entrada do
// adulto, ao lado do social (`RF-01-02`, `RF-14-08`).
export function loginPorCredencial(usuario: string, senha: string): Promise<AberturaDeSessao> {
  return chamarNucleo<AberturaDeSessao>("/v1/sessoes/credencial", {
    metodo: "POST",
    corpo: { usuario, senha },
  });
}

// Conclui a troca da senha provisória (`RF-01-12`); até isso acontecer,
// `eu()` recusa com `troca_de_senha_pendente` toda outra rota da sessão.
export function trocarSenha(token: string, senhaNova: string): Promise<void> {
  return chamarNucleo<void>("/v1/credenciais/senha", {
    metodo: "POST",
    corpo: { senha_nova: senhaNova },
    token,
  });
}

export function encerrarSessao(token: string): Promise<void> {
  return chamarNucleo<void>("/v1/sessoes/atual", { metodo: "DELETE", token });
}

export interface Eu {
  persona_id: string;
  papel: Papel;
  permissoes: Record<string, string[]>;
  /** Só vem para o Guerreiro(a): se a divulgação de dados foi autorizada
   * pelo responsável (`RF-05-50`). */
  divulgacao_autorizada?: boolean;
  /** Só vem para Mestre e Admin: se já há PIN de confirmação cadastrado —
   * nunca o PIN (`RF-09-121`, `RF-02-110`). */
  tem_pin_de_confirmacao?: boolean;
}

export function eu(token: string): Promise<Eu> {
  return chamarNucleo<Eu>("/v1/eu", { token });
}

// Cadastra ou troca o próprio PIN de confirmação de Mestre ou Admin — 4
// dígitos; o núcleo guarda só o verificador e não devolve nada
// (`RF-01-75`, `RF-09-121`, `RF-02-110`).
export function cadastrarPinDeConfirmacao(token: string, pin: string): Promise<void> {
  return chamarNucleo<void>("/v1/eu/pin-de-confirmacao", {
    metodo: "PUT",
    corpo: { pin },
    token,
  });
}
