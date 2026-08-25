import { ErroDaApi } from "comum/api";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import { type ItemDeCatalogoAvulso, listarCatalogoAvulso } from "../api/catalogoAvulso";
import { consultarMeusPontosExtras, type PontosExtras } from "../api/pontosExtras";
import { registrarTroca } from "../api/trocas";

interface Props {
  tokenDeTrabalho: string;
  aulaId: string;
  tokenDoGuerreiro: string;
  guerreiroId: string;
  aoConcluir: () => void;
  aoVoltar: () => void;
}

// O catálogo e o saldo vêm sempre sob o token do Guerreiro(a) — é a
// comunidade do vínculo dele que decide o que aparece (`RF-04-50`, design
// — decisão 4). Item de estoque zero não é oferecido, ainda que o núcleo o
// devolva ativo (`RF-04-54`, design — decisão 5).
export function TelaDeTroca({
  tokenDeTrabalho,
  aulaId,
  tokenDoGuerreiro,
  guerreiroId,
  aoConcluir,
  aoVoltar,
}: Props) {
  const [catalogo, definirCatalogo] = useState<ItemDeCatalogoAvulso[] | null>(null);
  const [pontosExtras, definirPontosExtras] = useState<PontosExtras | null>(null);
  const [itemEmEnvioId, definirItemEmEnvioId] = useState<string | null>(null);
  const [erroDeEnvio, definirErroDeEnvio] = useState<string | null>(null);

  useEffect(() => {
    let cancelado = false;
    Promise.all([
      listarCatalogoAvulso(tokenDoGuerreiro),
      consultarMeusPontosExtras(tokenDoGuerreiro),
    ]).then(([itens, pontos]) => {
      if (!cancelado) {
        definirCatalogo(itens);
        definirPontosExtras(pontos);
      }
    });
    return () => {
      cancelado = true;
    };
  }, [tokenDoGuerreiro]);

  async function confirmarEntrega(item: ItemDeCatalogoAvulso) {
    definirErroDeEnvio(null);
    definirItemEmEnvioId(item.id);
    try {
      await registrarTroca(
        aulaId,
        { item_de_catalogo_avulso_id: item.id, guerreiro_id: guerreiroId },
        tokenDeTrabalho,
      );
      aoConcluir();
    } catch (erroCapturado) {
      definirErroDeEnvio(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível concluir a troca. Tente novamente.",
      );
      definirItemEmEnvioId(null);
    }
  }

  if (catalogo === null || pontosExtras === null) {
    return (
      <Moldura>
        <Cabecalho
          titulo="Troca por recompensa avulsa"
          acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
        />
        <EstadoDaLista>Carregando o catálogo…</EstadoDaLista>
      </Moldura>
    );
  }

  const itensDisponiveis = catalogo.filter((item) => Number(item.estoque) > 0);

  return (
    <Moldura>
      <Cabecalho
        titulo="Troca por recompensa avulsa"
        subtitulo={`Saldo disponível: ${pontosExtras.saldo_disponivel} pontos`}
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />
      {erroDeEnvio && <Aviso tipo="erro">{erroDeEnvio}</Aviso>}
      {itensDisponiveis.length === 0 ? (
        <EstadoDaLista>Nenhum item disponível para troca agora.</EstadoDaLista>
      ) : (
        <ul className="cg-catalogo-avulso">
          {itensDisponiveis.map((item) => {
            const preco = item.preco_em_pontos_extras;
            const podeTrocar = preco !== null && preco <= pontosExtras.saldo_disponivel;
            const faltam = preco !== null ? preco - pontosExtras.saldo_disponivel : null;
            const emEnvio = itemEmEnvioId === item.id;
            return (
              <li key={item.id} className="cg-item-de-catalogo-avulso">
                <span>{item.nome}</span>
                <span>
                  {preco !== null ? `${preco} pontos` : "sem preço"} — estoque {item.estoque}
                </span>
                {podeTrocar ? (
                  <Botao
                    onClick={() => confirmarEntrega(item)}
                    desabilitado={itemEmEnvioId !== null}
                  >
                    {emEnvio ? "Confirmando…" : "Confirmar entrega"}
                  </Botao>
                ) : (
                  faltam !== null && (
                    <Aviso tipo="atencao">
                      Faltam {faltam} pontos para trocar por este item.
                    </Aviso>
                  )
                )}
              </li>
            );
          })}
        </ul>
      )}
    </Moldura>
  );
}
