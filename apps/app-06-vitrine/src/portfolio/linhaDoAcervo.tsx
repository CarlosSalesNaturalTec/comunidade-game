import { Avatar } from "comum/avatar";
import type { CriacaoPublica } from "../api/leituras";
import { FORMATADOR_DE_DATA } from "../guerreiros/carta";
import type { LinhaDeRegistro } from "../listas/ListaDeRegistros";
import { caminhoDoGuerreiro } from "../navegacao/recortes";
import { ProducaoDoAcervo } from "./ProducaoDoAcervo";

/** A **linha do acervo**, uma só para o portfólio da vitrine e para o da
 * página do Guerreiro(a) (`RF-03-85`, `RF-03-87`): o **título** como
 * identificação, a data em que o Mestre aprovou, a trilha — menos na criação
 * da culminância, em que o título já **é** o nome dela (`RN-03-43`) —, a
 * autoria por nick com o avatar de cada creditado, e a produção que **abre na
 * própria linha**.
 *
 * A linha **não** abre página: a criação original não tem página individual,
 * e são os **nicks** que abrem a de cada autor (`RF-03-03`). */
export function linhaDoAcervo(criacao: CriacaoPublica): LinhaDeRegistro {
  return {
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
  };
}

/** A chave estável de um item do acervo: o identificador só é único dentro
 * da fonte dele. */
export function idDoAcervo(criacao: CriacaoPublica): string {
  return `${criacao.fonte}-${criacao.id}`;
}
