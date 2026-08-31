export interface ItemDaFilaDePresenca {
  aula_id: string;
  nick: string;
  momento_do_fato: string;
}

function chaveDaFila(aulaId: string): string {
  return `app-01:fila-de-presenca:${aulaId}`;
}

// A fila guarda apenas presença — `aula_id`, `nick` e `momento_do_fato` —,
// nunca imagem, descritor ou _template_ (`RN-04-12`, `RN-04-13`, PRD-04 §8).
// Vive em `localStorage`, não em memória: recarregar a página na queda não
// pode perder quem já entrou (design — decisão 8).
export function lerFilaDePresenca(aulaId: string): ItemDaFilaDePresenca[] {
  try {
    const bruto = localStorage.getItem(chaveDaFila(aulaId));
    if (!bruto) return [];
    const itens = JSON.parse(bruto);
    return Array.isArray(itens) ? itens : [];
  } catch {
    return [];
  }
}

function gravarFilaDePresenca(aulaId: string, itens: ItemDaFilaDePresenca[]): void {
  localStorage.setItem(chaveDaFila(aulaId), JSON.stringify(itens));
}

export function enfileirarPresenca(item: ItemDaFilaDePresenca): void {
  gravarFilaDePresenca(item.aula_id, [...lerFilaDePresenca(item.aula_id), item]);
}

// O item some da fila assim que o núcleo o aceita — inclusive quando
// devolve o registro que já existia, que é sucesso (`RF-04-25`).
export function removerDaFilaDePresenca(item: ItemDaFilaDePresenca): void {
  const restante = lerFilaDePresenca(item.aula_id).filter(
    (candidato) =>
      !(candidato.nick === item.nick && candidato.momento_do_fato === item.momento_do_fato),
  );
  gravarFilaDePresenca(item.aula_id, restante);
}
