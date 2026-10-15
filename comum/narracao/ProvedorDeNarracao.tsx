import {
  createContext,
  type ReactNode,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import {
  armar,
  cancelar,
  existeSinteseDeFala,
  type Fala,
  falar,
  observarVozes,
  vozPreferida,
} from "./narracao";

interface ContextoDeNarracaoValor {
  /** Nasce **desligada**: o toque que a liga é o gesto que o navegador
   * exige antes da primeira fala, e é por isso que não existe um controle
   * de iniciar à parte (documento 15 §5.1). A escolha vale o aparelho, não
   * a pessoa, e morre com a recarga — não é gravada em lugar algum. */
  ligada: boolean;
  /** O navegador oferece síntese de fala. Sem ela a camada cala. */
  disponivel: boolean;
  alternarNarracao: () => void;
  /** O texto **curto** que a tela declarou, ao entrar nela. */
  narrar: (fala: Fala) => void;
  /** O texto **longo**, sob toque, **independente do liga e desliga**: o
   * próprio toque é o pedido e é o gesto que o navegador exige. */
  ouvir: (fala: Fala) => void;
  cancelarNarracao: () => void;
}

// Sem provedor montado a camada fica **inerte**: é o que mantém inalterada
// a aplicação que ainda não recebeu o roteiro dela — a narração desligada
// não oferece controle algum (design — decisão 3).
const INERTE: ContextoDeNarracaoValor = {
  ligada: false,
  disponivel: false,
  alternarNarracao: () => {},
  narrar: () => {},
  ouvir: () => {},
  cancelarNarracao: () => {},
};

const ContextoDeNarracao = createContext<ContextoDeNarracaoValor | null>(null);

/**
 * A camada que lê as telas em voz alta, montada ao lado do provedor de
 * sessão pela aplicação que já tem roteiro. Nenhuma rota e nenhuma entidade
 * participam: o navegador sintetiza, e o Backend API não sabe que isto
 * existe.
 */
export function ProvedorDeNarracao({ children }: { children: ReactNode }) {
  const [ligada, definirLigada] = useState(false);
  const [voz, definirVoz] = useState<SpeechSynthesisVoice | null>(null);
  const disponivel = existeSinteseDeFala();

  // A voz se escolhe uma vez, depois de `voiceschanged` (design — decisão
  // 5). Enquanto ela não vier, a camada cala — e, nascendo desligada, nada
  // fala antes de alguém ligar.
  useEffect(() => {
    if (!disponivel) return;
    definirVoz(vozPreferida());
    return observarVozes(() => definirVoz(vozPreferida()));
  }, [disponivel]);

  const narrar = useCallback(
    (fala: Fala) => {
      if (!ligada || !voz) return;
      falar(fala, voz);
    },
    [ligada, voz],
  );

  // Independente do liga e desliga: quem aciona o controle de ouvir está
  // pedindo aquela leitura, e o próprio acionamento é o gesto que o
  // navegador exige. Atrás do `ligada` ele desapareceria por padrão, agora
  // que a narração nasce desligada — justamente de quem menos lê (documento
  // 15 §5.1, design — decisão 3).
  const ouvir = useCallback(
    (fala: Fala) => {
      if (!voz) return;
      armar();
      falar(fala, voz);
    },
    [voz],
  );

  // O clique que **liga** é o gesto que libera o motor de fala — daí o
  // `armar()` aqui dentro, e daí não existir um controle de iniciar à parte
  // (design — decisões 1 e 2).
  const alternarNarracao = useCallback(() => {
    definirLigada((anterior) => {
      const proxima = !anterior;
      if (proxima) armar();
      else cancelar();
      return proxima;
    });
  }, []);

  const cancelarNarracao = useCallback(() => {
    cancelar();
  }, []);

  const valor = useMemo(
    () => ({
      ligada,
      disponivel,
      alternarNarracao,
      narrar,
      ouvir,
      cancelarNarracao,
    }),
    [ligada, disponivel, alternarNarracao, narrar, ouvir, cancelarNarracao],
  );

  return <ContextoDeNarracao.Provider value={valor}>{children}</ContextoDeNarracao.Provider>;
}

export function useNarracao(): ContextoDeNarracaoValor {
  return useContext(ContextoDeNarracao) ?? INERTE;
}

/**
 * Narra, ao entrar na tela, o texto curto que ela declarou. Recebe as
 * partes da fala **soltas**, e não o objeto: literal novo a cada render
 * faria a tela falar a cada render, o mesmo laço que a sondagem do quiz
 * evita pelo `id` da pergunta (design — decisão 7).
 *
 * A camada não escreve texto nenhum na tela: o que ela fala é a propriedade
 * que a tela declarou, já visível. Não há, portanto, texto que exista **só**
 * para a narração — e é por isso que nada aqui é escondido do leitor de
 * tela, que continua lendo a tela inteira (documento 15 §5.1, design —
 * decisão 8).
 */
export function useNarrarAoEntrar(texto: string | null, nick?: string): void {
  const { narrar } = useNarracao();
  useEffect(() => {
    if (texto === null) return;
    narrar({ texto, nick });
  }, [texto, nick, narrar]);
}
