import { EstadoDaLista } from "comum/react";
import type { NaturezaDoRecurso } from "../recursos/api";
import { ROTULO_DA_NATUREZA_DO_RECURSO, type TipoDeRecurso } from "../recursos/api";
import "./Catalogos.css";

interface Props {
  tipos: TipoDeRecurso[] | null;
}

// Lista densa do temperamento Operação (documento 15 §6). A rota devolve
// apenas o tipo com valor de referência vigente na data, e a aplicação não
// tem como distinguir "não existe" de "existe com vigência futura" — por
// isso o recorte é dito em texto, sempre, e não calculado
// (`RF-02-107`, `RF-07-02`, design — decisão 4).
export function ListaDeTiposDeRecurso({ tipos }: Props) {
  if (tipos === null) {
    return <EstadoDaLista>Carregando tipos de recurso…</EstadoDaLista>;
  }

  return (
    <>
      <EstadoDaLista>
        A lista traz os tipos com valor de referência vigente na data de hoje. Tipo cadastrado
        com vigência que começa adiante aparece a partir daquele dia.
      </EstadoDaLista>

      {tipos.length === 0 ? (
        <EstadoDaLista>Nenhum tipo de recurso cadastrado ainda.</EstadoDaLista>
      ) : (
        <ul className="catalogo" aria-label="Catálogo de tipos de recurso">
          {tipos.map((tipo) => (
            <li key={tipo.id} className="catalogo__item">
              <div className="catalogo__linha">
                <span className="catalogo__nome">{tipo.nome}</span>
                <span className="catalogo__marca">
                  {ROTULO_DA_NATUREZA_DO_RECURSO[tipo.natureza as NaturezaDoRecurso] ??
                    tipo.natureza}
                </span>
                <span className="catalogo__marca">Unidade: {tipo.unidade}</span>
                <span className="catalogo__marca">{tipo.valor_em_moedas} moedas</span>
                {tipo.exige_comprovante && (
                  <span className="catalogo__marca">Exige comprovante</span>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
