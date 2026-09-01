import { BotaoDeEntradaGoogle, useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type FormEvent, useState } from "react";
import { GOOGLE_CLIENT_ID } from "../api/configuracao";

interface Props {
  /** Recusa decidida pela própria App 08 — persona que entrou, mas não é
   * Apoiador (PRD-14 §4). Em linguagem simples, sem código de erro cru. */
  mensagemDeRecusa?: string | null;
  /** Caminho de volta à porta pública, quando a entrada abriu a partir dela
   * (design — decisão 1). */
  aoVoltar?: () => void;
}

// Os dois caminhos de entrada do Apoiador — login social e usuário e senha
// criados pela gestão. Login sem cadastro prévio é recusado pelo núcleo, e a
// mensagem já traz a orientação de usar o pré-cadastro (`RF-14-08`,
// `RF-14-10`, `RN-14-02`). Nenhuma tela de convite ou segundo acesso existe
// nesta aplicação (`RF-14-11`, `RN-14-04`).
export function TelaDeEntrada({ mensagemDeRecusa, aoVoltar }: Props) {
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
        titulo="Comunidade Game — Apoiador"
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
      {aoVoltar && (
        <Botao variante="secundaria" onClick={aoVoltar}>
          Voltar à porta pública
        </Botao>
      )}
    </Moldura>
  );
}
