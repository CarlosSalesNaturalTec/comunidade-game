import { listarApoiadores } from "../api/leituras";
import { ListaDeRegistros } from "../listas/ListaDeRegistros";
import { PREFIXO_DA_PAGINA_DO_APOIADOR } from "../navegacao/caminhos";

/** A seção **Apoiadores**: uma linha por Apoiador, com avatar, a
 * identificação exibida, o nível de sustento e o **total em moedas**, e a
 * linha abrindo a página individual dele (`RF-03-02`, `RF-03-03`,
 * `RF-03-10`).
 *
 * Quem não tem aporte homologado não chega aqui: o portão é do núcleo
 * (`RF-03-57`), e a tela não o anuncia com espaço vazio.
 *
 * A ordem é **alfabética** pela identificação exibida — **nunca** por valor,
 * que pódio de apoiador é proibido. É ela, com a ausência de posição e de
 * qualquer controle de ordenação, que impede o pódio (`RN-03-26`,
 * `RN-03-40`, `RN-14-38`). O valor sai sempre em moedas; reais nunca chegam
 * à vitrine (`RN-03-18`). */
export function SecaoDeApoiadores() {
  return (
    <ListaDeRegistros
      ler={listarApoiadores}
      chave="vitrine/apoiadores"
      idDe={(apoiador) => apoiador.id}
      linhaDe={(apoiador) => ({
        avatar: apoiador.avatar,
        identificacao: apoiador.identificacao.valor,
        destino: `${PREFIXO_DA_PAGINA_DO_APOIADOR}${encodeURIComponent(apoiador.id)}`,
        dados: `${apoiador.nome_do_nivel} · ${apoiador.total_em_moedas} moedas`,
      })}
      rotulo="Apoiadores"
      carregando="Carregando os Apoiadores…"
      falha="Não foi possível carregar os Apoiadores agora. Tente de novo."
      vazio="Nenhum Apoiador com aporte homologado por enquanto."
    />
  );
}
