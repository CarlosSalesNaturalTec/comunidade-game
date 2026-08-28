import { EstadoDaLista } from "comum/react";
import type { AnotacaoDaFichaDeVida } from "./api";

interface Props {
  anotacoes: AnotacaoDaFichaDeVida[];
  nomePorId: Map<string, string>;
}

const ROTULO_DO_TEOR: Record<string, string> = {
  cuidado: "Cuidado",
  perda: "Perda",
  dano: "Dano",
};

// Da anotação mais antiga à mais recente, como o núcleo já devolve — sem
// caminho de editar nem de remover anotação gravada (`RF-02-53`,
// `RN-02-21`). O autor é Admin ou Mestre; sem `GET /v1/admins`, o Admin
// aparece pelo papel, não pelo nome (design — decisão 4).
export function FichaDeVida({ anotacoes, nomePorId }: Props) {
  if (anotacoes.length === 0) {
    return <EstadoDaLista>Ainda não há anotação na ficha de vida.</EstadoDaLista>;
  }

  return (
    <ul className="ficha-de-vida">
      {anotacoes.map((anotacao) => (
        <li key={anotacao.id} className="ficha-de-vida__item">
          <span className="ficha-de-vida__teor">
            {ROTULO_DO_TEOR[anotacao.teor] ?? anotacao.teor}
          </span>
          {" — "}
          {anotacao.estado_de_conservacao}
          {" — "}
          {nomePorId.get(anotacao.autor_id) ?? "Admin"}
          {" — "}
          <time dateTime={anotacao.registrado_em}>
            {new Date(anotacao.registrado_em).toLocaleString("pt-BR")}
          </time>
        </li>
      ))}
    </ul>
  );
}
