import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { listarMinhasTrilhas, type TrilhaComProximaMissao } from "../api/trilha";
import { EscolhaDoPoder } from "./EscolhaDoPoder";
import { GuiaDaTrilha } from "./GuiaDaTrilha";
import { Progresso } from "./Progresso";

type Tela = "guia" | "trocar-de-trilha" | "progresso" | "escolher-poder";

// O bloco da trilha na Área do Guerreiro(a): sem nenhuma inscrição, leva à
// escolha do poder; com uma ou mais, abre no guia da trilha e permite
// alternar entre elas ou conferir o progresso (`RF-05-08`, `RF-05-09`,
// `RF-05-17`).
export function Trilha() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [trilhas, definirTrilhas] = useState<TrilhaComProximaMissao[] | null>(null);
  const [trilhaSelecionadaId, definirTrilhaSelecionadaId] = useState<string | null>(null);
  const [tela, definirTela] = useState<Tela>("guia");
  const [erro, definirErro] = useState<string | null>(null);

  const carregarTrilhas = useCallback(
    (manterSelecao = true) => {
      if (!sessao) return;
      definirErro(null);
      listarMinhasTrilhas(sessao.token)
        .then((resultado) => {
          definirTrilhas(resultado);
          definirTrilhaSelecionadaId((atual) =>
            manterSelecao && resultado.some((item) => item.id === atual)
              ? atual
              : (resultado[0]?.id ?? null),
          );
        })
        .catch((erroCapturado) => {
          if (
            erroCapturado &&
            typeof erroCapturado === "object" &&
            "codigo" in erroCapturado &&
            (erroCapturado.codigo === "sessao_ausente" ||
              erroCapturado.codigo === "sessao_invalida")
          ) {
            tratarRecusaDeSessao();
            return;
          }
          definirErro(
            "Não foi possível carregar as suas trilhas agora. Tente de novo em instantes.",
          );
        });
    },
    [sessao, tratarRecusaDeSessao],
  );

  useEffect(() => {
    carregarTrilhas(false);
  }, [carregarTrilhas]);

  function aoInscrever(trilhaId: string) {
    if (!sessao) return;
    listarMinhasTrilhas(sessao.token).then((resultado) => {
      definirTrilhas(resultado);
      definirTrilhaSelecionadaId(trilhaId);
      definirTela("guia");
    });
  }

  if (erro) return <Aviso tipo="erro">{erro}</Aviso>;
  if (trilhas === null) return <EstadoDaLista>Carregando as suas trilhas…</EstadoDaLista>;

  if (trilhas.length === 0 || tela === "escolher-poder") {
    return <EscolhaDoPoder aoInscrever={aoInscrever} />;
  }

  const trilhaSelecionada =
    trilhas.find((item) => item.id === trilhaSelecionadaId) ?? trilhas[0];

  return (
    <div className="cg-trilha">
      <nav className="cg-trilha__abas" aria-label="Trilha">
        <Botao
          variante={tela === "guia" ? "primaria" : "secundaria"}
          onClick={() => definirTela("guia")}
        >
          Guia
        </Botao>
        <Botao
          variante={tela === "progresso" ? "primaria" : "secundaria"}
          onClick={() => definirTela("progresso")}
        >
          Progresso
        </Botao>
      </nav>

      {tela === "guia" && (
        <GuiaDaTrilha
          trilha={trilhaSelecionada}
          aoAtualizarTrilhas={() => carregarTrilhas(true)}
          aoTrocarDeTrilha={() => definirTela("trocar-de-trilha")}
        />
      )}

      {tela === "trocar-de-trilha" && (
        <section aria-label="Trocar de trilha">
          <h2>Suas trilhas</h2>
          <ul className="cg-trilha__lista-de-trilhas">
            {trilhas.map((trilha) => (
              <li key={trilha.id}>
                <Botao
                  onClick={() => {
                    definirTrilhaSelecionadaId(trilha.id);
                    definirTela("guia");
                  }}
                >
                  {trilha.nome}
                </Botao>
              </li>
            ))}
          </ul>
          <Botao variante="secundaria" onClick={() => definirTela("escolher-poder")}>
            Escolher outro poder
          </Botao>
        </section>
      )}

      {tela === "progresso" && <Progresso />}
    </div>
  );
}
