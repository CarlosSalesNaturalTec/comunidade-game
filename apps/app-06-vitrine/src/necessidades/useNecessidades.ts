import { listarNecessidades, type NecessidadePublica } from "../api/leituras";
import { type EstadoDaLeitura, useLeitura } from "../leitura/useLeitura";

// Uma leitura por carga de página. A porta do convite é a única tela que lista
// as necessidades desde 2026-11-10, quando a seção própria saiu da abertura;
// a leitura única segue evitando consulta repetida, que gastaria a cota da
// chave à toa. A promessa mora só na
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
