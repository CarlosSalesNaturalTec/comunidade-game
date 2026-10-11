import { listarMestres } from "../api/leituras";
import { ListaDeRegistros } from "../listas/ListaDeRegistros";
import { PREFIXO_DA_PAGINA_DO_MESTRE } from "../navegacao/caminhos";

/** A seção **Mestres**: uma linha por Mestre, com avatar, a identificação
 * exibida e as áreas de habilidade, e a linha abrindo a página individual
 * dele em endereço próprio (`RF-03-02`, `RF-03-03`, `RF-03-07`).
 *
 * A ordem é **alfabética** pela identificação exibida, e vem do núcleo
 * (`RF-03-83`). O resto da carta — a prova pública, as trilhas de autoria e
 * as absorções — mora na página, como o documento 11 §8.2 manda. */
export function SecaoDeMestres() {
  return (
    <ListaDeRegistros
      ler={listarMestres}
      chave="vitrine/mestres"
      idDe={(mestre) => mestre.id}
      linhaDe={(mestre) => ({
        avatar: mestre.avatar,
        identificacao: mestre.identificacao.valor,
        destino: `${PREFIXO_DA_PAGINA_DO_MESTRE}${encodeURIComponent(mestre.id)}`,
        dados: mestre.areas_de_habilidade.join(", "),
      })}
      rotulo="Mestres"
      carregando="Carregando os Mestres…"
      falha="Não foi possível carregar os Mestres agora. Tente de novo."
      vazio="Nenhum Mestre publicado por enquanto."
    />
  );
}
