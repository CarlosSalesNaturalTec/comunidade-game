import type { ReactNode } from "react";
import type { Fala } from "../narracao/narracao";
import { useNarrarAoEntrar } from "../narracao/ProvedorDeNarracao";
import { Botao } from "./Botao";

interface Acao {
  rotulo: string;
  aoAcionar: () => void;
}

interface Props {
  titulo: string;
  subtitulo?: string;
  acao?: Acao;
  /** O controle que mora no **canto** da tela, ao lado da ação — hoje o
   * alternador da narração da tela inicial da App 01. É a tela que o passa,
   * e não o cabeçalho que o monta: assim ele aparece onde o documento 15
   * §5.1 o quer, e não nas outras telas que montam este cabeçalho (design —
   * decisão 5). */
  canto?: ReactNode;
  /** O que este cabeçalho **fala** ao entrar na tela. Omitida, fala o
   * próprio `titulo`, que é a propriedade declarada por quem montou a tela
   * — não texto extraído do documento apresentado. `null` cala este
   * cabeçalho. O **subtítulo não é narrado**: é onde mora a interpolação, e
   * saldo e sujeito de medição não são o que convém ouvir (documento 15
   * §5.1, design — decisão 4). */
  narracao?: Fala | null;
}

export function Cabecalho({ titulo, subtitulo, acao, canto, narracao }: Props) {
  const fala = narracao === undefined ? { texto: titulo } : narracao;
  useNarrarAoEntrar(fala === null ? null : fala.texto, fala?.nick);

  return (
    <header className="cg-cabecalho">
      <div className="cg-cabecalho__texto">
        <h1>{titulo}</h1>
        {subtitulo && <p>{subtitulo}</p>}
      </div>
      {(canto || acao) && (
        <div className="cg-cabecalho__canto">
          {canto}
          {acao && (
            <Botao variante="secundaria" onClick={acao.aoAcionar}>
              {acao.rotulo}
            </Botao>
          )}
        </div>
      )}
    </header>
  );
}
