import { listarCriacoes } from "../api/leituras";
import { ListaDeRegistros } from "../listas/ListaDeRegistros";
import { idDoAcervo, linhaDoAcervo } from "./linhaDoAcervo";

// O **portfólio** do `RF-03-08`, que é o acervo do documento 99 §6,
// invariante 5: cada item em **uma linha** (`linhaDoAcervo`), a mesma do
// portfólio da página do Guerreiro(a). A seção **mantém o nome** "Portfólio
// de criações originais" (decisão do fundador, 2026-11-04).
//
// As **três fontes** chegam na mesma lista, já ordenadas pelo núcleo: a
// comprovação aprovada do desafio prático, a criação da culminância e o
// registro aprovado da customização do kit (`RF-03-88`). Só
// aparece item com **aprovação do Mestre** e autorização vigente, portão que
// o núcleo aplica (`RN-03-41`, `RN-03-02`).
//
// A ordem é **decrescente** pela data de aprovação, e vem do núcleo
// (`RF-03-83`).
export function SecaoDoPortfolio() {
  return (
    <ListaDeRegistros
      carregando="Carregando o portfólio…"
      chave="vitrine/criacoes"
      falha="Não foi possível carregar o portfólio agora. Tente de novo."
      idDe={idDoAcervo}
      ler={listarCriacoes}
      linhaDe={linhaDoAcervo}
      rotulo="Portfólio de criações originais"
      vazio="Nenhuma criação original publicada por enquanto."
    />
  );
}
