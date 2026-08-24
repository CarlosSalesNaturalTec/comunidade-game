import { ErroDaApi } from "comum/api";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import { enviarDescritor } from "../api/descritor";
import { encerrarCaptura, gerarDescritor, provarVivacidade } from "../biometria/biometria";

interface Props {
  tokenDeTrabalho: string;
  guerreiroId: string;
  aoConcluir: () => void;
  aoVoltar: () => void;
}

type Estado = "pronta" | "capturando" | "vivacidade_reprovada" | "erro";

// A prova de vivacidade sempre antes do descritor, e nenhum envio acontece
// sem ela passar (`RF-04-13`, `RF-04-48`, documento 03 §3.3). O módulo de
// biometria é o único que toca a câmera — esta tela só chama as duas
// funções que ele expõe e nunca vê a fotografia (`RN-04-08`, `RN-04-12`).
export function TelaDeCaptura({ tokenDeTrabalho, guerreiroId, aoConcluir, aoVoltar }: Props) {
  const [estado, definirEstado] = useState<Estado>("pronta");
  const [mensagemDeErro, definirMensagemDeErro] = useState<string | null>(null);

  useEffect(() => {
    return () => {
      encerrarCaptura();
    };
  }, []);

  async function iniciarCaptura() {
    definirEstado("capturando");
    definirMensagemDeErro(null);
    try {
      const vivacidadeAprovada = await provarVivacidade();
      if (!vivacidadeAprovada) {
        definirEstado("vivacidade_reprovada");
        return;
      }
      const descritor = await gerarDescritor();
      await enviarDescritor(guerreiroId, { descritor }, tokenDeTrabalho);
      aoConcluir();
    } catch (erroCapturado) {
      definirEstado("erro");
      if (erroCapturado instanceof ErroDaApi && erroCapturado.status === 422) {
        definirMensagemDeErro(
          "O consentimento ainda não foi registrado. Volte ao termo antes de tentar de novo.",
        );
        return;
      }
      definirMensagemDeErro("Não foi possível concluir a captura. Tente novamente.");
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Captura da imagem"
        subtitulo="Olhe para a câmera. A fotografia não sai deste aparelho."
        acao={{ rotulo: "Voltar ao início", aoAcionar: aoVoltar }}
      />
      {estado === "capturando" && <EstadoDaLista>Capturando e verificando…</EstadoDaLista>}
      {estado === "vivacidade_reprovada" && (
        <Aviso tipo="atencao">
          Não foi possível confirmar que há uma pessoa diante da câmera. Tente de novo, com o
          rosto bem posicionado.
        </Aviso>
      )}
      {estado === "erro" && mensagemDeErro && <Aviso tipo="erro">{mensagemDeErro}</Aviso>}
      <Botao onClick={iniciarCaptura} desabilitado={estado === "capturando"}>
        {estado === "capturando" ? "Capturando…" : "Iniciar captura"}
      </Botao>
    </Moldura>
  );
}
