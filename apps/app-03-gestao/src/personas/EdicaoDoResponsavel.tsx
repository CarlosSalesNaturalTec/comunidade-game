import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useState } from "react";
import { alterarResponsavel, type ResponsavelDaLista } from "./api";

interface Props {
  responsavel: ResponsavelDaLista;
  aoSalvar: () => void;
  aoCancelar: () => void;
}

// A ficha do responsável: nome e e-mail, só pelo Admin (`RF-02-121`, decisão
// do fundador de 2026-11-27). O e-mail é o da conta Google com que ele entra
// na App 07; esvaziá-lo retira esse acesso, e a credencial de usuário e senha
// segue valendo (`RF-01-92`). No molde de `EdicaoDoAdulto`.
export function EdicaoDoResponsavel({ responsavel, aoSalvar, aoCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [nome, definirNome] = useState(responsavel.nome);
  const [email, definirEmail] = useState(responsavel.email);
  const [erroDeCampo, definirErroDeCampo] = useState<{
    campo: string;
    mensagem: string;
  } | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  const retiraOAcesso = responsavel.email !== "" && email.trim() === "";

  async function salvar(evento: FormEvent) {
    evento.preventDefault();
    if (!sessao) return;
    definirErro(null);
    definirErroDeCampo(null);
    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome do responsável." });
      return;
    }
    definirEnviando(true);
    try {
      await alterarResponsavel(
        responsavel.id,
        { nome: nome.trim(), email: email.trim() ? email.trim() : null },
        sessao.token,
      );
      aoSalvar();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "permissao_negada") {
        definirErro("Só o Admin altera a ficha do responsável.");
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
    <form onSubmit={salvar} noValidate aria-label="Editar ficha do responsável">
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Campo
        rotulo="Nome do responsável"
        valor={nome}
        aoAlterar={definirNome}
        erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
        focoInicial
      />
      <Campo
        rotulo="E-mail da conta Google (opcional)"
        tipo="email"
        valor={email}
        aoAlterar={definirEmail}
        erro={erroDeCampo?.campo === "email" ? erroDeCampo.mensagem : null}
      />
      {retiraOAcesso && (
        <Aviso tipo="atencao">
          Sem e-mail, o responsável deixa de entrar pela conta Google. O usuário e senha, se
          houver, continua valendo.
        </Aviso>
      )}
      <Botao tipo="submit" desabilitado={enviando}>
        Salvar
      </Botao>
      <Botao variante="secundaria" onClick={aoCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
