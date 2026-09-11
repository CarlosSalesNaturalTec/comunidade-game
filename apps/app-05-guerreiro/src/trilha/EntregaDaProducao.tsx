import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { existeTranscricaoDeFala, iniciarTranscricao } from "comum/fala";
import { Aviso, Botao } from "comum/react";
import { type FormEvent, useEffect, useId, useRef, useState } from "react";
import {
  type AtividadeDaMissaoPublica,
  entregarProducaoIndividual,
  type FormaDeEntregaDaProducao,
  type ProducaoDaMissao,
} from "../api/trilha";

interface Props {
  missaoId: string;
  atividades: AtividadeDaMissaoPublica[];
}

type FormaDeEntrega = FormaDeEntregaDaProducao | "encontro";

const FORMATOS_DE_FOTO = "image/jpeg,image/png,image/webp";

const MENSAGEM_SEM_TRANSCRICAO =
  "Este aparelho não transforma a sua fala em texto. Você pode escrever, fotografar o que fez " +
  "à mão ou levar ao Mestre no encontro.";

const MENSAGEM_DE_FALHA_NA_FALA =
  "Não consegui entender a sua fala. Fale de novo ou escreva o que você fez.";

function opcoesDeForma(transcreve: boolean): { valor: FormaDeEntrega; rotulo: string }[] {
  return [
    { valor: "texto" as FormaDeEntrega, rotulo: "Escrever" },
    ...(transcreve ? [{ valor: "audio" as FormaDeEntrega, rotulo: "Falar" }] : []),
    { valor: "foto" as FormaDeEntrega, rotulo: "Fotografar" },
    { valor: "encontro" as FormaDeEntrega, rotulo: "Entregar ao Mestre no encontro" },
  ];
}

function SeletorDeForma({
  forma,
  opcoes,
  aoEscolher,
}: {
  forma: FormaDeEntrega;
  opcoes: { valor: FormaDeEntrega; rotulo: string }[];
  aoEscolher: (forma: FormaDeEntrega) => void;
}) {
  return (
    <div
      className="cg-entrega-de-producao__formas"
      role="radiogroup"
      aria-label="Forma de entrega"
    >
      {opcoes.map((opcao) => (
        <Botao
          key={opcao.valor}
          variante={forma === opcao.valor ? "primaria" : "secundaria"}
          onClick={() => aoEscolher(opcao.valor)}
        >
          {opcao.rotulo}
        </Botao>
      ))}
    </div>
  );
}

