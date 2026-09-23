import { guardarVerificadorDoPin, type VerificadorDoPin } from "./pinDeConfirmacao";

export const PIN_DE_TESTE = "4821";

function paraBase64(bytes: Uint8Array): string {
  return btoa(String.fromCharCode(...bytes));
}

// Só para os testes: gera o verificador como o núcleo gera — PBKDF2-SHA256,
// com poucas iterações — e o guarda como a sessão de trabalho guardaria.
export async function verificadorDeTeste(
  pin = PIN_DE_TESTE,
  iteracoes = 1_000,
): Promise<VerificadorDoPin> {
  const sal = crypto.getRandomValues(new Uint8Array(16));
  const material = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(pin),
    "PBKDF2",
    false,
    ["deriveBits"],
  );
  const bits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", hash: "SHA-256", salt: sal, iterations: iteracoes },
    material,
    256,
  );
  return {
    algoritmo: "PBKDF2-SHA256",
    iteracoes,
    sal: paraBase64(sal),
    resumo: paraBase64(new Uint8Array(bits)),
  };
}

export async function guardarVerificadorDeTeste(
  personaId = "mestre-1",
  pin = PIN_DE_TESTE,
): Promise<void> {
  guardarVerificadorDoPin(personaId, await verificadorDeTeste(pin));
}
