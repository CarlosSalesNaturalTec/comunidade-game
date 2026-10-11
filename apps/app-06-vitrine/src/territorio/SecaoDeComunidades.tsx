import { listarComunidades } from "../api/leituras";
import { ListaDeRegistros } from "../listas/ListaDeRegistros";
import { caminhoDaComunidade } from "../navegacao/recortes";

// A seção **Comunidades Virtuais** do `RF-03-02`: uma linha por comunidade,
// **sem avatar**, com nome, localização e quantos Guerreiros e Guerreiras
// estão vinculados, e a linha abrindo a página da comunidade em endereço
// próprio (`RF-03-15`).
//
// A **representação visual** do território é da página, nunca da linha
// (documento 11 §8.3): é lá que a série é lida, e nenhuma foto de comunidade
// existe na plataforma.
//
// A comunidade abaixo do piso de coletores chega com os quatro indicadores
// nulos — e **continua na lista**, com o que a leitura devolveu: a linha não
// depende de indicador nenhum.
//
// Uma **única** leitura monta a página inteira: uma consulta por comunidade
// cairia no freio por origem (design — Decisão 7).
export function SecaoDeComunidades() {
  return (
    <ListaDeRegistros
      ler={listarComunidades}
      chave="comunidades"
      idDe={(comunidade) => comunidade.id}
      linhaDe={(comunidade) => ({
        identificacao: comunidade.nome,
        destino: caminhoDaComunidade(comunidade.id),
        dados: `${comunidade.localizacao} · ${comunidade.guerreiros_vinculados} Guerreiros e Guerreiras vinculados`,
      })}
      rotulo="Comunidades Virtuais"
      carregando="Carregando as Comunidades Virtuais…"
      falha="Não foi possível carregar as comunidades agora. Tente de novo."
      vazio="Nenhuma Comunidade Virtual publicada por enquanto."
      depoisDaLista={(dado) => (
        <p className="cg-comunidades__ciclo">Ciclo corrente: {dado.ciclo_rotulo}</p>
      )}
    />
  );
}
