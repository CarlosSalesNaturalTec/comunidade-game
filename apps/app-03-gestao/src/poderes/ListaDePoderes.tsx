import { Botao, EstadoDaLista } from "comum/react";
import "./ListaDePoderes.css";
import type { PoderDaLista } from "./api";
import { DesativarPoder } from "./DesativarPoder";

interface Props {
  poderes: PoderDaLista[] | null;
  podeGerenciar: boolean;
  aoEditar: (poder: PoderDaLista) => void;
  aoDesativar: () => void;
}

const ROTULO_DA_NATUREZA: Record<PoderDaLista["natureza"], string> = {
  de_guerreiro: "De guerreiro",
  derivado_do_aporte: "Derivado do aporte",
};

const ROTULO_DA_VIGENCIA: Record<PoderDaLista["vigencia"], string> = {
  vigente: "Vigente",
  ciclo_futuro: "Ciclo futuro",
};

// O poder desativado continua na lista, distinguido do ativo por rótulo
// textual, e a vigência distingue o poder do ciclo corrente do de ciclo
// futuro — nenhum dos dois se comunica só por cor (`RN-02-09`, `RN-02-21`).
// Lista densa do temperamento Operação (documento 15 §6).
export function ListaDePoderes({ poderes, podeGerenciar, aoEditar, aoDesativar }: Props) {
  if (poderes === null) {
    return <EstadoDaLista>Carregando poderes…</EstadoDaLista>;
  }

  if (poderes.length === 0) {
    return <EstadoDaLista>Nenhum poder cadastrado ainda.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-poderes" aria-label="Catálogo de Poderes">
      {poderes.map((poder) => (
        <li key={poder.id} className="lista-de-poderes__item">
          <div className="lista-de-poderes__linha">
            <span className="lista-de-poderes__nome">{poder.nome}</span>
            <span
              className={`lista-de-poderes__situacao lista-de-poderes__situacao--${
                poder.ativo ? "ativo" : "inativo"
              }`}
            >
              {poder.ativo ? "Ativo" : "Inativo"}
            </span>
            <span className="lista-de-poderes__natureza">
              {ROTULO_DA_NATUREZA[poder.natureza]}
            </span>
            <span className="lista-de-poderes__vigencia">
              {ROTULO_DA_VIGENCIA[poder.vigencia]}
            </span>
            {poder.papel && (
              <span className="lista-de-poderes__papel">Papel do Território</span>
            )}
            {poder.tecnico && <span className="lista-de-poderes__tecnico">Técnico</span>}
          </div>
          <p className="lista-de-poderes__descricao">{poder.descricao}</p>

          {podeGerenciar && (
            <div className="lista-de-poderes__acoes">
              <Botao variante="secundaria" onClick={() => aoEditar(poder)}>
                Editar
              </Botao>
              {poder.ativo && (
                <DesativarPoder idDoPoder={poder.id} onDesativado={aoDesativar} />
              )}
            </div>
          )}
        </li>
      ))}
    </ul>
  );
}
