import { Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import {
  chaveDaNecessidade,
  listarNecessidadesEmAberto,
  type NecessidadeDeRecurso,
} from "./api";

function formatarDataDaAula(isoDeInicio: string | null, isoDeFim: string | null): string {
  if (isoDeInicio === null || isoDeFim === null) return "";
  const inicio = new Date(isoDeInicio);
  const fim = new Date(isoDeFim);
  if (Number.isNaN(inicio.getTime()) || Number.isNaN(fim.getTime())) return isoDeInicio;
  const data = inicio.toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
  const horaDeInicio = inicio.toLocaleTimeString("pt-BR", {
    hour: "2-digit",
    minute: "2-digit",
  });
  const horaDeFim = fim.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
  return `${data}, ${horaDeInicio}–${horaDeFim}`;
}

// As necessidades em aberto, com a atividade — o recurso, a data e o
// horário da aula, o ponto de apoio —, a comunidade e o que falta em
// moedas — na da recompensa de marco, a trilha no lugar da aula
// (`RF-07-54`) —, como o núcleo as publica: sem somar, reordenar nem recalcular
// (`RF-14-24`, `RN-14-09`).
export function TelaDeNecessidadesEmAberto() {
  const [necessidades, definirNecessidades] = useState<NecessidadeDeRecurso[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    listarNecessidadesEmAberto()
      .then(definirNecessidades)
      .catch(() => definirErro("Não foi possível carregar as necessidades. Tente novamente."));
  }, []);

  return (
    <Moldura>
      <Cabecalho titulo="Necessidades em aberto" />
      {erro && <p role="alert">{erro}</p>}
      {necessidades === null && !erro && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {necessidades !== null && necessidades.length === 0 && (
        <EstadoDaLista>Não há necessidade em aberto no momento.</EstadoDaLista>
      )}
      {necessidades?.map((necessidade) => (
        <article key={chaveDaNecessidade(necessidade)}>
          <p>
            {necessidade.tipo_de_recurso_nome} —{" "}
            {necessidade.especie === "aula"
              ? formatarDataDaAula(necessidade.inicio_em, necessidade.fim_em)
              : `Recompensa de marco da trilha ${necessidade.trilha_nome}`}{" "}
            — {necessidade.ponto_de_apoio_nome}
          </p>
          <p>{necessidade.comunidade_virtual_nome}</p>
          <p>
            Falta {necessidade.quantidade_faltante}
            {necessidade.valor_em_moedas != null
              ? ` — ${necessidade.valor_em_moedas} moedas`
              : " — sem valor de referência ainda"}
          </p>
        </article>
      ))}
    </Moldura>
  );
}
