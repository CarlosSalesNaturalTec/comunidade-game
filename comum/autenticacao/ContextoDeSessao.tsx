import {
  createContext,
  type ReactNode,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import { ErroDaApi, ehRecusaDeChave, ehTrocaDeSenhaPendente } from "../api/cliente";
import type { Papel } from "../api/tipos";
import { encerrarSessao, eu, loginPorCredencial, loginSocial, trocarSenha } from "./api";
import {
  CHAVE_DE_ARMAZENAMENTO_PADRAO,
  gravarToken,
  lerToken,
  limparToken,
} from "./armazenamentoDeSessao";

export interface SessaoAberta {
  token: string;
  papel: Papel;
  permissoes: Record<string, string[]>;
  persona_id: string;
  /** Só vem para o Guerreiro(a): se a divulgação de dados foi autorizada
   * pelo responsável (`RF-05-50`). */
  divulgacao_autorizada?: boolean;
}

interface ContextoDeSessaoValor {
  sessao: SessaoAberta | null;
  restaurando: boolean;
  entrando: boolean;
  erroDeEntrada: string | null;
  entrarComGoogle: (idToken: string) => Promise<void>;
  /** Usuário e senha criados pela gestão — o segundo caminho de entrada do
   * adulto (`RF-01-02`, `RF-14-08`). Se a senha ainda é provisória, a
   * sessão não abre: `trocaDeSenhaPendente` passa a `true` em vez disso. */
  entrarComCredencial: (usuario: string, senha: string) => Promise<void>;
  /** Abre a sessão a partir de um token já emitido por outra rota que não
   * `/sessoes/social` — a confirmação humana do Guerreiro(a) na App 01,
   * por exemplo (`RF-04-29`). Grava o token, relê `GET /v1/eu` e, se o
   * núcleo não o reconhecer, o erro sobe para quem chamou tratar
   * (openspec — esqueleto-da-aula-presencial-e-equipe-da-aula). */
  entrarComToken: (token: string) => Promise<void>;
  sair: () => Promise<void>;
  /** Chamada por qualquer tela que receba `sessao_ausente` ou
   * `sessao_invalida` do núcleo (`RN-01-34`): devolve à entrada sem tentar
   * encerrar de novo uma sessão que o núcleo já não reconhece. */
  tratarRecusaDeSessao: () => void;
  /** `true` quando o adulto entrou com senha provisória: nenhuma outra
   * tela abre até `trocarSenhaProvisoria` concluir, sem caminho de
   * contorno (`RF-01-12`, `RF-14-09`). */
  trocaDeSenhaPendente: boolean;
  trocandoSenha: boolean;
  erroDeTrocaDeSenha: string | null;
  trocarSenhaProvisoria: (senhaNova: string) => Promise<void>;
}

const ContextoDeSessao = createContext<ContextoDeSessaoValor | null>(null);

interface ProvedorDeSessaoProps {
  children: ReactNode;
  /** Chave de `sessionStorage` desta sessão — o padrão de hoje quando
   * omitida. A App 01 instancia dois provedores aninhados, com chaves
   * distintas, para a sessão de trabalho do aparelho e a do Guerreiro(a)
   * conviverem sem que uma derrube a outra (design — decisão 1). */
  chaveDeArmazenamento?: string;
}

export function ProvedorDeSessao({
  children,
  chaveDeArmazenamento = CHAVE_DE_ARMAZENAMENTO_PADRAO,
}: ProvedorDeSessaoProps) {
  const [sessao, definirSessao] = useState<SessaoAberta | null>(null);
  const [restaurando, definirRestaurando] = useState(true);
  const [entrando, definirEntrando] = useState(false);
  const [erroDeEntrada, definirErroDeEntrada] = useState<string | null>(null);
  const [trocaDeSenhaPendente, definirTrocaDeSenhaPendente] = useState(false);
  const [tokenPendenteDeTroca, definirTokenPendenteDeTroca] = useState<string | null>(null);
  const [trocandoSenha, definirTrocandoSenha] = useState(false);
  const [erroDeTrocaDeSenha, definirErroDeTrocaDeSenha] = useState<string | null>(null);

  const restaurarSessao = useCallback(
    async (token: string): Promise<boolean> => {
      try {
        const quemSou = await eu(token);
        definirSessao({
          token,
          papel: quemSou.papel,
          permissoes: quemSou.permissoes,
          persona_id: quemSou.persona_id,
          divulgacao_autorizada: quemSou.divulgacao_autorizada,
        });
        definirTrocaDeSenhaPendente(false);
        definirTokenPendenteDeTroca(null);
        return true;
      } catch (erro) {
        if (ehTrocaDeSenhaPendente(erro)) {
          // O token continua válido — só a troca é que falta. Mantém o
          // token guardado para `trocarSenhaProvisoria` usar, sem devolver
          // à tela de entrada (`RF-01-12`, `RF-14-09`).
          definirSessao(null);
          definirTrocaDeSenhaPendente(true);
          definirTokenPendenteDeTroca(token);
          return false;
        }
        limparToken(chaveDeArmazenamento);
        definirSessao(null);
        definirTrocaDeSenhaPendente(false);
        definirTokenPendenteDeTroca(null);
        return false;
      }
    },
    [chaveDeArmazenamento],
  );

  useEffect(() => {
    const token = lerToken(chaveDeArmazenamento);
    if (!token) {
      definirRestaurando(false);
      return;
    }
    restaurarSessao(token).finally(() => definirRestaurando(false));
  }, [restaurarSessao, chaveDeArmazenamento]);

  const entrarComGoogle = useCallback(
    async (idToken: string) => {
      definirEntrando(true);
      definirErroDeEntrada(null);
      try {
        const abertura = await loginSocial(idToken);
        gravarToken(abertura.token, chaveDeArmazenamento);
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
    [restaurarSessao, chaveDeArmazenamento],
  );

  const entrarComCredencial = useCallback(
    async (usuario: string, senha: string) => {
      definirEntrando(true);
      definirErroDeEntrada(null);
      try {
        const abertura = await loginPorCredencial(usuario, senha);
        gravarToken(abertura.token, chaveDeArmazenamento);
        await restaurarSessao(abertura.token);
      } catch (erro) {
        if (ehRecusaDeChave(erro)) {
          definirErroDeEntrada(
            "Falha de configuração desta aplicação. Avise a equipe técnica.",
          );
        } else if (erro instanceof ErroDaApi) {
          // `login_sem_cadastro` e `credencial_invalida` já trazem, na
          // própria mensagem, o que dizer à pessoa (`RF-01-10`).
          definirErroDeEntrada(erro.message);
        } else {
          definirErroDeEntrada("Não foi possível entrar. Tente novamente em instantes.");
        }
      } finally {
        definirEntrando(false);
      }
    },
    [restaurarSessao, chaveDeArmazenamento],
  );

  const trocarSenhaProvisoria = useCallback(
    async (senhaNova: string) => {
      if (!tokenPendenteDeTroca) return;
      definirTrocandoSenha(true);
      definirErroDeTrocaDeSenha(null);
      try {
        await trocarSenha(tokenPendenteDeTroca, senhaNova);
        await restaurarSessao(tokenPendenteDeTroca);
      } catch (erro) {
        definirErroDeTrocaDeSenha(
          erro instanceof ErroDaApi
            ? erro.message
            : "Não foi possível trocar a senha. Tente novamente.",
        );
      } finally {
        definirTrocandoSenha(false);
      }
    },
    [tokenPendenteDeTroca, restaurarSessao],
  );

  const entrarComToken = useCallback(
    async (token: string) => {
      definirEntrando(true);
      definirErroDeEntrada(null);
      gravarToken(token, chaveDeArmazenamento);
      const restaurou = await restaurarSessao(token);
      definirEntrando(false);
      // Guerreiro(a) nunca tem credencial de usuário e senha, então este
      // caminho nunca encontra troca pendente — `!restaurou` aqui é sempre
      // sessão mesmo inválida (design — decisão 1).
      if (!restaurou) {
        definirErroDeEntrada("Não foi possível abrir a sessão. Tente novamente.");
      }
    },
    [restaurarSessao, chaveDeArmazenamento],
  );

  const sair = useCallback(async () => {
    const token = sessao?.token ?? tokenPendenteDeTroca ?? undefined;
    limparToken(chaveDeArmazenamento);
    definirSessao(null);
    definirErroDeEntrada(null);
    definirTrocaDeSenhaPendente(false);
    definirTokenPendenteDeTroca(null);
    definirErroDeTrocaDeSenha(null);
    if (token) {
      try {
        await encerrarSessao(token);
      } catch {
        // A sessão local já foi encerrada; uma falha ao avisar o núcleo não
        // devolve o adulto à tela de gestão.
      }
    }
  }, [sessao, tokenPendenteDeTroca, chaveDeArmazenamento]);

  const tratarRecusaDeSessao = useCallback(() => {
    limparToken(chaveDeArmazenamento);
    definirSessao(null);
    definirErroDeEntrada("Sua sessão terminou. Entre novamente.");
  }, [chaveDeArmazenamento]);

  return (
    <ContextoDeSessao.Provider
      value={{
        sessao,
        restaurando,
        entrando,
        erroDeEntrada,
        entrarComGoogle,
        entrarComCredencial,
        entrarComToken,
        sair,
        tratarRecusaDeSessao,
        trocaDeSenhaPendente,
        trocandoSenha,
        erroDeTrocaDeSenha,
        trocarSenhaProvisoria,
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
