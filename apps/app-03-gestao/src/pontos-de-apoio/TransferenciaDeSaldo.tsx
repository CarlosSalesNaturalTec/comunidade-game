import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useEffect, useId, useState } from "react";
import { ErroDaApi, ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import {
  listarSaldosDoPontoDeApoio,
  type PontoDeApoioDaLista,
  type SaldoDoTipoDeRecurso,
  transferirSaldo,
} from "./api";

interface Props {
  origem: PontoDeApoioDaLista;
  pontosDeApoio: PontoDeApoioDaLista[];
  onConcluida: () => void;
  onCancelar: () => void;
}

// O saldo disponível na origem é mostrado antes de confirmar, o destino
// nunca oferece o inativo nem a própria origem, e a quantidade acima do
// saldo é barrada antes de chegar ao núcleo (`RF-07-19`, `RN-07-33`).
export function TransferenciaDeSaldo({
  origem,
  pontosDeApoio,
  onConcluida,
  onCancelar,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoTipo = useId();
  const idDoDestino = useId();
  const [saldos, definirSaldos] = useState<SaldoDoTipoDeRecurso[] | null>(null);
  const [tipoId, definirTipoId] = useState("");
  const [quantidade, definirQuantidade] = useState("");
  const [destinoId, definirDestinoId] = useState("");
  const [motivo, definirMotivo] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<{
    campo: string;
    mensagem: string;
  } | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  useEffect(() => {
    if (!sessao) return;
    listarSaldosDoPontoDeApoio(origem.id, sessao.token)
      .then((lista) => {
        definirSaldos(lista);
        definirTipoId((atual) => atual || (lista[0]?.tipo_de_recurso_id ?? ""));
      })
      .catch((erro) => {
        if (ehRecusaDeSessao(erro)) {
          tratarRecusaDeSessao();
          return;
        }
        definirSaldos([]);
      });
  }, [origem.id, sessao, tratarRecusaDeSessao]);

  const destinosDisponiveis = pontosDeApoio.filter(
    (pontoDeApoio) => pontoDeApoio.id !== origem.id && pontoDeApoio.ativo,
  );
  const saldoSelecionado = saldos?.find((item) => item.tipo_de_recurso_id === tipoId) ?? null;

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!tipoId) {
      definirErroDeCampo({ campo: "tipo", mensagem: "Escolha o tipo de recurso." });
      return;
    }
    const quantidadeNumerica = Number(quantidade);
    if (!quantidade || Number.isNaN(quantidadeNumerica) || quantidadeNumerica <= 0) {
      definirErroDeCampo({
        campo: "quantidade",
        mensagem: "Informe uma quantidade maior que zero.",
      });
      return;
    }
    if (saldoSelecionado && quantidadeNumerica > Number(saldoSelecionado.saldo)) {
      definirErroDeCampo({
        campo: "quantidade",
        mensagem: `O saldo disponível na origem é ${saldoSelecionado.saldo}.`,
      });
      return;
    }
    if (!destinoId) {
      definirErroDeCampo({
        campo: "destino",
        mensagem: "Escolha o ponto de apoio de destino.",
      });
      return;
    }
    if (!motivo.trim()) {
      definirErroDeCampo({ campo: "motivo", mensagem: "Informe o motivo da transferência." });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      await transferirSaldo(
        {
          tipo_de_recurso_id: tipoId,
          ponto_de_apoio_origem_id: origem.id,
          ponto_de_apoio_destino_id: destinoId,
          quantidade,
          motivo,
        },
        sessao.token,
      );
      onConcluida();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDeRecusa(
        erro instanceof ErroDaApi
          ? erro.message
          : "Não foi possível transferir o saldo. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label={`Transferir saldo de ${origem.nome}`}>
      <div className="cg-campo">
        <label htmlFor={idDoTipo}>Tipo de recurso</label>
        <select
          id={idDoTipo}
          value={tipoId}
          onChange={(evento) => definirTipoId(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "tipo" || undefined}
        >
          <option value="">Selecione</option>
          {(saldos ?? []).map((item) => (
            <option key={item.tipo_de_recurso_id} value={item.tipo_de_recurso_id}>
              {item.nome} (saldo: {item.saldo})
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "tipo" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
        {saldos !== null && saldos.length === 0 && (
          <p role="status">Este ponto de apoio não tem saldo disponível para transferir.</p>
        )}
      </div>

      <Campo
        rotulo="Quantidade"
        tipo="number"
        valor={quantidade}
        aoAlterar={definirQuantidade}
        erro={erroDeCampo?.campo === "quantidade" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDoDestino}>Ponto de apoio de destino</label>
        <select
          id={idDoDestino}
          value={destinoId}
          onChange={(evento) => definirDestinoId(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "destino" || undefined}
        >
          <option value="">Selecione</option>
          {destinosDisponiveis.map((pontoDeApoio) => (
            <option key={pontoDeApoio.id} value={pontoDeApoio.id}>
              {pontoDeApoio.nome}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "destino" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <Campo
        rotulo="Motivo"
        valor={motivo}
        aoAlterar={definirMotivo}
        erro={erroDeCampo?.campo === "motivo" ? erroDeCampo.mensagem : null}
      />

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Transferir
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
