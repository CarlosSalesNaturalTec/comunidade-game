import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type FormEvent, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";

// A troca é a única tela que a senha provisória abre — nenhum botão de
// pular, cancelar ou continuar sem trocar existe aqui (`RF-14-09`,
// `RN-14-02`, PRD-14 §§5.2, 12).
export function TelaDeTrocaDeSenha() {
  const { trocarSenhaProvisoria, trocandoSenha, erroDeTrocaDeSenha } = useSessao();
  const [senhaNova, definirSenhaNova] = useState("");
  const [confirmacao, definirConfirmacao] = useState("");
  const [erroLocal, definirErroLocal] = useState<string | null>(null);

  function aoEnviar(evento: FormEvent) {
    evento.preventDefault();
    if (senhaNova !== confirmacao) {
      definirErroLocal("As duas senhas precisam ser iguais.");
      return;
    }
    definirErroLocal(null);
    trocarSenhaProvisoria(senhaNova);
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Troque sua senha"
        subtitulo="Esta senha foi criada pela gestão. Escolha uma nova antes de continuar."
      />
      <AvisoDeColeta dado="a senha nova" />
      <form onSubmit={aoEnviar}>
        <Campo
          rotulo="Senha nova"
          tipo="password"
          valor={senhaNova}
          aoAlterar={definirSenhaNova}
        />
        <Campo
          rotulo="Confirme a senha nova"
          tipo="password"
          valor={confirmacao}
          aoAlterar={definirConfirmacao}
        />
        <Botao tipo="submit" desabilitado={trocandoSenha}>
          Trocar senha
        </Botao>
      </form>
      {trocandoSenha && <Aviso tipo="andamento">Trocando…</Aviso>}
      {erroLocal && <Aviso tipo="erro">{erroLocal}</Aviso>}
      {erroDeTrocaDeSenha && <Aviso tipo="erro">{erroDeTrocaDeSenha}</Aviso>}
    </Moldura>
  );
}
