import { EstadoDaLista } from "comum/react";
import type { DesafioExtraDoGuerreiro } from "../api/desafiosEEquipes";

interface Props {
  extras: DesafioExtraDoGuerreiro[];
}

const ROTULO_DO_FORMATO: Record<string, string> = {
  presencial: "Presencial",
  on_line: "On-line",
};

function formatarData(valor: string): string {
  const data = new Date(valor);
  if (Number.isNaN(data.getTime())) return valor;
  return data.toLocaleDateString("pt-BR");
}

// Os desafios extras vigentes e elegíveis ao Guerreiro(a), apartados dos
// semanais — recompensa, quantidade, vigência e critério, em linguagem da
// criança. Leitura apenas: nenhuma ação de concluir, disputar, comprar ou
// trocar nasce daqui (`RF-05-20`, `RF-05-21`, `RN-05-18`, `RN-05-06`).
export function MeusDesafiosExtras({ extras }: Props) {
  if (extras.length === 0) {
    return <EstadoDaLista>Você não tem nenhum desafio extra disponível agora.</EstadoDaLista>;
  }

  return (
    <ul className="cg-lista-de-desafios-extras">
      {extras.map((extra) => {
        const esgotado = extra.quantidade_restante <= 0;
        return (
          <li
            key={extra.id}
            className={
              esgotado
                ? "cg-cartao-de-desafio-extra cg-cartao-de-desafio-extra--esgotado"
                : "cg-cartao-de-desafio-extra"
            }
          >
            <p className="cg-cartao-de-desafio-extra__origem">
              {extra.trilha_nome}
              {extra.missao_titulo ? ` — ${extra.missao_titulo}` : ""}
            </p>
            <h3>
              {extra.recompensa.tipo_de_recurso_nome} em {extra.recompensa.ponto_de_apoio_nome}
            </h3>
            {esgotado && (
              <p className="cg-cartao-de-desafio-extra__esgotado">
                As recompensas deste desafio já acabaram.
              </p>
            )}
            <p>
              <strong>Como conquistar:</strong> {extra.criterio_de_atribuicao}
            </p>
            <p>
              <strong>Como fazer:</strong> {ROTULO_DO_FORMATO[extra.formato] ?? extra.formato}
            </p>
            <p>
              <strong>Vale de:</strong> {formatarData(extra.vigencia_inicio)} até{" "}
              {formatarData(extra.vigencia_fim)}
            </p>
            <p>
              <strong>Recompensas:</strong> {extra.quantidade_restante} de{" "}
              {extra.quantidade_disponivel} ainda disponíveis
            </p>
            {extra.modalidade === "direcionado" && (
              <p className="cg-cartao-de-desafio-extra__direcionado">
                Este desafio foi feito especialmente para você.
              </p>
            )}
            <p className="cg-cartao-de-desafio-extra__pontos">
              {extra.pontos_extras} pontos extras — não contam para o seu nível na trilha.
            </p>
          </li>
        );
      })}
    </ul>
  );
}
