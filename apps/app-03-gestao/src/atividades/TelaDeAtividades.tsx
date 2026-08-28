import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { type AtividadeAvulsa, listarAtividadesAvulsas } from "./api";
import { FormularioDeAtividadeAvulsa } from "./FormularioDeAtividadeAvulsa";

const RECUSA_POR_PAPEL = "Só o Admin acessa a área Atividades.";

// O cadastro da atividade avulsa, oferecido só ao Admin — o Mestre autora
// a atividade de trilha na App 09 (`RF-02-29`, PRD-02 §3.2).
export function TelaDeAtividades() {
  const { sessao, sair } = useSessao();
  const podeAcessar = sessao?.papel === "admin";

  const [atividades, definirAtividades] = useState<AtividadeAvulsa[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const itens = await listarAtividadesAvulsas(sessao.token);
      definirAtividades(itens);
    } catch {
      definirErro("Não foi possível carregar as atividades. Tente novamente em instantes.");
    }
  }, [sessao]);

  useEffect(() => {
    if (!podeAcessar) return;
    carregar();
  }, [podeAcessar, carregar]);

  const aoCadastrar = useCallback(
    async (_atividade: AtividadeAvulsa) => {
      await carregar();
    },
    [carregar],
  );

  if (!podeAcessar) {
    return (
      <Moldura>
        <Cabecalho titulo="Atividades" acao={{ rotulo: "Sair", aoAcionar: sair }} />
        <Aviso tipo="erro">{RECUSA_POR_PAPEL}</Aviso>
      </Moldura>
    );
  }

  return (
    <Moldura>
      <Cabecalho titulo="Atividades" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      <FormularioDeAtividadeAvulsa onCadastrada={aoCadastrar} />

      {atividades === null ? (
        <EstadoDaLista>Carregando as atividades…</EstadoDaLista>
      ) : atividades.length === 0 ? (
        <EstadoDaLista>Nenhuma atividade avulsa cadastrada ainda.</EstadoDaLista>
      ) : (
        <ul aria-label="Atividades avulsas cadastradas">
          {atividades.map((atividade) => (
            <li key={atividade.id}>{atividade.titulo}</li>
          ))}
        </ul>
      )}
    </Moldura>
  );
}
