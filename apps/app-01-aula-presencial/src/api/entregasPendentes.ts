import { chamarNucleo } from "comum/api";

/** A pendência do encontro, como o núcleo a serve: nick e avatar de quem
 * conquistou, a trilha, o marco, o tipo de recurso e a quantidade. Nunca
 * valor em moedas nem em reais (`RF-09-75`, invariantes 12 e 16). */
export interface PendenciaDeEntrega {
  guerreiro_id: string;
  guerreiro_nick: string;
  guerreiro_avatar: string;
  trilha_id: string;
  trilha_nome: string;
  missao_id: string;
  missao_titulo: string;
  recompensa_de_marco_id: string;
  tipo_de_recurso_id: string;
  // O nome e a unidade do tipo, que o núcleo serve junto: sem eles a tela só
  // tem a quantidade a dizer, sem distinguir o livro da camisa nem do kit.
  tipo_de_recurso_nome: string;
  tipo_de_recurso_unidade: string;
  quantidade: string;
  quantidade_esgotada: boolean;
}

export interface EntregaRegistrada {
  id: string;
  recompensa_de_marco_id: string;
  guerreiro_id: string;
  ponto_de_apoio_id: string;
  lancamento_id: string;
  registrado_em: string;
}

// A fila **do encontro**: recortada pela aula, alcança só quem tem presença
// registrada nela, e vai sempre sob o token de trabalho — quem lê é o Mestre
// que abriu o aparelho (`RF-09-75`, design — decisão 1).
export function listarEntregasPendentesDoEncontro(
  aulaId: string,
  tokenDeTrabalho: string,
): Promise<PendenciaDeEntrega[]> {
  return chamarNucleo<PendenciaDeEntrega[]>(
    `/v1/recompensas-de-marco/pendentes?aula_id=${encodeURIComponent(aulaId)}`,
    { token: tokenDeTrabalho },
  );
}

// A confirmação declara a **aula**, nunca o ponto de apoio: no encontro o
// recurso sai do ponto de apoio que a aula declara, e os dois campos são
// mutuamente exclusivos no núcleo (`RF-09-76`, `RF-07-13`, documento 02 §8.1,
// design — decisão 2).
export function confirmarEntregaNoEncontro(
  recompensaDeMarcoId: string,
  entrada: { guerreiro_id: string; aula_id: string },
  tokenDeTrabalho: string,
): Promise<EntregaRegistrada> {
  return chamarNucleo<EntregaRegistrada>(
    `/v1/recompensas-de-marco/${recompensaDeMarcoId}/entregas`,
    { metodo: "POST", corpo: entrada, token: tokenDeTrabalho },
  );
}
