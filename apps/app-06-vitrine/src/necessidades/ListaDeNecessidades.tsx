import { Aviso, EstadoDaLista } from "comum/react";
import type { NecessidadePublica } from "../api/leituras";
import { useNecessidades } from "./useNecessidades";

// As necessidades de recurso em aberto das atividades sem lastro (`RF-03-47`).
// Lista, e não tabela: sete campos por necessidade não cabem em tabela no
// celular, e a vitrine é Mobile First (design — decisão 6).
//
// Tudo o que aparece vem do que o núcleo devolve — inclusive os nomes do tipo,
// da comunidade e do ponto de apoio. O valor sai em **moedas**, nunca em reais
// (`RF-03-10`, `RN-03-18`), e necessidade de tipo sem vigência de referência
// aparece sem valor: a vitrine não arbitra número nenhum.

const FORMATADOR_DE_HORARIO = new Intl.DateTimeFormat("pt-BR", {
  dateStyle: "short",
  timeStyle: "short",
});

function horario(valorComFuso: string): string {
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return FORMATADOR_DE_HORARIO.format(data);
}

function chaveDaNecessidade(necessidade: NecessidadePublica): string {
  return `${necessidade.aula_id}|${necessidade.tipo_de_recurso_id}`;
}

export function ListaDeNecessidades() {
  const estado = useNecessidades();

  if (estado.situacao === "carregando") {
    return <EstadoDaLista>Carregando as necessidades em aberto…</EstadoDaLista>;
  }
  if (estado.situacao === "falhou") {
    return (
      <Aviso tipo="erro">
        Não foi possível carregar as necessidades em aberto agora. Tente de novo.
      </Aviso>
    );
  }
  if (estado.dado.length === 0) {
    return (
      <EstadoDaLista>Nenhuma necessidade de recurso em aberto por enquanto.</EstadoDaLista>
    );
  }

  return (
    <ul className="cg-necessidades" aria-label="Necessidades de recurso em aberto">
      {estado.dado.map((necessidade) => (
        <li key={chaveDaNecessidade(necessidade)} className="cg-necessidades__item">
          <h4>{necessidade.tipo_de_recurso_nome}</h4>
          <p>Falta: {necessidade.quantidade_faltante}</p>
          <p>
            {necessidade.valor_em_moedas !== null
              ? `${necessidade.valor_em_moedas} moedas`
              : "Sem valor de referência vigente"}
          </p>
          <p>{necessidade.comunidade_virtual_nome}</p>
          <p>{necessidade.ponto_de_apoio_nome}</p>
          <p>
            Aula de {horario(necessidade.inicio_em)} a {horario(necessidade.fim_em)}
          </p>
        </li>
      ))}
    </ul>
  );
}
