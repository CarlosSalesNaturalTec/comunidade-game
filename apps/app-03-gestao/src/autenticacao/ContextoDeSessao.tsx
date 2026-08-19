import {
  createContext,
  type ReactNode,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import { ErroDaApi, ehRecusaDeChave } from "../api/cliente";
import type { Papel } from "../api/tipos";
import { encerrarSessao, eu, loginSocial } from "./api";
import { gravarToken, lerToken, limparToken } from "./armazenamentoDeSessao";

export interface SessaoAberta {
  token: string;
  papel: Papel;
  permissoes: Record<string, string[]>;
}

interface ContextoDeSessaoValor {
  sessao: SessaoAberta | null;
  restaurando: boolean;
  entrando: boolean;
  erroDeEntrada: string | null;
  entrarComGoogle: (idToken: string) => Promise<void>;
  sair: () => Promise<void>;
  /** Chamada por qualquer tela que receba `sessao_ausente` ou
   * `sessao_invalida` do núcleo (`RN-01-34`): devolve à entrada sem tentar
   * encerrar de novo uma sessão que o núcleo já não reconhece. */
  tratarRecusaDeSessao: () => void;
}

const ContextoDeSessao = createContext<ContextoDeSessaoValor | null>(null);

export function ProvedorDeSessao({ children }: { children: ReactNode }) {
  const [sessao, definirSessao] = useState<SessaoAberta | null>(null);
  const [restaurando, definirRestaurando] = useState(true);
  const [entrando, definirEntrando] = useState(false);
  const [erroDeEntrada, definirErroDeEntrada] = useState<string | null>(null);

  const restaurarSessao = useCallback(async (token: string): Promise<boolean> => {
    try {
      const quemSou = await eu(token);
      definirSessao({ token, papel: quemSou.papel, permissoes: quemSou.permissoes });
      return true;
    } catch {
      limparToken();
      definirSessao(null);
      return false;
    }
  }, []);

  useEffect(() => {
    const token = lerToken();
    if (!token) {
      definirRestaurando(false);
      return;
    }
    restaurarSessao(token).finally(() => definirRestaurando(false));
  }, [restaurarSessao]);

  const entrarComGoogle = useCallback(
    async (idToken: string) => {
      definirEntrando(true);
      definirErroDeEntrada(null);
      try {
        const abertura = await loginSocial(idToken);
        gravarToken(abertura.token);
        await restaurarSessao(abertura.token);
      } catch (erro) {
        if (ehRecusaDeChave(erro)) {
          definirErroDeEntrada(
            "Falha de configuração desta aplicação. Avise a equipe técnica.",
          );
        } else if (erro instanceof ErroDaApi) {
          // `login_sem_cadastro` já traz, na própria mensagem, a orientação
          // de solicitar participação pela vitrine (`RF-01-10`).
          definirErroDeEntrada(erro.message);
        } else {
          definirErroDeEntrada("Não foi possível entrar. Tente novamente em instantes.");
        }
      } finally {
        definirEntrando(false);
      }
    },
    [restaurarSessao],
  );

  const sair = useCallback(async () => {
    const token = sessao?.token;
    limparToken();
    definirSessao(null);
    definirErroDeEntrada(null);
    if (token) {
      try {
        await encerrarSessao(token);
      } catch {
        // A sessão local já foi encerrada; uma falha ao avisar o núcleo não
        // devolve o adulto à tela de gestão.
      }
    }
  }, [sessao]);

  const tratarRecusaDeSessao = useCallback(() => {
    limparToken();
    definirSessao(null);
    definirErroDeEntrada("Sua sessão terminou. Entre novamente.");
  }, []);

  return (
    <ContextoDeSessao.Provider
      value={{
        sessao,
        restaurando,
        entrando,
        erroDeEntrada,
        entrarComGoogle,
        sair,
        tratarRecusaDeSessao,
      }}
    >
      {children}
    </ContextoDeSessao.Provider>
  );
}

export function useSessao(): ContextoDeSessaoValor {
  const contexto = useContext(ContextoDeSessao);
  if (!contexto) {
    throw new Error("useSessao só pode ser usado dentro de ProvedorDeSessao.");
  }
  return contexto;
}
