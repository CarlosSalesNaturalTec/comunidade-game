import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import { TelaDeEvolucao } from "../evolucao/TelaDeEvolucao";
import { type GuerreiroVinculado, listarMeusGuerreiros } from "./api";

// A lista dos vinculados, cada um com o grau de parentesco, e a alternância
// entre eles como estado da própria aplicação — sem nova entrada e sem
// encerrar a sessão (`RF-13-04`, `RF-13-05`, `RN-13-04`). Nenhuma tela de
// cadastro de responsável ou de vínculo existe aqui: tudo isso é ato da
// gestão (`RF-13-06`).
export function TelaDeVinculados() {
  const { sessao } = useSessao();
  const [guerreiros, definirGuerreiros] = useState<GuerreiroVinculado[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [selecionadoId, definirSelecionadoId] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    listarMeusGuerreiros(sessao.token)
      .then((lista) => {
        definirGuerreiros(lista);
        definirSelecionadoId((atual) => atual ?? lista[0]?.id ?? null);
      })
      .catch(() => definirErro("Não foi possível carregar seus vinculados. Tente novamente."));
  }, [sessao]);

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
      {selecionado && <TelaDeEvolucao guerreiro={selecionado} />}
    </Moldura>
  );
}
