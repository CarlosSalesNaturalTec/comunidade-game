import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import {
  Aviso,
  Botao,
  Cabecalho,
  Campo,
  EstadoDaLista,
  MidiaDoNucleo,
  Moldura,
} from "comum/react";
import { useCallback, useEffect, useId, useState } from "react";
import {
  type ComprovacaoEntregue,
  type DesbloqueioPendente,
  julgarDesafioPratico,
  lerComprovacaoDoPratico,
  listarDesbloqueiosPendentes,
} from "../trilhas/api";

function formatarMomento(momento: string): string {
  return new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" }).format(
    new Date(momento),
  );
}

// A comprovação em mídia se apresenta pelo tipo **real** do arquivo, não pela
// forma que o Mestre declarou aceitar: a forma diz "vídeo", o tipo diz
// "video/webm", e é o tipo que decide se a tela exibe, toca ou oferece abrir
// (`RF-09-132`).
function midiaDaComprovacao(
  entregue: ComprovacaoEntregue,
): "imagem" | "video" | "audio" | null {
  const tipo = entregue.tipo_do_arquivo ?? "";
  if (tipo.startsWith("image/")) return "imagem";
  if (tipo.startsWith("video/")) return "video";
  if (tipo.startsWith("audio/")) return "audio";
  return null;
}

function temComprovacaoAPublicar(entregue: ComprovacaoEntregue | null): boolean {
  if (entregue === null || entregue.entrega_presencial) return false;
  return entregue.comprovacao !== null || entregue.tem_arquivo;
}

// A produção entregue, à vista do Mestre: julgar sem ver o que foi entregue é
// julgar às cegas, e o critério é o que ele mesmo escreveu para julgar por ele
// (`RF-09-132`, `RF-09-130`, `RF-05-93`).
function ProducaoEntregue({
  pendente,
  token,
}: {
  pendente: DesbloqueioPendente;
  token: string | null;
}) {
  const entregue = pendente.comprovacao_entregue;
  if (entregue === null) {
    return <p>Sem comprovação registrada nesta declaração.</p>;
  }
  if (entregue.entrega_presencial) {
    // Nunca apresentada como entrega faltando: é a alternativa de quem não
    // entrega pelo aparelho, e vale (`RN-05-51`).
    return <p>Entrega presencial: este Guerreiro(a) vai mostrar a produção no encontro.</p>;
  }

  const midia = entregue.tem_arquivo ? midiaDaComprovacao(entregue) : null;
  const buscar = (_id: string, chave: string) =>
    lerComprovacaoDoPratico(pendente.missao_id, pendente.guerreiro_id, chave);

  return (
    <div className="cg-bancada__producao">
      {entregue.comprovacao !== null && (
        <p className="cg-bancada__comprovacao-escrita">{entregue.comprovacao}</p>
      )}
      {midia !== null && (
        <MidiaDoNucleo
          id={pendente.id}
          buscar={buscar}
          token={token}
          tipo={midia}
          alt={`Produção entregue por ${pendente.guerreiro_nome ?? "este Guerreiro(a)"}`}
          textoDeErro="A produção entregue não abriu. Você ainda pode julgar."
        />
      )}
      {entregue.tem_arquivo && midia === null && (
        <p>
          A produção veio em arquivo que esta tela não exibe
          {entregue.tipo_do_arquivo !== null ? ` (${entregue.tipo_do_arquivo})` : ""}. Abra-o
          para conferir antes de julgar.
        </p>
      )}
      {/* Sem texto nem arquivo, a tela diz o que de fato aconteceu, e nunca
          um envio em andamento que não existe (`RF-09-132`, `RF-05-93`). */}
      {entregue.comprovacao === null &&
        !entregue.tem_arquivo &&
        (entregue.forma === null ? (
          <p>Este desafio não pedia comprovação quando foi declarado.</p>
        ) : (
          <p>
            O arquivo não chegou. O Guerreiro(a) ainda pode enviá-lo pela tela da missão até
            você julgar.
          </p>
        ))}
    </div>
  );
}