// A entrega da produção da missão, nas três formas mais o caminho do
// encontro presencial, sempre com o mesmo destaque (`RF-05-74`, `RF-05-78`,
// `RN-05-37`). A fala é transcrita no próprio aparelho, por `comum/fala`, e
// ao núcleo vai só o texto — a gravação nunca sai daqui (`RF-05-76`,
// `RN-05-32`, documento 03 §1.12); onde o aparelho não transcreve, a fala
// nem é oferecida. O aviso do descarte da foto vem antes do envio
// (`RN-05-36`), e a devolutiva, depois, nunca como nota — só como retorno
// construtivo que não vale ponto (`RF-05-75`, `RF-05-77`, `RN-05-05`).
export function EntregaDaProducao({ missaoId, atividades }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoCampo = useId();
  const idDaAtividade = useId();
  const [atividadeId, definirAtividadeId] = useState(atividades[0]?.id ?? "");
  const [forma, definirForma] = useState<FormaDeEntrega>("texto");
  const [producao, definirProducao] = useState("");
  const [arquivo, definirArquivo] = useState<File | null>(null);
  const [ouvindo, definirOuvindo] = useState(false);
  const [avisoDeFala, definirAvisoDeFala] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [erroDeCampo, definirErroDeCampo] = useState<string | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [resultado, definirResultado] = useState<ProducaoDaMissao | null>(null);
  const encerradorRef = useRef<(() => void) | null>(null);
  const transcreve = existeTranscricaoDeFala();

  // Sair da tela com o microfone aberto o fecha junto: ele nunca fica
  // ouvindo sozinho (`RN-05-32`).
  useEffect(() => {
    return () => encerradorRef.current?.();
  }, []);

  if (atividades.length === 0) return null;

  if (resultado) {
    return (
      <section aria-label="Entrega da produção" className="cg-entrega-de-producao">
        <Aviso tipo="sucesso">Sua produção foi guardada!</Aviso>
        {resultado.devolutiva ? (
          <div className="cg-entrega-de-producao__devolutiva">
            <h3>O que você mandou bem e o próximo passo</h3>
            <p>{resultado.devolutiva}</p>
          </div>
        ) : (
          <Aviso tipo="andamento">
            O retorno não veio agora, mas o que você escreveu está guardado — nada se perdeu.
          </Aviso>
        )}
        <Aviso tipo="andamento">
          Isso não vale ponto: o resultado da atividade fica aguardando o Mestre lançar.
        </Aviso>
      </section>
    );
  }

  function alternarFala() {
    if (ouvindo) {
      encerradorRef.current?.();
      return;
    }
    definirAvisoDeFala(null);
    definirErroDeCampo(null);
    definirOuvindo(true);
    encerradorRef.current = iniciarTranscricao({
      aoTranscrever: (transcricao) => definirProducao(transcricao),
      aoFalhar: () => definirAvisoDeFala(MENSAGEM_DE_FALHA_NA_FALA),
      aoEncerrar: () => {
        definirOuvindo(false);
        encerradorRef.current = null;
      },
    });
  }

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (forma === "encontro") return;
    if (!atividadeId) {
      definirErroDeCampo("Escolha a atividade que você está entregando.");
      return;
    }
    if (forma !== "foto" && !producao.trim()) {
      definirErroDeCampo(
        forma === "audio" ? "Fale ou escreva a sua produção." : "Escreva a sua produção.",
      );
      return;
    }
    if (forma === "foto" && !arquivo) {
      definirErroDeCampo("Escolha a foto para enviar.");
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      const producaoRegistrada = await entregarProducaoIndividual(
        missaoId,
        {
          atividadeId,
          forma,
          texto: forma === "foto" ? undefined : producao,
          arquivo: forma === "foto" && arquivo ? arquivo : undefined,
        },
        sessao.token,
      );
      definirResultado(producaoRegistrada);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.status === 503) {
        definirErroDeRecusa(
          "Não foi possível ler o que você enviou agora. Tente enviar de novo em instantes.",
        );
        return;
      }
      if (erro instanceof ErroDaApi) {
        definirErroDeRecusa(erro.message);
        return;
      }
      definirErroDeRecusa("Não foi possível entregar agora. Tente de novo em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <section aria-label="Entrega da produção" className="cg-entrega-de-producao">
      <h3>Como você vai entregar o que fez?</h3>
      <SeletorDeForma
        forma={forma}
        opcoes={opcoesDeForma(transcreve)}
        aoEscolher={definirForma}
      />
      {!transcreve && <Aviso tipo="atencao">{MENSAGEM_SEM_TRANSCRICAO}</Aviso>}

      {forma === "encontro" ? (
        <Aviso tipo="sucesso">
          Sem problema — você não perde a missão. É só levar o que fez para o Mestre no próximo
          encontro.
        </Aviso>
      ) : (
        <form onSubmit={aoSubmeter} aria-label="Formulário de entrega da produção">
          {atividades.length > 1 && (
            <div className="cg-campo">
              <label htmlFor={idDaAtividade}>Atividade</label>
              <select
                id={idDaAtividade}
                value={atividadeId}
                onChange={(evento) => definirAtividadeId(evento.target.value)}
              >
                {atividades.map((atividade) => (
                  <option key={atividade.id} value={atividade.id}>
                    {atividade.titulo}
                  </option>
                ))}
              </select>
            </div>
          )}

          {forma === "audio" && (
            <Aviso tipo="atencao">
              A sua fala virá para o texto aqui mesmo: a gravação não sai deste aparelho, e o
              que fica guardado é só o texto e o retorno.
            </Aviso>
          )}

          {forma !== "foto" && (
            <>
              <div className="cg-campo">
                <label htmlFor={idDoCampo}>Sua produção</label>
                <textarea
                  id={idDoCampo}
                  value={producao}
                  onChange={(evento) => definirProducao(evento.target.value)}
                  rows={8}
                />
              </div>
              {forma === "audio" && (
                <div className="cg-campo">
                  <Botao variante="secundaria" onClick={alternarFala} desabilitado={enviando}>
                    {ouvindo ? "Parar de ouvir" : "Falar a produção"}
                  </Botao>
                  {ouvindo && <p role="status">Ouvindo…</p>}
                  {avisoDeFala && <Aviso tipo="atencao">{avisoDeFala}</Aviso>}
                </div>
              )}
            </>
          )}

          {forma === "foto" && (
            <>
              <Aviso tipo="atencao">
                A foto é usada só para ler o que você fez — depois é descartada. Fica guardado
                só o texto e o retorno.
              </Aviso>
              <div className="cg-campo">
                <label htmlFor={idDoCampo}>Foto</label>
                <input
                  id={idDoCampo}
                  type="file"
                  accept={FORMATOS_DE_FOTO}
                  onChange={(evento) => definirArquivo(evento.target.files?.[0] ?? null)}
                />
              </div>
            </>
          )}

          {erroDeCampo && <Aviso tipo="erro">{erroDeCampo}</Aviso>}
          {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

          <Botao tipo="submit" desabilitado={enviando || ouvindo}>
            Entregar
          </Botao>
        </form>
      )}
    </section>
  );
}
