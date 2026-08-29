import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useEffect, useId, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import {
  type AutoriaDoConteudo,
  abrirEnvio,
  type ConteudoDaMissao,
  confirmarEnvio,
  consultarProgressoDaSessao,
  criarConteudo,
  enviarArquivo,
  type TipoDeConteudo,
} from "./api";

interface Props {
  idDaMissao: string;
  onSalvo: (conteudo: ConteudoDaMissao) => void;
  onCancelar: () => void;
}

const ROTULO_DO_TIPO: Record<TipoDeConteudo, string> = {
  texto: "Texto",
  imagem: "Imagem",
  link_externo: "Link para vídeo hospedado fora",
  video: "Vídeo",
  arquivo: "Arquivo de apoio (PDF, imagem ou áudio)",
};

const TIPOS_COM_ENVIO: TipoDeConteudo[] = ["imagem", "video", "arquivo"];

const MENSAGEM_DE_QUEDA_DE_REDE =
  "A conexão caiu no meio do envio. Quando ela voltar, toque em Tentar novamente.";

// Marca especificamente a queda durante o envio de bytes, para distinguir
// da recusa do núcleo (formato ou tamanho, já em linguagem simples) — a
// única categoria em que a retomada faz sentido (`RF-09-19`).
class QuedaDeRedeDuranteEnvio extends Error {}

function chaveDoRascunho(idDaMissao: string): string {
  return `comunidade-game:app-09-mestre:rascunho-de-conteudo:${idDaMissao}`;
}

// O tipo declara o formato aceito pelo `<input type="file">`, para o
// Mestre já ver a lista fechada antes de escolher (`RF-09-115`).
const FORMATOS_ACEITOS: Record<string, string> = {
  imagem: "image/jpeg,image/png,image/webp",
  video: "video/mp4,video/webm",
  arquivo: "application/pdf,image/jpeg,image/png,image/webp,audio/mpeg",
};

export function FormularioDeConteudo({ idDaMissao, onSalvo, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoTipo = useId();
  const idDaAutoria = useId();
  const [tipo, definirTipo] = useState<TipoDeConteudo>("texto");
  const [corpo, definirCorpo] = useState("");
  const [endereco, definirEndereco] = useState("");
  const [autoria, definirAutoria] = useState<AutoriaDoConteudo>("propria");
  const [fonte, definirFonte] = useState("");
  const [arquivo, definirArquivo] = useState<File | null>(null);
  const [progresso, definirProgresso] = useState<{ enviados: number; total: number } | null>(
    null,
  );
  const [enderecoDaSessao, definirEnderecoDaSessao] = useState<string | null>(null);
  const [conteudoId, definirConteudoId] = useState<string | null>(null);
  const [erroDeCampo, definirErroDeCampo] = useState<string | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  // Rascunho do texto: salva a cada alteração e recupera ao abrir a tela —
  // a queda de rede nunca perde o que já foi escrito (PRD-09 §10).
  useEffect(() => {
    const rascunho = localStorage.getItem(chaveDoRascunho(idDaMissao));
    if (rascunho) definirCorpo(rascunho);
  }, [idDaMissao]);

  useEffect(() => {
    if (tipo !== "texto") return;
    if (corpo) {
      localStorage.setItem(chaveDoRascunho(idDaMissao), corpo);
    } else {
      localStorage.removeItem(chaveDoRascunho(idDaMissao));
    }
  }, [corpo, tipo, idDaMissao]);

  function limparRascunho() {
    localStorage.removeItem(chaveDoRascunho(idDaMissao));
  }

  async function enviarArquivoComRetomada(idDoConteudo: string, arquivoAEnviar: File) {
    const endereco = await abrirEnvio(
      idDoConteudo,
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
    return confirmarEnvio(idDoConteudo, sessao?.token ?? "");
  }

  async function retomarEnvio() {
    if (!sessao || !arquivo || !enderecoDaSessao || !conteudoId) return;
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
      const conteudo = await confirmarEnvio(conteudoId, sessao.token);
      onSalvo(conteudo);
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

    if (tipo === "texto" && !corpo.trim()) {
      definirErroDeCampo("Escreva o texto da missão.");
      return;
    }
    if (tipo === "link_externo" && !endereco.trim()) {
      definirErroDeCampo("Informe o endereço do vídeo.");
      return;
    }
    if (TIPOS_COM_ENVIO.includes(tipo) && !arquivo) {
      definirErroDeCampo("Escolha o arquivo para enviar.");
      return;
    }
    if (autoria === "terceiro" && !fonte.trim()) {
      definirErroDeCampo("Conteúdo de terceiro exige a fonte.");
      return;
    }

    if (!sessao) return;
    definirEnviando(true);
    try {
      const conteudo = await criarConteudo(
        idDaMissao,
        {
          tipo,
          ordem: 1,
          corpo: tipo === "texto" ? corpo : undefined,
          endereco: tipo === "link_externo" ? endereco : undefined,
          autoria,
          fonte: autoria === "terceiro" ? fonte : undefined,
        },
        sessao.token,
      );

      if (TIPOS_COM_ENVIO.includes(tipo) && arquivo) {
        definirConteudoId(conteudo.id);
        const confirmado = await enviarArquivoComRetomada(conteudo.id, arquivo);
        limparRascunho();
        onSalvo(confirmado);
        return;
      }

      limparRascunho();
      onSalvo(conteudo);
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
      definirErroDeRecusa("Não foi possível salvar o conteúdo. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Novo conteúdo da missão">
      <AvisoDeColeta dado="o conteúdo autoral que você publica na missão" />
      <div className="cg-campo">
        <label htmlFor={idDoTipo}>Tipo de conteúdo</label>
        <select
          id={idDoTipo}
          value={tipo}
          onChange={(evento) => {
            definirTipo(evento.target.value as TipoDeConteudo);
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
          <label htmlFor="conteudo-corpo">Texto da missão</label>
          <textarea
            id="conteudo-corpo"
            value={corpo}
            onChange={(evento) => definirCorpo(evento.target.value)}
            rows={8}
          />
        </div>
      )}

      {tipo === "link_externo" && (
        <Campo
          rotulo="Endereço do vídeo"
          valor={endereco}
          aoAlterar={definirEndereco}
          tipo="url"
        />
      )}

      {TIPOS_COM_ENVIO.includes(tipo) && (
        <div className="cg-campo">
          <label htmlFor="conteudo-arquivo">Arquivo</label>
          <input
            id="conteudo-arquivo"
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

      <div className="cg-campo">
        <label htmlFor={idDaAutoria}>Autoria</label>
        <select
          id={idDaAutoria}
          value={autoria}
          onChange={(evento) => definirAutoria(evento.target.value as AutoriaDoConteudo)}
        >
          <option value="propria">Própria</option>
          <option value="terceiro">De terceiro</option>
        </select>
      </div>

      {autoria === "terceiro" && (
        <Campo
          rotulo="Fonte"
          valor={fonte}
          aoAlterar={definirFonte}
          erro={erroDeCampo === "Conteúdo de terceiro exige a fonte." ? erroDeCampo : null}
        />
      )}

      {erroDeCampo && erroDeCampo !== "Conteúdo de terceiro exige a fonte." && (
        <Aviso tipo="erro">{erroDeCampo}</Aviso>
      )}
      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Salvar conteúdo
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
