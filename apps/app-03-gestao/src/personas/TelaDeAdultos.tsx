import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Dialogo } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { type AdultoDaLista, listarApoiadores, listarMestres } from "./api";
import { FichaDoAdulto } from "./FichaDoAdulto";
import { FormularioDeAdulto } from "./FormularioDeAdulto";
import { ListaDeAdultos } from "./ListaDeAdultos";

interface Props {
  papel: "mestre" | "apoiador";
}

const ROTULO_DO_PAPEL: Record<Props["papel"], string> = {
  mestre: "Mestre",
  apoiador: "Apoiador",
};

export function TelaDeAdultos({ papel }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [adultos, definirAdultos] = useState<AdultoDaLista[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);
  const [adultoNaFicha, definirAdultoNaFicha] = useState<AdultoDaLista | null>(null);

  const podeCadastrar = sessao?.papel === "admin";

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const listar = papel === "mestre" ? listarMestres : listarApoiadores;
      const pagina = await listar(sessao.token);
      definirAdultos(pagina.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar a lista. Tente novamente em instantes.");
    }
  }, [sessao, papel, tratarRecusaDeSessao]);

  useEffect(() => {
    definirAdultos(null);
    carregar();
  }, [carregar]);

  const aoCadastrar = useCallback(async () => {
    definirMostrarFormulario(false);
    await carregar();
  }, [carregar]);

  const aoGravarNick = useCallback(async () => {
    definirAdultoNaFicha(null);
    await carregar();
  }, [carregar]);

  return (
    <div>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {podeCadastrar && !mostrarFormulario && (
        <Botao onClick={() => definirMostrarFormulario(true)}>
          Novo {ROTULO_DO_PAPEL[papel]}
        </Botao>
      )}

      {podeCadastrar && mostrarFormulario && (
        <FormularioDeAdulto
          papel={papel}
          onSalvo={aoCadastrar}
          onCancelar={() => definirMostrarFormulario(false)}
        />
      )}

      <ListaDeAdultos adultos={adultos} onAbrirFicha={definirAdultoNaFicha} />

      <Dialogo
        aberto={adultoNaFicha !== null}
        titulo={adultoNaFicha ? `Ficha de ${adultoNaFicha.nome}` : ""}
        aoFechar={() => definirAdultoNaFicha(null)}
      >
        {adultoNaFicha && (
          <FichaDoAdulto adulto={adultoNaFicha} onNickGravado={aoGravarNick} />
        )}
      </Dialogo>
    </div>
  );
}
