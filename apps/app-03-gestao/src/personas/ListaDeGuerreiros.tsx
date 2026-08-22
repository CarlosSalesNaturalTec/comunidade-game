import { Botao, EstadoDaLista } from "comum/react";
import type { GuerreiroDaLista } from "./api";

interface Props {
  guerreiros: GuerreiroDaLista[] | null;
  onEditar: (guerreiro: GuerreiroDaLista) => void;
}

// Lista densa do temperamento Operação (documento 15 §6). Nunca exibe
// imagem real — só nick e avatar, a representação pública do Guerreiro(a)
// (`RN-02-22`, invariante 12 do documento 99 §6).
export function ListaDeGuerreiros({ guerreiros, onEditar }: Props) {
  if (guerreiros === null) {
    return <EstadoDaLista>Carregando Guerreiros e Guerreiras…</EstadoDaLista>;
  }

  if (guerreiros.length === 0) {
    return <EstadoDaLista>Nenhum Guerreiro(a) cadastrado ainda.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-personas" aria-label="Guerreiros e Guerreiras">
      {guerreiros.map((guerreiro) => (
        <li key={guerreiro.id} className="lista-de-personas__item">
          <span className="lista-de-personas__nome">{guerreiro.nick}</span>
          <span className="lista-de-personas__detalhe">Avatar definido</span>
          <Botao variante="secundaria" onClick={() => onEditar(guerreiro)}>
            Editar
          </Botao>
        </li>
      ))}
    </ul>
  );
}
