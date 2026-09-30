import { PaginaDoApoiador } from "../adultos/PaginaDoApoiador";
import { PaginaDoMestre } from "../adultos/PaginaDoMestre";
import { PaginaDoGuerreiro } from "../guerreiros/PaginaDoGuerreiro";
import {
  apoiadorDoCaminho,
  comunidadeDoCaminho,
  mestreDoCaminho,
  nickDoCaminho,
} from "../navegacao/recortes";
import { PaginaDaComunidade } from "../territorio/PaginaDaComunidade";

/**
 * Monta, no aparelho, a página que o caminho pede. É o conteúdo da casca
 * `app.html`, e por isso decide pelo caminho: o documento servido é o mesmo
 * para todas as pessoas, e **nenhum perfil está nele** (`RF-03-13`,
 * `RF-03-14`, invariante 12 do documento 99).
 *
 * Também atende a comunidade criada depois da última publicação, que ainda não
 * tem arquivo próprio: o fallback do `firebase.json` a traz para cá.
 */
export function PaginaDePessoa() {
  const caminho = window.location.pathname;
  const nick = nickDoCaminho(caminho);
  if (nick !== null) return <PaginaDoGuerreiro nick={nick} />;

  const mestreId = mestreDoCaminho(caminho);
  if (mestreId !== null) return <PaginaDoMestre mestreId={mestreId} />;

  const apoiadorId = apoiadorDoCaminho(caminho);
  if (apoiadorId !== null) return <PaginaDoApoiador apoiadorId={apoiadorId} />;

  const comunidadeId = comunidadeDoCaminho(caminho);
  if (comunidadeId !== null) return <PaginaDaComunidade comunidadeId={comunidadeId} />;

  // Caminho que não é de nenhuma das quatro: a vitrine é pública e não tem
  // tela trancada, então não há para onde recusar — a saída é a raiz
  // (`RF-03-25`).
  return (
    <p>
      Endereço não encontrado. <a href="/">Voltar à vitrine</a>
    </p>
  );
}
