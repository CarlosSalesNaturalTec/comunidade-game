import { Aviso, EstadoDaLista } from "comum/react";
import { useEffect } from "react";
import type { ChaveDeSecaoInstitucional } from "../api/leituras";
import { ListaDeNecessidades } from "../necessidades/ListaDeNecessidades";
import { TextoInstitucional } from "./TextoInstitucional";
import { useConteudoInstitucional } from "./useConteudoInstitucional";

// As três seções institucionais do PRD-03 §6.5. O texto e o vídeo vêm do que
// o núcleo devolve: **nenhum valor fica escrito aqui** — nem a chave PIX
// (`RF-03-46`). Seção que ainda não foi publicada diz isso, sem inventar
// conteúdo (design — decisão 6).

function ConteudoDaSecao({
  secao,
  nome,
  aoChegar,
}: {
  secao: ChaveDeSecaoInstitucional;
  nome: string;
  aoChegar?: () => void;
}) {
  const estado = useConteudoInstitucional(secao);
  const publicada = estado.situacao === "pronta" && estado.dado.texto !== null;

  // biome-ignore lint/correctness/useExhaustiveDependencies: só a chegada do texto dispara.
  useEffect(() => {
    if (publicada) aoChegar?.();
  }, [publicada]);

  if (estado.situacao === "carregando") return <EstadoDaLista>Carregando…</EstadoDaLista>;
  if (estado.situacao === "falhou") {
    return (
      <Aviso tipo="erro">Não foi possível carregar esta seção agora. Tente de novo.</Aviso>
    );
  }
  const { texto, video_url } = estado.dado;
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

/** Leva a nota de transparência, que o texto reescrito por IA aponta pela
 * âncora do endereço, ao foco quando o conteúdo chega (`RF-03-48`). */
function irParaAAncoraDoEndereco() {
  const id = decodeURIComponent(window.location.hash.slice(1));
  if (id === "") return;
  const alvo = document.getElementById(id);
  if (alvo === null) return;
  alvo.scrollIntoView?.();
  alvo.focus();
}

export function SecaoQuemSomos() {
  return (
    <ConteudoDaSecao secao="quem-somos" nome="Quem somos" aoChegar={irParaAAncoraDoEndereco} />
  );
}

export function SecaoContatos() {
  return <ConteudoDaSecao secao="contatos" nome="Contatos" />;
}

export function SecaoComoApoiar() {
  return (
    <>
      <ConteudoDaSecao secao="como-apoiar" nome="Como apoiar" />
      {/* As necessidades em aberto aparecem aqui **e** na porta do convite: quem
          navega pela vitrine e não aciona a chamada também vê o que falta
          (`RF-03-47`, design — decisão 8). */}
      <h3>Necessidades de recurso em aberto</h3>
      <ListaDeNecessidades />
    </>
  );
}
