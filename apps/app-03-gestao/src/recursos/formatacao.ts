// Só formata o número que o núcleo devolveu — nunca converte nem soma
// (`RF-02-58`, `RF-02-45`, `RN-02-19`, design — decisão 4).
function formatarNumero(valor: string): string | null {
  const numero = Number(valor);
  if (valor.trim() === "" || Number.isNaN(numero)) return null;
  return numero.toLocaleString("pt-BR", { maximumFractionDigits: 2 });
}

export function formatarQuantidade(valor: string, unidade?: string): string {
  const numero = formatarNumero(valor);
  if (numero === null) return valor;
  return unidade ? `${numero} ${unidade}` : numero;
}

export function formatarMoedas(valor: string): string {
  const numero = formatarNumero(valor);
  if (numero === null) return valor;
  return `${numero} ${Number(valor) === 1 ? "moeda" : "moedas"}`;
}
