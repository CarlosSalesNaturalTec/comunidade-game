import { Botao, EstadoDaLista } from "comum/react";
import { useState } from "react";
import type { AdultoDaLista } from "./api";
import { FormularioDeNick } from "./FormularioDeNick";

interface Props {
  adultos: AdultoDaLista[] | null;
  onNickGravado: () => void;
}

// Sinaliza quem está sem nick e oferece o caminho de gravá-lo — sem nunca
// sugerir um (`RF-02-01`, `RN-14-10`). Lista densa do temperamento Operação
// (documento 15 §6).
export function ListaDeAdultos({ adultos, onNickGravado }: Props) {
  const [emEdicaoDeNick, definirEmEdicaoDeNick] = useState<string | null>(null);

  if (adultos === null) {
    return <EstadoDaLista>Carregando…</EstadoDaLista>;
  }

  if (adultos.length === 0) {
    return <EstadoDaLista>Nenhum cadastro ainda.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-personas" aria-label="Adultos cadastrados">
      {adultos.map((adulto) => (
        <li key={adulto.id} className="lista-de-personas__item">
          <span className="lista-de-personas__nome">{adulto.nome}</span>
          <span className="lista-de-personas__detalhe">{adulto.email}</span>

          {adulto.nick === null ? (
            <>
              <EstadoDaLista>Sem nick — não aparece em superfície pública.</EstadoDaLista>
              {emEdicaoDeNick === adulto.id ? (
                <FormularioDeNick
                  personaId={adulto.id}
                  onGravado={() => {
                    definirEmEdicaoDeNick(null);
                    onNickGravado();
                  }}
                  onCancelar={() => definirEmEdicaoDeNick(null)}
                />
              ) : (
                <Botao variante="secundaria" onClick={() => definirEmEdicaoDeNick(adulto.id)}>
                  Gravar nick
                </Botao>
              )}
            </>
          ) : (
            <span className="lista-de-personas__nick">{adulto.nick}</span>
          )}
        </li>
      ))}
    </ul>
  );
}
