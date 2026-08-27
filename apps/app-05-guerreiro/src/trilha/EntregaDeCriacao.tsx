import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useEffect, useId, useState } from "react";
import {
  abrirEnvio,
  type CriacaoOriginal,
  confirmarEnvio,
  consultarProgressoDaSessao,
  type EquipeDaTrilha,
  entregarCriacaoOriginal,
  enviarArquivo,
  obterMinhaEquipeDaTrilha,
  type TipoDeProducaoDaCriacaoOriginal,
} from "../api/criacaoOriginal";
import type { CulminanciaDaTrilha } from "../api/trilha";

interface Props {
  trilhaId: string;
  culminancia: CulminanciaDaTrilha;
  criacaoDevolvida: CriacaoOriginal | null;
  aoEntregar: () => void;
}

const ROTULO_DO_TIPO: Record<TipoDeProducaoDaCriacaoOriginal, string> = {
  texto: "Texto",
  imagem: "Imagem",
  link_externo: "Link para vídeo hospedado fora",
  video: "Vídeo",
  arquivo: "Arquivo",
};

const TIPOS_COM_ENVIO: TipoDeProducaoDaCriacaoOriginal[] = ["imagem", "video", "arquivo"];

const FORMATOS_ACEITOS: Record<string, string> = {
  imagem: "image/jpeg,image/png,image/webp",
  video: "video/mp4,video/webm",
  arquivo: "application/pdf,image/jpeg,image/png,image/webp,audio/mpeg",
};

const MENSAGEM_DE_QUEDA_DE_REDE =
  "A conexão caiu no meio do envio. Quando ela voltar, toque em Tentar novamente.";

class QuedaDeRedeDuranteEnvio extends Error {}

