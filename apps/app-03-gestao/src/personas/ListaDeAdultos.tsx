import type { ColunaDaTabela } from "comum/react";
import { Botao, EstadoDaLista, Tabela } from "comum/react";
import type { AdultoDaLista } from "./api";

interface Props {
  adultos: AdultoDaLista[] | null;
  onAbrirFicha: (adulto: AdultoDaLista) => void;
}

function textoDeArtefatos(adulto: AdultoDaLista): string {
  const quantidade = adulto.artefatos.length;
  if (quantidade === 0) return "Nenhum artefato";
  return quantidade === 1 ? "1 artefato" : `${quantidade} artefatos`;
}

// Tabela densa do temperamento Operação (documento 15 §6). A linha abre a
// ficha de leitura com a prova do cadastro; sinaliza quem está sem nick e
// deixa o caminho de gravá-lo para a ficha (`RF-02-01`, `RN-14-10`).
export function ListaDeAdultos({ adultos, onAbrirFicha }: Props) {
  if (adultos === null) {
    return <EstadoDaLista>Carregando…</EstadoDaLista>;
  }

  if (adultos.length === 0) {
    return <EstadoDaLista>Nenhum cadastro ainda.</EstadoDaLista>;
  }

  const colunas: ColunaDaTabela<AdultoDaLista>[] = [
    {
      chave: "nome",
      rotulo: "Nome",
      cabecalhoDeLinha: true,
      renderizar: (adulto) => (
        <Botao variante="secundaria" onClick={() => onAbrirFicha(adulto)}>
          {adulto.nome}
        </Botao>
      ),
    },
    {
      chave: "email",
      rotulo: "E-mail",
      recolhida: true,
      renderizar: (adulto) => adulto.email,
    },
    {
      chave: "nick",
      rotulo: "Nick",
      renderizar: (adulto) =>
        adulto.nick === null ? (
          <EstadoDaLista>Sem nick — não aparece em superfície pública.</EstadoDaLista>
        ) : (
          adulto.nick
        ),
    },
    {
      chave: "artefatos",
      rotulo: "Artefatos",
      recolhida: true,
      renderizar: textoDeArtefatos,
    },
  ];

  return (
    <Tabela
      legenda="Adultos cadastrados"
      colunas={colunas}
      linhas={adultos}
      chaveDaLinha={(adulto) => adulto.id}
    />
  );
}
