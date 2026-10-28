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
  corrigirConteudo,
  criarConteudo,
  enviarArquivo,
  type TipoDeConteudo,
} from "./api";

interface Props {
  idDaMissao: string;
  /** Presente, a tela **corrige** aquele conteúdo em vez de criar outro: o
   * tipo fica travado e o arquivo não se troca, porque para isso o caminho é
   * remover e cadastrar outro (`RF-09-123`, `RN-09-45`). */
  conteudo?: ConteudoDaMissao;
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

// A chave desce ao conteúdo quando a tela corrige: indexada só pela missão,
// corrigir um conteúdo e começar outro na mesma missão sobrescreveria um
// texto com o outro (design — decisão 8).
function chaveDoRascunho(idDaMissao: string, idDoConteudo?: string): string {
  const alvo = idDoConteudo ? `${idDaMissao}:${idDoConteudo}` : idDaMissao;
  return `comunidade-game:app-09-mestre:rascunho-de-conteudo:${alvo}`;
}

// O tipo declara o formato aceito pelo `<input type="file">`, para o
// Mestre já ver a lista fechada antes de escolher (`RF-09-115`).
const FORMATOS_ACEITOS: Record<string, string> = {
  imagem: "image/jpeg,image/png,image/webp",
  video: "video/mp4,video/webm",
  arquivo: "application/pdf,image/jpeg,image/png,image/webp,audio/mpeg",
};

export function FormularioDeConteudo({ idDaMissao, conteudo, onSalvo, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoTipo = useId();
  const idDaAutoria = useId();
  const ehCorrecao = conteudo !== undefined;
  const [tipo, definirTipo] = useState<TipoDeConteudo>(conteudo?.tipo ?? "texto");
  const [corpo, definirCorpo] = useState(conteudo?.corpo ?? "");
  const [endereco, definirEndereco] = useState(conteudo?.endereco ?? "");
  const [autoria, definirAutoria] = useState<AutoriaDoConteudo>(
    conteudo?.autoria ?? "propria",
  );
  const [fonte, definirFonte] = useState(conteudo?.fonte ?? "");
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
  const chave = chaveDoRascunho(idDaMissao, conteudo?.id);

  useEffect(() => {
    const rascunho = localStorage.getItem(chave);
    if (rascunho) definirCorpo(rascunho);
  }, [chave]);

  useEffect(() => {
    if (tipo !== "texto") return;
    if (corpo) {
      localStorage.setItem(chave, corpo);
    } else {
      localStorage.removeItem(chave);
    }
  }, [corpo, tipo, chave]);

  function limparRascunho() {
    localStorage.removeItem(chave);
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
    } catch (erro) {
      // Recusa não é queda de rede: convertê-la aqui apagava o motivo que a
      // camada de acesso agora preserva, e a tela dizia "conexão caiu"
      // quando o núcleo tinha explicado o que houve (`RF-01-02`, change
      // `cors-do-bucket-de-armazenamento` — decisão 5).
      if (erro instanceof ErroDaApi) throw erro;
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
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDeRecusa(
        erro instanceof ErroDaApi ? erro.message : MENSAGEM_DE_QUEDA_DE_REDE,
      );
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
    if (!ehCorrecao && TIPOS_COM_ENVIO.includes(tipo) && !arquivo) {
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
      if (ehCorrecao) {
        const corrigido = await corrigirConteudo(
          conteudo.id,
          {
            corpo: tipo === "texto" ? corpo : undefined,
            endereco: tipo === "link_externo" ? endereco : undefined,
            autoria,
            fonte: autoria === "terceiro" ? fonte : undefined,
          },
          sessao.token,
        );
        limparRascunho();
        onSalvo(corrigido);
        return;
      }

      const criado = await criarConteudo(
        idDaMissao,
        {
          tipo,
          corpo: tipo === "texto" ? corpo : undefined,
          endereco: tipo === "link_externo" ? endereco : undefined,
          autoria,
          fonte: autoria === "terceiro" ? fonte : undefined,
        },
        sessao.token,
      );

      if (TIPOS_COM_ENVIO.includes(tipo) && arquivo) {
        definirConteudoId(criado.id);
        const confirmado = await enviarArquivoComRetomada(criado.id, arquivo);
        limparRascunho();
        onSalvo(confirmado);
        return;
      }

      limparRascunho();
      onSalvo(criado);
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
    <form
      onSubmit={aoSubmeter}
      aria-label={ehCorrecao ? "Correção do conteúdo da missão" : "Novo conteúdo da missão"}
    >
      <AvisoDeColeta dado="o conteúdo autoral que você publica na missão" />
      {ehCorrecao ? (
        // Nem tipo nem arquivo se trocam: a tela não os oferece e diz o
        // caminho, em vez de deixar o Mestre descobrir pela recusa do núcleo
        // (`RN-09-45`).
        <div className="cg-campo">
          <p>Tipo de conteúdo: {ROTULO_DO_TIPO[tipo]}</p>
          <p>Para trocar o tipo ou o arquivo, remova este conteúdo e cadastre outro.</p>
        </div>
      ) : (
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
      )}

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

      {!ehCorrecao && TIPOS_COM_ENVIO.includes(tipo) && (
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
        {ehCorrecao ? "Salvar correção" : "Salvar conteúdo"}
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
