import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useEffect, useRef, useState } from "react";
import { DURACAO_DE_INATIVIDADE_EM_MINUTOS } from "../api/configuracao";
import { Carteira } from "../carteira/Carteira";
import { Coleta } from "../coleta/Coleta";

const UM_MINUTO_EM_MS = 60_000;
const EVENTOS_DE_ATIVIDADE = ["pointerdown", "keydown", "touchstart"] as const;

type Bloco = "coleta" | "carteira";

// Conteúdo da sessão aberta: o encerramento por saída e por inatividade, o
// bloco da coleta do território e o bloco da carteira, catálogo,
// conquistas e ranking — trilha, portfólio e acervo são fatias futuras do
// PRD-05 (proposal — Why).
export function AreaDoGuerreiro() {
  const { sair } = useSessao();
  const [avisando, definirAvisando] = useState(false);
  const [bloco, definirBloco] = useState<Bloco>("coleta");
  const referenciaDeReiniciar = useRef<() => void>(() => {});

  useEffect(() => {
    const duracaoEmMs = DURACAO_DE_INATIVIDADE_EM_MINUTOS * 60_000;
    let timeoutDeAviso: ReturnType<typeof setTimeout>;
    let timeoutDeEncerramento: ReturnType<typeof setTimeout>;

    function reiniciar() {
      clearTimeout(timeoutDeAviso);
      clearTimeout(timeoutDeEncerramento);
      definirAvisando(false);
      timeoutDeAviso = setTimeout(
        () => definirAvisando(true),
        Math.max(duracaoEmMs - UM_MINUTO_EM_MS, 0),
      );
      timeoutDeEncerramento = setTimeout(() => {
        sair();
      }, duracaoEmMs);
    }
    referenciaDeReiniciar.current = reiniciar;

    function aoDetectarAtividade() {
      reiniciar();
    }

    reiniciar();
    for (const evento of EVENTOS_DE_ATIVIDADE) {
      window.addEventListener(evento, aoDetectarAtividade);
    }
    return () => {
      clearTimeout(timeoutDeAviso);
      clearTimeout(timeoutDeEncerramento);
      for (const evento of EVENTOS_DE_ATIVIDADE) {
        window.removeEventListener(evento, aoDetectarAtividade);
      }
    };
  }, [sair]);

  return (
    <Moldura>
      <Cabecalho titulo="Minha Área" acao={{ rotulo: "Sair", aoAcionar: sair }} />
      {avisando && (
        <>
          <Aviso tipo="atencao">Você ainda está aí? Sua sessão vai fechar em 1 minuto.</Aviso>
          <Botao onClick={() => referenciaDeReiniciar.current()}>Continuar</Botao>
        </>
      )}

      <nav className="cg-area-do-guerreiro__blocos" aria-label="Área do Guerreiro(a)">
        <Botao
          variante={bloco === "coleta" ? "primaria" : "secundaria"}
          onClick={() => definirBloco("coleta")}
        >
          Coleta do território
        </Botao>
        <Botao
          variante={bloco === "carteira" ? "primaria" : "secundaria"}
          onClick={() => definirBloco("carteira")}
        >
          Minha carteira
        </Botao>
      </nav>

      {bloco === "coleta" ? <Coleta /> : <Carteira />}
    </Moldura>
  );
}
