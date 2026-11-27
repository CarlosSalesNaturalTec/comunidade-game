import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Avatar } from "comum/avatar";
import { Aviso, Botao, Campo, CampoDeDataHora, EstadoDaLista } from "comum/react";
import { type FormEvent, useCallback, useEffect, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import { listarGuerreirosVinculaveis } from "../responsaveis/api";
import type { AtividadeDoMestre, AulaDaTurma, PresencaDaAula } from "./api";
import { confirmarPresenca, lancarOcorrenciaDeConduta, listarPresencasDaAula } from "./api";

const ROTULO_DO_MODO: Record<string, string> = {
  reconhecimento: "Reconhecimento",
  confirmacao: "Confirmação",
};

// O nick nem sempre diz quem é a criança: o nome vai ao lado dele, e a marca
// diz ao Mestre quando o cadastro não o tem (`RF-09-145`).
const SEM_NOME = "sem nome";

const FORMATADOR_DA_HORA = new Intl.DateTimeFormat("pt-BR", { timeStyle: "short" });

// O nick é único sem distinção de maiúsculas no núcleo, então a forma
// normalizada identifica um só Guerreiro(a).
function normalizarNick(nick: string): string {
  return nick.trim().toLocaleLowerCase("pt-BR");
}

type ResolucaoDoNick = { id: string } | { erro: string };

interface Props {
  aula: AulaDaTurma;
  atividadesPresenciais: AtividadeDoMestre[];
  aoVoltar: () => void;
  aoAbrirLancamento: (atividade: AtividadeDoMestre) => void;
}

// A confirmação de presença que o App 01 não capturou e o lançamento da
// ocorrência de conduta — as duas escritas do encontro que o Mestre alcança
// nesta aula, junto com o atalho para lançar o resultado de uma atividade
// presencial dele (`RF-09-43`, `RF-09-45`, `RF-09-46`). Abre com os presentes
// da aula, por nick e avatar (`RF-09-145`, `RN-09-18`).
export function TelaDaAula({
  aula,
  atividadesPresenciais,
  aoVoltar,
  aoAbrirLancamento,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();

  const [presentes, definirPresentes] = useState<PresencaDaAula[] | null>(null);
  const [erroDosPresentes, definirErroDosPresentes] = useState<string | null>(null);

  const carregarPresentes = useCallback(async () => {
    if (!sessao) return;
    try {
      definirPresentes(await listarPresencasDaAula(aula.id, sessao.token));
      definirErroDosPresentes(null);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      // A falha fica só nesta seção: os formulários seguem disponíveis.
      definirErroDosPresentes(
        "Não foi possível carregar os presentes desta aula. Tente novamente em instantes.",
      );
    }
  }, [aula.id, sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregarPresentes();
  }, [carregarPresentes]);

  // Nick normalizado → id, dos Guerreiros e Guerreiras ativos das comunidades
  // do Mestre: ele digita o nick, e só o id encontrado vai ao núcleo
  // (`RF-09-45`, `RF-09-46`, `RN-09-18`). `null` enquanto carrega ou se falhou.
  const [idsPorNick, definirIdsPorNick] = useState<Map<string, string> | null>(null);

  useEffect(() => {
    if (!sessao) return;
    let cancelado = false;
    (async () => {
      const mapa = new Map<string, string>();
      try {
        let cursor: string | null = null;
        do {
          const pagina = await listarGuerreirosVinculaveis(sessao.token, cursor);
          for (const guerreiro of pagina.itens) {
            mapa.set(normalizarNick(guerreiro.nick), guerreiro.id);
          }
          cursor = pagina.proximo_cursor;
        } while (cursor);
        if (!cancelado) definirIdsPorNick(mapa);
      } catch (erroCapturado) {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirIdsPorNick(null);
      }
    })();
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  function resolverNick(nick: string): ResolucaoDoNick {
    const normalizado = normalizarNick(nick);
    if (!normalizado) return { erro: "Informe o nick do Guerreiro(a)." };
    if (idsPorNick === null) {
      return {
        erro: "Não foi possível conferir o nick agora. Tente novamente em instantes.",
      };
    }
    const id = idsPorNick.get(normalizado);
    if (!id) {
      return {
        erro: `Não encontramos o nick "${nick.trim()}" nas suas comunidades. Confira a grafia.`,
      };
    }
    return { id };
  }

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

    const resolucao = resolverNick(guerreiroDaPresenca);
    if ("erro" in resolucao) {
      definirErroDaPresenca(resolucao.erro);
      return;
    }
    if (!sessao) return;

    definirEnviandoPresenca(true);
    try {
      await confirmarPresenca(aula.id, resolucao.id, momentoDaPresenca, sessao.token);
      definirPresencaConfirmada(true);
      definirGuerreiroDaPresenca("");
      definirMomentoDaPresenca("");
      carregarPresentes();
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

    const resolucao = resolverNick(guerreiroDaOcorrencia);
    if ("erro" in resolucao) {
      definirErroDaOcorrencia(resolucao.erro);
      return;
    }
    if (!motivo.trim()) {
      definirErroDaOcorrencia("O motivo é obrigatório.");
      return;
    }
    if (!sessao) return;

    definirEnviandoOcorrencia(true);
    try {
      await lancarOcorrenciaDeConduta(
        resolucao.id,
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

      <section aria-label="Presentes nesta aula">
        <h2>Presentes nesta aula</h2>
        {erroDosPresentes && <Aviso tipo="erro">{erroDosPresentes}</Aviso>}
        {presentes === null && !erroDosPresentes && (
          <EstadoDaLista>Carregando os presentes…</EstadoDaLista>
        )}
        {presentes !== null && presentes.length === 0 && (
          <EstadoDaLista>Nenhuma presença registrada nesta aula.</EstadoDaLista>
        )}
        {presentes !== null && presentes.length > 0 && (
          <ul className="lista-de-turmas" aria-label="Presentes">
            {presentes.map((presenca) => (
              <li key={presenca.id} className="lista-de-turmas__item">
                <div className="lista-de-turmas__linha">
                  <span>
                    <Avatar avatar={presenca.avatar} tamanho={32} />{" "}
                    {presenca.nick ?? presenca.guerreiro_id} —{" "}
                    {presenca.nome?.trim() || SEM_NOME}
                  </span>
                  <span>
                    {FORMATADOR_DA_HORA.format(new Date(presenca.momento_do_fato))} ·{" "}
                    {ROTULO_DO_MODO[presenca.modo] ?? presenca.modo}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>

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
        <AvisoDeColeta dado="a presença do Guerreiro(a) na atividade" />
        {erroDaPresenca && <Aviso tipo="erro">{erroDaPresenca}</Aviso>}
        {presencaConfirmada && <Aviso tipo="sucesso">Presença confirmada.</Aviso>}
        <form onSubmit={aoConfirmarPresenca} aria-label="Confirmar presença">
          <Campo
            rotulo="Nick do Guerreiro(a)"
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
        <AvisoDeColeta dado="a ocorrência de conduta e o motivo da pontuação negativa" />
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
            rotulo="Nick do Guerreiro(a)"
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
