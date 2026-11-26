import type { ColunaDaTabela } from "comum/react";
import { Botao, EstadoDaLista, Tabela } from "comum/react";
import type { ResponsavelDaLista } from "./api";

interface Props {
  responsaveis: ResponsavelDaLista[] | null;
  onRetomar: (responsavel: ResponsavelDaLista) => void;
}

const SEM_NICK = "Guerreiro(a) sem nick";
const SEM_NOME = "sem nome";

// Nick, nome e grau de parentesco de cada vinculado: o nick sozinho nem
// sempre diz quem é a criança (decisão do fundador, 2026-11-26). A ausência
// de um ou de outro é dita, e o vinculado nunca some da linha.
function textoDosVinculados(responsavel: ResponsavelDaLista): string {
  return responsavel.vinculados
    .map(
      (vinculado) =>
        `${vinculado.nick.trim() || SEM_NICK} — ${vinculado.nome.trim() || SEM_NOME} (${vinculado.grau_de_parentesco})`,
    )
    .join(" · ");
}

// A linha abre a retomada do vínculo, e o cadastro sem vínculo é sinalizado.
// É o caso que mais alcança o Mestre, que cadastra presencialmente no
// encontro e é justamente quem interrompe o cadastro antes de vincular
// (`RF-09-122`, design — decisão 4).
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
