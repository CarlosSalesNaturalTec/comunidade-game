import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useState } from "react";
import { type AdultoDaLista, alterarAdulto, type PapelDoAdulto } from "./api";

interface Props {
  papel: PapelDoAdulto;
  adulto: AdultoDaLista;
  aoSalvar: (adulto: AdultoDaLista) => void;
  aoCancelar: () => void;
}

// Nome, e-mail e WhatsApp — e nada mais: nick, papel e termos de doação não
// se alteram pela gestão (`RF-02-117`, documento 02 §1). Trocar o e-mail
// troca o login social do adulto.
export function EdicaoDoAdulto({ papel, adulto, aoSalvar, aoCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [nome, definirNome] = useState(adulto.nome);
  const [email, definirEmail] = useState(adulto.email);
  const [whatsapp, definirWhatsapp] = useState(adulto.whatsapp ?? "");
  const [erroDeCampo, definirErroDeCampo] = useState<{
    campo: string;
    mensagem: string;
  } | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function salvar(evento: FormEvent) {
    evento.preventDefault();
    if (!sessao) return;
    definirErro(null);
    definirErroDeCampo(null);
    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome." });
      return;
    }
    if (!email.trim()) {
      definirErroDeCampo({ campo: "email", mensagem: "Informe o e-mail." });
      return;
    }
    definirEnviando(true);
    try {
      const salvo = await alterarAdulto(
        papel,
        adulto.id,
        { nome, email, whatsapp: whatsapp.trim() ? whatsapp : null },
        sessao.token,
      );
      aoSalvar(salvo);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "permissao_negada") {
        definirErro("Só o Admin altera o cadastro.");
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.campo) {
        definirErroDeCampo({ campo: erroCapturado.campo, mensagem: erroCapturado.message });
        return;
      }
      definirErro("Não foi possível salvar. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={salvar} noValidate>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Campo
        rotulo="Nome"
        valor={nome}
        aoAlterar={definirNome}
        erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
        focoInicial
      />
      <Campo
        rotulo="E-mail"
        tipo="email"
        valor={email}
        aoAlterar={definirEmail}
        erro={erroDeCampo?.campo === "email" ? erroDeCampo.mensagem : null}
      />
      <Campo rotulo="WhatsApp" valor={whatsapp} aoAlterar={definirWhatsapp} />
      <Botao tipo="submit" desabilitado={enviando}>
        Salvar
      </Botao>
      <Botao variante="secundaria" onClick={aoCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