// Entrega da criação nos cinco tipos, na modalidade que a culminância
// declara — individual ou de equipe, consultando a equipe homologada sem
// oferecer formá-la (`RF-05-40`, `RF-05-41`, `RN-05-12`). Devolvida,
// mostra o motivo em linguagem simples e reabre o caminho de reenvio, sem
// perder a autoria (`RF-05-42`, `RN-05-13`).
export function EntregaDeCriacao({
  trilhaId,
  culminancia,
  criacaoDevolvida,
  aoEntregar,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoTipo = useId();
  const [equipe, definirEquipe] = useState<EquipeDaTrilha | null>(null);
  const [semEquipe, definirSemEquipe] = useState(false);
  const [tipo, definirTipo] = useState<TipoDeProducaoDaCriacaoOriginal>("texto");
  const [producao, definirProducao] = useState("");
  const [arquivo, definirArquivo] = useState<File | null>(null);
  const [progresso, definirProgresso] = useState<{ enviados: number; total: number } | null>(
    null,
  );
  const [enderecoDaSessao, definirEnderecoDaSessao] = useState<string | null>(null);
  const [criacaoId, definirCriacaoId] = useState<string | null>(null);
  const [erroDeCampo, definirErroDeCampo] = useState<string | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  const emEquipe = culminancia.modalidade === "em_equipe";

  useEffect(() => {
    if (!emEquipe || !sessao) return;
    obterMinhaEquipeDaTrilha(trilhaId, sessao.token)
      .then(definirEquipe)
      .catch((erroCapturado) => {
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirSemEquipe(true);
      });
  }, [emEquipe, sessao, trilhaId, tratarRecusaDeSessao]);

  async function enviarArquivoComRetomada(idDaCriacao: string, arquivoAEnviar: File) {
    const endereco = await abrirEnvio(
      idDaCriacao,
      arquivoAEnviar.type,
      arquivoAEnviar.size,
      sessao?.token ?? "",
    );
    definirEnderecoDaSessao(endereco);
    try {
      await enviarArquivo(endereco, arquivoAEnviar, (enviados, total) =>
        definirProgresso({ enviados, total }),
      );
    } catch {
      throw new QuedaDeRedeDuranteEnvio();
    }
    return confirmarEnvio(idDaCriacao, sessao?.token ?? "");
  }

  async function retomarEnvio() {
    if (!sessao || !arquivo || !enderecoDaSessao || !criacaoId) return;
    definirErroDeRecusa(null);
    definirEnviando(true);
    try {
      const jaRecebido = await consultarProgressoDaSessao(enderecoDaSessao, arquivo.size);
      await enviarArquivo(
        enderecoDaSessao,
        arquivo,
        (enviados, total) => definirProgresso({ enviados, total }),
        jaRecebido,
      );
      await confirmarEnvio(criacaoId, sessao.token);
      aoEntregar();
    } catch {
      definirErroDeRecusa(MENSAGEM_DE_QUEDA_DE_REDE);
    } finally {
      definirEnviando(false);
    }
  }

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (tipo === "texto" && !producao.trim()) {
      definirErroDeCampo("Escreva o texto da sua criação.");
      return;
    }
    if (tipo === "link_externo" && !producao.trim()) {
      definirErroDeCampo("Informe o endereço do link.");
      return;
    }
    if (TIPOS_COM_ENVIO.includes(tipo) && !arquivo) {
      definirErroDeCampo("Escolha o arquivo para enviar.");
      return;
    }
    if (emEquipe && !equipe) {
      definirErroDeCampo("Você precisa integrar uma equipe homologada desta trilha.");
      return;
    }

    if (!sessao) return;
    definirEnviando(true);
    try {
      const criacao = await entregarCriacaoOriginal(
        culminancia.id,
        {
          equipe_id: emEquipe ? equipe?.id : undefined,
          tipo,
          producao: tipo === "texto" || tipo === "link_externo" ? producao : undefined,
        },
        sessao.token,
      );

      if (TIPOS_COM_ENVIO.includes(tipo) && arquivo) {
        definirCriacaoId(criacao.id);
        await enviarArquivoComRetomada(criacao.id, arquivo);
      }

      aoEntregar();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof QuedaDeRedeDuranteEnvio) {
        definirErroDeRecusa(MENSAGEM_DE_QUEDA_DE_REDE);
        return;
      }
      if (erro instanceof ErroDaApi) {
        definirErroDeRecusa(erro.message);
        return;
      }
      definirErroDeRecusa(
        "Não foi possível entregar a criação. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <div className="cg-entrega-de-criacao">
      {criacaoDevolvida && (
        <Aviso tipo="atencao">
          O Mestre pediu um ajuste: {criacaoDevolvida.motivo_da_devolucao}. Sua autoria
          continua garantida — é só reenviar.
        </Aviso>
      )}

      {emEquipe && equipe && (
        <div className="cg-entrega-de-criacao__equipe">
          <p>Sua equipe:</p>
          <ul>
            {equipe.integrantes.map((integrante) => (
              <li key={integrante.nick}>
                {integrante.nick}
                {integrante.papel && ` — ${integrante.papel}`}
              </li>
            ))}
          </ul>
        </div>
      )}

      {emEquipe && semEquipe && (
        <Aviso tipo="erro">
          Você precisa integrar uma equipe homologada desta trilha para entregar — a formação
          da equipe acontece no encontro presencial.
        </Aviso>
      )}

      {(!emEquipe || equipe) && (
        <form onSubmit={aoSubmeter} aria-label="Entrega da criação original">
          <div className="cg-campo">
            <label htmlFor={idDoTipo}>Tipo da produção</label>
            <select
              id={idDoTipo}
              value={tipo}
              onChange={(evento) => {
                definirTipo(evento.target.value as TipoDeProducaoDaCriacaoOriginal);
                definirArquivo(null);
              }}
            >
              {Object.entries(ROTULO_DO_TIPO).map(([valor, rotulo]) => (
                <option key={valor} value={valor}>
                  {rotulo}
                </option>
              ))}
            </select>
          </div>

          {tipo === "texto" && (
            <div className="cg-campo">
              <label htmlFor="criacao-producao">Sua criação</label>
              <textarea
                id="criacao-producao"
                value={producao}
                onChange={(evento) => definirProducao(evento.target.value)}
                rows={8}
              />
            </div>
          )}

          {tipo === "link_externo" && (
            <Campo
              rotulo="Endereço do link"
              valor={producao}
              aoAlterar={definirProducao}
              tipo="url"
            />
          )}

          {TIPOS_COM_ENVIO.includes(tipo) && (
            <div className="cg-campo">
              <label htmlFor="criacao-arquivo">Arquivo</label>
              <input
                id="criacao-arquivo"
                type="file"
                accept={FORMATOS_ACEITOS[tipo]}
                onChange={(evento) => definirArquivo(evento.target.files?.[0] ?? null)}
              />
              {progresso && (
                <p role="status">
                  Enviado {Math.round((progresso.enviados / progresso.total) * 100)}% de{" "}
                  {(progresso.total / (1024 * 1024)).toFixed(1)} MB
                </p>
              )}
              {enderecoDaSessao && !enviando && erroDeRecusa && (
                <Botao variante="secundaria" onClick={retomarEnvio}>
                  Tentar novamente
                </Botao>
              )}
            </div>
          )}

          {erroDeCampo && <Aviso tipo="erro">{erroDeCampo}</Aviso>}
          {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

          <Botao tipo="submit" desabilitado={enviando}>
            {criacaoDevolvida ? "Reenviar" : "Entregar"}
          </Botao>
        </form>
      )}
    </div>
  );
}
