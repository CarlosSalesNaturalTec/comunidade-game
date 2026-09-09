import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { listarTiposDeRecurso, type TipoDeRecurso } from "../recursos/api";
import { listarTodosOsTiposDeColeta, type TipoDeColeta } from "./api";
import { FormularioDeTipoDeColeta } from "./FormularioDeTipoDeColeta";
import { FormularioDeTipoDeRecurso } from "./FormularioDeTipoDeRecurso";
import { ListaDeTiposDeColeta } from "./ListaDeTiposDeColeta";
import { ListaDeTiposDeRecurso } from "./ListaDeTiposDeRecurso";

// Área própria, ao lado de Poderes, e não dentro de Recursos ou Território:
// catálogo é bem comum da plataforma, não dado de comunidade — a mesma
// razão pela qual Poderes já é área própria. Por isso nenhum seletor de
// comunidade aparece aqui (`RF-02-107`, `RF-02-108`, design — decisão 1).
export function TelaDeCatalogos() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [tiposDeRecurso, definirTiposDeRecurso] = useState<TipoDeRecurso[] | null>(null);
  const [tiposDeColeta, definirTiposDeColeta] = useState<TipoDeColeta[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [formularioAberto, definirFormularioAberto] = useState<"recurso" | "coleta" | null>(
    null,
  );

  // Toda persona em sessão lê os catálogos; só o Admin escreve
  // (`RN-02-20`, `RF-01-28`).
  const podeGerenciar = sessao?.papel === "admin";

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const [recursos, coletas] = await Promise.all([
        listarTiposDeRecurso(sessao.token),
        listarTodosOsTiposDeColeta(sessao.token),
      ]);
      definirTiposDeRecurso(recursos);
      definirTiposDeColeta(coletas);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar os catálogos. Tente novamente em instantes.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const aoCriar = useCallback(async () => {
    definirFormularioAberto(null);
    await carregar();
  }, [carregar]);

  return (
    <Moldura>
      <Cabecalho titulo="Catálogos" />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      <section aria-labelledby="catalogo-de-tipos-de-recurso">
        <h3 id="catalogo-de-tipos-de-recurso">Tipos de recurso</h3>

        {podeGerenciar && formularioAberto === null && (
          <Botao onClick={() => definirFormularioAberto("recurso")}>
            Novo tipo de recurso
          </Botao>
        )}

        {podeGerenciar && formularioAberto === "recurso" && (
          <FormularioDeTipoDeRecurso
            onSalvo={aoCriar}
            onCancelar={() => definirFormularioAberto(null)}
          />
        )}

        <ListaDeTiposDeRecurso tipos={tiposDeRecurso} />
      </section>

      <section aria-labelledby="catalogo-de-tipos-de-coleta">
        <h3 id="catalogo-de-tipos-de-coleta">Tipos de coleta</h3>

        {podeGerenciar && formularioAberto === null && (
          <Botao onClick={() => definirFormularioAberto("coleta")}>Novo tipo de coleta</Botao>
        )}

        {podeGerenciar && formularioAberto === "coleta" && (
          <FormularioDeTipoDeColeta
            onSalvo={aoCriar}
            onCancelar={() => definirFormularioAberto(null)}
          />
        )}

        <ListaDeTiposDeColeta tipos={tiposDeColeta} />
      </section>
    </Moldura>
  );
}
