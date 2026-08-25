import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useId, useState } from "react";
import {
  type AtividadeDoMestre,
  type AulaDaTurma,
  abrirPartida,
  type EquipeDaAula,
  listarEquipesDaAula,
  listarMinhasTurmas,
} from "./api";
import { TelaDeConducao } from "./TelaDeConducao";

// Documento 11 §4, já normalizada no núcleo (`trilhas.regra._normalizar_natureza`).
const NATUREZA_DE_COMPETICAO_AO_VIVO = "competição ao vivo";

function nomeDaEquipe(equipe: EquipeDaAula): string {
  return equipe.integrantes.map((integrante) => integrante.nick).join(", ") || "Equipe vazia";
}

export function TelaDeQuiz() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const idDoCampoDeAula = useId();
  const idDoCampoDeAtividade = useId();
  const ehMestreOuAdmin = sessao?.papel === "mestre" || sessao?.papel === "admin";

  const [aulas, definirAulas] = useState<AulaDaTurma[] | null>(null);
  const [atividadesDeQuiz, definirAtividadesDeQuiz] = useState<AtividadeDoMestre[] | null>(
    null,
  );
  const [aulaId, definirAulaId] = useState("");
  const [atividadeId, definirAtividadeId] = useState("");
  const [equipes, definirEquipes] = useState<EquipeDaAula[] | null>(null);
  const [equipesEscolhidas, definirEquipesEscolhidas] = useState<Set<string>>(new Set());
  const [erro, definirErro] = useState<string | null>(null);
  const [abrindo, definirAbrindo] = useState(false);
  const [partidaAberta, definirPartidaAberta] = useState<{
    id: string;
    missaoId: string;
  } | null>(null);

  useEffect(() => {
    if (!sessao || !ehMestreOuAdmin) return;
    listarMinhasTurmas(sessao.token)
      .then((turmas) => {
        definirAulas(turmas.itens);
        definirAtividadesDeQuiz(
          turmas.atividades_presenciais.filter(
            (atividade) => atividade.natureza === NATUREZA_DE_COMPETICAO_AO_VIVO,
          ),
        );
      })
      .catch((erroCapturado) => {
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro("Não foi possível carregar suas turmas. Tente novamente em instantes.");
      });
  }, [sessao, ehMestreOuAdmin, tratarRecusaDeSessao]);

  useEffect(() => {
    if (!sessao || !aulaId) {
      definirEquipes(null);
      return;
    }
    listarEquipesDaAula(aulaId, sessao.token)
      .then((pagina) => {
        definirEquipes(pagina.itens);
        definirEquipesEscolhidas(new Set(pagina.itens.map((equipe) => equipe.id)));
      })
      .catch(() => definirEquipes([]));
  }, [sessao, aulaId]);

  const alternarEquipe = useCallback((idDaEquipe: string) => {
    definirEquipesEscolhidas((atual) => {
      const proximo = new Set(atual);
      if (proximo.has(idDaEquipe)) {
        proximo.delete(idDaEquipe);
      } else {
        proximo.add(idDaEquipe);
      }
      return proximo;
    });
  }, []);

  const abrir = useCallback(async () => {
    if (!sessao || !aulaId || !atividadeId) return;
    definirErro(null);
    definirAbrindo(true);
    try {
      const partida = await abrirPartida(
        aulaId,
        atividadeId,
        Array.from(equipesEscolhidas),
        sessao.token,
      );
      const atividade = atividadesDeQuiz?.find((item) => item.id === atividadeId);
      definirPartidaAberta({ id: partida.id, missaoId: atividade?.missao_id ?? "" });
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível abrir a partida. Tente novamente.",
      );
    } finally {
      definirAbrindo(false);
    }
  }, [sessao, aulaId, atividadeId, equipesEscolhidas, atividadesDeQuiz, tratarRecusaDeSessao]);

  if (!ehMestreOuAdmin) {
    return (
      <Moldura>
        <Cabecalho titulo="Quiz ao Vivo" acao={{ rotulo: "Sair", aoAcionar: sair }} />
        <Aviso tipo="atencao">
          Esta área é do Mestre e do Admin. Fale com um Mestre se precisar conduzir uma
          partida.
        </Aviso>
      </Moldura>
    );
  }

  if (partidaAberta) {
    return (
      <Moldura>
        <Cabecalho titulo="Quiz ao Vivo" acao={{ rotulo: "Sair", aoAcionar: sair }} />
        <TelaDeConducao idDaPartida={partidaAberta.id} missaoId={partidaAberta.missaoId} />
      </Moldura>
    );
  }

  return (
    <Moldura>
      <Cabecalho titulo="Quiz ao Vivo" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {aulas === null && <EstadoDaLista>Carregando suas turmas…</EstadoDaLista>}

      {aulas !== null && atividadesDeQuiz !== null && atividadesDeQuiz.length === 0 && (
        <EstadoDaLista>Nenhuma atividade de Quiz ao Vivo cadastrada ainda.</EstadoDaLista>
      )}

      {aulas !== null && atividadesDeQuiz !== null && atividadesDeQuiz.length > 0 && (
        <>
          <div className="cg-campo">
            <label htmlFor={idDoCampoDeAula}>Aula</label>
            <select
              id={idDoCampoDeAula}
              value={aulaId}
              onChange={(evento) => definirAulaId(evento.target.value)}
            >
              <option value="">Escolha a aula</option>
              {aulas.map((aula) => (
                <option key={aula.id} value={aula.id}>
                  {new Date(aula.inicio_em).toLocaleString("pt-BR")}
                </option>
              ))}
            </select>
          </div>

          <div className="cg-campo">
            <label htmlFor={idDoCampoDeAtividade}>Atividade de Quiz ao Vivo</label>
            <select
              id={idDoCampoDeAtividade}
              value={atividadeId}
              onChange={(evento) => definirAtividadeId(evento.target.value)}
            >
              <option value="">Escolha a atividade</option>
              {atividadesDeQuiz.map((atividade) => (
                <option key={atividade.id} value={atividade.id}>
                  {atividade.titulo}
                </option>
              ))}
            </select>
          </div>

          {aulaId && equipes !== null && equipes.length === 0 && (
            <Aviso tipo="atencao">
              Nenhuma equipe formada nesta aula ainda. Peça aos Guerreiros e Guerreiras para
              formarem equipe no aparelho da aula.
            </Aviso>
          )}

          {aulaId && equipes !== null && equipes.length > 0 && (
            <fieldset>
              <legend>Equipes disputantes</legend>
              {equipes.map((equipe) => (
                <label key={equipe.id}>
                  <input
                    type="checkbox"
                    checked={equipesEscolhidas.has(equipe.id)}
                    onChange={() => alternarEquipe(equipe.id)}
                  />
                  {nomeDaEquipe(equipe)}
                </label>
              ))}
            </fieldset>
          )}

          {equipes !== null && equipes.length > 0 && (
            <Botao
              onClick={abrir}
              desabilitado={abrindo || !aulaId || !atividadeId || equipesEscolhidas.size === 0}
            >
              Abrir partida
            </Botao>
          )}
        </>
      )}
    </Moldura>
  );
}
