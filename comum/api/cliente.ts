import type { CorpoDeErro } from "./tipos";

const NOME_DO_CABECALHO_DA_CHAVE = "X-Chave-Aplicacao";
const NOME_DO_CABECALHO_DE_SESSAO = "Authorization";

/** O corpo de erro único do PRD-01, com os dois cabeçalhos sempre presentes
 * em toda chamada (`RF-01-02`, `RN-01-32`). */
export class ErroDaApi extends Error {
  readonly status: number;
  readonly codigo: string;
  readonly campo?: string;
  readonly sugestoes?: string[];

  constructor(status: number, corpo: CorpoDeErro) {
    super(corpo.mensagem);
    this.status = status;
    this.codigo = corpo.codigo;
    this.campo = corpo.campo;
    this.sugestoes = corpo.sugestoes;
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

interface ConfiguracaoDeAcesso {
  chaveDeAplicacao: string;
  urlDoNucleo: string;
}

// A chave e a URL não vêm embutidas em `comum/` — cada aplicação as declara
// e chama esta função uma vez, no `main.tsx`, antes de renderizar (design —
// decisão 6). Sem isso, `chamarNucleo` falha explícito em vez de partir com
// cabeçalho de chave vazio.
let configuracao: ConfiguracaoDeAcesso | null = null;

export function configurarAcessoAoNucleo(config: ConfiguracaoDeAcesso): void {
  configuracao = config;
}

function obterConfiguracao(): ConfiguracaoDeAcesso {
  if (!configuracao) {
    throw new Error(
      "chamarNucleo foi chamado antes de configurarAcessoAoNucleo — configure o acesso " +
        "ao núcleo no main.tsx da aplicação antes de renderizar.",
    );
  }
  return configuracao;
}

interface OpcoesDeChamada {
  metodo?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
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
  const { chaveDeAplicacao, urlDoNucleo } = obterConfiguracao();

  const cabecalhos: Record<string, string> = {
    [NOME_DO_CABECALHO_DA_CHAVE]: chaveDeAplicacao,
  };
  if (opcoes.token) {
    cabecalhos[NOME_DO_CABECALHO_DE_SESSAO] = `Bearer ${opcoes.token}`;
  }
  if (opcoes.corpo !== undefined) {
    cabecalhos["Content-Type"] = "application/json";
  }

  const resposta = await fetch(`${urlDoNucleo}${caminho}`, {
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

export interface ResultadoDoEnvioDeParte {
  concluido: boolean;
  /** Bytes que o armazenamento confirma ter recebido até agora — é daqui
   * que a retomada depois de queda de rede sabe de onde continuar
   * (`RF-09-19`). */
  bytesRecebidos: number;
}

// Envia uma parte do arquivo pelo protocolo `Content-Range` da sessão
// retomável (`abrir_envio`). O endereço da sessão pode ser relativo — a
// rota local do núcleo, fora de produção — ou absoluto — o Cloud Storage
// em produção, que é credencial própria e não recebe a chave do projeto
// (design — Risks). Usa `XMLHttpRequest`, não `fetch`, porque só ele
// expõe o progresso do envio.
export function enviarParteComProgresso(
  enderecoDaSessao: string,
  parte: Blob,
  contentRange: string,
  aoProgredir: (bytesEnviados: number) => void,
): Promise<ResultadoDoEnvioDeParte> {
  const { chaveDeAplicacao, urlDoNucleo } = obterConfiguracao();
  const relativo = !enderecoDaSessao.startsWith("http");
  const url = relativo ? `${urlDoNucleo}${enderecoDaSessao}` : enderecoDaSessao;

  return new Promise((resolve, reject) => {
    const requisicao = new XMLHttpRequest();
    requisicao.open("PUT", url);
    requisicao.setRequestHeader("Content-Range", contentRange);
    if (relativo) {
      requisicao.setRequestHeader(NOME_DO_CABECALHO_DA_CHAVE, chaveDeAplicacao);
    }
    requisicao.upload.onprogress = (evento) => {
      if (evento.lengthComputable) aoProgredir(evento.loaded);
    };
    requisicao.onload = () => {
      if (requisicao.status === 200 || requisicao.status === 201) {
        resolve({ concluido: true, bytesRecebidos: parte.size });
        return;
      }
      if (requisicao.status === 308) {
        const faixa = requisicao.getResponseHeader("Range");
        const bytesRecebidos = faixa ? Number(faixa.split("-")[1]) + 1 : 0;
        resolve({ concluido: false, bytesRecebidos });
        return;
      }
      reject(new Error("Não foi possível enviar o arquivo."));
    };
    requisicao.onerror = () => reject(new Error("Não foi possível enviar o arquivo."));
    requisicao.send(parte);
  });
}
