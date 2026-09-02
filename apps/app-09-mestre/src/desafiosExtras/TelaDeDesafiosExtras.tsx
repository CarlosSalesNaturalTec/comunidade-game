import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, EstadoDaLista, Moldura } from "comum/react";
import { type FormEvent, useCallback, useEffect, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import { listarMinhasTrilhas } from "../trilhas/api";
import {
  type CusteioDoDesafioExtra,
  type DesafioExtra,
  type FormatoDoDesafioExtra,
  listarFilaDeValidacao,
  listarMeusDesafiosExtras,
  type Modalidade,
  proporDesafioExtra,
  recusarDesafioExtraPeloMestre,
  validarDesafioExtra,
} from "./api";

const TETO_DE_PONTOS_EXTRAS = 10;

const RÓTULO_DA_SITUAÇÃO: Record<DesafioExtra["situacao"], string> = {
  em_validacao_do_mestre: "Em validação do Mestre",
  em_aprovacao_do_admin: "Em aprovação do Admin",
  publicado: "Publicado",
  recusado: "Recusado",
};

// A área única de desafios extras do Mestre: o que ele tem a validar das
// próprias trilhas, o formulário para propor, e o que ele mesmo propôs —
// nunca identificando Guerreiro(a) e nunca confirmando um nick (`RF-09-51`,
// `RF-09-52`, `RF-09-105` a `RF-09-112`, `RN-09-11`, `RN-09-40` a `RN-09-42`,
// `RN-14-20`, design — decisão 7).
export function TelaDeDesafiosExtras() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();

  const [minhasTrilhasIds, definirMinhasTrilhasIds] = useState<Set<string>>(new Set());

  const [fila, definirFila] = useState<DesafioExtra[] | null>(null);
  const [erroDaFila, definirErroDaFila] = useState<string | null>(null);
  const [decidindo, definirDecidindo] = useState<string | null>(null);
  const [parecerPorDesafio, definirParecerPorDesafio] = useState<Record<string, string>>({});
  const [motivoPorDesafio, definirMotivoPorDesafio] = useState<Record<string, string>>({});
  const [erroPorDesafio, definirErroPorDesafio] = useState<Record<string, string>>({});

  const [trilhaId, definirTrilhaId] = useState("");
  const [tipoDeRecursoId, definirTipoDeRecursoId] = useState("");
  const [pontoDeApoioId, definirPontoDeApoioId] = useState("");
  const [quantidadeDisponivel, definirQuantidadeDisponivel] = useState("1");
  const [criterioDeAtribuicao, definirCriterioDeAtribuicao] = useState("");
  const [pontosExtras, definirPontosExtras] = useState("1");
  const [formato, definirFormato] = useState<FormatoDoDesafioExtra>("on_line");
  const [custeio, definirCusteio] = useState<CusteioDoDesafioExtra>("saldo_de_recurso");
  const [aporteId, definirAporteId] = useState("");
  const [modalidade, definirModalidade] = useState<Modalidade>("aberto");
  const [nickDoDestinatario, definirNickDoDestinatario] = useState("");
  const [justificativaPedagogica, definirJustificativaPedagogica] = useState("");
  const [vigenciaInicio, definirVigenciaInicio] = useState("");
  const [vigenciaFim, definirVigenciaFim] = useState("");
  const [enviandoProposta, definirEnviandoProposta] = useState(false);
  const [erroDaProposta, definirErroDaProposta] = useState<string | null>(null);
  const [propostaRegistrada, definirPropostaRegistrada] = useState(false);

  const [meusDesafios, definirMeusDesafios] = useState<DesafioExtra[] | null>(null);
  const [erroDosMeusDesafios, definirErroDosMeusDesafios] = useState<string | null>(null);

  const pontosAcimaDoTeto = Number(pontosExtras) > TETO_DE_PONTOS_EXTRAS;
  const trilhaEhPropria = trilhaId.trim() !== "" && minhasTrilhasIds.has(trilhaId.trim());

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const [novaFila, minhasTrilhas, meus] = await Promise.all([
        listarFilaDeValidacao(sessao.token),
        listarMinhasTrilhas(sessao.token),
        listarMeusDesafiosExtras(sessao.token),
      ]);
      definirFila(novaFila);
      definirMinhasTrilhasIds(new Set(minhasTrilhas.map((trilha) => trilha.id)));
      definirMeusDesafios(meus);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDaFila(
        "Não foi possível carregar a fila agora. Tente novamente em instantes.",
      );
      definirErroDosMeusDesafios("Não foi possível carregar seus desafios agora.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  async function validar(desafio: DesafioExtra) {
    if (!sessao) return;
    const parecer = (parecerPorDesafio[desafio.id] ?? "").trim();
    if (!parecer) {
      definirErroPorDesafio((atual) => ({
        ...atual,
        [desafio.id]: "Escreva o parecer antes de validar.",
      }));
      return;
    }
    definirDecidindo(desafio.id);
    definirErroPorDesafio((atual) => ({ ...atual, [desafio.id]: "" }));
    try {
      await validarDesafioExtra(desafio.id, parecer, sessao.token);
      definirFila((atual) => (atual ?? []).filter((item) => item.id !== desafio.id));
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroPorDesafio((atual) => ({
        ...atual,
        [desafio.id]: "Não foi possível validar agora. Tente novamente em instantes.",
      }));
    } finally {
      definirDecidindo(null);
    }
  }

  async function recusar(desafio: DesafioExtra) {
    if (!sessao) return;
    const motivo = (motivoPorDesafio[desafio.id] ?? "").trim();
    if (!motivo) {
      definirErroPorDesafio((atual) => ({
        ...atual,
        [desafio.id]: "Escreva o motivo antes de recusar.",
      }));
      return;
    }
    definirDecidindo(desafio.id);
    definirErroPorDesafio((atual) => ({ ...atual, [desafio.id]: "" }));
    try {
      await recusarDesafioExtraPeloMestre(desafio.id, motivo, sessao.token);
      definirFila((atual) => (atual ?? []).filter((item) => item.id !== desafio.id));
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroPorDesafio((atual) => ({
        ...atual,
        [desafio.id]: "Não foi possível recusar agora. Tente novamente em instantes.",
      }));
    } finally {
      definirDecidindo(null);
    }
  }

  async function aoEnviarProposta(evento: FormEvent) {
    evento.preventDefault();
    if (!sessao) return;
    if (pontosAcimaDoTeto) {
      definirErroDaProposta(`Pontos extras acima do teto de ${TETO_DE_PONTOS_EXTRAS}.`);
      return;
    }
    definirEnviandoProposta(true);
    definirErroDaProposta(null);
    definirPropostaRegistrada(false);
    try {
      await proporDesafioExtra(
        {
          trilha_id: trilhaId,
          modalidade,
          nick_do_destinatario: modalidade === "direcionado" ? nickDoDestinatario : null,
          justificativa_do_vinculo:
            modalidade === "direcionado" ? justificativaPedagogica : null,
          tipo_de_recurso_id: tipoDeRecursoId,
          ponto_de_apoio_id: pontoDeApoioId,
          quantidade_disponivel: Number(quantidadeDisponivel),
          criterio_de_atribuicao: criterioDeAtribuicao,
          pontos_extras: Number(pontosExtras),
          formato,
          custeio,
          aporte_id: custeio === "aporte_do_proponente" ? aporteId : null,
          vigencia_inicio: vigenciaInicio,
          vigencia_fim: vigenciaFim,
        },
        sessao.token,
      );
      definirPropostaRegistrada(true);
      await carregar();
    } catch (erroCapturado) {
      definirErroDaProposta(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível registrar a proposta. Tente novamente.",
      );
    } finally {
      definirEnviandoProposta(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho titulo="Desafios extras" acao={{ rotulo: "Sair", aoAcionar: sair }} />
      <AvisoDeColeta dado="a proposta de desafio extra, o parecer da validação ou o motivo da recusa, e o nick e a justificativa pedagógica do direcionado, quando houver" />

      <h2>O que você tem a validar</h2>
      {erroDaFila && <Aviso tipo="erro">{erroDaFila}</Aviso>}
      {fila === null && <EstadoDaLista>Carregando a fila…</EstadoDaLista>}
      {fila !== null && fila.length === 0 && (
        <EstadoDaLista>Nenhum desafio extra esperando validação.</EstadoDaLista>
      )}
      {fila !== null && fila.length > 0 && (
        <ul className="lista-de-desafios-a-validar" aria-label="Desafios extras a validar">
          {fila.map((desafio) => (
            <li key={desafio.id} className="lista-de-desafios-a-validar__item">
              <p>Trilha: {desafio.trilha_id}</p>
              <p>
                Recompensa: {desafio.quantidade_disponivel} unidade(s) do tipo{" "}
                {desafio.tipo_de_recurso_id}
              </p>
              <p>Critério de atribuição: {desafio.criterio_de_atribuicao}</p>
              <p>Pontos extras: {desafio.pontos_extras}</p>
              <p>Formato: {desafio.formato === "on_line" ? "On-line" : "Presencial"}</p>
              <p>
                Custeio:{" "}
                {desafio.custeio === "aporte_do_proponente"
                  ? "Aporte do proponente"
                  : "Saldo de recurso"}
              </p>
              <p>
                Vigência: {desafio.vigencia_inicio} a {desafio.vigencia_fim}
              </p>
              {desafio.modalidade === "direcionado" && desafio.nick_do_destinatario && (
                <p>Direcionado ao nick: {desafio.nick_do_destinatario}</p>
              )}

              {erroPorDesafio[desafio.id] && (
                <Aviso tipo="erro">{erroPorDesafio[desafio.id]}</Aviso>
              )}

              <div className="cg-campo">
                <label htmlFor={`parecer-${desafio.id}`}>Parecer</label>
                <textarea
                  id={`parecer-${desafio.id}`}
                  value={parecerPorDesafio[desafio.id] ?? ""}
                  onChange={(evento) =>
                    definirParecerPorDesafio((atual) => ({
                      ...atual,
                      [desafio.id]: evento.target.value,
                    }))
                  }
                />
              </div>
              <Botao onClick={() => validar(desafio)} desabilitado={decidindo === desafio.id}>
                Validar
              </Botao>
              <p>O validado segue para a aprovação do Admin.</p>

              <div className="cg-campo">
                <label htmlFor={`motivo-${desafio.id}`}>Motivo da recusa</label>
                <textarea
                  id={`motivo-${desafio.id}`}
                  value={motivoPorDesafio[desafio.id] ?? ""}
                  onChange={(evento) =>
                    definirMotivoPorDesafio((atual) => ({
                      ...atual,
                      [desafio.id]: evento.target.value,
                    }))
                  }
                />
              </div>
              <Botao
                variante="secundaria"
                onClick={() => recusar(desafio)}
                desabilitado={decidindo === desafio.id}
              >
                Recusar
              </Botao>
              <p>O recusado não chega à aprovação do Admin.</p>
            </li>
          ))}
        </ul>
      )}

      <h2>Propor desafio extra</h2>
      <form onSubmit={aoEnviarProposta}>
        <Campo rotulo="Trilha" valor={trilhaId} aoAlterar={definirTrilhaId} />
        {trilhaId.trim() !== "" &&
          (trilhaEhPropria ? (
            <Aviso tipo="atencao">
              Na sua própria trilha, a validação pedagógica é dispensada: a proposta vai direto
              para a aprovação do Admin.
            </Aviso>
          ) : (
            <Aviso tipo="atencao">
              Nesta trilha, a proposta passa antes pela validação do Mestre autor dela, e
              depois pela aprovação do Admin.
            </Aviso>
          ))}
        <Campo
          rotulo="Tipo de recurso da recompensa"
          valor={tipoDeRecursoId}
          aoAlterar={definirTipoDeRecursoId}
        />
        <Campo
          rotulo="Ponto de apoio da recompensa"
          valor={pontoDeApoioId}
          aoAlterar={definirPontoDeApoioId}
        />
        <Campo
          rotulo="Quantidade disponível"
          tipo="number"
          valor={quantidadeDisponivel}
          aoAlterar={definirQuantidadeDisponivel}
        />
        <Campo
          rotulo="Critério de atribuição"
          valor={criterioDeAtribuicao}
          aoAlterar={definirCriterioDeAtribuicao}
        />
        <Campo
          rotulo="Pontos extras (até 10)"
          tipo="number"
          valor={pontosExtras}
          aoAlterar={definirPontosExtras}
          erro={pontosAcimaDoTeto ? `O teto é ${TETO_DE_PONTOS_EXTRAS} pontos.` : null}
        />

        <div className="cg-campo">
          <label htmlFor="formato-do-desafio">Formato</label>
          <select
            id="formato-do-desafio"
            value={formato}
            onChange={(evento) => definirFormato(evento.target.value as FormatoDoDesafioExtra)}
          >
            <option value="on_line">On-line</option>
            <option value="presencial">Presencial</option>
          </select>
        </div>

        <div className="cg-campo">
          <label htmlFor="custeio-do-desafio">Custeio da recompensa</label>
          <select
            id="custeio-do-desafio"
            value={custeio}
            onChange={(evento) => definirCusteio(evento.target.value as CusteioDoDesafioExtra)}
          >
            <option value="saldo_de_recurso">Saldo de recurso já existente</option>
            <option value="aporte_do_proponente">Um aporte meu já homologado</option>
          </select>
        </div>
        {custeio === "aporte_do_proponente" && (
          <Campo rotulo="Aporte que custeia" valor={aporteId} aoAlterar={definirAporteId} />
        )}

        <div className="cg-campo">
          <label htmlFor="modalidade-do-desafio">Modalidade</label>
          <select
            id="modalidade-do-desafio"
            value={modalidade}
            onChange={(evento) => definirModalidade(evento.target.value as Modalidade)}
          >
            <option value="aberto">Aberto — vale para quem estiver na trilha</option>
            <option value="direcionado">Direcionado — para um nick específico</option>
          </select>
        </div>
        {modalidade === "direcionado" && (
          <>
            <Campo
              rotulo="Nick do destinatário"
              valor={nickDoDestinatario}
              aoAlterar={definirNickDoDestinatario}
            />
            <Campo
              rotulo="Justificativa pedagógica"
              valor={justificativaPedagogica}
              aoAlterar={definirJustificativaPedagogica}
            />
          </>
        )}

        <Campo
          rotulo="Vigência — início"
          tipo="date"
          valor={vigenciaInicio}
          aoAlterar={definirVigenciaInicio}
        />
        <Campo
          rotulo="Vigência — fim"
          tipo="date"
          valor={vigenciaFim}
          aoAlterar={definirVigenciaFim}
        />

        <Botao tipo="submit" desabilitado={enviandoProposta}>
          Propor desafio
        </Botao>
      </form>
      {enviandoProposta && <Aviso tipo="andamento">Enviando…</Aviso>}
      {erroDaProposta && <Aviso tipo="erro">{erroDaProposta}</Aviso>}
      {propostaRegistrada && (
        <Aviso tipo="sucesso">Proposta registrada. Acompanhe o andamento abaixo.</Aviso>
      )}

      <h2>O que você propôs</h2>
      {erroDosMeusDesafios && <Aviso tipo="erro">{erroDosMeusDesafios}</Aviso>}
      {meusDesafios === null && !erroDosMeusDesafios && (
        <EstadoDaLista>Carregando…</EstadoDaLista>
      )}
      {meusDesafios !== null && meusDesafios.length === 0 && (
        <EstadoDaLista>Você ainda não propôs nenhum desafio extra.</EstadoDaLista>
      )}
      {meusDesafios?.map((desafio) => (
        <article key={desafio.id} className="cg-cartao-de-desafio-extra">
          <p>
            <strong>Situação:</strong> {RÓTULO_DA_SITUAÇÃO[desafio.situacao]}
          </p>
          {desafio.situacao === "recusado" && desafio.motivo_da_recusa && (
            <Aviso tipo="atencao">{desafio.motivo_da_recusa}</Aviso>
          )}
          {desafio.modalidade === "direcionado" && desafio.nick_do_destinatario && (
            <p>Direcionado ao nick: {desafio.nick_do_destinatario}</p>
          )}
          {desafio.situacao === "publicado" && (
            <p>Recompensas restantes: {desafio.quantidade_restante}.</p>
          )}
        </article>
      ))}
    </Moldura>
  );
}
