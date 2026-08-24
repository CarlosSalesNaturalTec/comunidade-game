import { chamarNucleo } from "comum/api";

export interface GuerreiroCadastrado {
  id: string;
  nome: string;
  nascimento: string;
  nick: string;
  avatar: string;
}

interface CadastroDoEncontro {
  nome: string;
  nascimento: string;
  nick: string;
  avatar: string;
  aula_id: string;
}

// A sessão de trabalho do aparelho autentica sem ser autora: a chave da
// App 01 já leva o núcleo ao caminho do encontro, que cria a persona sem
// criador (`RF-04-07`, `RF-04-10`, `RN-04-04`, design — decisão 1). A
// recusa por nick em uso chega como `ErroDaApi` com `campo === "nick"` e
// `sugestoes` preenchidas (`RF-04-08`); a recusa por idade fora da faixa
// chega com `campo === "nascimento"` (`RF-04-09`).
export function cadastrarGuerreiroNoEncontro(
  entrada: CadastroDoEncontro,
  tokenDeTrabalho: string,
): Promise<GuerreiroCadastrado> {
  return chamarNucleo<GuerreiroCadastrado>("/v1/guerreiros", {
    metodo: "POST",
    corpo: entrada,
    token: tokenDeTrabalho,
  });
}
