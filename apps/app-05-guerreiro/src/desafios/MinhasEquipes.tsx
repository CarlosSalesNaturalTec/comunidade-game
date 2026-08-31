import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import { listarMinhasEquipes, type MinhaEquipe } from "../api/desafiosEEquipes";

// As equipes de que o Guerreiro(a) participa, com o papel dele em cada
// uma e as atividades delas — colegas só por avatar e nick, e nenhuma
// ação de formar, editar, entrar, sair ou homologar equipe: isso acontece
// no encontro, no App 01 (`RF-05-22`, `RF-05-23`, `RF-05-24`, `RN-05-12`,
// `RN-05-15`, `RN-05-22`).
export function MinhasEquipes() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [equipes, definirEquipes] = useState<MinhaEquipe[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    const token = sessao.token;
    let cancelado = false;

    async function carregar() {
      definirErro(null);
      try {
        const resultado = await listarMinhasEquipes(token);
        if (cancelado) return;
        definirEquipes(resultado);
      } catch (erroCapturado) {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro(
          "Não foi possível carregar as suas equipes agora. Tente de novo em instantes.",
        );
      }
    }

    carregar();
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  return (
    <section className="cg-minhas-equipes" aria-label="Minhas equipes">
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {equipes !== null && !erro && (
        <Aviso tipo="andamento">
          A equipe se forma no encontro presencial, no App 01 — esta tela não forma, edita,
          entra, sai nem homologa equipe.
        </Aviso>
      )}

      {equipes === null && !erro && <EstadoDaLista>Carregando as suas equipes…</EstadoDaLista>}
      {equipes !== null && equipes.length === 0 && (
        <EstadoDaLista>Você ainda não integra nenhuma equipe.</EstadoDaLista>
      )}
      {equipes !== null && equipes.length > 0 && (
        <ul className="cg-lista-de-equipes">
          {equipes.map((equipe) => (
            <li key={equipe.id} className="cg-cartao-de-equipe">
              <h3>{equipe.aula_id !== null ? "Equipe da aula" : "Equipe da trilha"}</h3>
              {equipe.meu_papel && (
                <p>
                  <strong>Seu papel:</strong> {equipe.meu_papel}
                </p>
              )}

              <p className="cg-cartao-de-equipe__rotulo">Integrantes</p>
              <ul className="cg-lista-de-integrantes">
                {equipe.integrantes.map((integrante) => (
                  <li key={integrante.nick}>{integrante.nick}</li>
                ))}
              </ul>

              <p className="cg-cartao-de-equipe__rotulo">Atividades</p>
              {equipe.atividades.length === 0 ? (
                <EstadoDaLista>
                  Nenhuma atividade declarada para esta equipe ainda.
                </EstadoDaLista>
              ) : (
                <ul className="cg-lista-de-atividades-da-equipe">
                  {equipe.atividades.map((item) => (
                    <li key={item.atividade.id}>
                      {item.atividade.titulo}
                      {item.corrente && <Aviso tipo="andamento">Atividade corrente</Aviso>}
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
