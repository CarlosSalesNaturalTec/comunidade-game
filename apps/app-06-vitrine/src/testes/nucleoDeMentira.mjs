import { createServer } from "node:http";

/**
 * O núcleo de mentira que o build da vitrine consome quando não há núcleo de
 * verdade. Responde às **duas** rotas que o build lê: o conteúdo
 * institucional e a lista de comunidades (design — decisão 4).
 *
 * Serve a dois donos, e por isso mora num módulo só: o teste da saída do
 * build, que o sobe no próprio processo, e o `frontend-ci.yml`, que roda este
 * arquivo com `node` — na esteira o build acontece para conferir tipo e
 * montagem, sem núcleo de verdade para alcançar.
 *
 * É JavaScript, e não TypeScript, justamente para o `node` o executar direto,
 * sem carregador nenhum e sem dependência nova.
 */

export const PORTA_PADRAO = 4611;

export const TEXTO_QUEM_SOMOS =
  "## Nota de transparência sobre IA\n\nA plataforma usa IA e declara isso em público.";
export const TEXTO_COMO_APOIAR = "Chave PIX (CNPJ): 51.730.395/0001-19";

export const COMUNIDADE = {
  id: "zeferina",
  nome: "Guerreira Zeferina",
  localizacao: "Cabula, Salvador",
  series_abertas: 2,
  series_ativas: 1,
  registros_validos: 40,
  continuidade: 0.8,
  guerreiros_vinculados: 17,
};

/** @param {number} [porta] */
export function criarNucleoDeMentira(porta = PORTA_PADRAO) {
  const servidor = createServer((req, res) => {
    const caminho = new URL(req.url ?? "/", "http://local").pathname;
    res.setHeader("Content-Type", "application/json");
    if (caminho === "/v1/vitrine/conteudo-institucional") {
      return res.end(
        JSON.stringify([
          { secao: "quem-somos", texto: TEXTO_QUEM_SOMOS, video_url: null },
          { secao: "como-apoiar", texto: TEXTO_COMO_APOIAR, video_url: null },
          { secao: "contatos", texto: null, video_url: null },
        ]),
      );
    }
    if (caminho === "/v1/comunidades") {
      return res.end(
        JSON.stringify({
          itens: [COMUNIDADE],
          proximo_cursor: null,
          ciclo_rotulo: "Ciclo 01",
        }),
      );
    }
    res.statusCode = 404;
    res.end(JSON.stringify({ detalhe: "não encontrado" }));
  });
  return new Promise((pronto) => servidor.listen(porta, () => pronto(servidor)));
}

// Executado direto pelo `node`, sobe e fica de pé até ser derrubado.
if (import.meta.url === `file://${process.argv[1]}`) {
  await criarNucleoDeMentira();
  console.log(`núcleo de mentira em http://127.0.0.1:${PORTA_PADRAO}`);
}
