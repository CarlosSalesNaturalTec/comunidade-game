import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import { obterProgresso, type ProgressoDaTrilha } from "../api/trilha";

// Nível e quanto falta para o próximo, por trilha, mais pontos e badges —
// nível é percurso, nunca saldo de pontos, e nenhuma ação daqui lança
// resultado, presença ou mérito (`RF-05-15`, `RF-05-16`, `RN-05-03`,
// `RN-05-04`, `RN-05-06`).
export function Progresso() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [progresso, definirProgresso] = useState<ProgressoDaTrilha[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    let cancelado = false;
    obterProgresso(sessao.token)
      .then((resultado) => {
        if (!cancelado) definirProgresso(resultado);
      })
      .catch((erroCapturado) => {
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
          "Não foi possível carregar o seu progresso agora. Tente de novo em instantes.",
        );
      });
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  if (erro) return <Aviso tipo="erro">{erro}</Aviso>;
  if (progresso === null) return <EstadoDaLista>Carregando o seu progresso…</EstadoDaLista>;
  if (progresso.length === 0) {
    return <EstadoDaLista>Você ainda não está inscrito em nenhuma trilha.</EstadoDaLista>;
  }

  return (
    <section aria-label="Meu progresso">
      <h2>Meu progresso</h2>
      <ul className="cg-trilha__progresso">
        {progresso.map((item) => (
          <li key={item.trilha_id} className="cg-trilha__progresso-item">
            <h3>{item.trilha_nome}</h3>
            <p>Nível: {item.nivel_atual ?? "ainda sem nível"}</p>
            <p>
              Faltam {item.obrigatorias_totais - item.obrigatorias_desbloqueadas} de{" "}
              {item.obrigatorias_totais} missões obrigatórias para o próximo nível
            </p>
            <p>Pontos: {item.pontos_regulares}</p>
            {item.badges.length > 0 && <p>Badges: {item.badges.length}</p>}
          </li>
        ))}
      </ul>
    </section>
  );
}
