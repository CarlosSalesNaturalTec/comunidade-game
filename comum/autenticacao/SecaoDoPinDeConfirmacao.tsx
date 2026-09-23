import { type FormEvent, useEffect, useState } from "react";
import { ErroDaApi, ehRecusaDeSessao } from "../api/cliente";
import { Aviso } from "../react/Aviso";
import { Botao } from "../react/Botao";
import { Campo } from "../react/Campo";
import { cadastrarPinDeConfirmacao, eu } from "./api";

const FORMATO_DO_PIN = /^[0-9]{4}$/;

function soDigitos(valor: string): string {
  return valor.replace(/\D/g, "").slice(0, 4);
}

// O PIN de confirmação do Mestre (App 09) e do Admin (App 03): o mesmo
// formulário nas duas áreas, porque é a mesma credencial. Diz se já há PIN
// sem nunca mostrá-lo, pede-o duas vezes, mascarado, e recusa na própria
// tela o formato errado e as digitações diferentes, antes de enviar
// (`RF-09-121`, `RF-02-110`, `RF-01-75`).
interface Props {
  /** Token da sessão do adulto na área que hospeda a seção. */
  token: string;
  /** O que a área faz quando o núcleo recusa a sessão. */
  aoRecusarSessao: () => void;
}

export function SecaoDoPinDeConfirmacao({ token, aoRecusarSessao }: Props) {
  const [temPin, definirTemPin] = useState<boolean | null>(null);
  const [pin, definirPin] = useState("");
  const [repeticao, definirRepeticao] = useState("");
  const [erro, definirErro] = useState<string | null>(null);
  const [gravado, definirGravado] = useState(false);
  const [gravando, definirGravando] = useState(false);

  useEffect(() => {
    let cancelado = false;
    eu(token)
      .then((quemSou) => {
        if (!cancelado) definirTemPin(quemSou.tem_pin_de_confirmacao ?? false);
      })
      .catch((falha) => {
        if (ehRecusaDeSessao(falha)) aoRecusarSessao();
      });
    return () => {
      cancelado = true;
    };
  }, [token, aoRecusarSessao]);

  async function aoGravar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirGravado(false);
    if (!FORMATO_DO_PIN.test(pin)) {
      definirErro("O PIN tem 4 dígitos, só números.");
      return;
    }
    if (pin !== repeticao) {
      definirErro("As duas digitações do PIN não são iguais. Digite de novo.");
      definirPin("");
      definirRepeticao("");
      return;
    }
    definirErro(null);
    definirGravando(true);
    try {
      await cadastrarPinDeConfirmacao(token, pin);
      definirTemPin(true);
      definirGravado(true);
    } catch (falha) {
      if (ehRecusaDeSessao(falha)) {
        aoRecusarSessao();
        return;
      }
      definirErro(
        falha instanceof ErroDaApi
          ? falha.message
          : "Não foi possível gravar o PIN. Tente novamente em instantes.",
      );
    } finally {
      definirPin("");
      definirRepeticao("");
      definirGravando(false);
    }
  }

  return (
    <section aria-label="PIN de confirmação">
      <h2>PIN de confirmação</h2>
      <p>
        Serve para confirmar, no aparelho da aula (App 01), a identidade de um Guerreiro(a) que
        o reconhecimento não identificou. Só quem abriu o aparelho confirma, digitando este PIN
        na hora.
      </p>
      {temPin === true && <p>Você já tem PIN cadastrado. Para trocar, digite o novo.</p>}
      {temPin === false && <p>Você ainda não tem PIN cadastrado.</p>}
      <form onSubmit={aoGravar} aria-label="Cadastrar PIN de confirmação">
        <Campo
          rotulo="PIN (4 dígitos)"
          tipo="password"
          valor={pin}
          aoAlterar={(valor) => definirPin(soDigitos(valor))}
        />
        <Campo
          rotulo="Repita o PIN"
          tipo="password"
          valor={repeticao}
          aoAlterar={(valor) => definirRepeticao(soDigitos(valor))}
        />
        {erro && <Aviso tipo="erro">{erro}</Aviso>}
        {gravado && <Aviso tipo="sucesso">PIN cadastrado.</Aviso>}
        <Botao tipo="submit" desabilitado={gravando}>
          {temPin ? "Trocar PIN" : "Cadastrar PIN"}
        </Botao>
      </form>
    </section>
  );
}
