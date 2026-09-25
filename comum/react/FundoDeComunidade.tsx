import type { ReactNode } from "react";

// A **imagem de comunidade ao fundo** das telas da Arena (documento 15 §6.3):
// a foto da própria comunidade registrada na plataforma, atrás da cor chapada.
//
// Três garantias, e são elas que a distinguem de decoração:
//
// 1. **Nada se perde quando a imagem não carrega** (princípio 3, documento 15
//    §5). Por isso ela é `aria-hidden` com `alt` vazio: não é conteúdo, não
//    entra na árvore de acessibilidade e não carrega significado sozinha. Some
//    a imagem — rede fora, preferência do aparelho —, e a tela continua
//    dizendo tudo o que dizia.
// 2. **Os pisos de contraste do §3.3 continuam medidos sobre ela.** Texto,
//    componente, borda que informa e estado de foco nunca compõem com a
//    fotografia: quem os carrega se apoia numa **cor chapada opaca** — a
//    superfície dos tokens —, e é contra ela que o `4,5:1` e o `3:1` são
//    medidos, exatamente como em tela sem fundo nenhum. A foto aparece ao
//    redor e atrás dessas superfícies, nunca sob o texto. Nenhum valor de
//    transparência entra aqui: opacidade parcial devolveria a medida do
//    contraste à fotografia, que muda a cada comunidade.
// 3. **Sem imagem, só a cor chapada.** Comunidade que não escolheu foto não
//    ganha fundo nenhum — e a tela é exatamente a mesma.
//
// O peso do arquivo responde ao princípio 4 do documento 15 (celular modesto):
// `loading="lazy"` e `decoding="async"` tiram a foto do caminho crítico, e ela
// nunca atrasa o que a tela comunica.

interface Props {
  /** O endereço da foto registrada da comunidade, servido pelo núcleo.
   * `null` — comunidade sem foto escolhida — deixa só a cor chapada. */
  imagem: string | null;
  children: ReactNode;
}

export function FundoDeComunidade({ imagem, children }: Props) {
  return (
    <div className="cg-fundo-de-comunidade">
      {imagem && (
        <img
          className="cg-fundo-de-comunidade__imagem"
          src={imagem}
          alt=""
          aria-hidden="true"
          loading="lazy"
          decoding="async"
        />
      )}
      <div className="cg-fundo-de-comunidade__conteudo">{children}</div>
    </div>
  );
}
