import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import {
  Aviso,
  Botao,
  Campo,
  CampoDeDataHora,
  EstadoDaLista,
  MidiaDoNucleo,
} from "comum/react";
import { type FormEvent, useCallback, useEffect, useId, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import { enviarArquivo, lerComprovacaoDoPratico } from "../trilhas/api";
import {
  type AtividadeDoMestre,
  type AulaDaTurma,
  abrirEnvioDoComprovante,
  type DesfechoDoResultado,
  FORMAS_EM_TEXTO,
  type FormaDoComprovante,
  lancarResultadoDaAtividade,
  lerComprovanteDoResultado,
  lerSituacaoDoPratico,
  listarResultadosDaAula,
  type ResultadoDaAula,
  type SituacaoDoPratico,
} from "./api";

export type ResolucaoDoNick = { id: string } | { erro: string };

interface Props {
  aula: AulaDaTurma;
  atividadesPresenciais: AtividadeDoMestre[];
  resolverNick: (nick: string) => ResolucaoDoNick;
}

const ROTULO_DO_DESFECHO: Record<DesfechoDoResultado, string> = {
  realizada: "Realizada",
  realizada_com_merito: "Realizada com mérito",
  merito_extra_por_auxilio: "Mérito extra por auxílio aos colegas",
};

const ROTULO_DA_FORMA: Record<FormaDoComprovante, string> = {
  texto: "Texto",
  imagem: "Foto ou imagem",
  audio: "Áudio",
  video: "Vídeo",
  arquivo: "Arquivo (PDF)",
  link_externo: "Link",
};

// Os formatos que o núcleo aceita, por forma — a mesma lista fechada da
// criação original (`RF-01-78`).
const FORMATOS_DA_FORMA: Partial<Record<FormaDoComprovante, string>> = {
  imagem: "image/jpeg,image/png,image/webp",
  audio: "audio/mpeg",
  video: "video/mp4,video/webm",
  arquivo: "application/pdf",
};

const MIDIA_QUE_ABRE_NA_TELA: Partial<
  Record<FormaDoComprovante, "imagem" | "video" | "audio">
> = { imagem: "imagem", video: "video", audio: "audio" };

function midiaDoTipoDoArquivo(tipo: string | null): "imagem" | "video" | "audio" | null {
  if (tipo?.startsWith("image/")) return "imagem";
  if (tipo?.startsWith("video/")) return "video";
  if (tipo?.startsWith("audio/")) return "audio";
  return null;
}

// O Guerreiro(a) declarou e aguarda o Mestre: o julgamento recai sobre a
// entrega dele. Sem declaração, ou com a recusada, o Mestre declara em nome
// dele com o comprovante deste lançamento (`RN-09-66`).
function julgaAEntregaDoGuerreiro(situacao: SituacaoDoPratico): boolean {
  return situacao.estado === "aguardando";
}

function EntregaDoGuerreiro({
  situacao,
  guerreiroId,
  token,
}: {
  situacao: SituacaoDoPratico;
  guerreiroId: string;
  token: string | null;
}) {
  const entregue = situacao.comprovacao_entregue;
  if (entregue === null) return null;
  if (entregue.entrega_presencial) {
    return <p>O Guerreiro(a) escolheu mostrar a produção a você no encontro.</p>;
  }
  const midia = entregue.tem_arquivo ? midiaDoTipoDoArquivo(entregue.tipo_do_arquivo) : null;
  return (
    <div className="cg-bancada__producao">
      {entregue.comprovacao !== null && (
        <p className="cg-bancada__comprovacao-escrita">{entregue.comprovacao}</p>
      )}
      {midia !== null && (
        <MidiaDoNucleo
          id={`${situacao.missao_id}-${guerreiroId}`}
          buscar={(_id, chave) =>
            lerComprovacaoDoPratico(situacao.missao_id, guerreiroId, chave)
          }
          token={token}
          tipo={midia}
          alt="Produção entregue pelo Guerreiro(a)"
          textoDeErro="A produção entregue não abriu. Você ainda pode julgar."
          ampliavel
        />
      )}
    </div>
  );
}

function ComprovanteLancado({
  resultado,
  token,
}: {
  resultado: ResultadoDaAula;
  token: string | null;
}) {
  const [aberto, definirAberto] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  if (!resultado.tem_arquivo) {
    return <span>{resultado.comprovante_texto}</span>;
  }
  const midia = MIDIA_QUE_ABRE_NA_TELA[resultado.comprovante_tipo];
  if (midia === undefined) {
    return (
      <span>
        <Botao
          variante="secundaria"
          onClick={async () => {
            if (!token) return;
            try {
              const blob = await lerComprovanteDoResultado(resultado.id, token);
              window.open(URL.createObjectURL(blob), "_blank");
            } catch {
              definirErro("O arquivo não abriu. Tente novamente em instantes.");
            }
          }}
        >
          Abrir arquivo
        </Botao>
        {erro && <Aviso tipo="erro">{erro}</Aviso>}
      </span>
    );
  }
  if (!aberto) {
    return (
      <Botao variante="secundaria" onClick={() => definirAberto(true)}>
        Abrir comprovante
      </Botao>
    );
  }
  return (
    <MidiaDoNucleo
      id={resultado.id}
      buscar={lerComprovanteDoResultado}
      token={token}
      tipo={midia}
      alt={`Comprovante de ${resultado.nick ?? "Guerreiro(a)"}`}
      textoDeErro="O comprovante não abriu. Tente novamente em instantes."
      ampliavel
    />
  );
}

// O lançamento do resultado de uma atividade presencial do Mestre, no molde
// da ocorrência de conduta: a atividade num select, o Guerreiro(a) pelo nick,
// um por envio, com o comprovante obrigatório e, quando a missão tem prático
// que ele ainda não cumpriu, o julgamento no mesmo envio (`RF-09-43`,
// `RF-09-44`, `RF-09-148` a `RF-09-151`, `RN-09-18`, `RN-09-64` a `RN-09-66`).
export function LancamentoNaAula({ aula, atividadesPresenciais, resolverNick }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const token = sessao?.token ?? null;
  const idDoSelect = useId();
  const idDaForma = useId();
  const idDoArquivo = useId();
  const idDoDesfecho = useId();
  const idDoCumpriu = useId();
  const idDoPublicavel = useId();

  const [atividadeId, definirAtividadeId] = useState("");
  const [nick, definirNick] = useState("");
  const [forma, definirForma] = useState<FormaDoComprovante>("texto");
  const [texto, definirTexto] = useState("");
  const [arquivo, definirArquivo] = useState<File | null>(null);
  const [momento, definirMomento] = useState("");
  const [desfecho, definirDesfecho] = useState<DesfechoDoResultado>("realizada");
  const [cumpriu, definirCumpriu] = useState(true);
  const [publicavel, definirPublicavel] = useState(false);
  const [motivo, definirMotivo] = useState("");
  const [erro, definirErro] = useState<string | null>(null);
  const [confirmado, definirConfirmado] = useState(false);
  const [enviando, definirEnviando] = useState(false);
  const [progresso, definirProgresso] = useState<number | null>(null);

  const atividade = atividadesPresenciais.find((item) => item.id === atividadeId) ?? null;
  const resolucao = nick.trim() ? resolverNick(nick) : null;
  const guerreiroId = resolucao && "id" in resolucao ? resolucao.id : null;

  const [situacao, definirSituacao] = useState<SituacaoDoPratico | null>(null);
  const [erroDaSituacao, definirErroDaSituacao] = useState<string | null>(null);

  useEffect(() => {
    definirSituacao(null);
    definirErroDaSituacao(null);
    if (!token || !atividade || !guerreiroId) return;
    let cancelado = false;
    lerSituacaoDoPratico(atividade.missao_id, guerreiroId, token)
      .then((lida) => {
        if (cancelado) return;
        definirSituacao(lida);
        // Declarando em nome do Guerreiro(a), o comprovante tem de estar na
        // forma que o prático aceita: a tela já a propõe (`RN-09-66`).
        if (lida.exige_julgamento && !julgaAEntregaDoGuerreiro(lida) && lida.forma_aceita) {
          definirForma(lida.forma_aceita);
        }
      })
      .catch((erroCapturado) => {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErroDaSituacao(
          "Não foi possível conferir o desafio prático desta missão. Tente novamente em instantes.",
        );
      });
    return () => {
      cancelado = true;
    };
  }, [token, atividade, guerreiroId, tratarRecusaDeSessao]);

  const [lancados, definirLancados] = useState<ResultadoDaAula[] | null>(null);
  const [erroDosLancados, definirErroDosLancados] = useState<string | null>(null);

  const carregarLancados = useCallback(async () => {
    if (!token) return;
    try {
      definirLancados(await listarResultadosDaAula(aula.id, token));
      definirErroDosLancados(null);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDosLancados(
        "Não foi possível carregar os resultados lançados. Tente novamente em instantes.",
      );
    }
  }, [aula.id, token, tratarRecusaDeSessao]);

  useEffect(() => {
    carregarLancados();
  }, [carregarLancados]);

  const exigeJulgamento = situacao?.exige_julgamento === true;
  const emTexto = FORMAS_EM_TEXTO.includes(forma);
  const temComprovante = emTexto ? texto.trim() !== "" : arquivo !== null;
  // Publicável só sobre entrega cumprida e com comprovação a publicar
  // (`RN-09-52`): a do Guerreiro(a), quando julga a dele, ou o comprovante
  // deste lançamento, quando declara em nome dele.
  const podePublicar = (() => {
    if (!cumpriu || situacao === null) return false;
    if (julgaAEntregaDoGuerreiro(situacao)) {
      const entregue = situacao.comprovacao_entregue;
      return (
        entregue !== null &&
        !entregue.entrega_presencial &&
        (entregue.comprovacao !== null || entregue.tem_arquivo)
      );
    }
    return situacao.forma_aceita !== null && temComprovante;
  })();
  const negaAlgo = !cumpriu || (podePublicar && !publicavel);

  function limparGuerreiro() {
    definirNick("");
    definirTexto("");
    definirArquivo(null);
    definirCumpriu(true);
    definirPublicavel(false);
    definirMotivo("");
    definirProgresso(null);
  }

  async function aoLancar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErro(null);
    definirConfirmado(false);

    if (!atividade) {
      definirErro("Escolha a atividade.");
      return;
    }
    const resolvido = resolverNick(nick);
    if ("erro" in resolvido) {
      definirErro(resolvido.erro);
      return;
    }
    if (!temComprovante) {
      definirErro(
        emTexto
          ? "Escreva o comprovante do que o Guerreiro(a) produziu."
          : "Escolha o arquivo do comprovante.",
      );
      return;
    }
    if (exigeJulgamento && situacao !== null && !julgaAEntregaDoGuerreiro(situacao)) {
      if (situacao.forma_aceita !== null && situacao.forma_aceita !== forma) {
        definirErro(
          `Este desafio prático aceita comprovação em ${ROTULO_DA_FORMA[
            situacao.forma_aceita
          ].toLowerCase()}: o comprovante precisa estar nessa forma.`,
        );
        return;
      }
    }
    if (exigeJulgamento && negaAlgo && motivo.trim() === "") {
      definirErro(
        "Escreva o motivo: quando o julgamento nega algo, o Guerreiro(a) precisa saber por quê.",
      );
      return;
    }
    if (!token) return;

    definirEnviando(true);
    try {
      let comprovante: { tipo: FormaDoComprovante; texto?: string; envio_id?: string };
      if (emTexto) {
        comprovante = { tipo: forma, texto: texto.trim() };
      } else if (arquivo) {
        const envio = await abrirEnvioDoComprovante(
          atividade.id,
          forma,
          arquivo.type,
          arquivo.size,
          token,
        );
        await enviarArquivo(envio.endereco_da_sessao, arquivo, (enviados, total) =>
          definirProgresso(total > 0 ? Math.round((enviados / total) * 100) : 0),
        );
        comprovante = { tipo: forma, envio_id: envio.envio_id };
      } else {
        return;
      }
      await lancarResultadoDaAtividade(
        atividade.id,
        aula.id,
        {
          guerreiro_id: resolvido.id,
          momento_do_fato: momento,
          comprovante,
          desfecho,
          ...(exigeJulgamento
            ? {
                julgamento_do_pratico: {
                  cumpriu,
                  publicavel: publicavel && podePublicar,
                  motivo: motivo.trim() === "" ? null : motivo.trim(),
                },
              }
            : {}),
        },
        token,
      );
      definirConfirmado(true);
      limparGuerreiro();
      carregarLancados();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      // A recusa chega em linguagem simples, sem código nem jargão (`RN-09-16`).
      if (erroCapturado instanceof ErroDaApi) {
        definirErro(erroCapturado.message);
        return;
      }
      definirErro("Não foi possível registrar o lançamento. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
      definirProgresso(null);
    }
  }

  return (
    <section aria-label="Lançar resultado de uma atividade">
      <h2>Lançar resultado de uma atividade</h2>
      <AvisoDeColeta dado="o comprovante do resultado e o julgamento do desafio prático do Guerreiro(a)" />
      {atividadesPresenciais.length === 0 && <p>Nenhuma atividade presencial sua.</p>}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {confirmado && <Aviso tipo="sucesso">Lançamento registrado.</Aviso>}
      <form onSubmit={aoLancar} aria-label="Lançar resultado de uma atividade">
        <div className="cg-campo">
          <label htmlFor={idDoSelect}>Atividade</label>
          <select
            id={idDoSelect}
            value={atividadeId}
            onChange={(evento) => definirAtividadeId(evento.target.value)}
          >
            <option value="">Selecione a atividade</option>
            {atividadesPresenciais.map((item) => (
              <option key={item.id} value={item.id}>
                {item.titulo}
              </option>
            ))}
          </select>
        </div>
        <Campo rotulo="Nick do Guerreiro(a)" valor={nick} aoAlterar={definirNick} />

        <div className="cg-campo">
          <label htmlFor={idDaForma}>Forma do comprovante</label>
          <select
            id={idDaForma}
            value={forma}
            onChange={(evento) => {
              definirForma(evento.target.value as FormaDoComprovante);
              definirArquivo(null);
            }}
          >
            {Object.entries(ROTULO_DA_FORMA).map(([valor, rotulo]) => (
              <option key={valor} value={valor}>
                {rotulo}
              </option>
            ))}
          </select>
        </div>
        {forma === "texto" && (
          <Campo
            rotulo="Comprovante — o que foi produzido"
            valor={texto}
            aoAlterar={definirTexto}
          />
        )}
        {forma === "link_externo" && (
          <Campo
            rotulo="Endereço do comprovante"
            valor={texto}
            aoAlterar={definirTexto}
            tipo="url"
          />
        )}
        {!emTexto && (
          <div className="cg-campo">
            <label htmlFor={idDoArquivo}>Arquivo do comprovante</label>
            <input
              id={idDoArquivo}
              type="file"
              accept={FORMATOS_DA_FORMA[forma]}
              onChange={(evento) => definirArquivo(evento.target.files?.[0] ?? null)}
            />
          </div>
        )}
        {progresso !== null && <p>Enviando o comprovante… {progresso}%</p>}

        <CampoDeDataHora rotulo="Momento do fato" valor={momento} aoAlterar={definirMomento} />
        <div className="cg-campo">
          <label htmlFor={idDoDesfecho}>Desfecho</label>
          <select
            id={idDoDesfecho}
            value={desfecho}
            onChange={(evento) => definirDesfecho(evento.target.value as DesfechoDoResultado)}
          >
            {Object.entries(ROTULO_DO_DESFECHO).map(([valor, rotulo]) => (
              <option key={valor} value={valor}>
                {rotulo}
              </option>
            ))}
          </select>
        </div>

        {erroDaSituacao && <Aviso tipo="erro">{erroDaSituacao}</Aviso>}
        {situacao !== null && guerreiroId !== null && exigeJulgamento && (
          <fieldset aria-label="Julgamento do desafio prático">
            <legend>Julgamento do desafio prático da missão</legend>
            {situacao.criterio_de_aceite && (
              <p>
                <strong>Critério de aceite:</strong> {situacao.criterio_de_aceite}
              </p>
            )}
            {situacao.forma_aceita && (
              <p>Forma aceita: {ROTULO_DA_FORMA[situacao.forma_aceita].toLowerCase()}.</p>
            )}
            {julgaAEntregaDoGuerreiro(situacao) ? (
              <EntregaDoGuerreiro
                situacao={situacao}
                guerreiroId={guerreiroId}
                token={token}
              />
            ) : (
              <p>
                {situacao.estado === "nao_cumpriu"
                  ? "A entrega anterior não foi aceita. "
                  : "O Guerreiro(a) ainda não declarou este desafio. "}
                O comprovante deste lançamento será a comprovação do desafio prático
                {situacao.forma_aceita ? ", e precisa estar na forma aceita." : "."}
              </p>
            )}
            {situacao.estado === "nao_cumpriu" && situacao.motivo_do_julgamento && (
              <p>Motivo anterior: {situacao.motivo_do_julgamento}</p>
            )}
            <div className="cg-campo">
              <label htmlFor={idDoCumpriu}>
                <input
                  id={idDoCumpriu}
                  type="checkbox"
                  checked={cumpriu}
                  onChange={(evento) => definirCumpriu(evento.target.checked)}
                />{" "}
                Cumpriu o desafio — abre a missão seguinte e credita 5 pontos
              </label>
            </div>
            <div className="cg-campo">
              <label htmlFor={idDoPublicavel}>
                <input
                  id={idDoPublicavel}
                  type="checkbox"
                  checked={publicavel && podePublicar}
                  disabled={!podePublicar}
                  onChange={(evento) => definirPublicavel(evento.target.checked)}
                />{" "}
                Pode ir à vitrine pública
              </label>
            </div>
            <Campo
              rotulo="Motivo, em linguagem simples — é o Guerreiro(a) que lê"
              valor={motivo}
              aoAlterar={definirMotivo}
            />
          </fieldset>
        )}

        <Botao tipo="submit" desabilitado={enviando}>
          Lançar resultado
        </Botao>
      </form>

      <h3>Lançados nesta aula</h3>
      {erroDosLancados && <Aviso tipo="erro">{erroDosLancados}</Aviso>}
      {lancados === null && !erroDosLancados && (
        <EstadoDaLista>Carregando os lançamentos…</EstadoDaLista>
      )}
      {lancados !== null && lancados.length === 0 && (
        <EstadoDaLista>Nenhum resultado lançado nesta aula.</EstadoDaLista>
      )}
      {lancados !== null && lancados.length > 0 && (
        <ul className="lista-de-turmas" aria-label="Lançados nesta aula">
          {lancados.map((resultado) => (
            <li key={resultado.id} className="lista-de-turmas__item">
              <div className="lista-de-turmas__linha">
                <span>
                  {resultado.nick ?? "sem nick"} — {resultado.atividade_titulo} ·{" "}
                  {ROTULO_DO_DESFECHO[resultado.desfecho] ?? resultado.desfecho}
                </span>
              </div>
              <ComprovanteLancado resultado={resultado} token={token} />
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
