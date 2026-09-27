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

/** O estado é do **aparelho**, não da pessoa: persiste entre atendimentos e
 * NUNCA acompanha o Guerreiro(a) a outro aparelho (documento 15 §5.1). */
export const CHAVE_DA_NARRACAO_NO_APARELHO = "cg:narracao";

interface ContextoDeNarracaoValor {
  /** Nasce ligada; quem desliga não prende o próximo, que religa. */
  ligada: boolean;
  /** O gesto da pessoa já aconteceu — antes dele o navegador não fala. */
  armada: boolean;
  /** O navegador oferece síntese de fala. Sem ela não há o que armar. */
  disponivel: boolean;
  alternarNarracao: () => void;
  armarNarracao: () => void;
  /** O texto **curto** que a tela declarou, ao entrar nela. */
  narrar: (fala: Fala) => void;
  /** O texto **longo**, sob toque: o próprio toque é o gesto que o
   * navegador exige, e falar ali arma a narração de vez. */
  ouvir: (fala: Fala) => void;
  cancelarNarracao: () => void;
}

// Sem provedor montado a camada fica **inerte**: é o que mantém inalterada
// a aplicação que ainda não recebeu o roteiro dela — a narração desligada
// não oferece controle algum (design — decisão 3).
const INERTE: ContextoDeNarracaoValor = {
  ligada: false,
  armada: false,
  disponivel: false,
  alternarNarracao: () => {},
  armarNarracao: () => {},
  narrar: () => {},
  ouvir: () => {},
  cancelarNarracao: () => {},
};

const ContextoDeNarracao = createContext<ContextoDeNarracaoValor | null>(null);

// Aba privativa e dado de site bloqueado fazem `localStorage` lançar. A
// leitura que falha cai no padrão **ligado**, e a escrita que falha não
// derruba nada: a escolha vale a sessão (design — Risks).
function lerEscolhaDoAparelho(): boolean {
  try {
    return localStorage.getItem(CHAVE_DA_NARRACAO_NO_APARELHO) !== "desligada";
  } catch {
    return true;
  }
}

function gravarEscolhaDoAparelho(ligada: boolean): void {
  try {
    localStorage.setItem(CHAVE_DA_NARRACAO_NO_APARELHO, ligada ? "ligada" : "desligada");
  } catch {
    // Nada a fazer: a escolha vale esta sessão do aparelho.
  }
}

/**
 * A camada que lê as telas em voz alta, montada ao lado do provedor de
 * sessão pela aplicação que já tem roteiro. Nenhuma rota e nenhuma entidade
 * participam: o navegador sintetiza, e o Backend API não sabe que isto
 * existe.
 */
export function ProvedorDeNarracao({ children }: { children: ReactNode }) {
  const [ligada, definirLigada] = useState(lerEscolhaDoAparelho);
  const [armada, definirArmada] = useState(false);
  const [voz, definirVoz] = useState<SpeechSynthesisVoice | null>(null);
  const disponivel = existeSinteseDeFala();

  // A voz se escolhe uma vez, depois de `voiceschanged` (design — decisão
  // 5). Enquanto ela não vier, a camada cala — e nada fala antes do gesto
  // de armar, que vem depois disto.
  useEffect(() => {
    if (!disponivel) return;
    definirVoz(vozPreferida());
    return observarVozes(() => definirVoz(vozPreferida()));
  }, [disponivel]);

  const narrar = useCallback(
    (fala: Fala) => {
      if (!ligada || !armada || !voz) return;
      falar(fala, voz);
    },
    [ligada, armada, voz],
  );

  const ouvir = useCallback(
    (fala: Fala) => {
      if (!ligada || !voz) return;
      definirArmada(true);
      falar(fala, voz);
    },
    [ligada, voz],
  );

  const alternarNarracao = useCallback(() => {
    definirLigada((anterior) => {
      const proxima = !anterior;
      gravarEscolhaDoAparelho(proxima);
      if (!proxima) cancelar();
      return proxima;
    });
  }, []);

  const armarNarracao = useCallback(() => {
    armar();
    definirArmada(true);
  }, []);

  const cancelarNarracao = useCallback(() => {
    cancelar();
  }, []);

  const valor = useMemo(
    () => ({
      ligada,
      armada,
      disponivel,
      alternarNarracao,
      armarNarracao,
      narrar,
      ouvir,
      cancelarNarracao,
    }),
    [
      ligada,
      armada,
      disponivel,
      alternarNarracao,
      armarNarracao,
      narrar,
      ouvir,
      cancelarNarracao,
    ],
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
