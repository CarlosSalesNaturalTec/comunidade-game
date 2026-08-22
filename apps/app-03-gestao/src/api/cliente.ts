import { CHAVE_DE_APLICACAO, URL_DO_NUCLEO } from "./configuracao";
import type { CorpoDeErro } from "./tipos";

const NOME_DO_CABECALHO_DA_CHAVE = "X-Chave-Aplicacao";
const NOME_DO_CABECALHO_DE_SESSAO = "Authorization";

/** O corpo de erro único do PRD-01, com os dois cabeçalhos sempre presentes
 * em toda chamada (`RF-01-02`, `RN-01-32`). */
export class ErroDaApi extends Error {
  readonly status: number;
  readonly codigo: string;
  readonly campo?: string;

  constructor(status: number, corpo: CorpoDeErro) {
    super(corpo.mensagem);
    this.status = status;
    this.codigo = corpo.codigo;
    this.campo = corpo.campo;
  }
}

// A recusa da chave e a recusa da sessão são credenciais independentes
// (`RN-01-34`) e a tela decide diferente para cada uma: chave recusada é
// falha de implantação, sessão recusada devolve à entrada (design —
// Decisions).
const CODIGO_DE_RECUSA_DE_CHAVE = "chave_invalida";
const CODIGOS_DE_RECUSA_DE_SESSAO = new Set(["sessao_ausente", "sessao_invalida"]);

export function ehRecusaDeChave(erro: unknown): erro is ErroDaApi {
  return erro instanceof ErroDaApi && erro.codigo === CODIGO_DE_RECUSA_DE_CHAVE;
}

export function ehRecusaDeSessao(erro: unknown): erro is ErroDaApi {
  return erro instanceof ErroDaApi && CODIGOS_DE_RECUSA_DE_SESSAO.has(erro.codigo);
}

interface OpcoesDeChamada {
  metodo?: "GET" | "POST" | "PATCH" | "DELETE";
  corpo?: unknown;
  formulario?: FormData;
  token?: string | null;
}

// `formulario` serve as rotas que aceitam `multipart/form-data` — hoje só
// `POST /aportes` — sem mudar o contrato de quem já chama com `corpo`
// (`RF-02-84`). O navegador declara o `Content-Type` com o `boundary`
// sozinho; declará-lo aqui quebraria o envio.
export async function chamarNucleo<T>(
  caminho: string,
  opcoes: OpcoesDeChamada = {},
): Promise<T> {
  const cabecalhos: Record<string, string> = {
    [NOME_DO_CABECALHO_DA_CHAVE]: CHAVE_DE_APLICACAO,
  };
  if (opcoes.token) {
    cabecalhos[NOME_DO_CABECALHO_DE_SESSAO] = `Bearer ${opcoes.token}`;
  }
  if (opcoes.corpo !== undefined) {
    cabecalhos["Content-Type"] = "application/json";
  }

  const resposta = await fetch(`${URL_DO_NUCLEO}${caminho}`, {
    method: opcoes.metodo ?? "GET",
    headers: cabecalhos,
    body:
      opcoes.formulario ??
      (opcoes.corpo !== undefined ? JSON.stringify(opcoes.corpo) : undefined),
  });

  if (resposta.status === 204) {
    return undefined as T;
  }

  const corpo = (await resposta.json().catch(() => null)) as CorpoDeErro | T | null;

  if (!resposta.ok) {
    const corpoDeErro: CorpoDeErro = corpo
      ? (corpo as CorpoDeErro)
      : { codigo: "erro_de_rede", mensagem: "Não foi possível falar com o núcleo." };
    throw new ErroDaApi(resposta.status, corpoDeErro);
  }

  return corpo as T;
}
