import { chamarNucleo } from "comum/api";

interface ComunidadePublica {
  id: string;
  nome: string;
}

// Só o nome interessa aqui — a escolha de comunidade, quando há mais de
// uma aula vigente (`RF-04-03`). Leitura pública.
export async function buscarNomeDaComunidade(id: string): Promise<string> {
  const comunidade = await chamarNucleo<ComunidadePublica>(`/v1/comunidades/${id}`);
  return comunidade.nome;
}
