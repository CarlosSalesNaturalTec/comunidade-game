import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useId, useState } from "react";
import {
  avaliarDesafioExtra,
  type DesafioExtra,
  encerrarDesafioExtra,
  listarDesafiosExtrasPendentes,
  listarDesafiosExtrasPublicados,
} from "./api";

const ROTULO_DA_MODALIDADE: Record<DesafioExtra["modalidade"], string> = {
  aberto: "Aberto",
  direcionado: "Direcionado",
};

const ROTULO_DO_FORMATO: Record<DesafioExtra["formato"], string> = {
  presencial: "Presencial",
  on_line: "On-line",
};

const ROTULO_DO_CUSTEIO: Record<DesafioExtra["custeio"], string> = {
  aporte_do_proponente: "Absorção do proponente",
  saldo_de_recurso: "Saldo de recurso já existente",
};

function formatarData(valor: string): string {
  const data = new Date(`${valor}T00:00:00`);
  if (Number.isNaN(data.getTime())) return valor;
  return data.toLocaleDateString("pt-BR");
}

function formatarDataHora(valorComFuso: string): string {
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

// A natureza "desafios extras" da área Filas: a fila dos já validados pelo
// Mestre, a aprovação oferecida só com lastro provido ou a recusa com
// motivo, e os publicados com o encerramento — nunca uma área própria
// (`RF-02-27`, `RF-02-28`, `RF-02-106`, `RN-02-10`, `RN-02-11`, `RF-14-39`,
// `RN-14-20`, design — decisão 7). Nenhum dado de Guerreiro(a) aparece além
// do nick digitado no direcionado.
export function AvaliacaoDoDesafioExtra() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoMotivo = useId();

  const [pendentes, definirPendentes] = useState<DesafioExtra[] | null>(null);
  const [publicados, definirPublicados] = useState<DesafioExtra[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [selecionado, definirSelecionado] = useState<DesafioExtra | null>(null);
  const [motivo, definirMotivo] = useState("");
  const [erroDeMotivo, definirErroDeMotivo] = useState<string | null>(null);
  const [erroDoDesfecho, definirErroDoDesfecho] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState<"publicado" | "recusado" | null>(null);
  const [confirmandoId, definirConfirmandoId] = useState<string | null>(null);
  const [encerrando, definirEncerrando] = useState(false);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const [listaDePendentes, listaDePublicados] = await Promise.all([
        listarDesafiosExtrasPendentes(sessao.token),
        listarDesafiosExtrasPublicados(sessao.token),
      ]);
      definirPendentes(listaDePendentes);
      definirPublicados(listaDePublicados);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro(
        "Não foi possível carregar os desafios extras. Tente novamente em instantes.",
      );
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  function voltarParaAFila() {
    definirSelecionado(null);
    definirMotivo("");
    definirErroDeMotivo(null);
    definirErroDoDesfecho(null);
  }

  async function avaliar(situacao: "publicado" | "recusado") {
    if (!sessao || !selecionado) return;
    definirErroDeMotivo(null);
    definirErroDoDesfecho(null);

    if (situacao === "recusado" && !motivo.trim()) {
      definirErroDeMotivo("Informe o motivo da recusa.");
      return;
    }

    definirEnviando(situacao);
    try {
      await avaliarDesafioExtra(
        selecionado.id,
        { situacao, motivo: situacao === "recusado" ? motivo : undefined },
        sessao.token,
      );
      voltarParaAFila();
      await carregar();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi) {
        definirErroDoDesfecho(erroCapturado.message);
        return;
      }
      definirErroDoDesfecho(
        "Não foi possível registrar o desfecho. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(null);
    }
  }

  async function encerrar(id: string) {
    if (!sessao) return;
    definirEncerrando(true);
    try {
      await encerrarDesafioExtra(id, sessao.token);
      definirConfirmandoId(null);
      await carregar();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível encerrar o desafio. Tente novamente em instantes.");
    } finally {
      definirEncerrando(false);
    }
  }

  if (selecionado) {
    return (
      <div>
        <Botao variante="secundaria" onClick={voltarParaAFila}>
          Voltar para a fila
        </Botao>

        <dl>
          <dt>Trilha</dt>
          <dd>{selecionado.trilha_id}</dd>
          {selecionado.missao_id && (
            <>
              <dt>Missão</dt>
              <dd>{selecionado.missao_id}</dd>
            </>
          )}
          <dt>Modalidade</dt>
          <dd>{ROTULO_DA_MODALIDADE[selecionado.modalidade]}</dd>
          {selecionado.modalidade === "direcionado" && (
            <>
              <dt>Nick do destinatário</dt>
              <dd>{selecionado.nick_do_destinatario}</dd>
              <dt>Justificativa do vínculo</dt>
              <dd>{selecionado.justificativa_do_vinculo}</dd>
            </>
          )}
          <dt>Recompensa</dt>
          <dd>
            {selecionado.quantidade_disponivel} unidades do tipo de recurso{" "}
            {selecionado.tipo_de_recurso_id}
          </dd>
          <dt>Ponto de apoio</dt>
          <dd>{selecionado.ponto_de_apoio_id}</dd>
          <dt>Critério de atribuição</dt>
          <dd>{selecionado.criterio_de_atribuicao}</dd>
          <dt>Pontos extras</dt>
          <dd>{selecionado.pontos_extras}</dd>
          <dt>Formato</dt>
          <dd>{ROTULO_DO_FORMATO[selecionado.formato]}</dd>
          <dt>Custeio</dt>
          <dd>{ROTULO_DO_CUSTEIO[selecionado.custeio]}</dd>
          <dt>Vigência</dt>
          <dd>
            {formatarData(selecionado.vigencia_inicio)} a{" "}
            {formatarData(selecionado.vigencia_fim)}
          </dd>
        </dl>

        {selecionado.lastro_provido ? (
          <Aviso tipo="sucesso">Lastro da recompensa provido.</Aviso>
        ) : (
          <Aviso tipo="atencao">{selecionado.lastro_faltante}</Aviso>
        )}

        <div className="cg-campo">
          <label htmlFor={idDoMotivo}>Motivo da recusa</label>
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

        {erroDoDesfecho && <Aviso tipo="erro">{erroDoDesfecho}</Aviso>}

        {selecionado.lastro_provido && (
          <Botao onClick={() => avaliar("publicado")} desabilitado={enviando !== null}>
            Aprovar
          </Botao>
        )}
        <Botao
          variante="secundaria"
          onClick={() => avaliar("recusado")}
          desabilitado={enviando !== null}
        >
          Recusar
        </Botao>
      </div>
    );
  }

  return (
    <div>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      <h3>Pendentes de aprovação</h3>
      {pendentes === null && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {pendentes !== null && pendentes.length === 0 && (
        <EstadoDaLista>Nenhum desafio extra aguardando aprovação por enquanto.</EstadoDaLista>
      )}
      {pendentes !== null && pendentes.length > 0 && (
        <ul aria-label="Desafios extras pendentes de aprovação">
          {pendentes.map((desafio) => (
            <li key={desafio.id}>
              <button type="button" onClick={() => definirSelecionado(desafio)}>
                <span>
                  Trilha: {desafio.trilha_id}
                  {desafio.missao_id ? ` · Missão: ${desafio.missao_id}` : ""}
                </span>
                <span>{ROTULO_DA_MODALIDADE[desafio.modalidade]}</span>
                <span>{desafio.criterio_de_atribuicao}</span>
                <span>
                  Recompensa: {desafio.quantidade_disponivel} do tipo{" "}
                  {desafio.tipo_de_recurso_id} · Ponto de apoio: {desafio.ponto_de_apoio_id}
                </span>
                <span>
                  Pontos extras: {desafio.pontos_extras} · {ROTULO_DO_FORMATO[desafio.formato]}{" "}
                  · {ROTULO_DO_CUSTEIO[desafio.custeio]}
                </span>
                <span>
                  Vigência: {formatarData(desafio.vigencia_inicio)} a{" "}
                  {formatarData(desafio.vigencia_fim)}
                </span>
                <span>
                  {desafio.lastro_provido ? "Lastro provido" : desafio.lastro_faltante}
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}

      <h3>Publicados</h3>
      {publicados === null && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {publicados !== null && publicados.length === 0 && (
        <EstadoDaLista>Nenhum desafio extra publicado por enquanto.</EstadoDaLista>
      )}
      {publicados?.map((desafio) => (
        <article key={desafio.id}>
          <p>
            Restam {desafio.quantidade_restante} de {desafio.quantidade_disponivel}. Vigência:{" "}
            {formatarData(desafio.vigencia_inicio)} a {formatarData(desafio.vigencia_fim)}.
          </p>
          {desafio.encerrado_em ? (
            <Aviso tipo="atencao">
              Encerrado em {formatarDataHora(desafio.encerrado_em)}.
            </Aviso>
          ) : confirmandoId === desafio.id ? (
            <div>
              <Aviso tipo="atencao">
                Encerrar devolve ao ponto de apoio a recompensa ainda não entregue, e o desafio
                deixa de receber conclusão.
              </Aviso>
              <Botao onClick={() => encerrar(desafio.id)} desabilitado={encerrando}>
                Confirmar encerramento
              </Botao>
              <Botao
                variante="secundaria"
                onClick={() => definirConfirmandoId(null)}
                desabilitado={encerrando}
              >
                Voltar
              </Botao>
            </div>
          ) : (
            <Botao variante="secundaria" onClick={() => definirConfirmandoId(desafio.id)}>
              Encerrar
            </Botao>
          )}
        </article>
      ))}
    </div>
  );
}
