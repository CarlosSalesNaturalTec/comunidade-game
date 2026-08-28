import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import type { AporteHomologado } from "../aportes/api";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import type { AdultoDaLista } from "../personas/api";
import { FormularioDeAdulto } from "../personas/FormularioDeAdulto";
import { avaliarSolicitacaoDeParticipacao, type SolicitacaoDeParticipacao } from "./api";
import { HomologacaoDoAporte } from "./HomologacaoDoAporte";

interface Props {
  solicitacao: SolicitacaoDeParticipacao;
  onFechar: () => void;
  onAvaliado: (solicitacao: SolicitacaoDeParticipacao) => void;
}

const DADO_COLETADO = "a solicitação de participação — nome, e-mail, WhatsApp e apresentação";

// Detalhe da solicitação: desfecho, e — quando aceita — o encaminhamento
// ao cadastro pré-preenchido e a homologação do aporte declarado
// (`RF-02-19`, `RF-02-20`, `RF-02-83`, `RF-02-84`, `RF-02-86`).
export function AvaliacaoDaSolicitacao({ solicitacao, onFechar, onAvaliado }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoParecer = useId();

  const [parecer, definirParecer] = useState("");
  const [erroDeParecer, definirErroDeParecer] = useState<string | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState<"aceita" | "recusada" | null>(null);
  const [adultoCriado, definirAdultoCriado] = useState<AdultoDaLista | null>(null);
  const [aporteHomologado, definirAporteHomologado] = useState<AporteHomologado | null>(null);

  const jaAvaliada = solicitacao.decidido_em !== null;

  async function avaliar(situacao: "aceita" | "recusada") {
    definirErroDeParecer(null);
    definirErroDeRecusa(null);

    if (situacao === "recusada" && !parecer.trim()) {
      definirErroDeParecer("Informe o motivo da recusa.");
      return;
    }
    if (!sessao) return;

    definirEnviando(situacao);
    try {
      const atualizada = await avaliarSolicitacaoDeParticipacao(
        solicitacao.id,
        { situacao, parecer: parecer || undefined },
        sessao.token,
      );
      onAvaliado(atualizada);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "solicitacao_ja_avaliada") {
        definirErroDeRecusa("Esta solicitação já tem um desfecho gravado.");
        return;
      }
      definirErroDeRecusa(
        "Não foi possível registrar o desfecho. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(null);
    }
  }

  function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    avaliar("aceita");
  }

  const podeAbrirCadastro = solicitacao.situacao === "aceita" && !adultoCriado;
  const aportavelAgora =
    adultoCriado !== null &&
    solicitacao.pretensao === "apoiador" &&
    solicitacao.aporte_declarado !== null &&
    aporteHomologado === null;

  return (
    <div>
      <Botao variante="secundaria" onClick={onFechar}>
        Voltar para a fila
      </Botao>

      <AvisoDeColeta dado={DADO_COLETADO} />

      <dl>
        <dt>Nome ou razão social</dt>
        <dd>{solicitacao.nome_ou_razao_social}</dd>
        <dt>E-mail</dt>
        <dd>{solicitacao.email}</dd>
        <dt>WhatsApp</dt>
        <dd>{solicitacao.whatsapp}</dd>
        <dt>Pretensão</dt>
        <dd>{solicitacao.pretensao === "mestre" ? "Mestre" : "Apoiador"}</dd>
        <dt>Apresentação</dt>
        <dd>{solicitacao.apresentacao}</dd>
        {solicitacao.instituicao && (
          <>
            <dt>Instituição</dt>
            <dd>{solicitacao.instituicao}</dd>
          </>
        )}
        {solicitacao.links && (
          <>
            <dt>Links</dt>
            <dd>{solicitacao.links}</dd>
          </>
        )}
        {solicitacao.pretensao === "apoiador" && (
          <>
            <dt>Nick pretendido</dt>
            <dd>{solicitacao.nick ?? "—"}</dd>
            <dt>Aporte declarado</dt>
            <dd>{solicitacao.aporte_declarado ?? "—"}</dd>
            <dt>Comprovante</dt>
            {/* O conteúdo do arquivo nunca sai do núcleo por esta rota
                (`RN-01-28`); aqui só a existência, ainda não exibível. */}
            <dd>
              {solicitacao.comprovante_anexado
                ? "Anexado — leitura do arquivo entra em change própria."
                : "Nenhum comprovante anexado."}
            </dd>
          </>
        )}
      </dl>

      {jaAvaliada ? (
        <dl>
          <dt>Desfecho</dt>
          <dd>{solicitacao.situacao === "aceita" ? "Aceita" : "Recusada"}</dd>
          <dt>Parecer</dt>
          <dd>{solicitacao.parecer ?? "—"}</dd>
        </dl>
      ) : (
        <form onSubmit={aoSubmeter} aria-label="Avaliar solicitação">
          <div className="cg-campo">
            <label htmlFor={idDoParecer}>Parecer</label>
            <textarea
              id={idDoParecer}
              value={parecer}
              onChange={(evento) => definirParecer(evento.target.value)}
              aria-invalid={Boolean(erroDeParecer) || undefined}
            />
            {erroDeParecer && (
              <p role="alert" className="cg-campo__erro">
                {erroDeParecer}
              </p>
            )}
          </div>

          {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

          <Botao tipo="submit" desabilitado={enviando !== null}>
            Aceitar
          </Botao>
          <Botao
            variante="secundaria"
            desabilitado={enviando !== null}
            onClick={() => avaliar("recusada")}
          >
            Recusar
          </Botao>
        </form>
      )}

      {podeAbrirCadastro && (
        <FormularioDeAdulto
          papel={solicitacao.pretensao}
          valorInicial={{
            nome: solicitacao.nome_ou_razao_social,
            email: solicitacao.email,
            whatsapp: solicitacao.whatsapp,
            nick: solicitacao.pretensao === "apoiador" ? (solicitacao.nick ?? "") : undefined,
          }}
          onSalvo={definirAdultoCriado}
          onCancelar={onFechar}
        />
      )}

      {adultoCriado && !aportavelAgora && aporteHomologado === null && (
        <Aviso tipo="sucesso">
          {solicitacao.pretensao === "mestre" ? "Mestre" : "Apoiador"} cadastrado.
        </Aviso>
      )}

      {aportavelAgora && (
        <HomologacaoDoAporte
          provedorId={adultoCriado.id}
          solicitacaoDeParticipacaoId={solicitacao.id}
          aporteDeclarado={solicitacao.aporte_declarado}
          onHomologado={definirAporteHomologado}
        />
      )}

      {aporteHomologado && (
        <Aviso tipo="sucesso">
          Aporte homologado: {aporteHomologado.valor_em_moedas} moedas.
        </Aviso>
      )}
    </div>
  );
}
