import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { useCallback, useEffect, useId, useState } from "react";
import {
  anularPergunta,
  type EstadoDaPartida,
  encerrarPartida,
  lerEstadoDaPartida,
  liberarResultado,
  listarPerguntasDaMissao,
  type PerguntaDeQuiz,
  porPerguntaNoAr,
} from "./api";

const INTERVALO_DE_SONDAGEM_EM_MS = 2000;

const MENSAGEM_DE_PERDA_DE_CONTATO =
  "Perdemos contato com o núcleo. A tela segue com o último estado conhecido e volta a atualizar sozinha assim que a rede voltar.";

interface Props {
  idDaPartida: string;
  missaoId: string;
}

export function TelaDeConducao({ idDaPartida, missaoId }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoCampo = useId();
  const [estado, definirEstado] = useState<EstadoDaPartida | null>(null);
  const [perdeuContato, definirPerdeuContato] = useState(false);
  const [perguntas, definirPerguntas] = useState<PerguntaDeQuiz[] | null>(null);
  const [perguntaEscolhidaId, definirPerguntaEscolhidaId] = useState("");
  const [erro, definirErro] = useState<string | null>(null);
  const [processando, definirProcessando] = useState(false);

  const sondar = useCallback(async () => {
    if (!sessao) return;
    try {
      const novoEstado = await lerEstadoDaPartida(idDaPartida, sessao.token);
      definirEstado(novoEstado);
      definirPerdeuContato(false);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirPerdeuContato(true);
    }
  }, [sessao, idDaPartida, tratarRecusaDeSessao]);

  useEffect(() => {
    sondar();
    const intervalo = setInterval(sondar, INTERVALO_DE_SONDAGEM_EM_MS);
    return () => clearInterval(intervalo);
  }, [sondar]);

  useEffect(() => {
    if (!sessao) return;
    listarPerguntasDaMissao(missaoId, sessao.token)
      .then((pagina) => definirPerguntas(pagina.itens))
      .catch(() => definirPerguntas([]));
  }, [sessao, missaoId]);

  const executar = useCallback(
    async (acao: () => Promise<EstadoDaPartida>) => {
      definirErro(null);
      definirProcessando(true);
      try {
        const novoEstado = await acao();
        definirEstado(novoEstado);
      } catch (erroCapturado) {
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro(
          erroCapturado instanceof ErroDaApi
            ? erroCapturado.message
            : "Não foi possível concluir a ação. Tente novamente.",
        );
      } finally {
        definirProcessando(false);
      }
    },
    [tratarRecusaDeSessao],
  );

  const aoIniciarPergunta = useCallback(() => {
    if (!sessao || !perguntaEscolhidaId) return;
    executar(() => porPerguntaNoAr(idDaPartida, perguntaEscolhidaId, sessao.token));
  }, [sessao, idDaPartida, perguntaEscolhidaId, executar]);

  const aoLiberarResultado = useCallback(() => {
    if (!sessao) return;
    executar(() => liberarResultado(idDaPartida, sessao.token));
  }, [sessao, idDaPartida, executar]);

  const aoAnular = useCallback(() => {
    const perguntaId = estado?.pergunta_no_ar?.pergunta_id;
    if (!sessao || !perguntaId) return;
    executar(async () => {
      await anularPergunta(idDaPartida, perguntaId, sessao.token);
      return lerEstadoDaPartida(idDaPartida, sessao.token);
    });
  }, [sessao, idDaPartida, estado, executar]);

  const aoEncerrar = useCallback(() => {
    if (!sessao) return;
    executar(async () => {
      await encerrarPartida(idDaPartida, sessao.token);
      return lerEstadoDaPartida(idDaPartida, sessao.token);
    });
  }, [sessao, idDaPartida, executar]);

  if (!estado) {
    return <p role="status">Carregando a partida…</p>;
  }

  const totalDeEquipes = estado.equipes_disputantes.length;
  const totalDeRespostas = estado.equipes_que_responderam.length;
  const perguntaNoAr = estado.pergunta_no_ar;

  return (
    <div>
      {perdeuContato && <Aviso tipo="atencao">{MENSAGEM_DE_PERDA_DE_CONTATO}</Aviso>}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {perguntaNoAr && (
        <section aria-label="Pergunta no ar">
          <h2>{perguntaNoAr.enunciado}</h2>
          <ul>
            {perguntaNoAr.alternativas.map((alternativa, indice) => (
              <li key={alternativa}>
                {indice + 1}. {alternativa}
              </li>
            ))}
          </ul>

          {!perguntaNoAr.resultado_liberado && (
            <>
              <p role="status">
                {totalDeRespostas} de {totalDeEquipes} equipes já responderam.
              </p>
              <Botao onClick={aoLiberarResultado} desabilitado={processando}>
                Liberar resultado
              </Botao>
            </>
          )}

          {perguntaNoAr.resultado_liberado && (
            <Aviso tipo="sucesso">
              A alternativa correta é a {perguntaNoAr.alternativa_correta}.{" "}
              {perguntaNoAr.equipes_que_acertaram &&
              perguntaNoAr.equipes_que_acertaram.length > 0
                ? `Acertaram ${perguntaNoAr.equipes_que_acertaram.length} equipe(s), e a primeira foi a equipe ${perguntaNoAr.primeira_equipe_a_acertar}.`
                : "Nenhuma equipe acertou."}
            </Aviso>
          )}

          <Botao variante="secundaria" onClick={aoAnular} desabilitado={processando}>
            Anular esta pergunta
          </Botao>
        </section>
      )}

      {estado.situacao === "aberta" && (
        <section aria-label="Pôr pergunta no ar">
          <div className="cg-campo">
            <label htmlFor={idDoCampo}>Próxima pergunta</label>
            <select
              id={idDoCampo}
              value={perguntaEscolhidaId}
              onChange={(evento) => definirPerguntaEscolhidaId(evento.target.value)}
            >
              <option value="">Escolha uma pergunta do banco</option>
              {(perguntas ?? []).map((pergunta) => (
                <option key={pergunta.id} value={pergunta.id}>
                  {pergunta.enunciado}
                </option>
              ))}
            </select>
          </div>
          <Botao
            onClick={aoIniciarPergunta}
            desabilitado={processando || !perguntaEscolhidaId}
          >
            Pôr pergunta no ar
          </Botao>
        </section>
      )}

      {estado.situacao === "aberta" && (
        <Botao variante="secundaria" onClick={aoEncerrar} desabilitado={processando}>
          Encerrar partida
        </Botao>
      )}

      {estado.situacao === "encerrada" && (
        <Aviso tipo="sucesso">
          Partida encerrada. A pontuação foi lançada automaticamente às equipes.
        </Aviso>
      )}
    </div>
  );
}
