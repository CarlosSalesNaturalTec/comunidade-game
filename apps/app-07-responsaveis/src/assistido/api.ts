import { chamarNucleo } from "comum/api";

export interface GuerreiroVinculavel {
  id: string;
  nick: string;
  avatar: string;
}

interface Pagina<T> {
  itens: T[];
  proximo_cursor: string | null;
}

// Guerreiros e Guerreiras da comunidade do vínculo vigente de quem opera —
// a mesma leitura que a App 09 já usa para vincular responsável
// (`RF-09-62`).
export function listarGuerreirosVinculaveis(token: string): Promise<GuerreiroVinculavel[]> {
  return chamarNucleo<Pagina<GuerreiroVinculavel>>("/v1/guerreiros/vinculaveis", {
    token,
  }).then((pagina) => pagina.itens);
}

export interface ResponsavelVinculado {
  id: string;
  nome: string;
  grau_de_parentesco: string;
}

// Quem responde por aquele Guerreiro(a), para o modo assistido escolher
// qual responsável está presente (`RF-13-35`, `RN-13-03`).
export function listarResponsaveisDoGuerreiro(
  guerreiroId: string,
  token: string,
): Promise<ResponsavelVinculado[]> {
  return chamarNucleo<ResponsavelVinculado[]>(`/v1/guerreiros/${guerreiroId}/responsaveis`, {
    token,
  });
}

export interface AutorizacaoAssistidaSaida {
  id: string;
  responsavel_id: string;
  decisao: "concede" | "nega";
  registrado_em: string;
}

// O ato assistido: quem opera é a mesma pessoa que testemunha, no mesmo
// precedente do termo impresso da biometria — a versão do termo é
// carimbada pelo núcleo, nunca declarada aqui (`RF-13-35`, `RF-13-36`,
// `RF-13-38`, `RN-13-16`).
export function registrarAutorizacaoAssistida(
  guerreiroId: string,
  responsavelId: string,
  decisao: "concede" | "nega",
  testemunhaId: string,
  token: string,
): Promise<AutorizacaoAssistidaSaida> {
  return chamarNucleo<AutorizacaoAssistidaSaida>(
    `/v1/guerreiros/${guerreiroId}/autorizacao/assistida`,
    {
      metodo: "POST",
      corpo: { responsavel_id: responsavelId, decisao, testemunha_id: testemunhaId },
      token,
    },
  );
}
