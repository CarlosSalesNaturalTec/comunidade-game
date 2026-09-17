// A mesma distância que o núcleo calcula em `_distancia_euclidiana`
// (`backend/src/nucleo/biometria/regra.py`): raiz da soma dos quadrados,
// sobre o descritor cru, sem normalizar.
//
// É duplicação deliberada de lógica entre as duas pontas — a única do
// repositório — e ela existe porque o número precisa ser **comparável**: a
// bancada de calibração mede aqui o valor que o Mestre vai gravar como limiar
// lá (`RF-04-63`, design — decisão 1). Calcular no núcleo mandaria descritor
// de criança pela rede para uma finalidade que não é identificar, contra a
// finalidade única do `RN-04-06`.
//
// `distancia.test.ts` prende as duas implementações com valores fixos: se o
// cálculo do núcleo mudar, o teste daqui quebra junto, e a divergência aparece
// no CI em vez de no encontro.
//
// Fica em arquivo próprio, fora de `biometria.ts`, para que medir não exija
// carregar a Human nem tocar a câmera.

// `null` quando os tamanhos diferem — o mesmo que o núcleo devolve, e o que
// faz a comparação nunca conferir por engano entre descritores incompatíveis.
export function distanciaEntreDescritores(a: number[], b: number[]): number | null {
  if (a.length !== b.length) return null;
  let soma = 0;
  for (let i = 0; i < a.length; i++) {
    const diferenca = a[i] - b[i];
    soma += diferenca * diferenca;
  }
  return Math.sqrt(soma);
}
