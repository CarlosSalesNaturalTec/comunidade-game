import { Botao, EstadoDaLista } from "comum/react";
import type { ComunidadeDaLista } from "../comunidades/api";
import type { GuerreiroDaLista } from "./api";

interface Props {
  guerreiros: GuerreiroDaLista[] | null;
  comunidades: ComunidadeDaLista[];
  onEditar: (guerreiro: GuerreiroDaLista) => void;
}

function formatarData(valorComFuso: string): string {
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return data.toLocaleDateString("pt-BR");
}

// Lista densa do temperamento Operação (documento 15 §6). Nunca exibe
// imagem real — só nick e avatar, a representação pública do Guerreiro(a)
// (`RN-02-22`, invariante 12 do documento 99 §6). A comunidade do vínculo
// vigente é leitura, sem caminho de troca — não há transferência no Ciclo
// 01 (`RF-02-15`, `RN-02-06`).
export function ListaDeGuerreiros({ guerreiros, comunidades, onEditar }: Props) {
  if (guerreiros === null) {
    return <EstadoDaLista>Carregando Guerreiros e Guerreiras…</EstadoDaLista>;
  }

  if (guerreiros.length === 0) {
    return <EstadoDaLista>Nenhum Guerreiro(a) cadastrado ainda.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-personas" aria-label="Guerreiros e Guerreiras">
      {guerreiros.map((guerreiro) => {
        const comunidade = comunidades.find(
          (item) => item.id === guerreiro.comunidade_virtual_id,
        );
        return (
          <li key={guerreiro.id} className="lista-de-personas__item">
            <span className="lista-de-personas__nome">{guerreiro.nick}</span>
            <span className="lista-de-personas__detalhe">Avatar definido</span>
            {guerreiro.comunidade_virtual_id && guerreiro.vinculo_iniciado_em ? (
              <span className="lista-de-personas__detalhe">
                {comunidade ? comunidade.nome : "Comunidade"} — desde{" "}
                {formatarData(guerreiro.vinculo_iniciado_em)}
              </span>
            ) : (
              <EstadoDaLista>Ainda sem vínculo de comunidade.</EstadoDaLista>
            )}
            <Botao variante="secundaria" onClick={() => onEditar(guerreiro)}>
              Editar
            </Botao>
          </li>
        );
      })}
    </ul>
  );
}
