import { ErroDaApi } from "comum/api";
import { eu } from "comum/autenticacao/api";
import { useCallback, useEffect, useRef, useState } from "react";
import { registrarPresenca } from "../api/presencas";
import { confirmarSessaoDeGuerreiro } from "../api/sessoesDeGuerreiro";
import { useEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";
import {
  type ItemDaFilaDePresenca,
  lerFilaDePresenca,
  removerDaFilaDePresenca,
} from "./filaDePresenca";

function chaveDoItem(item: ItemDaFilaDePresenca): string {
  return `${item.nick}::${item.momento_do_fato}`;
}

// Refaz, por item, a sequência que a entrada por confirmação já usa hoje —
// nenhuma rota nova, nenhum contrato novo (design — decisão 7): abre uma
// sessão de Guerreiro(a) que ninguém usará, lê `GET /v1/eu` para o
// identificador e registra a presença com a hora do fato original. O token
// aberto nunca é gravado — expira sozinho.
async function sincronizarItem(
  item: ItemDaFilaDePresenca,
  tokenDeTrabalho: string,
): Promise<"sincronizado" | "falha_de_rede" | "falha_de_dado"> {
  try {
    const abertura = await confirmarSessaoDeGuerreiro(item.nick, tokenDeTrabalho);
    const quemSou = await eu(abertura.token);
    await registrarPresenca(
      item.aula_id,
      {
        guerreiro_id: quemSou.persona_id,
        modo: "confirmacao",
        momento_do_fato: item.momento_do_fato,
      },
      tokenDeTrabalho,
    );
    removerDaFilaDePresenca(item);
    return "sincronizado";
  } catch (erro) {
    // Resposta do núcleo que recusa (nick errado, por exemplo) prova que a
    // rede está de pé — só a ausência de resposta é falha de rede (design —
    // Risks: "nick errado só falha na volta da rede").
    return erro instanceof ErroDaApi ? "falha_de_dado" : "falha_de_rede";
  }
}

export interface ItemDaFilaComSituacao extends ItemDaFilaDePresenca {
  falhou: boolean;
}

// Roda no aparelho do Mestre/Admin, sempre que há aula escolhida: sincroniza
// sozinha ao montar, na transição de sem rede para com rede, e no evento
// `online` do navegador — que aqui é só o gatilho da nova tentativa, nunca a
// prova de que o núcleo responde (design — decisão 9).
export function useSincronizacaoDaFilaDePresenca(
  aulaId: string | null,
  tokenDeTrabalho: string | null,
) {
  const { marcarFalhaDeRede, marcarSucessoDeRede, semRede } = useEstadoDeRede();
  const [itens, definirItens] = useState<ItemDaFilaDePresenca[]>(() =>
    aulaId ? lerFilaDePresenca(aulaId) : [],
  );
  const [falhas, definirFalhas] = useState<Set<string>>(new Set());
  const [sincronizando, definirSincronizando] = useState(false);
  const semRedeAnteriorRef = useRef(semRede);

  const sincronizarTudo = useCallback(async () => {
    if (!aulaId || !tokenDeTrabalho) return;
    definirSincronizando(true);
    try {
      for (const item of lerFilaDePresenca(aulaId)) {
        const desfecho = await sincronizarItem(item, tokenDeTrabalho);
        if (desfecho === "sincronizado") {
          marcarSucessoDeRede();
          definirFalhas((atual) => {
            const proximo = new Set(atual);
            proximo.delete(chaveDoItem(item));
            return proximo;
          });
        } else if (desfecho === "falha_de_dado") {
          marcarSucessoDeRede();
          definirFalhas((atual) => new Set(atual).add(chaveDoItem(item)));
        } else {
          marcarFalhaDeRede();
          definirFalhas((atual) => new Set(atual).add(chaveDoItem(item)));
        }
      }
    } finally {
      definirItens(lerFilaDePresenca(aulaId));
      definirSincronizando(false);
    }
  }, [aulaId, tokenDeTrabalho, marcarSucessoDeRede, marcarFalhaDeRede]);

  const tentarDeNovo = useCallback(
    async (item: ItemDaFilaDePresenca) => {
      if (!tokenDeTrabalho) return;
      definirSincronizando(true);
      try {
        const desfecho = await sincronizarItem(item, tokenDeTrabalho);
        if (desfecho === "sincronizado" || desfecho === "falha_de_dado") {
          marcarSucessoDeRede();
        } else {
          marcarFalhaDeRede();
        }
        if (desfecho === "sincronizado") {
          definirFalhas((atual) => {
            const proximo = new Set(atual);
            proximo.delete(chaveDoItem(item));
            return proximo;
          });
        } else {
          definirFalhas((atual) => new Set(atual).add(chaveDoItem(item)));
        }
      } finally {
        if (item.aula_id) definirItens(lerFilaDePresenca(item.aula_id));
        definirSincronizando(false);
      }
    },
    [tokenDeTrabalho, marcarSucessoDeRede, marcarFalhaDeRede],
  );

  // biome-ignore lint/correctness/useExhaustiveDependencies: roda só ao montar, para retomar a fila de uma sessão anterior.
  useEffect(() => {
    sincronizarTudo();
  }, []);

  useEffect(() => {
    if (semRedeAnteriorRef.current && !semRede) {
      sincronizarTudo();
    }
    semRedeAnteriorRef.current = semRede;
  }, [semRede, sincronizarTudo]);

  useEffect(() => {
    window.addEventListener("online", sincronizarTudo);
    return () => window.removeEventListener("online", sincronizarTudo);
  }, [sincronizarTudo]);

  const itensComSituacao: ItemDaFilaComSituacao[] = itens.map((item) => ({
    ...item,
    falhou: falhas.has(chaveDoItem(item)),
  }));

  return { itens: itensComSituacao, sincronizando, tentarDeNovo };
}
