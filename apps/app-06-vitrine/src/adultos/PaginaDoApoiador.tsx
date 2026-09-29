import { ErroDaApi } from "comum/api";
import {
  Aviso,
  Botao,
  CartaDoPersonagem,
  cartaEstaCompleta,
  EstadoDaLista,
} from "comum/react";
import { type ApoiadorPublico, obterApoiadorPorId } from "../api/leituras";
import { ChamadaDeParticipacao } from "../convite/ChamadaDeParticipacao";
import { useLeitura } from "../leitura/useLeitura";
import { cartaDoApoiador } from "./cartas";
import { ProvaPublica } from "./ProvaPublica";

interface Props {
  apoiadorId: string;
  irPara: (destino: string) => void;
}

/** Apoiador sem aporte homologado, persona de outro papel e identificador
 * inexistente recebem **a mesma** tela: o núcleo devolve o mesmo 404 nos três
 * casos (`RF-03-57`, `RN-03-01`). */
const NAO_ENCONTRADO = "Não encontrado.";

export function PaginaDoApoiador({ apoiadorId, irPara }: Props) {
  const estado = useLeitura(
    () => obterApoiadorPorId(apoiadorId),
    `vitrine/apoiadores/${apoiadorId}`,
  );

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

      {estado.situacao === "pronta" && <Pagina apoiador={estado.dado} />}

      {estado.situacao === "pronta" && <ChamadaDeParticipacao irPara={irPara} />}
    </section>
  );
}

function Pagina({ apoiador }: { apoiador: ApoiadorPublico }) {
  const dados = cartaDoApoiador(apoiador);

  return (
    <>
      <h2>{apoiador.identificacao.valor}</h2>
      {cartaEstaCompleta(dados) ? (
        <CartaDoPersonagem dados={dados} />
      ) : (
        <EstadoDaLista>
          A leitura veio incompleta — a carta não é apresentada. O que há está abaixo.
        </EstadoDaLista>
      )}

      {/* Aportes sempre em moedas da plataforma, nunca em reais
          (`RF-03-10`, `RN-03-18`). */}
      <h3>Aportes</h3>
      <p>{apoiador.total_em_moedas} moedas</p>

      <h3>Nível de sustento e selos</h3>
      <p>
        Nível {apoiador.nivel_de_sustento} — {apoiador.nome_do_nivel}
      </p>
      {apoiador.selos.length === 0 ? (
        <EstadoDaLista>Nenhum selo ainda.</EstadoDaLista>
      ) : (
        <ul className="cg-selos-do-apoiador">
          {apoiador.selos.map((selo) => (
            <li key={`${selo.familia}-${selo.nome}`}>{selo.nome}</li>
          ))}
        </ul>
      )}

      <h3>Desafios extras propostos</h3>
      {apoiador.desafios_propostos.length === 0 ? (
        <EstadoDaLista>Nenhum desafio publicado ainda.</EstadoDaLista>
      ) : (
        <ul className="cg-desafios-do-apoiador">
          {apoiador.desafios_propostos.map((desafio) => (
            // Trilha, período e contagem. Quem concluiu **não** aparece, e o
            // direcionado não se abre (`RF-03-80`, `RN-03-37`).
            <li key={`${desafio.trilha}-${desafio.periodo_inicio}`}>
              <strong>{desafio.trilha}</strong> — de {desafio.periodo_inicio} a{" "}
              {desafio.periodo_fim} —{" "}
              {desafio.concluiram === 1 ? "1 concluiu" : `${desafio.concluiram} concluíram`}
            </li>
          ))}
        </ul>
      )}

      <ProvaPublica artefatos={apoiador.artefatos} />
    </>
  );
}
