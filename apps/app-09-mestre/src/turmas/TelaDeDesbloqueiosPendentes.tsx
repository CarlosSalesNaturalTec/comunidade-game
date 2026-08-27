import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import {
  type DesbloqueioPendente,
  julgarDesafioPratico,
  listarDesbloqueiosPendentes,
} from "../trilhas/api";

function formatarMomento(momento: string): string {
  return new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" }).format(
    new Date(momento),
  );
}

// A bancada dos desafios práticos declarados como cumpridos, ainda não
// julgados, das próprias trilhas — julgar abre a missão seguinte para
// aquele Guerreiro(a), e não passar nunca o elimina (`RF-09-26`,
// `RF-09-117`, `RF-05-13`, `RF-05-14`).
export function TelaDeDesbloqueiosPendentes() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const [pendentes, definirPendentes] = useState<DesbloqueioPendente[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [julgando, definirJulgando] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const resultado = await listarDesbloqueiosPendentes(sessao.token);
      definirPendentes(resultado);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar a bancada. Tente novamente em instantes.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  async function julgar(pendente: DesbloqueioPendente, aprovado: boolean) {
    if (!sessao) return;
    definirJulgando(pendente.id);
    definirErro(null);
    try {
      await julgarDesafioPratico(
        pendente.missao_id,
        pendente.guerreiro_id,
        aprovado,
        sessao.token,
      );
      definirPendentes((atual) => (atual ?? []).filter((item) => item.id !== pendente.id));
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível julgar agora. Tente novamente em instantes.");
    } finally {
      definirJulgando(null);
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Desafios práticos a julgar"
        acao={{ rotulo: "Sair", aoAcionar: sair }}
      />
      <p>
        Julgar que passou abre a missão seguinte para aquele Guerreiro(a). Não passar não o
        elimina.
      </p>

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {pendentes === null && <EstadoDaLista>Carregando a bancada…</EstadoDaLista>}
      {pendentes !== null && pendentes.length === 0 && (
        <EstadoDaLista>Nenhum desafio prático esperando julgamento.</EstadoDaLista>
      )}
      {pendentes !== null && pendentes.length > 0 && (
        <ul
          className="lista-de-desbloqueios-pendentes"
          aria-label="Desafios práticos a julgar"
        >
          {pendentes.map((pendente) => (
            <li key={pendente.id} className="lista-de-desbloqueios-pendentes__item">
              <p>
                <strong>{pendente.guerreiro_nome ?? "Guerreiro(a)"}</strong> —{" "}
                {pendente.missao_titulo}
              </p>
              <p>Declarado em {formatarMomento(pendente.momento)}</p>
              <Botao
                onClick={() => julgar(pendente, true)}
                desabilitado={julgando === pendente.id}
              >
                Passou
              </Botao>
              <Botao
                variante="secundaria"
                onClick={() => julgar(pendente, false)}
                desabilitado={julgando === pendente.id}
              >
                Não passou
              </Botao>
            </li>
          ))}
        </ul>
      )}
    </Moldura>
  );
}
