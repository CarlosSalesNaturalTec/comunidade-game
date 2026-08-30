import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import { declararRecompensaDeMarco, type RecompensaDeMarco } from "../recompensas/api";
import type { TipoDeRecurso } from "../recursos/api";
import type { MissaoDaTrilha } from "./api";

interface Props {
  idDaTrilha: string;
  missao: MissaoDaTrilha;
  tiposDeRecurso: TipoDeRecurso[];
  recompensas: RecompensaDeMarco[];
  onDeclarada: (recompensa: RecompensaDeMarco) => void;
}

// O marco alcançado é sempre o desbloqueio desta missão — a tela nunca
// oferece preço, saldo de pontos nem aviso de lastro, que só é conferido na
// entrega (`RF-09-84`, `RF-09-71`, `RF-09-72`, `RN-09-26`, `RN-09-27`,
// `RN-09-39`).
export function DeclaracaoDeRecompensa({
  idDaTrilha,
  missao,
  tiposDeRecurso,
  recompensas,
  onDeclarada,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoTipo = useId();
  const idDaQuantidade = useId();
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);
  const [tipoDeRecursoId, definirTipoDeRecursoId] = useState("");
  const [quantidade, definirQuantidade] = useState("");
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  const tipoPorId = new Map(tiposDeRecurso.map((tipo) => [tipo.id, tipo]));

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErro(null);

    if (!tipoDeRecursoId) {
      definirErro("Escolha o tipo de recurso da recompensa.");
      return;
    }
    if (!quantidade || Number(quantidade) <= 0) {
      definirErro("Informe uma quantidade maior que zero.");
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      const recompensa = await declararRecompensaDeMarco(
        idDaTrilha,
        { missao_id: missao.id, tipo_de_recurso_id: tipoDeRecursoId, quantidade },
        sessao.token,
      );
      definirMostrarFormulario(false);
      definirTipoDeRecursoId("");
      definirQuantidade("");
      onDeclarada(recompensa);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi) {
        definirErro(erroCapturado.message);
        return;
      }
      definirErro("Não foi possível declarar a recompensa. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <section aria-label={`Recompensa de marco de ${missao.titulo}`}>
      <h4>Recompensa pelo desbloqueio</h4>

      {recompensas.length > 0 ? (
        <ul>
          {recompensas.map((recompensa) => (
            <li key={recompensa.id}>
              {recompensa.quantidade}{" "}
              {tipoPorId.get(recompensa.tipo_de_recurso_id)?.nome ?? "recurso"}
            </li>
          ))}
        </ul>
      ) : (
        <p>Nenhuma recompensa declarada para este marco.</p>
      )}

      {mostrarFormulario ? (
        <form onSubmit={aoSubmeter}>
          <div className="cg-campo">
            <label htmlFor={idDoTipo}>Tipo de recurso</label>
            <select
              id={idDoTipo}
              value={tipoDeRecursoId}
              onChange={(evento) => definirTipoDeRecursoId(evento.target.value)}
            >
              <option value="">Selecione</option>
              {tiposDeRecurso.map((tipo) => (
                <option key={tipo.id} value={tipo.id}>
                  {tipo.nome}
                </option>
              ))}
            </select>
          </div>

          <div className="cg-campo">
            <label htmlFor={idDaQuantidade}>Quantidade</label>
            <input
              id={idDaQuantidade}
              type="number"
              min="0"
              step="any"
              value={quantidade}
              onChange={(evento) => definirQuantidade(evento.target.value)}
            />
          </div>

          {erro && <Aviso tipo="erro">{erro}</Aviso>}

          <Botao tipo="submit" desabilitado={enviando}>
            Declarar recompensa
          </Botao>
          <Botao variante="secundaria" onClick={() => definirMostrarFormulario(false)}>
            Cancelar
          </Botao>
        </form>
      ) : (
        <Botao variante="secundaria" onClick={() => definirMostrarFormulario(true)}>
          Declarar recompensa
        </Botao>
      )}
    </section>
  );
}
