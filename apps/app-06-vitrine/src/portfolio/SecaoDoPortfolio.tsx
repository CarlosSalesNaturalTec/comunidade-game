import { Aviso, EstadoDaLista } from "comum/react";
import { listarCriacoes } from "../api/leituras";
import { FORMATADOR_DE_DATA } from "../guerreiros/carta";
import { useLeitura } from "../leitura/useLeitura";

// O portfólio do `RF-03-08`: cada criação com a **trilha**, a **data** e a
// **autoria por nick**. Sem título — a criação original não tem esse campo
// no modelo, e inventá-lo seria decisão nova (decisão do fundador,
// 2026-09-28). Só aparece criação cujos creditados têm autorização vigente,
// portão que o núcleo aplica (`RN-03-02`).
export function SecaoDoPortfolio() {
  const estado = useLeitura(listarCriacoes, "vitrine/criacoes");

  if (estado.situacao === "carregando") {
    return <EstadoDaLista>Carregando o portfólio…</EstadoDaLista>;
  }
  if (estado.situacao === "falhou") {
    return (
      <Aviso tipo="erro">Não foi possível carregar o portfólio agora. Tente de novo.</Aviso>
    );
  }
  if (estado.dado.itens.length === 0) {
    return <EstadoDaLista>Nenhuma criação original publicada por enquanto.</EstadoDaLista>;
  }

  return (
    <ul className="cg-portfolio">
      {estado.dado.itens.map((criacao) => (
        <li key={`${criacao.trilha_id}-${criacao.validada_em}`}>
          <strong>{criacao.trilha}</strong> —{" "}
          {FORMATADOR_DE_DATA.format(new Date(criacao.validada_em))}
          <span className="cg-portfolio__autoria">
            {" "}
            · por {criacao.autores.map((autor) => autor.nick).join(", ")}
          </span>
        </li>
      ))}
    </ul>
  );
}
