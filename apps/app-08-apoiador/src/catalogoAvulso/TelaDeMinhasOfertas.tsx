import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import { listarMinhasOfertas, type MinhaOfertaDeCatalogoAvulso } from "./api";

const RÓTULO_DA_SITUAÇÃO: Record<
  MinhaOfertaDeCatalogoAvulso["situacao_de_homologacao"],
  string
> = {
  nao_se_aplica: "Não se aplica",
  pendente: "Pendente de homologação",
  homologado: "Homologado",
  recusado: "Recusado",
};

// O acompanhamento do que o Apoiador ofertou, em qualquer situação: pendente,
// recusado com motivo, ativo com estoque restante e trocas, ou inativo com o
// que falta — sem nome, nick, avatar, aula, data de troca individual ou
// campo de contato (`RF-14-80`, `RF-14-81`, `RN-14-44`, `RF-14-59`).
export function TelaDeMinhasOfertas() {
  const { sessao } = useSessao();
  const [ofertas, definirOfertas] = useState<MinhaOfertaDeCatalogoAvulso[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    listarMinhasOfertas(sessao.token)
      .then(definirOfertas)
      .catch(() => definirErro("Não foi possível carregar suas ofertas. Tente novamente."));
  }, [sessao]);

  return (
    <Moldura>
      <Cabecalho titulo="Minhas ofertas" />
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {ofertas === null && !erro && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {ofertas !== null && ofertas.length === 0 && (
        <EstadoDaLista>Você ainda não ofertou nenhum item.</EstadoDaLista>
      )}
      {ofertas?.map((oferta) => (
        <article key={oferta.id} className="cg-cartao-de-oferta-de-catalogo-avulso">
          <p>
            <strong>{oferta.nome}</strong>
          </p>
          <p>
            <strong>Situação:</strong> {RÓTULO_DA_SITUAÇÃO[oferta.situacao_de_homologacao]}
          </p>
          {oferta.situacao_de_homologacao === "recusado" && oferta.homologacao_motivo && (
            <Aviso tipo="atencao">{oferta.homologacao_motivo}</Aviso>
          )}
          {oferta.ativo ? (
            <p>
              Ativo — estoque restante: {oferta.estoque}. Preço:{" "}
              {oferta.preco_em_pontos_extras} pontos extras. Trocas entregues:{" "}
              {oferta.quantidade_de_trocas}.
            </p>
          ) : (
            oferta.situacao_de_homologacao !== "pendente" &&
            oferta.situacao_de_homologacao !== "recusado" && (
              <Aviso tipo="atencao">
                {oferta.preco_de_referencia_ausente
                  ? "Ainda não há preço de referência vigente para este tipo de recurso."
                  : oferta.quantidade_faltante
                    ? `Faltam ${oferta.quantidade_faltante} unidades de lastro no ponto de apoio.`
                    : "Este item ainda não está ativo."}
              </Aviso>
            )
          )}
        </article>
      ))}
    </Moldura>
  );
}
