import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, CampoDeDataHora } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import {
  type CadenciaDeColeta,
  criarDesafioDeColeta,
  type DesafioDeColetaDaMissao,
  NIVEIS_DO_LOCAL,
  type NivelDoLocal,
  type TipoDeColeta,
} from "./api";

interface Props {
  idDaMissao: string;
  tiposDeColeta: TipoDeColeta[];
  onSalvo: (desafio: DesafioDeColetaDaMissao) => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

export const ROTULO_DO_NIVEL: Record<NivelDoLocal, string> = {
  comunidade: "Comunidade",
  bairro: "Bairro",
  rua: "Rua",
  condominio: "Condomínio",
  bloco: "Bloco",
  quadra: "Quadra",
};

const ROTULO_DA_CADENCIA: Record<CadenciaDeColeta, string> = {
  diaria: "Diária",
  semanal: "Semanal",
  mensal: "Mensal",
};

// O tipo vem só do catálogo — nenhuma ação de criar tipo novo, e só os
// ativos aparecem para escolha (`RF-09-27`, `RN-09-16`). Sem campo de
// etiqueta ODS: ela é herdada da missão, ou da trilha na falta dela, e o
// núcleo recusa desafio que a declare (`RN-09-36`).
export function FormularioDeDesafioDeColeta({
  idDaMissao,
  tiposDeColeta,
  onSalvo,
  onCancelar,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoTipo = useId();
  const idDaCadencia = useId();
  const idDaGranularidade = useId();
  const idDosRegistros = useId();
  const tiposAtivos = tiposDeColeta.filter((tipo) => tipo.ativo);
  const [tipoDeColetaId, definirTipoDeColetaId] = useState("");
  const [cadencia, definirCadencia] = useState<CadenciaDeColeta>("semanal");
  const [vigenciaInicio, definirVigenciaInicio] = useState("");
  const [vigenciaFim, definirVigenciaFim] = useState("");
  const [granularidadeExigida, definirGranularidadeExigida] = useState<NivelDoLocal>("rua");
  const [registrosQuePontuam, definirRegistrosQuePontuam] = useState("1");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  const tipoEscolhido = tiposAtivos.find((tipo) => tipo.id === tipoDeColetaId) ?? null;

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!tipoDeColetaId) {
      definirErroDeCampo({
        campo: "tipo_de_coleta_id",
        mensagem: "Escolha o tipo de coleta.",
      });
      return;
    }
    if (!vigenciaInicio || !vigenciaFim) {
      definirErroDeCampo({
        campo: "vigencia_inicio",
        mensagem: "Informe a vigência, com início e fim.",
      });
      return;
    }
    const registros = Number.parseInt(registrosQuePontuam, 10);
    if (!Number.isFinite(registros) || registros < 1) {
      definirErroDeCampo({
        campo: "registros_que_pontuam_por_periodo",
        mensagem: "A quantidade de registros que pontuam precisa ser ao menos 1.",
      });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      const desafio = await criarDesafioDeColeta(
        {
          missao_id: idDaMissao,
          tipo_de_coleta_id: tipoDeColetaId,
          cadencia,
          vigencia_inicio: vigenciaInicio,
          vigencia_fim: vigenciaFim,
          granularidade_exigida: granularidadeExigida,
          registros_que_pontuam_por_periodo: registros,
        },
        sessao.token,
      );
      onSalvo(desafio);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa(
        "Não foi possível declarar o desafio. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Novo desafio de coleta">
      <div className="cg-campo">
        <label htmlFor={idDoTipo}>Tipo de coleta</label>
        <select
          id={idDoTipo}
          value={tipoDeColetaId}
          onChange={(evento) => definirTipoDeColetaId(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "tipo_de_coleta_id" || undefined}
        >
          <option value="">Selecione</option>
          {tiposAtivos.map((tipo) => (
            <option key={tipo.id} value={tipo.id}>
              {tipo.nome}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "tipo_de_coleta_id" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      {tipoEscolhido && (
        <p>
          Forma de registro: {tipoEscolhido.forma_de_registro}
          {tipoEscolhido.unidade && <> · Unidade: {tipoEscolhido.unidade}</>}
        </p>
      )}

      <div className="cg-campo">
        <label htmlFor={idDaCadencia}>Cadência</label>
        <select
          id={idDaCadencia}
          value={cadencia}
          onChange={(evento) => definirCadencia(evento.target.value as CadenciaDeColeta)}
        >
          {(Object.keys(ROTULO_DA_CADENCIA) as CadenciaDeColeta[]).map((valor) => (
            <option key={valor} value={valor}>
              {ROTULO_DA_CADENCIA[valor]}
            </option>
          ))}
        </select>
      </div>

      <CampoDeDataHora
        rotulo="Início da vigência"
        valor={vigenciaInicio}
        aoAlterar={definirVigenciaInicio}
        erro={erroDeCampo?.campo === "vigencia_inicio" ? erroDeCampo.mensagem : null}
      />
      <CampoDeDataHora
        rotulo="Fim da vigência"
        valor={vigenciaFim}
        aoAlterar={definirVigenciaFim}
        erro={erroDeCampo?.campo === "vigencia_fim" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDaGranularidade}>Granularidade exigida</label>
        <select
          id={idDaGranularidade}
          value={granularidadeExigida}
          onChange={(evento) =>
            definirGranularidadeExigida(evento.target.value as NivelDoLocal)
          }
        >
          {NIVEIS_DO_LOCAL.map((valor) => (
            <option key={valor} value={valor}>
              {ROTULO_DO_NIVEL[valor]}
            </option>
          ))}
        </select>
      </div>

      <div className="cg-campo">
        <label htmlFor={idDosRegistros}>Registros do período que pontuam</label>
        <input
          id={idDosRegistros}
          type="number"
          min={1}
          value={registrosQuePontuam}
          onChange={(evento) => definirRegistrosQuePontuam(evento.target.value)}
          aria-invalid={
            erroDeCampo?.campo === "registros_que_pontuam_por_periodo" || undefined
          }
        />
        {erroDeCampo?.campo === "registros_que_pontuam_por_periodo" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Declarar desafio
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
