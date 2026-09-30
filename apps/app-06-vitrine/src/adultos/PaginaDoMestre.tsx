import { ErroDaApi } from "comum/api";
import {
  Aviso,
  Botao,
  CartaDoPersonagem,
  cartaEstaCompleta,
  EstadoDaLista,
  PalcoDoPersonagem,
} from "comum/react";
import { type MestrePublico, obterMestrePorId } from "../api/leituras";
import { ChamadaDeParticipacao } from "../convite/ChamadaDeParticipacao";
import { useLeitura } from "../leitura/useLeitura";
import { navegarPara } from "../navegacao/navegar";
import { cartaDoMestre } from "./cartas";
import { ProvaPublica } from "./ProvaPublica";

interface Props {
  mestreId: string;
  irPara?: (destino: string) => void;
}

/** Identificador inexistente e persona de outro papel recebem **a mesma**
 * tela: o núcleo devolve o mesmo 404 nos dois casos (`RN-03-01`). */
const NAO_ENCONTRADO = "Não encontrado.";

export function PaginaDoMestre({ mestreId, irPara = navegarPara }: Props) {
  const estado = useLeitura(() => obterMestrePorId(mestreId), `vitrine/mestres/${mestreId}`);

  return (
    <section className="cg-pagina-do-guerreiro" aria-label="Página pública">
      <Botao variante="secundaria" onClick={() => irPara("/")}>
        Voltar à vitrine
      </Botao>

      {estado.situacao === "carregando" && <EstadoDaLista>Carregando a página…</EstadoDaLista>}

      {estado.situacao === "falhou" &&
        (estado.erro instanceof ErroDaApi && estado.erro.status === 404 ? (
          <Aviso tipo="atencao">{NAO_ENCONTRADO}</Aviso>
        ) : (
          <Aviso tipo="erro">Não foi possível carregar a página agora. Tente de novo.</Aviso>
        ))}

      {estado.situacao === "pronta" && <Pagina mestre={estado.dado} irPara={irPara} />}
    </section>
  );
}

/** A página no **palco da Arena**: a carta é a apresentação e domina a
 * tela, a chamada é a decisão única, e o resto fica de apoio — abaixo e
 * menor (documento 15 §6). Voltar não entra no palco: é saída. */
function Pagina({
  mestre,
  irPara,
}: {
  mestre: MestrePublico;
  irPara: (destino: string) => void;
}) {
  const dados = cartaDoMestre(mestre);

  return (
    <PalcoDoPersonagem
      rotulo={`Página de ${mestre.identificacao.valor}`}
      // A chamada fecha toda página individual que publica alguém
      // (`RF-03-39`), e nada de quem estava sendo visto viaja com ela
      // (`RF-03-41`).
      decisao={<ChamadaDeParticipacao irPara={irPara} />}
      apoio={<Apoio mestre={mestre} />}
    >
      <h2>{mestre.identificacao.valor}</h2>
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

/** O que a página ainda comunica depois da decisão, abaixo e menor que a
 * carta — é o campo que o palco tem para isso. */
function Apoio({ mestre }: { mestre: MestrePublico }) {
  return (
    <>
      <h3>Habilidades</h3>
      {mestre.areas_de_habilidade.length === 0 ? (
        <EstadoDaLista>Nenhuma trilha publicada ainda.</EstadoDaLista>
      ) : (
        <ul className="cg-areas-do-mestre">
          {mestre.areas_de_habilidade.map((area) => (
            <li key={area}>{area}</li>
          ))}
        </ul>
      )}

      <h3>Trilhas de autoria</h3>
      {mestre.trilhas_de_autoria.length === 0 ? (
        <EstadoDaLista>Nenhuma trilha publicada ainda.</EstadoDaLista>
      ) : (
        <ul className="cg-trilhas-do-mestre">
          {mestre.trilhas_de_autoria.map((trilha) => (
            <li key={trilha.id}>
              <strong>{trilha.nome}</strong> — {trilha.area_do_conhecimento}
            </li>
          ))}
        </ul>
      )}

      <ProvaPublica artefatos={mestre.artefatos} />

      <h3>Sustentou atividade sem recurso</h3>
      <p>{mestre.absorcoes === 1 ? "1 vez" : `${mestre.absorcoes} vezes`}</p>
    </>
  );
}
