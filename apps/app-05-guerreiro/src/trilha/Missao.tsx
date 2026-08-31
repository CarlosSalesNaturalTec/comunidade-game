import { Aviso, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import {
  type MissaoNoPercurso,
  type MissaoPublica,
  obterTrilhaPublica,
  type TrilhaPublicaComMissoes,
} from "../api/trilha";
import { DesafioDeDesbloqueio } from "./DesafioDeDesbloqueio";
import { EntregaDaProducao } from "./EntregaDaProducao";
import { Sondagem } from "./Sondagem";

interface Props {
  trilhaId: string;
  missao: MissaoNoPercurso;
  aoDesbloquear: () => void;
}

function conteudoLegivel(conteudo: MissaoPublica["conteudos"][number]): string | null {
  if (conteudo.tipo === "texto") return conteudo.corpo;
  if (conteudo.tipo === "link_externo") return conteudo.endereco;
  return conteudo.referencia;
}

// Conteúdo e bibliografia da missão, na ordem do autor, com crédito e
// licença — vindos de `GET /v1/trilhas/{id}`, nunca duplicados na leitura
// do percurso (`RF-05-11`, `RF-05-12`, design — decisão 6). Missão
// bloqueada mostra o motivo, nunca cadeado mudo (`RF-05-10`).
export function Missao({ trilhaId, missao, aoDesbloquear }: Props) {
  const [trilhaPublica, definirTrilhaPublica] = useState<TrilhaPublicaComMissoes | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    let cancelado = false;
    obterTrilhaPublica(trilhaId)
      .then((resultado) => {
        if (!cancelado) definirTrilhaPublica(resultado);
      })
      .catch(() => {
        if (!cancelado) {
          definirErro(
            "Não foi possível carregar o conteúdo agora. Tente de novo em instantes.",
          );
        }
      });
    return () => {
      cancelado = true;
    };
  }, [trilhaId]);

  if (!missao.desbloqueada && !missao.e_proxima) {
    return (
      <Aviso tipo="atencao">
        Essa missão ainda está trancada. {missao.motivo_do_bloqueio}
      </Aviso>
    );
  }

  const missaoPublica = trilhaPublica?.missoes.find((item) => item.id === missao.id);

  return (
    <article aria-label={missao.titulo} className="cg-trilha__missao">
      <h2>{missao.titulo}</h2>
      {missao.obrigatoria === false && (
        <Aviso tipo="andamento">
          Essa missão é opcional — ela não conta no que falta para o próximo nível.
        </Aviso>
      )}

      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {!erro && missaoPublica === undefined && (
        <EstadoDaLista>Carregando o conteúdo da missão…</EstadoDaLista>
      )}

      {missaoPublica && (
        <>
          <ol className="cg-trilha__conteudos">
            {missaoPublica.conteudos
              .slice()
              .sort((a, b) => a.ordem - b.ordem)
              .map((conteudo) => (
                <li key={conteudo.id}>
                  {conteudoLegivel(conteudo)}
                  {conteudo.autoria === "terceiro" && conteudo.fonte && (
                    <span className="cg-trilha__credito"> — fonte: {conteudo.fonte}</span>
                  )}
                </li>
              ))}
          </ol>
          {trilhaPublica && (
            <p className="cg-trilha__credito">
              Crédito: {trilhaPublica.autor_nome ?? "Mestre autor"} — licença{" "}
              {trilhaPublica.licenca}
            </p>
          )}

          {missaoPublica.bibliografia.length > 0 && (
            <div className="cg-trilha__bibliografia">
              <h3>Bibliografia</h3>
              <ul>
                {missaoPublica.bibliografia.map((item) => (
                  <li key={item.id}>
                    {item.titulo} — {item.capitulo}
                    {item.disponivel === true && " (disponível no seu ponto de apoio)"}
                    {item.disponivel === false && " (sem exemplar no seu ponto de apoio)"}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}

      {missao.aguardando_mestre && (
        <Aviso tipo="andamento">
          Você declarou que cumpriu! Agora é só esperar o Mestre conferir.
        </Aviso>
      )}

      {missao.e_proxima &&
        !missao.aguardando_mestre &&
        missao.desafio_de_desbloqueio &&
        (missao.e_sondagem ? (
          <Sondagem
            missaoId={missao.id}
            desafio={missao.desafio_de_desbloqueio}
            aoResponder={aoDesbloquear}
          />
        ) : (
          <DesafioDeDesbloqueio
            missaoId={missao.id}
            desafio={missao.desafio_de_desbloqueio}
            aoDesbloquear={aoDesbloquear}
          />
        ))}

      {missao.desbloqueada && missaoPublica && (
        <EntregaDaProducao missaoId={missao.id} atividades={missaoPublica.atividades} />
      )}
    </article>
  );
}
