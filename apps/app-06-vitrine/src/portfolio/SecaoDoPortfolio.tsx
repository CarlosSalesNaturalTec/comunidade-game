import { Avatar } from "comum/avatar";
import { listarCriacoes } from "../api/leituras";
import { FORMATADOR_DE_DATA } from "../guerreiros/carta";
import { ListaDeRegistros } from "../listas/ListaDeRegistros";
import { caminhoDoGuerreiro } from "../navegacao/recortes";
import { ProducaoDoAcervo } from "./ProducaoDoAcervo";

// O **portfólio** do `RF-03-08`, que é o acervo do documento 99 §6,
// invariante 5: cada item em **uma linha**, com o **título** como
// identificação, a data em que o Mestre aprovou, a autoria por nick com o
// avatar de cada creditado, e a produção que **abre na própria linha**
// (`RF-03-84`, `RF-03-85`). A seção **mantém o nome** "Portfólio de criações
// originais" (decisão do fundador, 2026-11-04).
//
// As **duas fontes** chegam na mesma lista, já ordenadas pelo núcleo: a
// comprovação aprovada do desafio prático e a criação da culminância. Só
// aparece item com **aprovação do Mestre** e autorização vigente, portão que
// o núcleo aplica (`RN-03-41`, `RN-03-02`).
//
// A **trilha** sai ao lado da data, menos na criação da culminância, em que o
// título já **é** o nome dela — repeti-lo seria dizer duas vezes a mesma
// coisa (`RN-03-43`, design — decisão 4).
//
// A ordem é **decrescente** pela data de aprovação, e vem do núcleo
// (`RF-03-83`).
//
// A linha **não** abre página: a criação original não tem página individual,
// e são os **nicks** que abrem a de cada autor (`RF-03-03`, design —
// decisão 3).
export function SecaoDoPortfolio() {
  return (
    <ListaDeRegistros
      carregando="Carregando o portfólio…"
      chave="vitrine/criacoes"
      falha="Não foi possível carregar o portfólio agora. Tente de novo."
      idDe={(criacao) => `${criacao.fonte}-${criacao.id}`}
      ler={listarCriacoes}
      linhaDe={(criacao) => ({
        identificacao: criacao.titulo,
        dados: (
          <>
            {FORMATADOR_DE_DATA.format(new Date(criacao.validada_em))}
            {criacao.fonte !== "criacao_original" && (
              <span className="cg-portfolio__trilha">
                {" · "}
                {criacao.trilha}
              </span>
            )}
            <span className="cg-portfolio__autoria">
              {" · por "}
              {criacao.autores.map((autor) => (
                <a
                  className="cg-portfolio__autor"
                  href={caminhoDoGuerreiro(autor.nick)}
                  key={autor.nick}
                >
                  <Avatar avatar={autor.avatar} tamanho={24} />
                  {autor.nick}
                </a>
              ))}
            </span>
            <ProducaoDoAcervo item={criacao} />
          </>
        ),
      })}
      rotulo="Portfólio de criações originais"
      vazio="Nenhuma criação original publicada por enquanto."
    />
  );
}
