import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { type ComunidadeDaLista, listarComunidades } from "../comunidades/api";
import { type GuerreiroDaLista, listarGuerreiros } from "./api";
import { FormularioDeGuerreiro } from "./FormularioDeGuerreiro";
import { ListaDeGuerreiros } from "./ListaDeGuerreiros";

export function TelaDeGuerreiros() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [comunidades, definirComunidades] = useState<ComunidadeDaLista[]>([]);
  const [guerreiros, definirGuerreiros] = useState<GuerreiroDaLista[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [formulario, definirFormulario] = useState<"nenhum" | "novo" | GuerreiroDaLista>(
    "nenhum",
  );

  const podeCadastrar = sessao?.papel === "admin";

  useEffect(() => {
    listarComunidades()
      .then((pagina) => definirComunidades(pagina.itens))
      .catch(() => {
        definirErro("Não foi possível carregar as comunidades. Tente novamente em instantes.");
      });
  }, []);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const pagina = await listarGuerreiros(sessao.token);
      definirGuerreiros(pagina.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar os Guerreiros e Guerreiras. Tente novamente.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const aoSalvar = useCallback(async () => {
    definirFormulario("nenhum");
    await carregar();
  }, [carregar]);

  return (
    <div>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {podeCadastrar && formulario === "nenhum" && (
        <Botao onClick={() => definirFormulario("novo")}>Novo Guerreiro(a)</Botao>
      )}

      {podeCadastrar && formulario === "novo" && (
        <FormularioDeGuerreiro
          comunidades={comunidades}
          onSalvo={aoSalvar}
          onCancelar={() => definirFormulario("nenhum")}
        />
      )}

      {podeCadastrar && formulario !== "nenhum" && formulario !== "novo" && (
        <FormularioDeGuerreiro
          comunidades={comunidades}
          guerreiroExistente={formulario}
          onSalvo={aoSalvar}
          onCancelar={() => definirFormulario("nenhum")}
        />
      )}

      <ListaDeGuerreiros
        guerreiros={guerreiros}
        comunidades={comunidades}
        onEditar={(g) => definirFormulario(g)}
      />
    </div>
  );
}
