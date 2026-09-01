import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { type CatalogoDeTermo, consultarTermos, registrarLeituraDeTermo } from "./api";

interface Props {
  /** Versão que uma decisão antiga do histórico da autorização pediu para
   * abrir — a tela rola até ela em vez de mostrar só a vigente
   * (`RF-13-33`). */
  versaoFocada?: string | null;
}

const FORMATADOR_DE_DATA_HORA = new Intl.DateTimeFormat("pt-BR", {
  dateStyle: "short",
  timeStyle: "short",
});

function formatarDataHora(momentoISO: string): string {
  return FORMATADOR_DE_DATA_HORA.format(new Date(momentoISO));
}

// O texto do termo vigente em linguagem simples, com a leitura registrada
// assim que a tela abre, e o histórico das versões anteriores — cada uma
// com o texto que valia naquela data (`RF-13-32`, `RF-13-33`, `RF-13-34`).
// A tela nunca concede nem revoga autorização: essa decisão continua na
// tela de autorização.
export function TelaDeTermos({ versaoFocada }: Props) {
  const { sessao } = useSessao();
  const [catalogo, definirCatalogo] = useState<CatalogoDeTermo[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [leituraRegistradaEm, definirLeituraRegistradaEm] = useState<string | null>(null);
  const [versaoAberta, definirVersaoAberta] = useState<string | null>(null);

  const carregar = useCallback(() => {
    if (!sessao) return;
    return consultarTermos(sessao.token)
      .then(definirCatalogo)
      .catch(() => definirErro("Não foi possível carregar o termo. Tente novamente."));
  }, [sessao]);

  useEffect(() => {
    definirCatalogo(null);
    definirErro(null);
    definirLeituraRegistradaEm(null);
    carregar();
  }, [carregar]);

  useEffect(() => {
    definirVersaoAberta(versaoFocada ?? null);
  }, [versaoFocada]);

  const termo = catalogo?.[0] ?? null;

  // A leitura é registrada quando a pessoa efetivamente lê o termo — assim
  // que o texto vigente chega à tela (`RF-13-32`).
  useEffect(() => {
    if (!sessao || !termo) return;
    registrarLeituraDeTermo(termo.vigente.versao, sessao.token)
      .then((leitura) => definirLeituraRegistradaEm(leitura.lida_em))
      .catch(() => {
        // Falha ao registrar a leitura não impede a pessoa de ler o texto,
        // que já está na tela — só a confirmação some.
      });
  }, [sessao, termo]);

  if (erro) {
    return <Aviso tipo="erro">{erro}</Aviso>;
  }

  if (catalogo === null) {
    return <EstadoDaLista>Carregando…</EstadoDaLista>;
  }

  if (!termo) {
    return <EstadoDaLista>Nenhum termo disponível ainda.</EstadoDaLista>;
  }

  const versaoParaMostrar =
    versaoAberta && versaoAberta !== termo.vigente.versao
      ? termo.historico.find((item) => item.versao === versaoAberta)
      : termo.vigente;

  return (
    <section aria-label="Termo">
      <section>
        <h2>Termo vigente — versão {termo.vigente.versao}</h2>
        <p style={{ whiteSpace: "pre-line" }}>{termo.vigente.texto}</p>
        {leituraRegistradaEm && (
          <Aviso tipo="sucesso">
            Leitura registrada em {formatarDataHora(leituraRegistradaEm)}. Isso é prova de que
            você leu — não é uma decisão de autorização.
          </Aviso>
        )}
      </section>

      {versaoAberta && versaoParaMostrar && versaoAberta !== termo.vigente.versao && (
        <section aria-label={`Versão ${versaoAberta} do termo`}>
          <h2>Versão {versaoAberta} — a que valia na decisão consultada</h2>
          <p style={{ whiteSpace: "pre-line" }}>{versaoParaMostrar.texto}</p>
        </section>
      )}

      <section>
        <h2>Histórico de versões</h2>
        {termo.historico.length === 0 && (
          <EstadoDaLista>Nenhuma versão anterior registrada.</EstadoDaLista>
        )}
        {termo.historico.length > 0 && (
          <ul aria-label="Histórico do termo">
            {termo.historico.map((item) => (
              <li key={item.versao}>
                Versão {item.versao} — valia até{" "}
                {formatarDataHora(termo.vigente.vigente_desde)}
                <button type="button" onClick={() => definirVersaoAberta(item.versao)}>
                  Ver texto desta versão
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </section>
  );
}
