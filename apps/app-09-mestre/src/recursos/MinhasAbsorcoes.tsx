import { Aviso, EstadoDaLista } from "comum/react";
import type { AbsorcaoDoMestre } from "./api";

interface Props {
  absorcoes: AbsorcaoDoMestre[] | null;
  nomeDoTipoDeRecurso: (id: string) => string;
  nomeDoPontoDeApoio: (id: string) => string;
}

const ROTULO_DA_SITUACAO: Record<AbsorcaoDoMestre["situacao_de_ressarcimento"], string> = {
  em_aberto: "Ressarcimento em aberto",
  ressarcido: "Ressarcido",
  nao_se_aplica: "Não se aplica — absorção de serviço",
};

function formatarData(valor: string): string {
  const data = new Date(valor);
  if (Number.isNaN(data.getTime())) return valor;
  return data.toLocaleDateString("pt-BR");
}

// Somente leitura, do próprio Mestre: nenhuma ação de exigir, apressar,
// reordenar ou cancelar (`RF-09-59`). A situação "não se aplica" é
// apresentada como o que é — absorção de serviço —, nunca como pendência.
export function MinhasAbsorcoes({
  absorcoes,
  nomeDoTipoDeRecurso,
  nomeDoPontoDeApoio,
}: Props) {
  return (
    <section aria-label="Acompanhamento do ressarcimento">
      <Aviso tipo="andamento">
        A plataforma não guarda dado bancário. Havendo receita destinada a você, a chave PIX é
        enviada por e-mail ao Admin.
      </Aviso>

      {absorcoes === null && <EstadoDaLista>Carregando as absorções…</EstadoDaLista>}

      {absorcoes !== null && absorcoes.length === 0 && (
        <EstadoDaLista>Você ainda não absorveu nenhum recurso.</EstadoDaLista>
      )}

      {absorcoes !== null && absorcoes.length > 0 && (
        <ul className="minhas-absorcoes" aria-label="Absorções registradas">
          {absorcoes.map((absorcao) => (
            <li key={absorcao.id} className="minhas-absorcoes__item">
              <span className="minhas-absorcoes__tipo">
                {nomeDoTipoDeRecurso(absorcao.tipo_de_recurso_id)}
              </span>
              <span className="minhas-absorcoes__quantidade">{absorcao.quantidade}</span>
              <span className="minhas-absorcoes__ponto-de-apoio">
                {nomeDoPontoDeApoio(absorcao.ponto_de_apoio_id)}
              </span>
              <span className="minhas-absorcoes__valor">
                {absorcao.valor_em_moedas} moedas
              </span>
              <span className="minhas-absorcoes__data">
                {formatarData(absorcao.data_do_aporte)}
              </span>
              <span className="minhas-absorcoes__situacao">
                {ROTULO_DA_SITUACAO[absorcao.situacao_de_ressarcimento]}
              </span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
