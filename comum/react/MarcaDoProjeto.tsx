import simboloColorido from "../marca/simbolo.svg?raw";
import simboloMono from "../marca/simbolo-mono.svg?raw";

// A marca do projeto no topo de cada aplicação: o **símbolo** e o nome em
// texto ao lado (documento 15 §§1, 5, princípios 3 e 6).
//
// É o **símbolo**, e nunca a marca horizontal: esta já traz o nome em curvas, e
// com o nome em texto ao lado o nome apareceria duas vezes. A horizontal serve
// vitrine, rodapé e documento (`marca/README.md` §1).
//
// O nome é **texto de verdade**, não imagem: quem não vê o símbolo lê o nome, e
// é o princípio 3 do documento 15 aplicado à própria marca.
//
// As duas versões são **embutidas no documento**, e não buscadas por `<img>`:
// a monocromática usa `currentColor` e só herda a cor do texto quando está no
// mesmo documento que ela. Vêm do arquivo, por `?raw`, para `comum/marca/`
// seguir sendo a fonte única — duplicar o traço aqui deixaria as duas cópias
// divergirem sem ninguém notar. O conteúdo é ativo versionado do próprio
// repositório, e `comum/marca.test.ts` garante que nenhum deles traz `<script>`.
//
// As duas são apresentadas sempre, e **o CSS escolhe**: a colorida no claro, a
// monocromática no escuro e sobre a foto de comunidade (documento 15 §6.3). A
// aplicação não decide — nenhuma delas pode esquecer de trocar.

interface Props {
  /** O destino do link, quando a marca leva à abertura da aplicação. Sem ele,
   * a marca é só apresentação e não é acionável. */
  href?: string;
}

export function MarcaDoProjeto({ href }: Props) {
  const conteudo = (
    <>
      <span
        className="cg-marca__simbolo cg-marca__simbolo--colorida"
        aria-hidden="true"
        // biome-ignore lint/security/noDangerouslySetInnerHtml: ativo versionado do próprio repositório, embutido para a monocromática herdar a cor do texto
        dangerouslySetInnerHTML={{ __html: simboloColorido }}
      />
      <span
        className="cg-marca__simbolo cg-marca__simbolo--mono"
        aria-hidden="true"
        // biome-ignore lint/security/noDangerouslySetInnerHtml: idem
        dangerouslySetInnerHTML={{ __html: simboloMono }}
      />
      <span className="cg-marca__nome">Comunidade Game</span>
    </>
  );

  return href === undefined ? (
    <div className="cg-marca">{conteudo}</div>
  ) : (
    <a className="cg-marca" href={href}>
      {conteudo}
    </a>
  );
}
