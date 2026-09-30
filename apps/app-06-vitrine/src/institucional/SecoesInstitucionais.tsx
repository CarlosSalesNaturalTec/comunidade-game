import { EstadoDaLista } from "comum/react";
import type { SecaoInstitucionalPublica } from "../api/leituras";
import { ListaDeNecessidades } from "../necessidades/ListaDeNecessidades";
import { TextoInstitucional } from "./TextoInstitucional";

// As três seções institucionais do PRD-03 §6.5. O texto e o vídeo vêm do que
// o núcleo devolve: **nenhum valor fica escrito aqui** — nem a chave PIX
// (`RF-03-46`). Seção que ainda não foi publicada diz isso, sem inventar
// conteúdo (design — decisão 6).
//
// A apresentação é **pura**: o institucional sai no documento servido
// (PRD-03 §10), e para isso o Astro renderiza `ApresentacaoDaSecao` no build
// com o que buscou ali. Quem ainda lê o institucional em tempo de visita é a
// porta do convite, pela chave PIX, e ela tem a sua própria leitura.

/** A seção já lida, apresentada. Não busca nada: serve ao render do build e ao
 * da ilha, e é o que faz o texto institucional existir no documento. */
export function ApresentacaoDaSecao({
  dado,
  nome,
}: {
  dado: SecaoInstitucionalPublica;
  nome: string;
}) {
  const { texto, video_url } = dado;
  return (
    <>
      {video_url !== null && (
        // Link, e nunca player embutido: o player de terceiro carregaria
        // recurso e cookie de fora ao abrir a página (`RF-03-51`, design —
        // decisão 5). O visitante decide sair.
        <p>
          <a href={video_url} target="_blank" rel="noopener noreferrer">
            Assistir ao vídeo de apresentação
          </a>
        </p>
      )}
      {texto === null ? (
        <EstadoDaLista>O conteúdo de “{nome}” ainda não foi publicado.</EstadoDaLista>
      ) : (
        <TextoInstitucional texto={texto} />
      )}
    </>
  );
}

/** As necessidades em aberto aparecem aqui **e** na porta do convite: quem
 * navega pela vitrine e não aciona a chamada também vê o que falta
 * (`RF-03-47`, design — decisão 8). É ilha: a lista muda a cada aporte, e
 * congelá-la na publicação mostraria necessidade já atendida. */
export function NecessidadesEmAberto() {
  return (
    <>
      <h3>Necessidades de recurso em aberto</h3>
      <ListaDeNecessidades />
    </>
  );
}
