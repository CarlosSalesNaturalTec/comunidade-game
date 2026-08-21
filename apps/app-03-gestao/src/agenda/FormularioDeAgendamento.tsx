import { Aviso, Botao, CampoDeDataHora } from "comum/react";
import { type FormEvent, useEffect, useId, useState } from "react";
import { ErroDaApi, ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import type { ComunidadeDaLista } from "../comunidades/api";
import { listarPontosDeApoio, type PontoDeApoioDaLista } from "../pontos-de-apoio/api";
import { agendarAula } from "./api";

interface Props {
  comunidades: ComunidadeDaLista[];
  onAgendada: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const RECUSA_POR_PAPEL = "Só o Admin agenda aula.";

export function FormularioDeAgendamento({ comunidades, onAgendada, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoCampoDeComunidade = useId();
  const idDoCampoDePontoDeApoio = useId();
  const [comunidadeId, definirComunidadeId] = useState(comunidades[0]?.id ?? "");
  const [pontosDeApoio, definirPontosDeApoio] = useState<PontoDeApoioDaLista[]>([]);
  const [pontoDeApoioId, definirPontoDeApoioId] = useState("");
  const [inicioEm, definirInicioEm] = useState("");
  const [fimEm, definirFimEm] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  // O seletor de ponto de apoio refaz a consulta filtrada pela comunidade
  // escolhida, sempre que ela muda (design — decisão 5).
  useEffect(() => {
    if (!sessao || !comunidadeId) {
      definirPontosDeApoio([]);
      return;
    }
    let cancelado = false;
    listarPontosDeApoio(sessao.token, comunidadeId)
      .then((pagina) => {
        if (!cancelado) definirPontosDeApoio(pagina.itens);
      })
      .catch(() => {
        if (!cancelado) definirPontosDeApoio([]);
      });
    return () => {
      cancelado = true;
    };
  }, [sessao, comunidadeId]);

  useEffect(() => {
    definirPontoDeApoioId((atual) =>
      pontosDeApoio.some((ponto) => ponto.id === atual) ? atual : (pontosDeApoio[0]?.id ?? ""),
    );
  }, [pontosDeApoio]);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!comunidadeId) {
      definirErroDeCampo({
        campo: "comunidade_virtual_id",
        mensagem: "Escolha a comunidade.",
      });
      return;
    }
    if (!pontoDeApoioId) {
      definirErroDeCampo({
        campo: "ponto_de_apoio_id",
        mensagem: "Escolha o ponto de apoio.",
      });
      return;
    }
    if (!inicioEm) {
      definirErroDeCampo({ campo: "inicio_em", mensagem: "Informe o horário inicial." });
      return;
    }
    if (!fimEm) {
      definirErroDeCampo({ campo: "fim_em", mensagem: "Informe o horário final." });
      return;
    }
    // O horário final não posterior ao inicial é apontado no próprio campo,
    // sem chamar o núcleo (`RF-02-12`).
    if (new Date(fimEm).getTime() <= new Date(inicioEm).getTime()) {
      definirErroDeCampo({
        campo: "fim_em",
        mensagem: "O horário final precisa ser posterior ao inicial.",
      });
      return;
    }

    if (!sessao) return;

    definirEnviando(true);
    try {
      await agendarAula(
        {
          comunidade_virtual_id: comunidadeId,
          ponto_de_apoio_id: pontoDeApoioId,
          inicio_em: inicioEm,
          fim_em: fimEm,
        },
        sessao.token,
      );
      onAgendada();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "permissao_negada") {
        definirErroDeRecusa(RECUSA_POR_PAPEL);
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa("Não foi possível agendar a aula. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Nova Aula">
      <div className="cg-campo">
        <label htmlFor={idDoCampoDeComunidade}>Comunidade</label>
        <select
          id={idDoCampoDeComunidade}
          value={comunidadeId}
          onChange={(evento) => definirComunidadeId(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "comunidade_virtual_id" || undefined}
        >
          <option value="">Selecione</option>
          {comunidades.map((comunidade) => (
            <option key={comunidade.id} value={comunidade.id}>
              {comunidade.nome}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "comunidade_virtual_id" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <CampoDeDataHora
        rotulo="Horário inicial"
        valor={inicioEm}
        aoAlterar={definirInicioEm}
        erro={erroDeCampo?.campo === "inicio_em" ? erroDeCampo.mensagem : null}
      />

      <CampoDeDataHora
        rotulo="Horário final"
        valor={fimEm}
        aoAlterar={definirFimEm}
        erro={erroDeCampo?.campo === "fim_em" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDoCampoDePontoDeApoio}>Ponto de apoio</label>
        <select
          id={idDoCampoDePontoDeApoio}
          value={pontoDeApoioId}
          onChange={(evento) => definirPontoDeApoioId(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "ponto_de_apoio_id" || undefined}
        >
          <option value="">Selecione</option>
          {pontosDeApoio.map((pontoDeApoio) => (
            <option key={pontoDeApoio.id} value={pontoDeApoio.id}>
              {pontoDeApoio.nome}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "ponto_de_apoio_id" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Agendar
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
