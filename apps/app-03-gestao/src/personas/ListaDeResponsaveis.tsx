import type { ColunaDaTabela } from "comum/react";
import { Botao, EstadoDaLista, Tabela } from "comum/react";
import type { ResponsavelDaLista } from "./api";

interface Props {
  responsaveis: ResponsavelDaLista[] | null;
  onRetomar: (responsavel: ResponsavelDaLista) => void;
  onEditar: (responsavel: ResponsavelDaLista) => void;
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

// Como o responsável entra: o e-mail da conta Google e o usuário da credencial
// de usuário e senha, ou a falta dos dois — nunca a senha (`RF-01-92`,
// decisão do fundador de 2026-11-27).
export function textoDoAcesso(responsavel: ResponsavelDaLista): string {
  const partes = [
    responsavel.email && `Google: ${responsavel.email}`,
    responsavel.usuario && `Usuário: ${responsavel.usuario}`,
  ].filter(Boolean);
  return partes.length > 0 ? partes.join(" · ") : "Sem acesso";
}

// Tabela densa do temperamento Operação (documento 15 §6), no padrão de
// `ListaDeAdultos`. A linha abre a retomada do vínculo, e o cadastro sem
// vínculo é sinalizado — é ele que a lista existe para revelar, porque até
// aqui um responsável cadastrado e não vinculado ficava inalcançável pela
// gestão (`RF-02-111`, design — decisões 6 e 8).
export function ListaDeResponsaveis({ responsaveis, onRetomar, onEditar }: Props) {
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
    {
      chave: "acesso",
      rotulo: "Acesso",
      renderizar: (responsavel) => textoDoAcesso(responsavel),
    },
    {
      chave: "ficha",
      rotulo: "Ficha",
      renderizar: (responsavel) => (
        <Botao variante="secundaria" onClick={() => onEditar(responsavel)}>
          Editar ficha
        </Botao>
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
