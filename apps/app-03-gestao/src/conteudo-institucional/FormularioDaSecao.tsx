import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import {
  publicarSecao,
  SECAO_COM_VIDEO,
  type SecaoInstitucional,
  type SecaoPublicada,
} from "./api";

interface Props {
  secao: SecaoInstitucional;
  rotulo: string;
  publicada: SecaoPublicada;
  onPublicada: (publicada: SecaoPublicada) => void;
}

// Publicar substitui a versão vigente da seção, uma seção por vez: o núcleo
// guarda uma linha por seção, e o histórico de quem publicou o quê vive na
// trilha de auditoria (`RF-02-80`).
export function FormularioDaSecao({ secao, rotulo, publicada, onPublicada }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoTexto = useId();
  const [texto, definirTexto] = useState(publicada.texto ?? "");
  const [videoUrl, definirVideoUrl] = useState(publicada.video_url ?? "");
  const [erroDeCampo, definirErroDeCampo] = useState<{
    campo?: string;
    mensagem: string;
  } | null>(null);
  const [enviando, definirEnviando] = useState(false);

  const ofereceVideo = secao === SECAO_COM_VIDEO;

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);

    if (!texto.trim()) {
      definirErroDeCampo({ campo: "texto", mensagem: "O texto da seção é obrigatório." });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      const atualizada = await publicarSecao(
        secao,
        // Publicar sem o link retira o anterior — campo vazio é ausência, não
        // texto vazio (`RF-03-49`).
        { texto, video_url: ofereceVideo && videoUrl.trim() ? videoUrl.trim() : null },
        sessao.token,
      );
      onPublicada(atualizada);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      // A recusa que o núcleo declarou vira a frase do domínio, no campo que
      // ele nomeou quando nomeia um; falha de camada aparece como o que é
      // (invariante 25 do documento 99 §6).
      if (erro instanceof ErroDaApi) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeCampo({
        mensagem: "Não foi possível publicar a seção. Tente novamente em instantes.",
      });
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label={`Publicar ${rotulo}`}>
      <div className="cg-campo">
        <label htmlFor={idDoTexto}>Texto</label>
        <textarea
          id={idDoTexto}
          value={texto}
          onChange={(evento) => definirTexto(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "texto" || undefined}
        />
        {erroDeCampo?.campo === "texto" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      {ofereceVideo && (
        <Campo
          rotulo="Link do vídeo de apresentação (opcional)"
          valor={videoUrl}
          aoAlterar={definirVideoUrl}
          erro={erroDeCampo?.campo === "video_url" ? erroDeCampo.mensagem : null}
        />
      )}

      {erroDeCampo && !erroDeCampo.campo && <Aviso tipo="erro">{erroDeCampo.mensagem}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Publicar {rotulo}
      </Botao>
    </form>
  );
}
