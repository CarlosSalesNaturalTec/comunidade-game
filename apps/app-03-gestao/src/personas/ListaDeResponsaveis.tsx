import type { ColunaDaTabela } from "comum/react";
import { Botao, EstadoDaLista, Tabela } from "comum/react";
import type { ResponsavelDaLista } from "./api";

interface Props {
  responsaveis: ResponsavelDaLista[] | null;
  onRetomar: (responsavel: ResponsavelDaLista) => void;
}

const SEM_NICK = "Guerreiro(a) sem nick";

function textoDosVinculados(responsavel: ResponsavelDaLista): string {
  return responsavel.vinculados
    .map(
      (vinculado) => `${vinculado.nick.trim() || SEM_NICK} (${vinculado.grau_de_parentesco})`,
    )
    .join(" · ");
}

// Tabela densa do temperamento Operação (documento 15 §6), no padrão de
// `ListaDeAdultos`. A linha abre a retomada do vínculo, e o cadastro sem
// vínculo é sinalizado — é ele que a lista existe para revelar, porque até
// aqui um responsável cadastrado e não vinculado ficava inalcançável pela
// gestão (`RF-02-111`, design — decisões 6 e 8).
export function ListaDeResponsaveis({ responsaveis, onRetomar }: Props) {
  if (responsaveis === null) {
    return <EstadoDaLista>Carregando…</EstadoDaLista>;
  }

  if (responsaveis.length === 0) {
    return <EstadoDaLista>Nenhum responsável cadastrado ainda.</EstadoDaLista>;
  }

  const colunas: ColunaDaTabela<ResponsavelDaLista>[] = [
    {
      chave: "nome",
      rotulo: "Nome",
      cabecalhoDeLinha: true,
      renderizar: (responsavel) => (
        <Botao variante="secundaria" onClick={() => onRetomar(responsavel)}>
          {responsavel.nome}
        </Botao>
      ),
    },
    {
      chave: "vinculados",
      rotulo: "Guerreiros e Guerreiras vinculados",
      renderizar: (responsavel) =>
        responsavel.vinculados.length === 0 ? (
          <EstadoDaLista>Sem Guerreiro(a) vinculado — cadastro por concluir.</EstadoDaLista>
        ) : (
          textoDosVinculados(responsavel)
        ),
    },
  ];

  return (
    <Tabela
      legenda="Responsáveis cadastrados"
      colunas={colunas}
      linhas={responsaveis}
      chaveDaLinha={(responsavel) => responsavel.id}
    />
  );
}
