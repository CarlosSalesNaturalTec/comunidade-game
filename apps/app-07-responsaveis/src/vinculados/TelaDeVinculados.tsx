import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import { TelaDeAutorizacao } from "../autorizacao/TelaDeAutorizacao";
import { TelaDaImagemDoOnboarding } from "../biometria/TelaDaImagemDoOnboarding";
import { ProvedorDeDireitos } from "../direitos/ContextoDeDireitos";
import { TelaDeEvolucao } from "../evolucao/TelaDeEvolucao";
import { TelaDePropostas } from "../propostas/TelaDePropostas";
import { TelaDeSolicitacoes } from "../solicitacoes/TelaDeSolicitacoes";
import { TelaDeTermos } from "../termos/TelaDeTermos";
import { TelaDeTransparencia } from "../transparencia/TelaDeTransparencia";
import { type GuerreiroVinculado, listarMeusGuerreiros } from "./api";

type Aba =
  | "evolucao"
  | "autorizacao"
  | "solicitacoes"
  | "imagem"
  | "transparencia"
  | "termos"
  | "propostas";

interface Props {
  /** Cresce a cada vez que um `AvisoDeColeta` fora desta tela pede a
   * transparência — inclusive antes de haver vinculado selecionado
   * (`RF-13-41`). */
  pedidoDeTransparencia?: number;
}

// A lista dos vinculados, cada um com o grau de parentesco, e a alternância
// entre eles como estado da própria aplicação — sem nova entrada e sem
// encerrar a sessão (`RF-13-04`, `RF-13-05`, `RN-13-04`). Nenhuma tela de
// cadastro de responsável ou de vínculo existe aqui: tudo isso é ato da
// gestão (`RF-13-06`).
export function TelaDeVinculados({ pedidoDeTransparencia = 0 }: Props) {
  const { sessao } = useSessao();
  const [guerreiros, definirGuerreiros] = useState<GuerreiroVinculado[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [selecionadoId, definirSelecionadoId] = useState<string | null>(null);
  // A aba não reseta ao trocar de vinculado: trocar mantém a mesma aba,
  // agora com os dados do novo vinculado (`RF-13-05`, `RN-13-04`).
  const [aba, definirAba] = useState<Aba>("evolucao");
  // A versão que uma decisão antiga do histórico da autorização pediu para
  // abrir na tela do termo (`RF-13-33`).
  const [versaoDoTermoFocada, definirVersaoDoTermoFocada] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    listarMeusGuerreiros(sessao.token)
      .then((lista) => {
        definirGuerreiros(lista);
        definirSelecionadoId((atual) => atual ?? lista[0]?.id ?? null);
      })
      .catch(() => definirErro("Não foi possível carregar seus vinculados. Tente novamente."));
  }, [sessao]);

  useEffect(() => {
    if (pedidoDeTransparencia > 0) {
      definirAba("transparencia");
    }
  }, [pedidoDeTransparencia]);

  if (erro) {
    return (
      <Moldura>
        <Aviso tipo="erro">{erro}</Aviso>
      </Moldura>
    );
  }

  if (guerreiros === null) {
    return (
      <Moldura>
        <EstadoDaLista>Carregando…</EstadoDaLista>
      </Moldura>
    );
  }

  if (guerreiros.length === 0) {
    return (
      <Moldura>
        <Cabecalho titulo="Seus vinculados" />
        <EstadoDaLista>Nenhum vinculado ainda. Procure a gestão no encontro.</EstadoDaLista>
      </Moldura>
    );
  }

  const selecionado = guerreiros.find((guerreiro) => guerreiro.id === selecionadoId) ?? null;

  return (
    <ProvedorDeDireitos irParaTransparencia={() => definirAba("transparencia")}>
      <Moldura>
        <Cabecalho titulo="Seus vinculados" />
        <nav className="cg-navegacao-de-area" aria-label="Vinculados">
          {guerreiros.map((guerreiro) => (
            <Botao
              key={guerreiro.id}
              variante={guerreiro.id === selecionadoId ? "primaria" : "secundaria"}
              onClick={() => definirSelecionadoId(guerreiro.id)}
            >
              {guerreiro.nick} · {guerreiro.grau_de_parentesco}
            </Botao>
          ))}
        </nav>
        {selecionado && (
          <>
            <nav className="cg-navegacao-de-area" aria-label={`Áreas de ${selecionado.nick}`}>
              <Botao
                variante={aba === "evolucao" ? "primaria" : "secundaria"}
                onClick={() => definirAba("evolucao")}
              >
                Evolução
              </Botao>
              <Botao
                variante={aba === "autorizacao" ? "primaria" : "secundaria"}
                onClick={() => definirAba("autorizacao")}
              >
                Autorização
              </Botao>
              <Botao
                variante={aba === "transparencia" ? "primaria" : "secundaria"}
                onClick={() => definirAba("transparencia")}
              >
                Transparência
              </Botao>
              <Botao
                variante={aba === "termos" ? "primaria" : "secundaria"}
                onClick={() => definirAba("termos")}
              >
                Termo
              </Botao>
              <Botao
                variante={aba === "solicitacoes" ? "primaria" : "secundaria"}
                onClick={() => definirAba("solicitacoes")}
              >
                Solicitações
              </Botao>
              <Botao
                variante={aba === "propostas" ? "primaria" : "secundaria"}
                onClick={() => definirAba("propostas")}
              >
                Propostas
              </Botao>
              <Botao
                variante={aba === "imagem" ? "primaria" : "secundaria"}
                onClick={() => definirAba("imagem")}
              >
                Imagem do onboarding
              </Botao>
            </nav>
            {aba === "evolucao" && <TelaDeEvolucao guerreiro={selecionado} />}
            {aba === "autorizacao" && (
              <TelaDeAutorizacao
                guerreiro={selecionado}
                aoAbrirVersaoDoTermo={(versao) => {
                  definirVersaoDoTermoFocada(versao);
                  definirAba("termos");
                }}
              />
            )}
            {aba === "transparencia" && <TelaDeTransparencia guerreiro={selecionado} />}
            {aba === "termos" && <TelaDeTermos versaoFocada={versaoDoTermoFocada} />}
            {aba === "solicitacoes" && <TelaDeSolicitacoes guerreiro={selecionado} />}
            {aba === "propostas" && <TelaDePropostas />}
            {aba === "imagem" && <TelaDaImagemDoOnboarding guerreiro={selecionado} />}
          </>
        )}
      </Moldura>
    </ProvedorDeDireitos>
  );
}
