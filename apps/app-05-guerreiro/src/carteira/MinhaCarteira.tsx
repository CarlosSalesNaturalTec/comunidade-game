import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import { listarMeusPontosExtras, type PontosExtras } from "../api/carteira";

// A carteira: acumulado e saldo disponível separados e rotulados, sem soma
// e sem ponto regular, mais o estado do próprio perfil público — leitura
// apenas, já que autorizar é ato do responsável na App 07 (`RF-05-82`,
// `RF-05-50`, `RN-05-39`, `RN-05-40`, `RN-05-42`).
export function MinhaCarteira() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [pontos, definirPontos] = useState<PontosExtras | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    const token = sessao.token;
    let cancelado = false;

    async function carregar() {
      definirErro(null);
      try {
        const resultado = await listarMeusPontosExtras(token);
        if (cancelado) return;
        definirPontos(resultado);
      } catch (erroCapturado) {
        if (cancelado) return;
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
          "Não foi possível carregar a sua carteira agora. Tente de novo em instantes.",
        );
      }
    }

    carregar();
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  return (
    <section className="cg-carteira-secao" aria-label="Minha carteira">
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {pontos === null && !erro && <EstadoDaLista>Carregando a sua carteira…</EstadoDaLista>}

      {pontos !== null && (
        <div className="cg-carteira__contas">
          <p className="cg-carteira__conta">
            <strong>Acumulado:</strong> {pontos.acumulado} pontos extras
          </p>
          <p className="cg-carteira__conta">
            <strong>Saldo disponível:</strong> {pontos.saldo_disponivel} pontos extras
          </p>
          <Aviso tipo="andamento">
            O acumulado só cresce — é o seu histórico inteiro. Quem dá para trocar é o saldo
            disponível.
          </Aviso>
        </div>
      )}

      <div className="cg-carteira__perfil">
        <h2>Meu perfil público</h2>
        {sessao?.divulgacao_autorizada ? (
          <Aviso tipo="sucesso">
            Seu responsável autorizou mostrar seu avatar e apelido para todo mundo ver.
          </Aviso>
        ) : (
          <Aviso tipo="atencao">
            Seu perfil ainda não aparece para outras pessoas. Quem decide isso é o seu
            responsável.
          </Aviso>
        )}
      </div>
    </section>
  );
}
