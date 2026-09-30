import { listarMestres, type MestrePublico } from "../api/leituras";
import { PREFIXO_DA_PAGINA_DO_MESTRE } from "../navegacao/caminhos";
import { navegarPara } from "../navegacao/navegar";
import { cartaDoMestre } from "./cartas";
import { SecaoDeAdultos } from "./SecaoDeAdultos";

interface Props {
  irPara?: (destino: string) => void;
}

export function SecaoDeMestres({ irPara = navegarPara }: Props) {
  return (
    <SecaoDeAdultos<MestrePublico>
      listar={listarMestres}
      chave="vitrine/mestres"
      cartaDe={cartaDoMestre}
      identificacaoDe={(mestre) => mestre.identificacao.valor}
      idDe={(mestre) => mestre.id}
      prefixoDoCaminho={PREFIXO_DA_PAGINA_DO_MESTRE}
      vazio="Nenhum Mestre publicado por enquanto."
      irPara={irPara}
    />
  );
}
