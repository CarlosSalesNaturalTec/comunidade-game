import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo, CampoDeDataHora } from "comum/react";
import { type FormEvent, useState } from "react";
import type { AtividadeDoMestre, AulaDaTurma } from "./api";
import { confirmarPresenca, lancarOcorrenciaDeConduta } from "./api";

interface Props {
  aula: AulaDaTurma;
  atividadesPresenciais: AtividadeDoMestre[];
  aoVoltar: () => void;
  aoAbrirLancamento: (atividade: AtividadeDoMestre) => void;
}

// A confirmação de presença que o App 01 não capturou e o lançamento da
// ocorrência de conduta — as duas escritas do encontro que o Mestre alcança
// nesta aula, junto com o atalho para lançar o resultado de uma atividade
// presencial dele (`RF-09-43`, `RF-09-45`, `RF-09-46`).
export function TelaDaAula({
  aula,
  atividadesPresenciais,
  aoVoltar,
  aoAbrirLancamento,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();

  const [guerreiroDaPresenca, definirGuerreiroDaPresenca] = useState("");
  const [momentoDaPresenca, definirMomentoDaPresenca] = useState("");
  const [erroDaPresenca, definirErroDaPresenca] = useState<string | null>(null);
  const [presencaConfirmada, definirPresencaConfirmada] = useState(false);
  const [enviandoPresenca, definirEnviandoPresenca] = useState(false);

  const [atividadeDaOcorrencia, definirAtividadeDaOcorrencia] = useState("");
  const [guerreiroDaOcorrencia, definirGuerreiroDaOcorrencia] = useState("");
  const [motivo, definirMotivo] = useState("");
  const [momentoDaOcorrencia, definirMomentoDaOcorrencia] = useState("");
  const [erroDaOcorrencia, definirErroDaOcorrencia] = useState<string | null>(null);
  const [ocorrenciaLancada, definirOcorrenciaLancada] = useState(false);
  const [enviandoOcorrencia, definirEnviandoOcorrencia] = useState(false);

  async function aoConfirmarPresenca(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDaPresenca(null);
    definirPresencaConfirmada(false);
    if (!sessao) return;

    definirEnviandoPresenca(true);
    try {
      await confirmarPresenca(aula.id, guerreiroDaPresenca, momentoDaPresenca, sessao.token);
      definirPresencaConfirmada(true);
      definirGuerreiroDaPresenca("");
      definirMomentoDaPresenca("");
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi) {
        definirErroDaPresenca(erroCapturado.message);
        return;
      }
      definirErroDaPresenca(
        "Não foi possível confirmar a presença. Tente novamente em instantes.",
      );
    } finally {
      definirEnviandoPresenca(false);
    }
  }

  async function aoLancarOcorrencia(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDaOcorrencia(null);
    definirOcorrenciaLancada(false);

    if (!motivo.trim()) {
      definirErroDaOcorrencia("O motivo é obrigatório.");
      return;
    }
    if (!sessao) return;

    definirEnviandoOcorrencia(true);
    try {
      await lancarOcorrenciaDeConduta(
        guerreiroDaOcorrencia,
        aula.id,
        atividadeDaOcorrencia,
        motivo,
        momentoDaOcorrencia,
        sessao.token,
      );
      definirOcorrenciaLancada(true);
      definirGuerreiroDaOcorrencia("");
      definirMotivo("");
      definirMomentoDaOcorrencia("");
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      // O teto da aula e as demais recusas chegam em linguagem simples,
      // sem código nem jargão (`RN-09-09`, `RN-09-16`).
      if (erroCapturado instanceof ErroDaApi) {
        definirErroDaOcorrencia(erroCapturado.message);
        return;
      }
      definirErroDaOcorrencia(
        "Não foi possível lançar a ocorrência. Tente novamente em instantes.",
      );
    } finally {
      definirEnviandoOcorrencia(false);
    }
  }

  return (
    <main className="cg-moldura">
      <header className="cg-cabecalho">
        <div className="cg-cabecalho__texto">
          <h1>Encontro</h1>
        </div>
        <Botao variante="secundaria" onClick={aoVoltar}>
          Voltar
        </Botao>
      </header>

      <section aria-label="Atividades presenciais desta aula">
        <h2>Lançar resultado de uma atividade</h2>
        {atividadesPresenciais.length === 0 && <p>Nenhuma atividade presencial sua.</p>}
        <ul className="lista-de-turmas" aria-label="Atividades para lançamento">
          {atividadesPresenciais.map((atividade) => (
            <li key={atividade.id} className="lista-de-turmas__item">
              <span>{atividade.titulo}</span>
              <Botao variante="secundaria" onClick={() => aoAbrirLancamento(atividade)}>
                Lançar
              </Botao>
            </li>
          ))}
        </ul>
      </section>

      <section aria-label="Confirmação de presença">
        <h2>Confirmar presença</h2>
        {erroDaPresenca && <Aviso tipo="erro">{erroDaPresenca}</Aviso>}
        {presencaConfirmada && <Aviso tipo="sucesso">Presença confirmada.</Aviso>}
        <form onSubmit={aoConfirmarPresenca} aria-label="Confirmar presença">
          <Campo
            rotulo="Identificador do Guerreiro(a)"
            valor={guerreiroDaPresenca}
            aoAlterar={definirGuerreiroDaPresenca}
          />
          <CampoDeDataHora
            rotulo="Momento em que esteve presente"
            valor={momentoDaPresenca}
            aoAlterar={definirMomentoDaPresenca}
          />
          <Botao tipo="submit" desabilitado={enviandoPresenca}>
            Confirmar presença
          </Botao>
        </form>
      </section>

      <section aria-label="Ocorrência de conduta">
        <h2>Lançar ocorrência de conduta</h2>
        <p>
          O lançamento vale no ato, sem revisão de outro Admin. Nenhum valor é pedido: o débito
          é fixo.
        </p>
        {erroDaOcorrencia && <Aviso tipo="erro">{erroDaOcorrencia}</Aviso>}
        {ocorrenciaLancada && <Aviso tipo="sucesso">Ocorrência registrada.</Aviso>}
        <form onSubmit={aoLancarOcorrencia} aria-label="Lançar ocorrência de conduta">
          <div className="cg-campo">
            <label htmlFor="atividade-da-ocorrencia">Atividade</label>
            <select
              id="atividade-da-ocorrencia"
              value={atividadeDaOcorrencia}
              onChange={(evento) => definirAtividadeDaOcorrencia(evento.target.value)}
            >
              <option value="">Selecione a atividade</option>
              {atividadesPresenciais.map((atividade) => (
                <option key={atividade.id} value={atividade.id}>
                  {atividade.titulo}
                </option>
              ))}
            </select>
          </div>
          <Campo
            rotulo="Identificador do Guerreiro(a)"
            valor={guerreiroDaOcorrencia}
            aoAlterar={definirGuerreiroDaOcorrencia}
          />
          <Campo rotulo="Motivo" valor={motivo} aoAlterar={definirMotivo} />
          <CampoDeDataHora
            rotulo="Momento do fato"
            valor={momentoDaOcorrencia}
            aoAlterar={definirMomentoDaOcorrencia}
          />
          <Botao tipo="submit" desabilitado={enviandoOcorrencia}>
            Lançar ocorrência
          </Botao>
        </form>
      </section>
    </main>
  );
}
