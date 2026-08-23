import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { listarMinhasTrilhas, type TrilhaDoMestre } from "../trilhas/api";
import { listarBancoDeQuiz, type PerguntaDeQuiz } from "./api";
import { FormularioDePergunta } from "./FormularioDePergunta";
import { ListaDoBanco } from "./ListaDoBanco";

// A casa do Mestre para o Quiz ao Vivo: cadastra a pergunta com a missão a
// que ela se refere e lê o próprio banco, filtrável por trilha e por
// missão (`RF-09-36` a `RF-09-40`).
export function TelaDoBancoDeQuiz() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const [trilhas, definirTrilhas] = useState<TrilhaDoMestre[]>([]);
  const [perguntas, definirPerguntas] = useState<PerguntaDeQuiz[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);
  const [trilhaId, definirTrilhaId] = useState("");
  const [missaoId, definirMissaoId] = useState("");

  const carregarTrilhas = useCallback(async () => {
    if (!sessao) return;
    try {
      const lista = await listarMinhasTrilhas(sessao.token);
      definirTrilhas(lista);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar as suas trilhas. Tente novamente em instantes.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  const carregarPerguntas = useCallback(async () => {
    if (!sessao) return;
    try {
      const pagina = await listarBancoDeQuiz({ trilhaId, missaoId }, sessao.token);
      definirPerguntas(pagina.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro(
        "Não foi possível carregar o banco de perguntas. Tente novamente em instantes.",
      );
    }
  }, [sessao, trilhaId, missaoId, tratarRecusaDeSessao]);

  useEffect(() => {
    carregarTrilhas();
  }, [carregarTrilhas]);

  useEffect(() => {
    carregarPerguntas();
  }, [carregarPerguntas]);

  return (
    <Moldura>
      <Cabecalho titulo="Banco do Quiz" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {!mostrarFormulario && (
        <Botao onClick={() => definirMostrarFormulario(true)}>Nova pergunta</Botao>
      )}

      {mostrarFormulario && (
        <FormularioDePergunta
          trilhas={trilhas}
          onSalvo={async () => {
            definirMostrarFormulario(false);
            await carregarPerguntas();
          }}
          onCancelar={() => definirMostrarFormulario(false)}
        />
      )}

      <ListaDoBanco
        perguntas={perguntas}
        trilhas={trilhas}
        trilhaId={trilhaId}
        missaoId={missaoId}
        aoAlterarTrilha={definirTrilhaId}
        aoAlterarMissao={definirMissaoId}
      />
    </Moldura>
  );
}
