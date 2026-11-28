import { Botao, EstadoDaLista } from "comum/react";
import { useState } from "react";
import "./ListaDeComunidades.css";
import type { ComunidadeDaLista, ContornoDaComunidade } from "./api";
import { FormularioDeContorno } from "./FormularioDeContorno";

interface Props {
  comunidades: ComunidadeDaLista[] | null;
  /** Só o Admin cadastra ou substitui o contorno (`RF-02-122`, PRD-02 §4). */
  podeGravarContorno?: boolean;
  onContornoGravado?: () => void;
}

function formatarData(iso: string): string {
  return new Date(iso).toLocaleDateString("pt-BR");
}

// Origem, data e atribuição saem como o núcleo as devolve; a ausência de
// contorno é informação, nunca erro (`RF-02-122`, `RN-08-31`).
function SituacaoDoContorno({ contorno }: { contorno: ContornoDaComunidade | null }) {
  if (contorno === null) {
    return <EstadoDaLista>Ainda sem contorno.</EstadoDaLista>;
  }
  return (
    <span className="lista-de-comunidades__contorno">
      Contorno de {contorno.origem_osm}, copiado em {formatarData(contorno.copiado_em)} ·{" "}
      {contorno.credito} · {contorno.licenca}
    </span>
  );
}

// Comunidade abaixo do piso de coletores aparece sem os indicadores do
// território, e a ausência deles nunca é apresentada como falha
// (`RF-08-30`, `RF-08-31`, `RN-08-28`). Lista densa do temperamento
// Operação (documento 15 §6).
export function ListaDeComunidades({
  comunidades,
  podeGravarContorno = false,
  onContornoGravado,
}: Props) {
  const [contornoAberto, definirContornoAberto] = useState<string | null>(null);

  if (comunidades === null) {
    return <EstadoDaLista>Carregando comunidades…</EstadoDaLista>;
  }

  if (comunidades.length === 0) {
    return <EstadoDaLista>Nenhuma Comunidade Virtual cadastrada ainda.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-comunidades" aria-label="Comunidades Virtuais">
      {comunidades.map((comunidade) => {
        const contorno = comunidade.contorno ?? null;
        const temContorno = contorno !== null;
        return (
          <li key={comunidade.id} className="lista-de-comunidades__item">
            <span className="lista-de-comunidades__nome">{comunidade.nome}</span>
            <span className="lista-de-comunidades__localizacao">{comunidade.localizacao}</span>
            {comunidade.registros_validos === null ? (
              <EstadoDaLista>Ainda sem indicadores do território.</EstadoDaLista>
            ) : (
              <span className="lista-de-comunidades__indicadores">
                {comunidade.series_ativas} séries ativas · {comunidade.registros_validos}{" "}
                registros válidos
              </span>
            )}
            <SituacaoDoContorno contorno={contorno} />
            {podeGravarContorno && contornoAberto !== comunidade.id && (
              <Botao
                variante="secundaria"
                onClick={() => definirContornoAberto(comunidade.id)}
              >
                {temContorno ? "Substituir contorno" : "Cadastrar contorno"}
              </Botao>
            )}
            {podeGravarContorno && contornoAberto === comunidade.id && (
              <div className="lista-de-comunidades__formulario">
                <FormularioDeContorno
                  idDaComunidade={comunidade.id}
                  nomeDaComunidade={comunidade.nome}
                  substituindo={temContorno}
                  onGravado={() => {
                    definirContornoAberto(null);
                    onContornoGravado?.();
                  }}
                  onCancelar={() => definirContornoAberto(null)}
                />
              </div>
            )}
          </li>
        );
      })}
    </ul>
  );
}
