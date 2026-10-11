import { listarRanking } from "../api/leituras";
import { ListaDeRegistros } from "../listas/ListaDeRegistros";
import { caminhoDoGuerreiro } from "../navegacao/recortes";

// O ranking público do `RF-03-09`: **só pontos regulares** e **só quem tem
// divulgação autorizada**, portão que o núcleo aplica (`RN-03-02`). Ponto
// extra, moeda e valor em reais não entram aqui (invariante 16 do documento
// 99 §6).
//
// Cada posição sai em **uma linha**, com avatar, nick, posição e pontos
// regulares, e a linha abre a página individual daquele Guerreiro(a)
// (`RF-03-03`). A ordem é a da posição, que o núcleo já devolve ordenada
// (`RF-03-83`). A linha não vai além de avatar e nick: nada mais de criança
// aparece aqui (invariantes 10 e 12 do documento 99 §6).
export function SecaoDoRanking() {
  return (
    <ListaDeRegistros
      ler={listarRanking}
      chave="vitrine/rankings"
      idDe={(item) => item.nick}
      linhaDe={(item) => ({
        avatar: item.avatar,
        identificacao: item.nick,
        destino: caminhoDoGuerreiro(item.nick),
        dados: (
          <>
            <span className="cg-ranking__posicao">{item.posicao}º</span> ·{" "}
            {item.pontos_regulares} pontos regulares
          </>
        ),
      })}
      rotulo="Ranking"
      carregando="Carregando o ranking…"
      falha="Não foi possível carregar o ranking agora. Tente de novo."
      vazio="Nenhuma posição publicada por enquanto."
    />
  );
}
