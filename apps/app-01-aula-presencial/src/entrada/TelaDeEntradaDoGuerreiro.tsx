import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { useState } from "react";
import { confirmarSessaoDeGuerreiro } from "../api/sessoesDeGuerreiro";

interface Props {
  tokenDeTrabalho: string;
  aoVoltar: () => void;
}

// Sem câmera nesta fatia: todo Guerreiro(a) entra pela confirmação humana
// do Mestre ou Admin em sessão de trabalho — o caminho que o `RF-04-15` já
// prevê para quem não tem _template_ (`RF-04-29`, proposal — decisão 1).
// Nenhum identificador de persona aparece nesta tela nem sai do núcleo
// (design — decisão 1.1).
export function TelaDeEntradaDoGuerreiro({ tokenDeTrabalho, aoVoltar }: Props) {
  const { entrarComToken } = useSessao();
  const [nick, definirNick] = useState("");
  const [confirmando, definirConfirmando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);

  async function confirmar() {
    definirErro(null);
    definirConfirmando(true);
    try {
      const abertura = await confirmarSessaoDeGuerreiro(nick.trim(), tokenDeTrabalho);
      await entrarComToken(abertura.token);
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível confirmar. Tente novamente.",
      );
    } finally {
      definirConfirmando(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Quem está chegando?"
        subtitulo="A criança diz o nick, e um Mestre ou Admin confirma quem ela é."
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />
      <Campo rotulo="Nick" valor={nick} aoAlterar={definirNick} />
      <Botao onClick={confirmar} desabilitado={confirmando || nick.trim().length === 0}>
        {confirmando ? "Confirmando…" : "Confirmar identidade"}
      </Botao>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
    </Moldura>
  );
}
