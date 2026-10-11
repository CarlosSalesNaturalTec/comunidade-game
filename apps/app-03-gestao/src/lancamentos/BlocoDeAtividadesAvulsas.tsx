import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { type AtividadeAvulsa, listarAtividadesAvulsas } from "../atividades/api";
import type { PainelDoDia } from "../painel-do-dia/api";
import { LancamentoDaAtividadeAvulsa } from "./LancamentoDaAtividadeAvulsa";

interface Props {
  aulaId: string;
  presencas: PainelDoDia["presencas"];
  equipes: PainelDoDia["equipes"];
  onLancado: () => void;
}

const MENSAGEM_SEM_AVULSA = "Este encontro não tem atividade avulsa cadastrada.";

const MENSAGEM_DE_FALHA =
  "Não foi possível carregar as atividades avulsas. Tente novamente em instantes.";

// As avulsas da aula vigente, lidas pelo filtro por aula — elas não entram
// na programação do encontro, então o painel do dia não as traz
// (`RF-02-112`).
export function BlocoDeAtividadesAvulsas({ aulaId, presencas, equipes, onLancado }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [avulsas, definirAvulsas] = useState<AtividadeAvulsa[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      definirAvulsas(await listarAtividadesAvulsas(sessao.token, aulaId));
      definirErro(null);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro(MENSAGEM_DE_FALHA);
    }
  }, [sessao, aulaId, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  return (
    <section aria-label="Atividades avulsas do encontro">
      <h2>Atividades avulsas</h2>

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {avulsas === null && !erro && (
        <EstadoDaLista>Carregando as atividades avulsas…</EstadoDaLista>
      )}

      {avulsas !== null && avulsas.length === 0 && (
        <EstadoDaLista>{MENSAGEM_SEM_AVULSA}</EstadoDaLista>
      )}

      {avulsas?.map((atividade) => (
        <LancamentoDaAtividadeAvulsa
          key={atividade.id}
          aulaId={aulaId}
          atividade={atividade}
          presencas={presencas}
          equipes={equipes}
          onLancado={onLancado}
        />
      ))}
    </section>
  );
}
