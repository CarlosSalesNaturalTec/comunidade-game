import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import { formatarMoedas } from "../compartilhado/escada";
import { type AporteDeclarado, listarMinhasDeclaracoesDeAporte } from "./api";

const RÓTULO_DA_SITUAÇÃO: Record<AporteDeclarado["situacao"], string> = {
  pendente: "Pendente",
  homologada: "Homologada",
  recusada: "Recusada",
};

const RÓTULO_DA_ORIGEM: Record<AporteDeclarado["origem_da_escolha"], string> = {
  necessidade: "Necessidade publicada",
  valor_sugerido: "Valor sugerido",
  valor_livre: "Valor livre",
};

function formatarData(isoDeData: string): string {
  const data = new Date(isoDeData);
  return Number.isNaN(data.getTime())
    ? isoDeData
    : data.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric" });
}

// A situação de cada declaração do Apoiador em sessão — pendente,
// homologada ou recusada com motivo —, em moedas: esta não é a tela em que
// se declara a transferência. Sem edição, reenvio ou ato algum sobre a
// situação: a mudança é da gestão (`RF-14-27`, `RN-14-08`).
export function TelaDeSituacaoDasDeclaracoes() {
  const { sessao } = useSessao();
  const [declaracoes, definirDeclaracoes] = useState<AporteDeclarado[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    listarMinhasDeclaracoesDeAporte(sessao.token)
      .then(definirDeclaracoes)
      .catch(() =>
        definirErro("Não foi possível carregar suas declarações. Tente novamente."),
      );
  }, [sessao]);

  return (
    <Moldura>
      <Cabecalho titulo="Situação das declarações" />
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {declaracoes === null && !erro && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {declaracoes !== null && declaracoes.length === 0 && (
        <EstadoDaLista>Você ainda não declarou nenhum aporte.</EstadoDaLista>
      )}
      {declaracoes?.map((declaracao) => (
        <article key={declaracao.id} className="cg-cartao-de-declaracao">
          <p>
            <strong>Situação:</strong> {RÓTULO_DA_SITUAÇÃO[declaracao.situacao]}
          </p>
          <p>
            {formatarData(declaracao.registrado_em)} —{" "}
            {formatarMoedas(Number(declaracao.valor_declarado))} —{" "}
            {RÓTULO_DA_ORIGEM[declaracao.origem_da_escolha]}
          </p>
          {declaracao.situacao === "recusada" && declaracao.motivo_da_recusa && (
            <Aviso tipo="atencao">{declaracao.motivo_da_recusa}</Aviso>
          )}
        </article>
      ))}
    </Moldura>
  );
}
