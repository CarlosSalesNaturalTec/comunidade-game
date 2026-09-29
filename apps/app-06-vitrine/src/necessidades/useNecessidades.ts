import { listarNecessidades, type NecessidadePublica } from "../api/leituras";
import { type EstadoDaLeitura, useLeitura } from "../leitura/useLeitura";

// Uma leitura por carga de página, compartilhada pela porta do convite e pelo
// bloco de "Como apoiar": as duas telas mostram a mesma lista, e duas consultas
// gastariam a cota da chave à toa (design — decisão 5). A promessa mora só na
// memória do módulo, que morre na recarga — nada vai ao aparelho (`RF-03-38`,
// `RN-03-15`, `RN-03-22`). Leitura que falhou não fica guardada.
let leituraEmMemoria: Promise<NecessidadePublica[]> | null = null;

function lerUmaVez(): Promise<NecessidadePublica[]> {
  if (leituraEmMemoria === null) {
    leituraEmMemoria = listarNecessidades().catch((erro) => {
      leituraEmMemoria = null;
      throw erro;
    });
  }
  return leituraEmMemoria;
}

/** Para os testes: esquece a leitura em memória. */
export function esquecerNecessidades(): void {
  leituraEmMemoria = null;
}

export function useNecessidades(): EstadoDaLeitura<NecessidadePublica[]> {
  return useLeitura(lerUmaVez, "vitrine/necessidades");
}
