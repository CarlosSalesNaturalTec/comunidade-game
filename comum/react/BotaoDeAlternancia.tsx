import { Icone, type NomeDeGlifo } from "./Icone";

interface Props {
  /** O rótulo acessível, **obrigatório**: o botão não tem texto visível, e
   * `Icone` é decorativo para a tecnologia assistiva. O documento 15 §5 não
   * abre exceção — ícone nunca é a única forma de identificar um elemento
   * acionável. Muda com o estado, porque diz o que o toque vai fazer. */
  rotulo: string;
  ligado: boolean;
  /** Um glifo por estado, distintos pela **forma**: a cor sozinha nunca diz
   * o estado (documento 15 §5). */
  glifoLigado: NomeDeGlifo;
  glifoDesligado: NomeDeGlifo;
  onClick: () => void;
  desabilitado?: boolean;
}

// O alternador apresentado só pelo glifo, para o controle que liga e desliga
// uma coisa só. Reaproveita `cg-botao` pelo alvo de toque de 48 px e pelo
// foco visível que a classe já garante (documento 15 §5), e acrescenta só a
// caixa quadrada do ícone.
//
// O estado sai por dois caminhos que não dependem de cor: a **forma** do
// glifo, para quem olha, e `aria-pressed`, para quem navega por leitor de
// tela. Nenhum dos dois é a cor do botão (design — decisão 4).
export function BotaoDeAlternancia({
  rotulo,
  ligado,
  glifoLigado,
  glifoDesligado,
  onClick,
  desabilitado = false,
}: Props) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={desabilitado}
      aria-label={rotulo}
      aria-pressed={ligado}
      className="cg-botao cg-botao--icone"
    >
      <Icone glifo={ligado ? glifoLigado : glifoDesligado} />
    </button>
  );
}
