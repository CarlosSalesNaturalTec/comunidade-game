import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { type FormEvent, useId, useState } from "react";
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

const FORMATOS_ACEITOS: Record<"audio" | "foto", string> = {
  audio: "audio/webm,audio/mp4,audio/mpeg",
  foto: "image/jpeg,image/png,image/webp",
};

const OPCOES_DE_FORMA: { valor: FormaDeEntrega; rotulo: string }[] = [
  { valor: "texto", rotulo: "Escrever" },
  { valor: "audio", rotulo: "Gravar a fala" },
  { valor: "foto", rotulo: "Fotografar" },
  { valor: "encontro", rotulo: "Entregar ao Mestre no encontro" },
];

function SeletorDeForma({
  forma,
  aoEscolher,
}: {
  forma: FormaDeEntrega;
  aoEscolher: (forma: FormaDeEntrega) => void;
}) {
  return (
    <div
      className="cg-entrega-de-producao__formas"
      role="radiogroup"
      aria-label="Forma de entrega"
    >
      {OPCOES_DE_FORMA.map((opcao) => (
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
// `RN-05-37`). O aviso do descarte vem antes do envio de áudio ou foto
// (`RF-05-76`, `RN-05-36`), e a devolutiva, depois, nunca como nota — só
// como retorno construtivo que não vale ponto (`RF-05-75`, `RF-05-77`,
// `RN-05-05`).
export function EntregaDaProducao({ missaoId, atividades }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoCampo = useId();
  const idDaAtividade = useId();
  const [atividadeId, definirAtividadeId] = useState(atividades[0]?.id ?? "");
  const [forma, definirForma] = useState<FormaDeEntrega>("texto");
  const [producao, definirProducao] = useState("");
  const [arquivo, definirArquivo] = useState<File | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [erroDeCampo, definirErroDeCampo] = useState<string | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [resultado, definirResultado] = useState<ProducaoDaMissao | null>(null);

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

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (forma === "encontro") return;
    if (!atividadeId) {
      definirErroDeCampo("Escolha a atividade que você está entregando.");
      return;
    }
    if (forma === "texto" && !producao.trim()) {
      definirErroDeCampo("Escreva a sua produção.");
      return;
    }
    if ((forma === "audio" || forma === "foto") && !arquivo) {
      definirErroDeCampo(
        forma === "audio" ? "Grave o áudio para enviar." : "Escolha a foto para enviar.",
      );
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
          texto: forma === "texto" ? producao : undefined,
          arquivo: forma !== "texto" && arquivo ? arquivo : undefined,
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
      <SeletorDeForma forma={forma} aoEscolher={definirForma} />

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

          {forma === "texto" && (
            <div className="cg-campo">
              <label htmlFor={idDoCampo}>Sua produção</label>
              <textarea
                id={idDoCampo}
                value={producao}
                onChange={(evento) => definirProducao(evento.target.value)}
                rows={8}
              />
            </div>
          )}

          {(forma === "audio" || forma === "foto") && (
            <>
              <Aviso tipo="atencao">
                {forma === "audio" ? "O áudio" : "A foto"} é usado só para ler o que você fez —
                depois é descartado. Fica guardado só o texto e o retorno.
              </Aviso>
              <div className="cg-campo">
                <label htmlFor={idDoCampo}>{forma === "audio" ? "Áudio" : "Foto"}</label>
                <input
                  id={idDoCampo}
                  type="file"
                  accept={FORMATOS_ACEITOS[forma]}
                  onChange={(evento) => definirArquivo(evento.target.files?.[0] ?? null)}
                />
              </div>
            </>
          )}

          {erroDeCampo && <Aviso tipo="erro">{erroDeCampo}</Aviso>}
          {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

          <Botao tipo="submit" desabilitado={enviando}>
            Entregar
          </Botao>
        </form>
      )}
    </section>
  );
}
