import { ErroDaApi } from "comum/api";
import {
  Aviso,
  Botao,
  CartaDoPersonagem,
  cartaEstaCompleta,
  EstadoDaLista,
  PalcoDoPersonagem,
} from "comum/react";
import { type GuerreiroPublico, obterGuerreiroPorNick } from "../api/leituras";
import { ChamadaDeParticipacao } from "../convite/ChamadaDeParticipacao";
import { esperaEmLinguagemSimples } from "../formularios/espera";
import { useLeitura } from "../leitura/useLeitura";
import { navegarPara } from "../navegacao/navegar";
import { cartaDoGuerreiro, FORMATADOR_DE_DATA } from "./carta";

interface Props {
  nick: string;
  irPara?: (destino: string) => void;
}

/** Nick inexistente e nick sem autorização recebem **a mesma** tela, sem
 * revelar qual dos dois casos ocorreu (`RF-03-11`, `RN-03-07`, PRD-03
 * §§5.6, 5.7). */
const NAO_ENCONTRADO = "Não encontrado.";

export function PaginaDoGuerreiro({ nick, irPara = navegarPara }: Props) {
  const estado = useLeitura(() => obterGuerreiroPorNick(nick), `vitrine/guerreiros/${nick}`);

  return (
    <section className="cg-pagina-do-guerreiro" aria-label="Página pública">
      <Botao variante="secundaria" onClick={() => irPara("/")}>
        Voltar à vitrine
      </Botao>

      {estado.situacao === "carregando" && <EstadoDaLista>Carregando a página…</EstadoDaLista>}

      {estado.situacao === "falhou" && <RecusaDaLeitura erro={estado.erro} />}

      {estado.situacao === "pronta" && <Pagina guerreiro={estado.dado} irPara={irPara} />}
    </section>
  );
}

function RecusaDaLeitura({ erro }: { erro: unknown }) {
  if (erro instanceof ErroDaApi && erro.status === 404) {
    return <Aviso tipo="atencao">{NAO_ENCONTRADO}</Aviso>;
  }
  // O freio por origem é resposta esperada, não falha: a tela diz o motivo e
  // a espera em linguagem simples, e **não** pede CAPTCHA, cadastro nem
  // login (`RF-03-36`, `RF-03-37`, `RN-03-08`, design — decisão 8).
  if (erro instanceof ErroDaApi && erro.status === 429) {
    return (
      <Aviso tipo="atencao">
        Muitas consultas seguidas deste aparelho. {esperaEmLinguagemSimples(erro)}
      </Aviso>
    );
  }
  return <Aviso tipo="erro">Não foi possível carregar a página agora. Tente de novo.</Aviso>;
}

/** A página no **palco da Arena**: a carta é a apresentação e domina a tela, a
 * chamada é a decisão única, e o portfólio fica de apoio — abaixo e menor
 * (documento 15 §6). Voltar não entra no palco: é saída, e fica acima dele. */
function Pagina({
  guerreiro,
  irPara,
}: {
  guerreiro: GuerreiroPublico;
  irPara: (destino: string) => void;
}) {
  const dados = cartaDoGuerreiro(guerreiro);
  const criacoes = guerreiro.criacoes ?? [];

  return (
    <PalcoDoPersonagem
      rotulo={`Página de ${guerreiro.nick}`}
      // A chamada fecha a página individual que publica alguém (`RF-03-39`):
      // ela é do projeto, e nada do Guerreiro(a) visto viaja com ela
      // (`RF-03-41`). A tela de "não encontrado" não convida a nada, e por
      // isso ela só existe aqui, no ramo de leitura pronta.
      decisao={<ChamadaDeParticipacao irPara={irPara} />}
      apoio={
        <>
          <h3>Portfólio</h3>
          {criacoes.length === 0 ? (
            <EstadoDaLista>Nenhuma criação original validada ainda.</EstadoDaLista>
          ) : (
            <ul className="cg-portfolio">
              {criacoes.map((criacao) => (
                <li key={`${criacao.trilha}-${criacao.validada_em}`}>
                  <strong>{criacao.trilha}</strong> —{" "}
                  {FORMATADOR_DE_DATA.format(new Date(criacao.validada_em))}
                </li>
              ))}
            </ul>
          )}
        </>
      }
    >
      <h2>{guerreiro.nick}</h2>
      {cartaEstaCompleta(dados) ? (
        <CartaDoPersonagem dados={dados} />
      ) : (
        <EstadoDaLista>
          A leitura veio incompleta — a carta não é apresentada. O que há está abaixo.
        </EstadoDaLista>
      )}
    </PalcoDoPersonagem>
  );
}
