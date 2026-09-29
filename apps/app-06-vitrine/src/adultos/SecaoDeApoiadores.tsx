import { type ApoiadorPublico, listarApoiadores } from "../api/leituras";
import { PREFIXO_DA_PAGINA_DO_APOIADOR } from "../navegacao/caminhos";
import { cartaDoApoiador } from "./cartas";
import { SecaoDeAdultos } from "./SecaoDeAdultos";

interface Props {
  irPara: (destino: string) => void;
}

/** Quem não tem aporte homologado não chega aqui: o portão é do núcleo
 * (`RF-03-57`), e a tela não o anuncia com espaço vazio. A ordem é a que o
 * núcleo devolve — **nunca** por valor, que pódio de apoiador é proibido
 * (`RN-14-38`). */
export function SecaoDeApoiadores({ irPara }: Props) {
  return (
    <SecaoDeAdultos<ApoiadorPublico>
      listar={listarApoiadores}
      chave="vitrine/apoiadores"
      cartaDe={cartaDoApoiador}
      identificacaoDe={(apoiador) => apoiador.identificacao.valor}
      idDe={(apoiador) => apoiador.id}
      prefixoDoCaminho={PREFIXO_DA_PAGINA_DO_APOIADOR}
      vazio="Nenhum Apoiador com aporte homologado por enquanto."
      irPara={irPara}
    />
  );
}
