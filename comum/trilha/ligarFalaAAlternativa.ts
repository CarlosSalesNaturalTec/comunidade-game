// A ligação da resposta falada da sondagem à alternativa mais próxima
// (`RF-05-98`, design — decisão 4). Função pura: nada de rede nem de modelo
// de IA — a sondagem não define nível (`RN-05-34`), e errar a ligação não
// custa nada à criança.

// Limiares técnicos da aproximação, não regra de produto: aceitar a melhor
// alternativa só quando ela é parecida o bastante **e** claramente à frente
// da segunda — empate é dúvida, e dúvida segue como transcrição literal.
const SEMELHANCA_MINIMA = 0.6;
const FOLGA_SOBRE_A_SEGUNDA = 0.15;

const LETRAS = ["a", "b", "c", "d"];
const NUMEROS: Record<string, number> = {
  "1": 1,
  um: 1,
  uma: 1,
  "2": 2,
  dois: 2,
  duas: 2,
  "3": 3,
  tres: 3,
  "4": 4,
  quatro: 4,
};
const ORDINAIS: Record<string, number> = {
  primeira: 1,
  primeiro: 1,
  segunda: 2,
  segundo: 2,
  terceira: 3,
  terceiro: 3,
  quarta: 4,
  quarto: 4,
};
// Palavras que acompanham a letra ou a posição sem mudar o sentido.
const MOLDURA = new Set([
  "a",
  "e",
  "o",
  "letra",
  "alternativa",
  "opcao",
  "resposta",
  "numero",
  "minha",
  "eu",
  "acho",
  "que",
]);

export function normalizar(texto: string): string {
  return texto
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

// "letra b", "a segunda", "alternativa 3", "b": a fala que aponta a posição.
// Só vale quando, tirada a moldura, sobra **uma** palavra que é posição.
function posicaoApontada(palavras: string[], total: number): number | null {
  const resto = palavras.filter((palavra) => !MOLDURA.has(palavra));
  let candidata: number | undefined;
  if (resto.length === 1) {
    const [palavra] = resto;
    candidata =
      NUMEROS[palavra] ??
      ORDINAIS[palavra] ??
      (LETRAS.includes(palavra) ? LETRAS.indexOf(palavra) + 1 : undefined);
  } else if (resto.length === 0 && palavras.length === 2 && palavras[0] === "letra") {
    // "letra a" e "letra e": a letra caiu na moldura.
    candidata = LETRAS.indexOf(palavras[1]) + 1 || undefined;
  } else if (resto.length === 0 && palavras.length === 1 && LETRAS.includes(palavras[0])) {
    candidata = LETRAS.indexOf(palavras[0]) + 1;
  }
  if (candidata === undefined || candidata < 1 || candidata > total) return null;
  return candidata;
}

function bigramas(texto: string): string[] {
  const compacto = texto.replace(/\s/g, "");
  if (compacto.length < 2) return compacto ? [compacto] : [];
  const pares: string[] = [];
  for (let indice = 0; indice < compacto.length - 1; indice += 1) {
    pares.push(compacto.slice(indice, indice + 2));
  }
  return pares;
}

// Coeficiente de Dice sobre bigramas: tolera a pequena diferença de
// transcrição ("fotosintese", "foto síntese") sem dicionário.
export function semelhanca(a: string, b: string): number {
  const deA = bigramas(a);
  const deB = bigramas(b);
  if (deA.length === 0 || deB.length === 0) return 0;
  const restantes = [...deB];
  let comuns = 0;
  for (const par of deA) {
    const achado = restantes.indexOf(par);
    if (achado >= 0) {
      comuns += 1;
      restantes.splice(achado, 1);
    }
  }
  return (2 * comuns) / (deA.length + deB.length);
}

/**
 * Devolve a alternativa (contada a partir de 1, como o núcleo) que a fala
 * aponta, ou `null` quando nenhuma é claramente a mais próxima — silêncio
 * incluído. `null` faz a resposta seguir como transcrição literal.
 */
export function ligarFalaAAlternativa(
  transcricao: string,
  alternativas: string[],
): number | null {
  const fala = normalizar(transcricao);
  if (fala === "" || alternativas.length === 0) return null;

  const normalizadas = alternativas.map(normalizar);
  const exata = normalizadas.indexOf(fala);
  if (exata >= 0) return exata + 1;

  const apontada = posicaoApontada(fala.split(" "), alternativas.length);
  if (apontada !== null) return apontada;

  const notas = normalizadas.map((alternativa) => semelhanca(fala, alternativa));
  const ordenadas = [...notas].sort((x, y) => y - x);
  const [melhor, segunda = 0] = ordenadas;
  if (melhor < SEMELHANCA_MINIMA || melhor - segunda < FOLGA_SOBRE_A_SEGUNDA) return null;
  return notas.indexOf(melhor) + 1;
}
