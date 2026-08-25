import { ErroDaApi } from "comum/api";
import { Aviso, Botao, Cabecalho, Campo, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import {
  criarEquipe,
  type Equipe,
  entrarNaEquipe,
  listarEquipesDaAula,
  sairDaEquipe,
} from "../api/equipes";

interface Props {
  aulaId: string;
  token: string;
  aoVoltar: () => void;
  /** Presente só quando a sessão abriu por confirmação presencial — é o
   * que autoriza o Mestre ou Admin a recadastrar a imagem de referência
   * (`RF-04-22`, design — decisão 4). */
  podeRecadastrarImagem?: boolean;
  aoRecadastrarImagem?: () => void;
  /** Leva ao caminho das trilhas: da equipe escolhida — sempre uma em que
   * o Guerreiro(a) já integra — à programação do encontro (`RF-04-35`). */
  aoEscolherEquipe: (equipeId: string) => void;
}

function papelOuNulo(papel: string): string | null {
  const aparado = papel.trim();
  return aparado.length === 0 ? null : aparado;
}

// Formação da equipe da aula: criar, entrar e sair, sem aprovação de
// terceiro (`RF-04-30` a `RF-04-34`, `RF-04-59`). Um Guerreiro(a) integra
// mais de uma equipe da mesma aula (`RF-04-33`) — por isso o pertencimento
// é um conjunto, não um valor único.
export function TelaDeEquipes({
  aulaId,
  token,
  aoVoltar,
  podeRecadastrarImagem = false,
  aoRecadastrarImagem,
  aoEscolherEquipe,
}: Props) {
  const [equipes, definirEquipes] = useState<Equipe[] | null>(null);
  const [papel, definirPapel] = useState("");
  const [minhasEquipesIds, definirMinhasEquipesIds] = useState<Set<string>>(new Set());
  const [erro, definirErro] = useState<string | null>(null);
  const [emAndamento, definirEmAndamento] = useState(false);

  const recarregar = useCallback(async () => {
    const pagina = await listarEquipesDaAula(aulaId, token);
    definirEquipes(pagina.itens);
  }, [aulaId, token]);

  useEffect(() => {
    recarregar();
  }, [recarregar]);

  async function executar(acao: () => Promise<void>) {
    definirErro(null);
    definirEmAndamento(true);
    try {
      await acao();
      await recarregar();
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível concluir. Tente novamente.",
      );
    } finally {
      definirEmAndamento(false);
    }
  }

  function criar() {
    executar(async () => {
      const equipe = await criarEquipe(aulaId, papelOuNulo(papel), token);
      definirMinhasEquipesIds((atual) => new Set(atual).add(equipe.id));
    });
  }

  function entrar(equipeId: string) {
    executar(async () => {
      await entrarNaEquipe(equipeId, papelOuNulo(papel), token);
      definirMinhasEquipesIds((atual) => new Set(atual).add(equipeId));
    });
  }

  function sair(equipeId: string) {
    executar(async () => {
      await sairDaEquipe(equipeId, token);
      definirMinhasEquipesIds((atual) => {
        const proximo = new Set(atual);
        proximo.delete(equipeId);
        return proximo;
      });
    });
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Equipes desta aula"
        subtitulo="Crie uma equipe ou entre numa já formada."
        acao={{ rotulo: "Voltar ao início", aoAcionar: aoVoltar }}
      />
      <Campo rotulo="Seu papel na equipe (opcional)" valor={papel} aoAlterar={definirPapel} />
      <Botao onClick={criar} desabilitado={emAndamento}>
        Criar equipe
      </Botao>
      {podeRecadastrarImagem && aoRecadastrarImagem && (
        <Botao variante="secundaria" onClick={aoRecadastrarImagem}>
          Recadastrar imagem deste Guerreiro(a)
        </Botao>
      )}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {equipes === null ? (
        <EstadoDaLista>Carregando as equipes…</EstadoDaLista>
      ) : equipes.length === 0 ? (
        <EstadoDaLista>Nenhuma equipe formada ainda nesta aula.</EstadoDaLista>
      ) : (
        <ul className="cg-lista-de-equipes">
          {equipes.map((equipe) => {
            const jaEstaNesta = minhasEquipesIds.has(equipe.id);
            return (
              <li key={equipe.id} className="cg-equipe">
                <div className="cg-equipe__integrantes">
                  {equipe.integrantes.map((integrante) => (
                    <span key={integrante.nick} className="cg-integrante">
                      <span className="cg-integrante__avatar" aria-hidden="true">
                        {(integrante.avatar ?? integrante.nick).slice(0, 1).toUpperCase()}
                      </span>
                      {integrante.nick}
                    </span>
                  ))}
                </div>
                {jaEstaNesta ? (
                  <>
                    <Botao
                      variante="secundaria"
                      onClick={() => sair(equipe.id)}
                      desabilitado={emAndamento}
                    >
                      Sair desta equipe
                    </Botao>
                    <Botao onClick={() => aoEscolherEquipe(equipe.id)}>
                      Ver a missão desta equipe
                    </Botao>
                  </>
                ) : (
                  <Botao
                    variante="secundaria"
                    onClick={() => entrar(equipe.id)}
                    desabilitado={emAndamento}
                  >
                    Entrar nesta equipe
                  </Botao>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </Moldura>
  );
}
