import { chamarNucleo } from "comum/api";

export interface VerificadorDoPin {
  algoritmo: string;
  iteracoes: number;
  sal: string;
  resumo: string;
}

interface EstadoDoPin {
  personaId: string;
  verificador: VerificadorDoPin | null;
  erros: number;
  bloqueado: boolean;
}

// Mesma chave-mãe da sessão de trabalho: o verificador vive só enquanto ela
// dura e sai junto com ela. O PIN nunca é gravado — só o verificador de quem
// abriu a sessão, o contador de erros seguidos e a marca de bloqueio, para
// que recarregar a página não os zere (`RN-04-38`, design — decisão 7).
const CHAVE_DO_ESTADO_DO_PIN = "app-01:sessao-trabalho:pin";

// Cinco erros seguidos bloqueiam o PIN neste aparelho até novo login
// Google, com ou sem rede (`RN-04-38`, documento 03 §1.1).
export const ERROS_ATE_O_BLOQUEIO = 5;

export const FORMATO_DO_PIN = /^[0-9]{4}$/;

// As frases dos desfechos do PIN vivem ao lado da conferência, e não na tela
// que as usa: os três atos que pedem o PIN — confirmar identidade, encerrar a
// sessão de trabalho e abrir a bancada de medição — recusam com a **mesma**
// redação, e três cópias seriam três redações (`RN-04-41`, design —
// decisão 1).
export const MENSAGEM_DE_PIN_ERRADO =
  "PIN errado. Digite de novo o PIN de quem abriu o aparelho.";
export const MENSAGEM_DE_PIN_BLOQUEADO =
  "PIN bloqueado neste aparelho depois de cinco erros seguidos. Para confirmar de novo, " +
  "entre outra vez pelo Google.";
export const MENSAGEM_DE_PIN_NAO_CADASTRADO =
  "Quem abriu o aparelho ainda não tem PIN de confirmação. O Mestre cadastra na App 09, e o " +
  "Admin, na App 03.";
// O aparelho aberto sem que o verificador tenha chegado: não há o que
// conferir aqui, e conferir é o que o ato exige (`RN-04-38`).
export const MENSAGEM_SEM_VERIFICADOR_NO_APARELHO =
  "Este aparelho não recebeu o verificador do PIN de quem o abriu, e sem ele o PIN não pode " +
  "ser conferido aqui. Abra o aparelho de novo com rede.";

export function buscarVerificadorDoPin(tokenDeTrabalho: string): Promise<VerificadorDoPin> {
  return chamarNucleo<VerificadorDoPin>("/v1/eu/pin-de-confirmacao/verificador", {
    token: tokenDeTrabalho,
  });
}

function lerEstado(): EstadoDoPin | null {
  try {
    const bruto = sessionStorage.getItem(CHAVE_DO_ESTADO_DO_PIN);
    return bruto ? (JSON.parse(bruto) as EstadoDoPin) : null;
  } catch {
    return null;
  }
}

function gravarEstado(estado: EstadoDoPin): void {
  sessionStorage.setItem(CHAVE_DO_ESTADO_DO_PIN, JSON.stringify(estado));
}

export function estadoDoPinDe(personaId: string): EstadoDoPin | null {
  const estado = lerEstado();
  return estado?.personaId === personaId ? estado : null;
}

export function guardarVerificadorDoPin(
  personaId: string,
  verificador: VerificadorDoPin | null,
): void {
  const anterior = estadoDoPinDe(personaId);
  gravarEstado({
    personaId,
    verificador,
    erros: anterior?.erros ?? 0,
    bloqueado: anterior?.bloqueado ?? false,
  });
}

export function apagarEstadoDoPin(): void {
  sessionStorage.removeItem(CHAVE_DO_ESTADO_DO_PIN);
}

export function verificadorGuardado(): VerificadorDoPin | null {
  return lerEstado()?.verificador ?? null;
}

export function pinBloqueadoNoAparelho(): boolean {
  return lerEstado()?.bloqueado ?? false;
}

export function marcarPinBloqueado(): void {
  const estado = lerEstado();
  if (estado) gravarEstado({ ...estado, bloqueado: true });
}

/** Conta um erro seguido e diz se ele bloqueou o PIN. */
export function registrarErroDePin(): boolean {
  const estado = lerEstado();
  if (!estado) return false;
  const erros = estado.erros + 1;
  const bloqueado = erros >= ERROS_ATE_O_BLOQUEIO;
  gravarEstado({ ...estado, erros, bloqueado });
  return bloqueado;
}

export function zerarErrosDePin(): void {
  const estado = lerEstado();
  if (estado && estado.erros !== 0) gravarEstado({ ...estado, erros: 0 });
}

function deBase64(texto: string): Uint8Array<ArrayBuffer> {
  return Uint8Array.from(atob(texto), (caractere) => caractere.charCodeAt(0));
}

// A mesma derivação do núcleo — PBKDF2-HMAC-SHA256 com o sal e as iterações
// do próprio verificador —, pelo `SubtleCrypto` do navegador, sem biblioteca
// nova (design — decisão 1).
export async function pinConfereNoAparelho(
  pin: string,
  verificador: VerificadorDoPin,
): Promise<boolean> {
  const material = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(pin),
    "PBKDF2",
    false,
    ["deriveBits"],
  );
  const esperado = deBase64(verificador.resumo);
  const bits = await crypto.subtle.deriveBits(
    {
      name: "PBKDF2",
      hash: "SHA-256",
      salt: deBase64(verificador.sal),
      iterations: verificador.iteracoes,
    },
    material,
    esperado.length * 8,
  );
  const calculado = new Uint8Array(bits);
  if (calculado.length !== esperado.length) return false;
  let diferenca = 0;
  for (let indice = 0; indice < calculado.length; indice += 1) {
    diferenca |= calculado[indice] ^ esperado[indice];
  }
  return diferenca === 0;
}

/** A situação do PIN neste aparelho, antes de qualquer dígito: é ela que diz
 * se o ato pede o campo, passa sem ele ou é recusado de saída. */
export type SituacaoDoPin = "pronto" | "bloqueado" | "sem_pin_cadastrado" | "sem_verificador";

export function situacaoDoPinNoAparelho(): SituacaoDoPin {
  if (pinBloqueadoNoAparelho()) return "bloqueado";
  const estado = lerEstado();
  if (!estado) return "sem_verificador";
  return estado.verificador ? "pronto" : "sem_pin_cadastrado";
}

/** O desfecho de uma conferência: os quatro da situação, mais o PIN que não
 * confere. */
export type DesfechoDoPin = SituacaoDoPin | "confere" | "pin_errado";

// A conferência do PIN no aparelho, com os desfechos dela, num lugar só: os
// três atos que pedem o PIN — confirmar identidade, encerrar a sessão de
// trabalho e abrir a bancada — conferem o mesmo verificador, contra o mesmo
// contador de cinco erros, e cada cópia do laço seria um contador próprio
// (`RN-04-41`, `RN-04-38`, design — decisão 1).
export async function conferirPinNoAparelho(pin: string): Promise<DesfechoDoPin> {
  const situacao = situacaoDoPinNoAparelho();
  if (situacao !== "pronto") return situacao;
  const verificador = verificadorGuardado();
  if (!verificador) return "sem_verificador";
  if (!(await pinConfereNoAparelho(pin, verificador))) {
    // O quinto erro seguido bloqueia, e quem chama recusa pelo bloqueio —
    // nunca pelo erro (`RN-04-38`).
    return registrarErroDePin() ? "bloqueado" : "pin_errado";
  }
  zerarErrosDePin();
  return "confere";
}
