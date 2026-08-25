import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { AnexoDaDigitalizacao } from "./AnexoDaDigitalizacao";
import { obterPainelDoDia, type PainelDoDia } from "./api";

const INTERVALO_DE_SONDAGEM_EM_MS = 10000;

const MENSAGEM_DE_PERDA_DE_CONTATO =
  "Perdemos contato com o núcleo. O painel segue com o último estado conhecido e volta a atualizar sozinho assim que a rede voltar.";

const MENSAGEM_SEM_ENCONTRO = "Não há encontro em andamento agora.";

function nomeDaEquipe(equipe: PainelDoDia["equipes"][number]): string {
  return equipe.integrantes.map((integrante) => integrante.nick).join(", ") || "Equipe vazia";
}

const ROTULO_DA_PENDENCIA: Record<string, string> = {
  lancamento_da_atividade_realizada: "Falta lançar a atividade realizada desta aula.",
  digitalizacao_do_termo: "Termo de biometria assinado, aguardando o anexo da digitalização.",
};

// A leitura do encontro em andamento, atualizada por sondagem, sem
// caminho de escrita além do anexo da digitalização — cada pendência
// listada aponta para quem a resolve (`RF-02-41` a `RF-02-48`,
// `RF-02-69`, `RN-02-12`, documento 03 §1).
export function TelaDoPainelDoDia() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const [painel, definirPainel] = useState<PainelDoDia | null>(null);
  const [semRede, definirSemRede] = useState(false);

  const sondar = useCallback(async () => {
    if (!sessao) return;
    try {
      const proximo = await obterPainelDoDia(sessao.token);
      definirPainel(proximo);
      definirSemRede(false);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirSemRede(true);
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    sondar();
    const intervalo = setInterval(sondar, INTERVALO_DE_SONDAGEM_EM_MS);
    return () => clearInterval(intervalo);
  }, [sondar]);

  const ehAdmin = sessao?.papel === "admin";

  return (
    <Moldura>
      <Cabecalho titulo="Painel do dia" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {semRede && <Aviso tipo="atencao">{MENSAGEM_DE_PERDA_DE_CONTATO}</Aviso>}

      {painel === null && !semRede && <EstadoDaLista>Carregando o painel…</EstadoDaLista>}

      {painel !== null && painel.aula_id === null && (
        <EstadoDaLista>{MENSAGEM_SEM_ENCONTRO}</EstadoDaLista>
      )}

      {painel !== null && painel.aula_id !== null && (
        <>
          <section aria-label="Presenças">
            <h2>Quem chegou</h2>
            {painel.presencas.length === 0 && (
              <EstadoDaLista>Ninguém registrou presença ainda.</EstadoDaLista>
            )}
            {painel.presencas.length > 0 && (
              <ul>
                {painel.presencas.map((presenca) => (
                  <li key={presenca.guerreiro_id}>
                    {presenca.nick} —{" "}
                    {presenca.modo === "reconhecimento" ? "reconhecimento" : "confirmada"}
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section aria-label="Aguardando aparelho">
            <h2>Aguardando aparelho</h2>
            {painel.aguardando_aparelho.length === 0 && (
              <EstadoDaLista>Ninguém aguardando aparelho.</EstadoDaLista>
            )}
            {painel.aguardando_aparelho.length > 0 && (
              <ul>
                {painel.aguardando_aparelho.map((guerreiro) => (
                  <li key={guerreiro.guerreiro_id}>{guerreiro.nick}</li>
                ))}
              </ul>
            )}
          </section>

          <section aria-label="Equipes e missão">
            <h2>Equipes</h2>
            {painel.equipes.length === 0 && (
              <EstadoDaLista>Nenhuma equipe formada ainda.</EstadoDaLista>
            )}
            {painel.equipes.length > 0 && (
              <ul>
                {painel.equipes.map((equipe) => (
                  <li key={equipe.id}>
                    {nomeDaEquipe(equipe)} — {equipe.missao_titulo ?? "sem missão declarada"}
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section aria-label="Previsto e provido">
            <h2>Previsto e provido</h2>
            {painel.atividades_previstas.length === 0 && (
              <EstadoDaLista>Nenhuma atividade prevista para este encontro.</EstadoDaLista>
            )}
            {painel.atividades_previstas.length > 0 && (
              <ul>
                {painel.atividades_previstas.map((atividade) => (
                  <li key={atividade.id}>
                    {atividade.missao_titulo} — {atividade.titulo}
                  </li>
                ))}
              </ul>
            )}
            {painel.recursos_providos.length === 0 && (
              <EstadoDaLista>Nenhum recurso reservado para este encontro.</EstadoDaLista>
            )}
            {painel.recursos_providos.length > 0 && (
              <ul>
                {painel.recursos_providos.map((recurso) => (
                  <li key={recurso.tipo_de_recurso_id}>
                    {recurso.tipo_de_recurso_id}: {recurso.quantidade}
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section aria-label="Saldo do ponto de apoio">
            <h2>Saldo do ponto de apoio</h2>
            {painel.saldo_do_ponto_de_apoio.length === 0 && (
              <EstadoDaLista>Nenhum saldo registrado neste ponto de apoio.</EstadoDaLista>
            )}
            {painel.saldo_do_ponto_de_apoio.length > 0 && (
              <ul>
                {painel.saldo_do_ponto_de_apoio.map((saldo) => (
                  <li key={saldo.tipo_de_recurso_id}>
                    {saldo.tipo_de_recurso_id}: {saldo.saldo}
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section aria-label="Lançamentos pendentes">
            <h2>Lançamentos pendentes</h2>
            {painel.pendencias.length === 0 && (
              <EstadoDaLista>Nenhuma pendência para este encontro.</EstadoDaLista>
            )}
            {painel.pendencias.length > 0 && (
              <ul>
                {painel.pendencias.map((pendencia, indice) => (
                  <li key={`${pendencia.tipo}-${pendencia.guerreiro_id ?? indice}`}>
                    {pendencia.nick ? `${pendencia.nick} — ` : ""}
                    {ROTULO_DA_PENDENCIA[pendencia.tipo] ?? pendencia.tipo}
                    {pendencia.tipo === "digitalizacao_do_termo" &&
                      pendencia.consentimento_id &&
                      ehAdmin && (
                        <AnexoDaDigitalizacao
                          consentimentoId={pendencia.consentimento_id}
                          token={sessao?.token ?? ""}
                          aoAnexar={sondar}
                        />
                      )}
                  </li>
                ))}
              </ul>
            )}
          </section>
        </>
      )}
    </Moldura>
  );
}
