import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import {
  desativarTipoDeRecurso,
  excluirTipoDeRecurso,
  listarTiposDeRecurso,
  reativarTipoDeRecurso,
  type TipoDeRecurso,
} from "../recursos/api";
import { AcoesDoTipo } from "./AcoesDoTipo";
import {
  desativarTipoDeColeta,
  excluirTipoDeColeta,
  listarTodosOsTiposDeColeta,
  reativarTipoDeColeta,
  type TipoDeColeta,
} from "./api";
import { EdicaoDeTipoDeRecurso } from "./EdicaoDeTipoDeRecurso";
import { FormularioDeTipoDeColeta } from "./FormularioDeTipoDeColeta";
import { FormularioDeTipoDeRecurso } from "./FormularioDeTipoDeRecurso";
import { ListaDeTiposDeColeta } from "./ListaDeTiposDeColeta";
import { ListaDeTiposDeRecurso } from "./ListaDeTiposDeRecurso";

// O que está aberto em cada seção: nada, o cadastro, ou a edição de um tipo.
type Formulario =
  | null
  | { catalogo: "recurso"; tipo?: TipoDeRecurso }
  | { catalogo: "coleta"; tipo?: TipoDeColeta };

// Área própria, ao lado de Poderes, e não dentro de Recursos ou Território:
// catálogo é bem comum da plataforma, não dado de comunidade — a mesma
// razão pela qual Poderes já é área própria. Por isso nenhum seletor de
// comunidade aparece aqui (`RF-02-107`, `RF-02-108`, design — decisão 1).
export function TelaDeCatalogos() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [tiposDeRecurso, definirTiposDeRecurso] = useState<TipoDeRecurso[] | null>(null);
  const [tiposDeColeta, definirTiposDeColeta] = useState<TipoDeColeta[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [formulario, definirFormulario] = useState<Formulario>(null);

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

  const aoSalvar = useCallback(async () => {
    definirFormulario(null);
    await carregar();
  }, [carregar]);

  const fechar = () => definirFormulario(null);

  // Editar, Desativar/Reativar e Excluir em cada linha, só para o Admin
  // (`RF-02-113` a `RF-02-115`).
  const acoesDeRecurso = podeGerenciar
    ? (tipo: TipoDeRecurso) => (
        <AcoesDoTipo
          ativo={tipo.ativo}
          aoEditar={() => definirFormulario({ catalogo: "recurso", tipo })}
          desativar={(token) => desativarTipoDeRecurso(tipo.id, token)}
          reativar={(token) => reativarTipoDeRecurso(tipo.id, token)}
          excluir={(token) => excluirTipoDeRecurso(tipo.id, token)}
          aoAlterar={carregar}
        />
      )
    : undefined;

  const acoesDeColeta = podeGerenciar
    ? (tipo: TipoDeColeta) => (
        <AcoesDoTipo
          ativo={tipo.ativo}
          aoEditar={() => definirFormulario({ catalogo: "coleta", tipo })}
          desativar={(token) => desativarTipoDeColeta(tipo.id, token)}
          reativar={(token) => reativarTipoDeColeta(tipo.id, token)}
          excluir={(token) => excluirTipoDeColeta(tipo.id, token)}
          aoAlterar={carregar}
        />
      )
    : undefined;

  return (
    <Moldura>
      <Cabecalho titulo="Catálogos" />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      <section aria-labelledby="catalogo-de-tipos-de-recurso">
        <h3 id="catalogo-de-tipos-de-recurso">Tipos de recurso</h3>

        {podeGerenciar && formulario === null && (
          <Botao onClick={() => definirFormulario({ catalogo: "recurso" })}>
            Novo tipo de recurso
          </Botao>
        )}

        {podeGerenciar && formulario?.catalogo === "recurso" && !formulario.tipo && (
          <FormularioDeTipoDeRecurso onSalvo={aoSalvar} onCancelar={fechar} />
        )}

        {podeGerenciar && formulario?.catalogo === "recurso" && formulario.tipo && (
          <EdicaoDeTipoDeRecurso
            key={formulario.tipo.id}
            tipo={formulario.tipo}
            onSalvo={aoSalvar}
            onCancelar={fechar}
          />
        )}

        <ListaDeTiposDeRecurso tipos={tiposDeRecurso} acoes={acoesDeRecurso} />
      </section>

      <section aria-labelledby="catalogo-de-tipos-de-coleta">
        <h3 id="catalogo-de-tipos-de-coleta">Tipos de coleta</h3>

        {podeGerenciar && formulario === null && (
          <Botao onClick={() => definirFormulario({ catalogo: "coleta" })}>
            Novo tipo de coleta
          </Botao>
        )}

        {podeGerenciar && formulario?.catalogo === "coleta" && (
          <FormularioDeTipoDeColeta
            key={formulario.tipo?.id ?? "novo"}
            tipoEmEdicao={formulario.tipo}
            onSalvo={aoSalvar}
            onCancelar={fechar}
          />
        )}

        <ListaDeTiposDeColeta tipos={tiposDeColeta} acoes={acoesDeColeta} />
      </section>
    </Moldura>
  );
}
