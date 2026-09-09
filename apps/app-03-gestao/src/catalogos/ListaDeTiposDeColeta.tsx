import { EstadoDaLista } from "comum/react";
import { ROTULO_DA_FORMA_DE_REGISTRO, type TipoDeColeta } from "./api";
import "./Catalogos.css";

interface Props {
  tipos: TipoDeColeta[] | null;
}

// Lista densa do temperamento Operação (documento 15 §6). O tipo
// desativado segue na lista, distinguido por rótulo textual e nunca só por
// cor: é o que o núcleo já recusa em desafio novo (`RF-02-108`,
// `RF-08-06`).
export function ListaDeTiposDeColeta({ tipos }: Props) {
  if (tipos === null) {
    return <EstadoDaLista>Carregando tipos de coleta…</EstadoDaLista>;
  }

  if (tipos.length === 0) {
    return <EstadoDaLista>Nenhum tipo de coleta cadastrado ainda.</EstadoDaLista>;
  }

  return (
    <ul className="catalogo" aria-label="Catálogo de tipos de coleta">
      {tipos.map((tipo) => (
        <li key={tipo.id} className="catalogo__item">
          <div className="catalogo__linha">
            <span className="catalogo__nome">{tipo.nome}</span>
            <span
              className={`catalogo__situacao catalogo__situacao--${
                tipo.ativo ? "ativo" : "inativo"
              }`}
            >
              {tipo.ativo ? "Ativo" : "Inativo"}
            </span>
            <span className="catalogo__marca">
              {ROTULO_DA_FORMA_DE_REGISTRO[tipo.forma_de_registro] ?? tipo.forma_de_registro}
            </span>
            {tipo.unidade && <span className="catalogo__marca">Unidade: {tipo.unidade}</span>}
            {tipo.faixa_minima !== null && tipo.faixa_maxima !== null && (
              <span className="catalogo__marca">
                Faixa: {tipo.faixa_minima} a {tipo.faixa_maxima}
              </span>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
}
