import { Aviso, EstadoDaLista } from "comum/react";
import { lerCoberturaDeOds } from "../api/leituras";
import { useLeitura } from "../leitura/useLeitura";
import { DestaqueDaMeta1718 } from "./DestaqueDaMeta1718";

// O painel de cobertura da Agenda 2030 do `RF-03-22`: agregado por
// **comunidade** e por **ciclo**, com o rótulo do ciclo a que os números se
// referem. Nenhuma etiqueta aparece ligada a um Guerreiro(a) — a rota não
// oferece esse recorte e a tela não o monta (`RF-03-24`, `RN-03-19`).
export function SecaoDaCobertura() {
  const estado = useLeitura(lerCoberturaDeOds, "vitrine/ods/cobertura");

  if (estado.situacao === "carregando") {
    return <EstadoDaLista>Carregando a cobertura da Agenda 2030…</EstadoDaLista>;
  }
  if (estado.situacao === "falhou") {
    return (
      <Aviso tipo="erro">Não foi possível carregar a cobertura agora. Tente de novo.</Aviso>
    );
  }
  if (estado.dado.length === 0) {
    return (
      <EstadoDaLista>
        Nenhuma comunidade tocou um objetivo da Agenda 2030 neste ciclo ainda.
      </EstadoDaLista>
    );
  }

  return (
    <div className="cg-cobertura">
      <ul className="cg-cobertura__comunidades">
        {estado.dado.map((linha) => (
          <li key={linha.comunidade_id}>
            <h3>{linha.comunidade_nome}</h3>
            <p>Ciclo {linha.ciclo}</p>
            <p>Objetivos cobertos: {linha.objetivos.join(", ")}</p>
          </li>
        ))}
      </ul>
      <DestaqueDaMeta1718 />
    </div>
  );
}
