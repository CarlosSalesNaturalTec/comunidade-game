import { navegarPara } from "../navegacao/navegar";
import { BuscaPorNick } from "./BuscaPorNick";

interface Props {
  irPara?: (destino: string) => void;
}

/** A seção **Guerreiros e Guerreiras**: a **consulta por nick exato** e nada
 * mais. A vitrine não lista, não pagina e não rotaciona Guerreiros e
 * Guerreiras em seção alguma (`RF-03-12`, `RF-03-13`, `RN-03-06`).
 *
 * Quem tem divulgação autorizada segue público pelo **ranking** e pelo
 * **portfólio**, com a página individual a um clique, e por endereço direto —
 * que é o que o `RF-03-12` sempre permitiu.
 *
 * `GET /v1/vitrine/guerreiros` **permanece servida** pelo núcleo para quem
 * constrói sobre a API; a vitrine é que deixou de consumi-la, pelo mesmo
 * precedente de `/vitrine/poderes` (design — decisão 7). */
export function SecaoDeGuerreiros({ irPara = navegarPara }: Props) {
  return (
    <>
      <p>
        A vitrine não lista quem está cadastrado. A página de um Guerreiro ou de uma Guerreira
        se alcança pelo nick exato, pelo ranking e pelo nick de quem assina uma criação no
        portfólio.
      </p>
      <BuscaPorNick irPara={irPara} />
    </>
  );
}
