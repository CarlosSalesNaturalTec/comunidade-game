import { chamarNucleo } from "comum/api";

export interface AulaVigente {
  id: string;
  comunidade_virtual_id: string;
  inicio_em: string;
  fim_em: string;
}

interface PaginaDeAulas {
  itens: AulaVigente[];
  proximo_cursor: string | null;
}

// Pública quanto à persona — chave de aplicação sim, credencial não — e é
// relida ao abrir a sessão de trabalho e a cada volta à tela inicial, para
// que a janela da aula seja sempre a que o núcleo diz ser vigente agora
// (`RF-04-02`, `RF-04-05`, design — decisão 3).
export function listarAulasVigentes(): Promise<PaginaDeAulas> {
  return chamarNucleo<PaginaDeAulas>("/v1/aulas/vigentes");
}
