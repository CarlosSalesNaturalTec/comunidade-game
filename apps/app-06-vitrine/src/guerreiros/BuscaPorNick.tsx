import { Botao, Campo } from "comum/react";
import { type FormEvent, useState } from "react";
import { navegarPara } from "../navegacao/navegar";

interface Props {
  irPara?: (destino: string) => void;
}

// Busca por **nick exato**: sem sugestão, sem completação e sem lista de
// nicks — é o que impede a varredura, junto do freio por origem
// (`RF-03-11`, `RF-03-12`, `RN-03-06`, PRD-03 §5.6).
//
// A busca **encaminha ao endereço** da página, e é a página que consulta: o
// nick inexistente e o nick sem autorização chegam assim à mesma tela de
// "não encontrado", pelo caminho da busca e pelo endereço direto
// (`RN-03-07`).
export function BuscaPorNick({ irPara = navegarPara }: Props) {
  const [nick, definirNick] = useState("");

  function aoEnviar(evento: FormEvent) {
    evento.preventDefault();
    const procurado = nick.trim();
    if (procurado.length === 0) return;
    irPara(`/guerreiros/${encodeURIComponent(procurado)}`);
  }

  return (
    <form className="cg-busca" onSubmit={aoEnviar} aria-label="Procurar por nick">
      <Campo rotulo="Nick exato" valor={nick} aoAlterar={definirNick} />
      <p className="cg-busca__ajuda">
        A busca aceita o nick exato, e não sugere nem completa nomes.
      </p>
      <Botao tipo="submit">Procurar</Botao>
    </form>
  );
}
