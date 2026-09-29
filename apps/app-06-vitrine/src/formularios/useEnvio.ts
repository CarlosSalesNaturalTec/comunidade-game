import { ErroDaApi } from "comum/api";
import { useState } from "react";
import type { RegistroDaSolicitacao } from "../api/solicitacoes";
import { esperaEmLinguagemSimples } from "./espera";

type Estado =
  | { situacao: "preenchendo" }
  | { situacao: "enviando" }
  | { situacao: "registrada"; registro: RegistroDaSolicitacao }
  | { situacao: "falhou"; mensagem: string };

/** Envio de formulário público. O que foi digitado vive no componente, em
 * memória: falhar ou ser freado não apaga nada, e nada vai ao aparelho
 * (`RN-03-22`). O freio (429) é resposta esperada: explica a espera, sem
 * CAPTCHA, cadastro ou login (`RF-03-35`, `RF-03-37`). */
export function useEnvio(enviar: () => Promise<RegistroDaSolicitacao>) {
  const [estado, definirEstado] = useState<Estado>({ situacao: "preenchendo" });

  async function disparar() {
    definirEstado({ situacao: "enviando" });
    try {
      definirEstado({ situacao: "registrada", registro: await enviar() });
    } catch (erro) {
      if (erro instanceof ErroDaApi && erro.status === 429) {
        definirEstado({
          situacao: "falhou",
          mensagem: `Você enviou este formulário muitas vezes seguidas deste aparelho, e por isso precisa esperar um pouco. ${esperaEmLinguagemSimples(erro)}`,
        });
      } else {
        definirEstado({
          situacao: "falhou",
          mensagem:
            "Não foi possível enviar agora. O que você preencheu continua aqui; tente de novo.",
        });
      }
    }
  }

  return { estado, disparar };
}
