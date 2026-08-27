import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import {
  inscreverNaTrilha,
  listarPoderesDoCatalogo,
  type PoderPublico,
  type TrilhaPublica,
} from "../api/trilha";

interface Props {
  aoInscrever: (trilhaId: string) => void;
}

// Catálogo de poderes do ciclo e as trilhas publicadas de cada um — sem
// teto de quantas trilhas o Guerreiro(a) escolhe, e sem ação de
// desinscrever, porque a inscrição não se desfaz (`RF-05-09`, `RN-05-43`,
// `RN-05-44`).
export function EscolhaDoPoder({ aoInscrever }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [poderes, definirPoderes] = useState<PoderPublico[] | null>(null);
  const [poderEscolhido, definirPoderEscolhido] = useState<PoderPublico | null>(null);
  const [inscrevendo, definirInscrevendo] = useState<string | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    let cancelado = false;
    listarPoderesDoCatalogo()
      .then((resultado) => {
        if (!cancelado) definirPoderes(resultado);
      })
      .catch(() => {
        if (!cancelado) {
          definirErro(
            "Não foi possível carregar os poderes agora. Tente de novo em instantes.",
          );
        }
      });
    return () => {
      cancelado = true;
    };
  }, []);

  async function inscrever(trilha: TrilhaPublica) {
    if (!sessao) return;
    definirInscrevendo(trilha.id);
    definirErro(null);
    try {
      await inscreverNaTrilha(trilha.id, sessao.token);
      aoInscrever(trilha.id);
    } catch (erroCapturado) {
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
      definirErro("Não foi possível se inscrever agora. Tente de novo em instantes.");
    } finally {
      definirInscrevendo(null);
    }
  }

  if (erro) return <Aviso tipo="erro">{erro}</Aviso>;
  if (poderes === null) return <EstadoDaLista>Carregando os poderes…</EstadoDaLista>;

  if (poderEscolhido === null) {
    return (
      <section aria-label="Escolha do poder">
        <h2>Escolha um poder</h2>
        {poderes.length === 0 && (
          <EstadoDaLista>Ainda não há poder publicado neste ciclo.</EstadoDaLista>
        )}
        <ul className="cg-trilha__lista-de-poderes">
          {poderes.map((poder) => (
            <li key={poder.id}>
              <Botao onClick={() => definirPoderEscolhido(poder)}>{poder.nome}</Botao>
            </li>
          ))}
        </ul>
      </section>
    );
  }

  return (
    <section aria-label={`Trilhas de ${poderEscolhido.nome}`}>
      <Botao variante="secundaria" onClick={() => definirPoderEscolhido(null)}>
        Voltar aos poderes
      </Botao>
      <h2>Trilhas de {poderEscolhido.nome}</h2>
      <p>{poderEscolhido.descricao}</p>
      {poderEscolhido.trilhas.length === 0 && (
        <EstadoDaLista>Ainda não há trilha publicada para este poder.</EstadoDaLista>
      )}
      <ul className="cg-trilha__lista-de-trilhas">
        {poderEscolhido.trilhas.map((trilha) => (
          <li key={trilha.id}>
            <span>{trilha.nome}</span>
            <Botao onClick={() => inscrever(trilha)} desabilitado={inscrevendo === trilha.id}>
              {inscrevendo === trilha.id ? "Inscrevendo…" : "Inscrever-se"}
            </Botao>
          </li>
        ))}
      </ul>
    </section>
  );
}
