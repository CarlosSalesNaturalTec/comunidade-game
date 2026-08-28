import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { obterPainelDoDia, type PainelDoDia } from "../painel-do-dia/api";
import { ConferenciaDePresencas } from "./ConferenciaDePresencas";
import { LancamentoDaAtividade } from "./LancamentoDaAtividade";
import { RegistroDeInfracao } from "./RegistroDeInfracao";

const MENSAGEM_SEM_ENCONTRO = "Não há encontro em andamento agora.";

const MENSAGEM_DE_FALHA =
  "Não foi possível carregar o encontro. Tente novamente em instantes.";

// O encontro se fecha aqui, antes de a aula acabar: desfecho de cada
// participante, presenças conferidas e infração registrada. O painel do
// dia segue de leitura — é daqui que a pendência dele é resolvida
// (`RF-02-34`, `RF-02-36`, `RF-02-37`, `RF-02-39`, `RF-02-46`, `RF-02-47`).
export function TelaDeLancamentos() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const [painel, definirPainel] = useState<PainelDoDia | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const proximo = await obterPainelDoDia(sessao.token);
      definirPainel(proximo);
      definirErro(null);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro(MENSAGEM_DE_FALHA);
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const ehMestre = sessao?.papel === "mestre";

  return (
    <Moldura>
      <Cabecalho titulo="Lançamentos" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {painel === null && !erro && <EstadoDaLista>Carregando o encontro…</EstadoDaLista>}

      {painel !== null && painel.aula_id === null && (
        <EstadoDaLista>{MENSAGEM_SEM_ENCONTRO}</EstadoDaLista>
      )}

      {painel !== null &&
        painel.aula_id !== null &&
        (ehMestre ? (
          <RegistroDeInfracao
            aulaId={painel.aula_id}
            presencas={painel.presencas}
            atividadesPrevistas={painel.atividades_previstas}
          />
        ) : (
          <>
            <h2>Atividade realizada</h2>
            <LancamentoDaAtividade
              aulaId={painel.aula_id}
              presencas={painel.presencas}
              atividadesPrevistas={painel.atividades_previstas}
              onLancado={carregar}
            />

            <ConferenciaDePresencas
              aulaId={painel.aula_id}
              comunidadeVirtualId={painel.comunidade_virtual_id}
              presencas={painel.presencas}
              onAlterado={carregar}
            />

            <h2>Registrar infração</h2>
            <RegistroDeInfracao
              aulaId={painel.aula_id}
              presencas={painel.presencas}
              atividadesPrevistas={painel.atividades_previstas}
            />
          </>
        ))}
    </Moldura>
  );
}
