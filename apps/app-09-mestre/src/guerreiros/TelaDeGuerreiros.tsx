import { useSessao } from "comum/autenticacao";
import { Avatar } from "comum/avatar";
import { HistoricoDePontuacao, lerHistoricoDePontuacaoDoGuerreiro } from "comum/pontuacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { type GuerreiroVinculavel, listarGuerreirosVinculaveis } from "../responsaveis/api";

// Os Guerreiros e Guerreiras ativos das comunidades do vínculo vigente do
// Mestre, por nick e avatar — nunca imagem real, nome civil ou contato —, e a
// ficha de cada um com o histórico de pontuação (`RF-09-143`, `RF-09-144`,
// `RN-09-18`). A lista reaproveita a leitura dos vinculáveis, que já recorta
// pela comunidade do vínculo (design — decisão 7).
export function TelaDeGuerreiros() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [guerreiros, definirGuerreiros] = useState<GuerreiroVinculavel[] | null>(null);
  const [cursor, definirCursor] = useState<string | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [aberto, definirAberto] = useState<GuerreiroVinculavel | null>(null);

  const carregar = useCallback(
    async (depoisDe: string | null) => {
      if (!sessao) return;
      definirErro(null);
      try {
        const pagina = await listarGuerreirosVinculaveis(sessao.token, depoisDe);
        definirGuerreiros((anteriores) =>
          depoisDe && anteriores ? [...anteriores, ...pagina.itens] : pagina.itens,
        );
        definirCursor(pagina.proximo_cursor);
      } catch {
        definirErro("Não foi possível carregar os Guerreiros e Guerreiras. Tente novamente.");
      }
    },
    [sessao],
  );

  useEffect(() => {
    carregar(null);
  }, [carregar]);

  const token = sessao?.token;
  const guerreiroId = aberto?.id;
  const ler = useCallback(
    (cursorDoHistorico: string | null) =>
      lerHistoricoDePontuacaoDoGuerreiro(token ?? "", guerreiroId ?? "", cursorDoHistorico),
    [token, guerreiroId],
  );

  if (aberto) {
    return (
      <section aria-label={`Ficha de ${aberto.nick}`}>
        <Botao variante="secundaria" onClick={() => definirAberto(null)}>
          Voltar à lista
        </Botao>
        <h1>
          <Avatar avatar={aberto.avatar} tamanho={48} /> {aberto.nick}
        </h1>
        <HistoricoDePontuacao ler={ler} aoRecusarSessao={tratarRecusaDeSessao} />
      </section>
    );
  }

  return (
    <section aria-label="Guerreiros e Guerreiras">
      <h1>Guerreiros e Guerreiras</h1>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {guerreiros === null && !erro && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {guerreiros !== null && guerreiros.length === 0 && (
        <EstadoDaLista>
          Nenhum Guerreiro(a) ativo nas comunidades do seu vínculo.
        </EstadoDaLista>
      )}
      {guerreiros !== null && guerreiros.length > 0 && (
        <ul className="cg-lista-de-guerreiros">
          {guerreiros.map((guerreiro) => (
            <li key={guerreiro.id}>
              <Avatar avatar={guerreiro.avatar} tamanho={32} /> {guerreiro.nick}{" "}
              <Botao variante="secundaria" onClick={() => definirAberto(guerreiro)}>
                Abrir a ficha de {guerreiro.nick}
              </Botao>
            </li>
          ))}
        </ul>
      )}
      {cursor && (
        <Botao variante="secundaria" onClick={() => carregar(cursor)}>
          Carregar mais
        </Botao>
      )}
    </section>
  );
}
