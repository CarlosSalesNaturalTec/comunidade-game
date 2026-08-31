import { BotaoDeEntradaGoogle, useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type FormEvent, useState } from "react";
import { GOOGLE_CLIENT_ID } from "../api/configuracao";

interface Props {
  /** Recusa decidida pela própria App 07 — persona que entrou, mas não é
   * responsável (PRD-13 §4). Em linguagem simples, sem código de erro cru. */
  mensagemDeRecusa?: string | null;
}

// Os dois caminhos de entrada do responsável — login social e usuário e
// senha criados pela gestão. Login sem cadastro prévio é recusado pelo
// núcleo, com a orientação de procurar a gestão no encontro (`RF-13-01`,
// `RF-13-03`, `RN-13-01`, `RN-13-02`). Nenhuma tela de autocadastro existe
// nesta aplicação (`RF-13-06`).
export function TelaDeEntrada({ mensagemDeRecusa }: Props) {
  const { entrarComGoogle, entrarComCredencial, entrando, erroDeEntrada } = useSessao();
  const [usuario, definirUsuario] = useState("");
  const [senha, definirSenha] = useState("");

  function aoEnviar(evento: FormEvent) {
    evento.preventDefault();
    entrarComCredencial(usuario, senha);
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Comunidade Game — Responsáveis"
        subtitulo="Entre com a conta Google vinculada ao seu cadastro, ou com usuário e senha."
      />
      <BotaoDeEntradaGoogle clientId={GOOGLE_CLIENT_ID} aoReceberIdToken={entrarComGoogle} />
      <form onSubmit={aoEnviar}>
        <Campo rotulo="Usuário" valor={usuario} aoAlterar={definirUsuario} />
        <Campo rotulo="Senha" tipo="password" valor={senha} aoAlterar={definirSenha} />
        <Botao tipo="submit" desabilitado={entrando}>
          Entrar
        </Botao>
      </form>
      {entrando && <Aviso tipo="andamento">Entrando…</Aviso>}
      {erroDeEntrada && <Aviso tipo="erro">{erroDeEntrada}</Aviso>}
      {mensagemDeRecusa && <Aviso tipo="erro">{mensagemDeRecusa}</Aviso>}
    </Moldura>
  );
}
