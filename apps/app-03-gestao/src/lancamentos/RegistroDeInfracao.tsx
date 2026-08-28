import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { useId, useState } from "react";
import type { AtividadePrevista, PainelDoDia } from "../painel-do-dia/api";
import { registrarOcorrenciaDeConduta } from "./api";

interface Props {
  aulaId: string;
  presencas: PainelDoDia["presencas"];
  atividadesPrevistas: AtividadePrevista[];
}

const AVISO_DE_DESCUIDO_ACIDENTAL =
  "Descuido acidental com material comum não é infração e não gera pontuação negativa.";

// Registro no ato, sem fila de revisão e sem campo de valor: o número vem
// da tabela do documento 11 §5 (`RF-02-37`, `RN-02-13`, `RN-02-14`).
export function RegistroDeInfracao({ aulaId, presencas, atividadesPrevistas }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoGuerreiro = useId();
  const idDaAtividade = useId();
  const [guerreiroId, definirGuerreiroId] = useState("");
  const [atividadeId, definirAtividadeId] = useState(atividadesPrevistas[0]?.id ?? "");
  const [motivo, definirMotivo] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<{
    campo: string;
    mensagem: string;
  } | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [gravada, definirGravada] = useState(false);

  async function aoSubmeter() {
    definirErroDeCampo(null);
    definirErroDeRecusa(null);
    definirGravada(false);

    if (!guerreiroId) {
      definirErroDeCampo({ campo: "guerreiro", mensagem: "Escolha o Guerreiro(a)." });
      return;
    }
    if (!atividadeId) {
      definirErroDeCampo({ campo: "atividade", mensagem: "Escolha a atividade." });
      return;
    }
    if (!motivo.trim()) {
      definirErroDeCampo({ campo: "motivo", mensagem: "Informe o motivo." });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      await registrarOcorrenciaDeConduta(
        {
          guerreiro_id: guerreiroId,
          aula_id: aulaId,
          atividade_id: atividadeId,
          motivo,
          momento_do_fato: new Date().toISOString(),
        },
        sessao.token,
      );
      definirGravada(true);
      definirMotivo("");
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDeRecusa(
        erro instanceof ErroDaApi
          ? erro.message
          : "Não foi possível registrar a infração. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <section aria-label="Registrar infração">
      <Aviso tipo="atencao">{AVISO_DE_DESCUIDO_ACIDENTAL}</Aviso>

      <div className="cg-campo">
        <label htmlFor={idDoGuerreiro}>Guerreiro(a)</label>
        <select
          id={idDoGuerreiro}
          value={guerreiroId}
          onChange={(evento) => definirGuerreiroId(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "guerreiro" || undefined}
        >
          <option value="">Selecione</option>
          {presencas.map((presenca) => (
            <option key={presenca.guerreiro_id} value={presenca.guerreiro_id}>
              {presenca.nick}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "guerreiro" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <div className="cg-campo">
        <label htmlFor={idDaAtividade}>Atividade</label>
        <select
          id={idDaAtividade}
          value={atividadeId}
          onChange={(evento) => definirAtividadeId(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "atividade" || undefined}
        >
          <option value="">Selecione</option>
          {atividadesPrevistas.map((atividade) => (
            <option key={atividade.id} value={atividade.id}>
              {atividade.missao_titulo} — {atividade.titulo}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "atividade" && (
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
      {gravada && <Aviso tipo="sucesso">Infração registrada — valeu no ato.</Aviso>}

      <Botao onClick={aoSubmeter} desabilitado={enviando}>
        Registrar infração
      </Botao>
    </section>
  );
}
