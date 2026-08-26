import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import {
  type ItemDeCatalogoAvulso,
  listarCatalogoAvulso,
  listarMinhasTrocas,
  type Troca,
} from "../api/carteira";

function formatarData(valorIso: string): string {
  return new Date(valorIso).toLocaleDateString("pt-BR");
}

function ehRecusaDeSessao(erro: unknown): boolean {
  return (
    !!erro &&
    typeof erro === "object" &&
    "codigo" in erro &&
    (erro.codigo === "sessao_ausente" || erro.codigo === "sessao_invalida")
  );
}

// O catálogo avulso da comunidade e o histórico das próprias trocas, na
// mesma tela — sem ação de trocar ou reservar, porque a troca acontece
// presencialmente com o Mestre, ao fim do encontro (`RF-05-83`, `RF-05-86`,
// `RF-05-87`, `RF-05-88`).
export function CatalogoAvulso() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [itens, definirItens] = useState<ItemDeCatalogoAvulso[] | null>(null);
  const [nomesDosItens, definirNomesDosItens] = useState<Record<string, string>>({});
  const [trocas, definirTrocas] = useState<Troca[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    const token = sessao.token;
    let cancelado = false;

    async function carregar() {
      definirErro(null);
      try {
        const [catalogo, historico] = await Promise.all([
          listarCatalogoAvulso(token),
          listarMinhasTrocas(token),
        ]);
        if (cancelado) return;
        definirItens(catalogo.filter((item) => item.ativo));
        definirNomesDosItens(Object.fromEntries(catalogo.map((item) => [item.id, item.nome])));
        definirTrocas(historico);
      } catch (erroCapturado) {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro("Não foi possível carregar o catálogo agora. Tente de novo em instantes.");
      }
    }

    carregar();
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  return (
    <section className="cg-catalogo-avulso" aria-label="Catálogo avulso">
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      <div className="cg-catalogo-avulso__catalogo">
        <h2>Catálogo</h2>
        <Aviso tipo="andamento">
          A troca acontece presencialmente, com o Mestre, ao fim do encontro. Aqui você só
          confere o que tem disponível.
        </Aviso>

        {itens === null && !erro && <EstadoDaLista>Carregando o catálogo…</EstadoDaLista>}
        {itens !== null && itens.length === 0 && (
          <EstadoDaLista>
            Ainda não há recompensa avulsa disponível na sua comunidade.
          </EstadoDaLista>
        )}
        {itens !== null && itens.length > 0 && (
          <ul className="cg-lista-do-catalogo">
            {itens.map((item) => (
              <li key={item.id} className="cg-cartao-do-catalogo">
                <p className="cg-cartao-do-catalogo__titulo">{item.nome}</p>
                <p>
                  Preço:{" "}
                  {item.preco_em_pontos_extras !== null
                    ? `${item.preco_em_pontos_extras} pontos extras`
                    : "ainda sem preço cadastrado"}
                </p>
                <p>Estoque: {item.estoque}</p>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="cg-catalogo-avulso__historico">
        <h2>Histórico de trocas</h2>
        {trocas === null && !erro && <EstadoDaLista>Carregando o histórico…</EstadoDaLista>}
        {trocas !== null && trocas.length === 0 && (
          <EstadoDaLista>Você ainda não fez nenhuma troca.</EstadoDaLista>
        )}
        {trocas !== null && trocas.length > 0 && (
          <ul className="cg-lista-do-historico">
            {trocas.map((troca) => (
              <li key={troca.id} className="cg-cartao-do-historico">
                <p className="cg-cartao-do-historico__titulo">
                  {nomesDosItens[troca.item_de_catalogo_avulso_id] ??
                    "Item fora do catálogo atual"}
                </p>
                <p>Preço cobrado: {troca.preco_cobrado} pontos extras</p>
                <p>Data: {formatarData(troca.registrado_em)}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
