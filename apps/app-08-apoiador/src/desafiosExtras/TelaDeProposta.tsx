import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type FormEvent, useState } from "react";
import {
  type CusteioDoDesafioExtra,
  type FormatoDoDesafioExtra,
  type Modalidade,
  proporDesafioExtra,
} from "./api";

const TETO_DE_PONTOS_EXTRAS = 10;

// A proposta do Apoiador: trilha em andamento, recompensa (tipo de recurso e
// quantidade), critério de atribuição, vigência, modalidade, pontos extras,
// formato e custeio — no direcionado, nick e justificativa, sem confirmar
// existência (`RF-14-29` a `RF-14-33`, `RF-14-74` a `RF-14-76`).
export function TelaDeProposta() {
  const { sessao } = useSessao();
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
  const [justificativaDoVinculo, definirJustificativaDoVinculo] = useState("");
  const [vigenciaInicio, definirVigenciaInicio] = useState("");
  const [vigenciaFim, definirVigenciaFim] = useState("");
  const [enviando, definirEnviando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [sucesso, definirSucesso] = useState(false);

  const pontosAcimaDoTeto = Number(pontosExtras) > TETO_DE_PONTOS_EXTRAS;

  async function aoEnviar(evento: FormEvent) {
    evento.preventDefault();
    if (!sessao) return;
    if (pontosAcimaDoTeto) {
      definirErro(`Pontos extras acima do teto de ${TETO_DE_PONTOS_EXTRAS}.`);
      return;
    }
    definirEnviando(true);
    definirErro(null);
    definirSucesso(false);
    try {
      await proporDesafioExtra(
        {
          trilha_id: trilhaId,
          modalidade,
          nick_do_destinatario: modalidade === "direcionado" ? nickDoDestinatario : null,
          justificativa_do_vinculo:
            modalidade === "direcionado" ? justificativaDoVinculo : null,
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
      definirSucesso(true);
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível registrar a proposta. Tente novamente.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Propor desafio extra"
        subtitulo="Sobre uma trilha em andamento, com a recompensa que você provê."
      />
      <form onSubmit={aoEnviar}>
        <Campo rotulo="Trilha" valor={trilhaId} aoAlterar={definirTrilhaId} />
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
              rotulo="Justificativa do vínculo"
              valor={justificativaDoVinculo}
              aoAlterar={definirJustificativaDoVinculo}
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

        <Botao tipo="submit" desabilitado={enviando}>
          Propor desafio
        </Botao>
      </form>
      {enviando && <Aviso tipo="andamento">Enviando…</Aviso>}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {sucesso && (
        <Aviso tipo="sucesso">
          Proposta registrada. Acompanhe o andamento em "Meus desafios".
        </Aviso>
      )}
    </Moldura>
  );
}
