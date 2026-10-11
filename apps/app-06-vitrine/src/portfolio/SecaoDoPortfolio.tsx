import { Avatar } from "comum/avatar";
import { listarCriacoes } from "../api/leituras";
import { FORMATADOR_DE_DATA } from "../guerreiros/carta";
import { ListaDeRegistros } from "../listas/ListaDeRegistros";
import { caminhoDoGuerreiro } from "../navegacao/recortes";

// O portfólio do `RF-03-08`: cada criação em **uma linha**, com a **trilha**,
// a **data** e a **autoria por nick**, com o avatar de cada creditado. Sem
// título — a criação original não tem esse campo no modelo, e inventá-lo
// seria decisão nova (decisão do fundador, 2026-09-28). Só aparece criação
// cujos creditados têm autorização vigente, portão que o núcleo aplica
// (`RN-03-02`).
//
// A ordem é **decrescente** por data de validação, e vem do núcleo
// (`RF-03-83`).
//
// A linha **não** abre página: a criação original não tem página individual,
// e são os **nicks** que abrem a de cada autor (`RF-03-03`, design —
// decisão 3).
export function SecaoDoPortfolio() {
  return (
    <ListaDeRegistros
      ler={listarCriacoes}
      chave="vitrine/criacoes"
      idDe={(criacao) => `${criacao.trilha_id}-${criacao.validada_em}`}
      linhaDe={(criacao) => ({
        identificacao: criacao.trilha,
        dados: (
          <>
            {FORMATADOR_DE_DATA.format(new Date(criacao.validada_em))}
            <span className="cg-portfolio__autoria">
              {" · por "}
              {criacao.autores.map((autor) => (
                <a
                  key={autor.nick}
                  className="cg-portfolio__autor"
                  href={caminhoDoGuerreiro(autor.nick)}
                >
                  <Avatar avatar={autor.avatar} tamanho={24} />
                  {autor.nick}
                </a>
              ))}
            </span>
          </>
        ),
      })}
      rotulo="Portfólio de criações originais"
      carregando="Carregando o portfólio…"
      falha="Não foi possível carregar o portfólio agora. Tente de novo."
      vazio="Nenhuma criação original publicada por enquanto."
    />
  );
}