// Os dois vereditos e o motivo de **uma** pendência, enviados num ato só
// (`RF-09-133`, `RF-09-134`).
function Julgamento({
  pendente,
  julgando,
  aoJulgar,
}: {
  pendente: DesbloqueioPendente;
  julgando: boolean;
  aoJulgar: (veredito: {
    cumpriu: boolean;
    publicavel: boolean;
    motivo: string | null;
  }) => void;
}) {
  const [cumpriu, definirCumpriu] = useState(true);
  const [publicavel, definirPublicavel] = useState(false);
  const [motivo, definirMotivo] = useState("");
  const idDoCumpriu = useId();
  const idDoPublicavel = useId();

  // `publicavel` só vale sobre entrega cumprida e com comprovação gravada: o
  // inválido se impede antes do toque, não se explica depois dele (`RN-09-52`).
  const podePublicar = cumpriu && temComprovacaoAPublicar(pendente.comprovacao_entregue);
  // O motivo é exigido quando o julgamento nega algo — e não publicar só é
  // negativa quando publicar era possível (`RN-09-53`).
  const negaAlgo = !cumpriu || (podePublicar && !publicavel);
  const faltaMotivo = negaAlgo && motivo.trim() === "";

  return (
    <div className="cg-bancada__julgamento">
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
        {!podePublicar && (
          <p className="cg-bancada__nota">
            {cumpriu
              ? "Não há comprovação a publicar nesta declaração."
              : "Só a entrega que você julgar cumprida pode ir à vitrine."}
          </p>
        )}
      </div>

      <Campo
        rotulo="Motivo, em linguagem simples — é o Guerreiro(a) que lê"
        valor={motivo}
        aoAlterar={definirMotivo}
      />
      {faltaMotivo && (
        <p className="cg-bancada__nota">
          Escreva o motivo: quando o julgamento nega algo, o Guerreiro(a) precisa saber por
          quê.
        </p>
      )}

      <Botao
        onClick={() =>
          aoJulgar({
            cumpriu,
            publicavel: publicavel && podePublicar,
            motivo: motivo.trim() === "" ? null : motivo.trim(),
          })
        }
        desabilitado={julgando || faltaMotivo}
      >
        Julgar
      </Botao>
    </div>
  );
}

// A bancada dos desafios práticos declarados como cumpridos, ainda não
// julgados, das próprias trilhas — com a **produção à vista** e os **dois
// vereditos**: cumprir abre a missão seguinte e credita os 5 pontos, e
// publicável leva a entrega à vitrine. Não passar nunca elimina ninguém
// (`RF-09-26`, `RF-09-117`, `RF-09-132` a `RF-09-135`, `RF-05-13`,
// `RF-05-14`).
export function TelaDeDesbloqueiosPendentes() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [pendentes, definirPendentes] = useState<DesbloqueioPendente[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [julgando, definirJulgando] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const resultado = await listarDesbloqueiosPendentes(sessao.token);
      definirPendentes(resultado);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar a bancada. Tente novamente em instantes.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  async function julgar(
    pendente: DesbloqueioPendente,
    veredito: { cumpriu: boolean; publicavel: boolean; motivo: string | null },
  ) {
    if (!sessao) return;
    definirJulgando(pendente.id);
    definirErro(null);
    try {
      await julgarDesafioPratico(
        pendente.missao_id,
        pendente.guerreiro_id,
        veredito,
        sessao.token,
      );
      definirPendentes((atual) => (atual ?? []).filter((item) => item.id !== pendente.id));
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      // A recusa chega com o motivo e **sem** limpar o que o Mestre marcou ou
      // escreveu: o estado do julgamento vive na pendência, que não é
      // remontada.
      definirErro(
        erroCapturado instanceof Error && erroCapturado.message
          ? erroCapturado.message
          : "Não foi possível julgar agora. Tente novamente em instantes.",
      );
    } finally {
      definirJulgando(null);
    }
  }

  return (
    <Moldura>
      <Cabecalho titulo="Desafios práticos a julgar" />
      <p>
        <strong>Cumpriu</strong> abre a missão seguinte para aquele Guerreiro(a) e credita 5
        pontos. <strong>Pode ir à vitrine</strong> é o que leva a produção ao portfólio público
        — e só isso. Não passar não o elimina: ele entrega de novo, sem limite.
      </p>

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {pendentes === null && <EstadoDaLista>Carregando a bancada…</EstadoDaLista>}
      {pendentes !== null && pendentes.length === 0 && (
        <EstadoDaLista>Nenhum desafio prático esperando julgamento.</EstadoDaLista>
      )}
      {pendentes !== null && pendentes.length > 0 && (
        <ul
          className="lista-de-desbloqueios-pendentes"
          aria-label="Desafios práticos a julgar"
        >
          {pendentes.map((pendente) => (
            <li key={pendente.id} className="lista-de-desbloqueios-pendentes__item">
              <p>
                <strong>{pendente.guerreiro_nome ?? "Guerreiro(a)"}</strong> —{" "}
                {pendente.missao_titulo}
              </p>
              <p>Declarado em {formatarMomento(pendente.momento)}</p>

              {pendente.criterio_de_aceite !== null && (
                <p className="cg-bancada__criterio">
                  <strong>Critério que você declarou:</strong> {pendente.criterio_de_aceite}
                </p>
              )}

              <ProducaoEntregue pendente={pendente} token={sessao?.token ?? null} />

              <Julgamento
                pendente={pendente}
                julgando={julgando === pendente.id}
                aoJulgar={(veredito) => julgar(pendente, veredito)}
              />
            </li>
          ))}
        </ul>
      )}
    </Moldura>
  );
}
