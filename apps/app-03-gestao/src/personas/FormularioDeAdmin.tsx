import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import { incluirAdmin } from "./api";

interface Props {
  onSalvo: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const DADO_COLETADO = "o nome, o e-mail e o WhatsApp do Admin";

// Único caminho de entrada de um Admin novo — nunca autocadastro, nunca por
// login (`RF-02-05`, `RN-02-02`).
export function FormularioDeAdmin({ onSalvo, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [nome, definirNome] = useState("");
  const [email, definirEmail] = useState("");
  const [whatsapp, definirWhatsapp] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome." });
      return;
    }
    if (!email.trim()) {
      definirErroDeCampo({ campo: "email", mensagem: "Informe o e-mail." });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      await incluirAdmin({ nome, email, whatsapp: whatsapp || undefined }, sessao.token);
      onSalvo();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "permissao_negada") {
        definirErroDeRecusa("Só o Admin inclui outro Admin.");
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa("Não foi possível incluir o Admin. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Novo Admin">
      <AvisoDeColeta dado={DADO_COLETADO} />

      <Campo
        rotulo="Nome"
        valor={nome}
        aoAlterar={definirNome}
        erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="E-mail"
        tipo="email"
        valor={email}
        aoAlterar={definirEmail}
        erro={erroDeCampo?.campo === "email" ? erroDeCampo.mensagem : null}
      />
      <Campo rotulo="WhatsApp (opcional)" valor={whatsapp} aoAlterar={definirWhatsapp} />

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Incluir
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
