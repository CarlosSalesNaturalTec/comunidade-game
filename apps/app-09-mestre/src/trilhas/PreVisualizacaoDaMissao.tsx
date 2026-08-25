import { Botao } from "comum/react";
import type { MissaoDaTrilha } from "./api";

interface Props {
  missao: MissaoDaTrilha;
  autorNome: string | null;
  onFechar: () => void;
}

// A licença é fixa, a mesma que a leitura pública da trilha já declara
// (documento 03 — código aberto e CC BY-SA); não é parâmetro de operação.
const LICENCA = "CC BY-SA";

// Apresenta o conteúdo e a bibliografia na mesma forma da leitura pública
// da trilha (`GET /v1/trilhas/{id}`) — o contrato que a App 05 vai
// consumir —, mas a partir do que já está em memória nesta sessão: a
// trilha ainda em rascunho não sai por aquela rota (`RF-09-04`), e a
// pré-visualização nunca grava nem publica nada (`RF-09-25`, design —
// Risks).
export function PreVisualizacaoDaMissao({ missao, autorNome, onFechar }: Props) {
  const conteudos = [...(missao.conteudos ?? [])].sort((a, b) => a.ordem - b.ordem);
  const bibliografia = missao.bibliografia ?? [];

  return (
    <section aria-label={`Pré-visualização de ${missao.titulo}`} className="cg-moldura">
      <h2>Pré-visualização — {missao.titulo}</h2>
      <p>
        Licença {LICENCA}
        {autorNome && <> · por {autorNome}</>}
      </p>

      {conteudos.length === 0 && <p>Nenhum conteúdo escrito ainda.</p>}
      <ul aria-label="Conteúdo da missão">
        {conteudos.map((conteudo) => (
          <li key={conteudo.id}>
            {conteudo.tipo === "texto" && <p>{conteudo.corpo}</p>}
            {conteudo.tipo === "link_externo" && (
              <a href={conteudo.endereco ?? "#"}>{conteudo.endereco}</a>
            )}
            {(conteudo.tipo === "imagem" ||
              conteudo.tipo === "video" ||
              conteudo.tipo === "arquivo") && (
              <p>{conteudo.referencia ? "Arquivo enviado." : "Envio ainda não concluído."}</p>
            )}
            {conteudo.autoria === "terceiro" && conteudo.fonte && (
              <p>Fonte: {conteudo.fonte}</p>
            )}
          </li>
        ))}
      </ul>

      <h3>Bibliografia</h3>
      {bibliografia.length === 0 && <p>Nenhuma bibliografia declarada ainda.</p>}
      <ul aria-label="Bibliografia da missão">
        {bibliografia.map((entrada) => (
          <li key={entrada.id}>
            {entrada.titulo} — {entrada.capitulo}
          </li>
        ))}
      </ul>

      <Botao onClick={onFechar}>Fechar pré-visualização</Botao>
    </section>
  );
}
