import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import { avaliarSugestao, type Sugestao } from "./api";

interface Props {
  sugestao: Sugestao;
  onFechar: () => void;
  onAvaliado: (sugestao: Sugestao) => void;
}

const ROTULO_DO_PAPEL: Record<string, string> = {
  guerreiro: "Guerreiro(a)",
  mestre: "Mestre",
  apoiador: "Apoiador",
  responsavel: "Responsável",
  admin: "Admin",
};

// O retorno acontece só dentro da plataforma — nenhum caminho de e-mail
// (`RN-02-25`). A adotada credita os 20 extras e o badge de protagonismo na
// regra do núcleo; aqui só mostra o que foi creditado (`RF-01-56`,
// `RN-01-50`).
export function AvaliacaoDeSugestao({ sugestao, onFechar, onAvaliado }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoParecer = useId();
  const idDoMotivo = useId();

  const [parecer, definirParecer] = useState("");
  const [motivo, definirMotivo] = useState("");
  const [erroDeMotivo, definirErroDeMotivo] = useState<string | null>(null);
  const [erroDeEnvio, definirErroDeEnvio] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState<"adotada" | "nao_adotada" | null>(null);

  const jaAvaliada = sugestao.decidido_em !== null;

  async function avaliar(situacao: "adotada" | "nao_adotada") {
    definirErroDeMotivo(null);
    definirErroDeEnvio(null);

    if (situacao === "nao_adotada" && !motivo.trim()) {
      definirErroDeMotivo("Informe o motivo do retorno.");
      return;
    }
    if (!sessao) return;

    definirEnviando(situacao);
    try {
      const atualizada = await avaliarSugestao(
        sugestao.id,
        {
          situacao,
          parecer: parecer || undefined,
          motivo_do_retorno: situacao === "nao_adotada" ? motivo : undefined,
        },
        sessao.token,
      );
      onAvaliado(atualizada);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "solicitacao_ja_avaliada") {
        definirErroDeEnvio("Esta sugestão já tem um desfecho gravado.");
        return;
      }
      definirErroDeEnvio(
        "Não foi possível registrar o desfecho. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(null);
    }
  }

  function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    avaliar("adotada");
  }

  return (
    <div>
      <Botao variante="secundaria" onClick={onFechar}>
        Voltar para a fila
      </Botao>

      <dl>
        <dt>Autor</dt>
        <dd>{ROTULO_DO_PAPEL[sugestao.papel_do_autor] ?? sugestao.papel_do_autor}</dd>
        <dt>Teor</dt>
        <dd>{sugestao.texto}</dd>
      </dl>

      {jaAvaliada ? (
        <>
          <dl>
            <dt>Desfecho</dt>
            <dd>{sugestao.situacao === "adotada" ? "Adotada" : "Não adotada"}</dd>
            <dt>Parecer</dt>
            <dd>{sugestao.parecer ?? "—"}</dd>
            {sugestao.situacao === "nao_adotada" && (
              <>
                <dt>Motivo do retorno</dt>
                <dd>{sugestao.motivo_do_retorno ?? "—"}</dd>
              </>
            )}
          </dl>
          {sugestao.situacao === "adotada" && (
            <Aviso tipo="sucesso">
              20 pontos extras e o badge de protagonismo foram creditados a quem propôs.
            </Aviso>
          )}
        </>
      ) : (
        <form onSubmit={aoSubmeter} aria-label="Avaliar sugestão">
          <div className="cg-campo">
            <label htmlFor={idDoParecer}>Parecer</label>
            <textarea
              id={idDoParecer}
              value={parecer}
              onChange={(evento) => definirParecer(evento.target.value)}
            />
          </div>

          <div className="cg-campo">
            <label htmlFor={idDoMotivo}>Motivo do retorno (obrigatório se não adotada)</label>
            <textarea
              id={idDoMotivo}
              value={motivo}
              onChange={(evento) => definirMotivo(evento.target.value)}
              aria-invalid={Boolean(erroDeMotivo) || undefined}
            />
            {erroDeMotivo && (
              <p role="alert" className="cg-campo__erro">
                {erroDeMotivo}
              </p>
            )}
          </div>

          {erroDeEnvio && <Aviso tipo="erro">{erroDeEnvio}</Aviso>}

          <Botao tipo="submit" desabilitado={enviando !== null}>
            Adotar
          </Botao>
          <Botao
            variante="secundaria"
            desabilitado={enviando !== null}
            onClick={() => avaliar("nao_adotada")}
          >
            Não adotar
          </Botao>
        </form>
      )}
    </div>
  );
}
