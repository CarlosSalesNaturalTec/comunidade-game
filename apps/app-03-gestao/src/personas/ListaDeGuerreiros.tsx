import type { ColunaDaTabela } from "comum/react";
import { Botao, EstadoDaLista, Tabela } from "comum/react";
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

// Tabela densa do temperamento Operação (documento 15 §6). Nunca exibe
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

  function comVinculo(guerreiro: GuerreiroDaLista) {
    return Boolean(guerreiro.comunidade_virtual_id && guerreiro.vinculo_iniciado_em);
  }

  const colunas: ColunaDaTabela<GuerreiroDaLista>[] = [
    {
      chave: "nick",
      rotulo: "Nick",
      cabecalhoDeLinha: true,
      renderizar: (guerreiro) => guerreiro.nick,
    },
    {
      chave: "avatar",
      rotulo: "Avatar",
      recolhida: true,
      renderizar: () => "Avatar definido",
    },
    {
      chave: "comunidade",
      rotulo: "Comunidade",
      renderizar: (guerreiro) => {
        if (!comVinculo(guerreiro)) {
          return <EstadoDaLista>Ainda sem vínculo de comunidade.</EstadoDaLista>;
        }
        const comunidade = comunidades.find(
          (item) => item.id === guerreiro.comunidade_virtual_id,
        );
        return comunidade ? comunidade.nome : "Comunidade";
      },
    },
    {
      chave: "vinculo",
      rotulo: "Início do vínculo",
      recolhida: true,
      renderizar: (guerreiro) =>
        comVinculo(guerreiro) && guerreiro.vinculo_iniciado_em
          ? `Desde ${formatarData(guerreiro.vinculo_iniciado_em)}`
          : "—",
    },
    {
      chave: "acoes",
      rotulo: "Ações",
      renderizar: (guerreiro) => (
        <Botao variante="secundaria" onClick={() => onEditar(guerreiro)}>
          Editar
        </Botao>
      ),
    },
  ];

  return (
    <Tabela
      legenda="Guerreiros e Guerreiras"
      colunas={colunas}
      linhas={guerreiros}
      chaveDaLinha={(guerreiro) => guerreiro.id}
    />
  );
}
