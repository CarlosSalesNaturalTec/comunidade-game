import { EstadoDaLista } from "comum/react";
import "./Territorio.css";
import type { DesafioPublicadoDaLista } from "./api";

interface Props {
  desafios: DesafioPublicadoDaLista[] | null;
}

const ROTULO_DA_CADENCIA: Record<string, string> = {
  diaria: "Diária",
  semanal: "Semanal",
  mensal: "Mensal",
};

function formatarData(valorComFuso: string): string {
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return data.toLocaleDateString("pt-BR");
}

// Leitura de acompanhamento: nenhum caminho de criar, editar ou apagar
// desafio — a autoria é do Mestre na App 09 (`RF-02-17`, PRD-02 §3.2).
// Desafio sem série é informação, nunca falha.
export function ListaDeDesafiosPublicados({ desafios }: Props) {
  if (desafios === null) {
    return <EstadoDaLista>Carregando os desafios de coleta…</EstadoDaLista>;
  }

  if (desafios.length === 0) {
    return <EstadoDaLista>Nenhum desafio de coleta publicado ainda.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-desafios-publicados" aria-label="Desafios de coleta publicados">
      {desafios.map((desafio) => (
        <li key={desafio.id} className="lista-de-desafios-publicados__item">
          <span className="lista-de-desafios-publicados__nome">
            {desafio.tipo_de_coleta.nome}
          </span>
          <span>{ROTULO_DA_CADENCIA[desafio.cadencia] ?? desafio.cadencia}</span>
          <span>
            {formatarData(desafio.vigencia_inicio)} – {formatarData(desafio.vigencia_fim)}
          </span>
          <span>{desafio.quantidade_de_series_ativas} série(s) ativa(s)</span>
        </li>
      ))}
    </ul>
  );
}
