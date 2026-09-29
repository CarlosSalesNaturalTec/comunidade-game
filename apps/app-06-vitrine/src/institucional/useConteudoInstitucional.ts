import {
  type ChaveDeSecaoInstitucional,
  lerConteudoInstitucional,
  type SecaoInstitucionalPublica,
} from "../api/leituras";
import { type EstadoDaLeitura, useLeitura } from "../leitura/useLeitura";

// Uma leitura por carga de página, compartilhada pelas três seções: três
// consultas por tela cairiam no freio por origem à toa (design — decisão 7).
// A promessa mora só na memória do módulo, que morre na recarga — nada vai ao
// aparelho (`RN-03-22`). Leitura que falhou não fica guardada.
let leituraEmMemoria: Promise<SecaoInstitucionalPublica[]> | null = null;

function lerUmaVez(): Promise<SecaoInstitucionalPublica[]> {
  if (leituraEmMemoria === null) {
    leituraEmMemoria = lerConteudoInstitucional().catch((erro) => {
      leituraEmMemoria = null;
      throw erro;
    });
  }
  return leituraEmMemoria;
}

/** Para os testes: esquece a leitura em memória. */
export function esquecerConteudoInstitucional(): void {
  leituraEmMemoria = null;
}

export function useConteudoInstitucional(
  secao: ChaveDeSecaoInstitucional,
): EstadoDaLeitura<SecaoInstitucionalPublica> {
  const estado = useLeitura(lerUmaVez, "conteudo-institucional");
  if (estado.situacao !== "pronta") return estado;
  const encontrada = estado.dado.find((item) => item.secao === secao);
  return {
    situacao: "pronta",
    dado: encontrada ?? { secao, texto: null, video_url: null },
  };
}
