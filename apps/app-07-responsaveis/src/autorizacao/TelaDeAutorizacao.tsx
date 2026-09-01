import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import type { GuerreiroVinculado } from "../vinculados/api";
import {
  type Autorizacao,
  decidirAutorizacao,
  type EstadoDaAutorizacao,
  lerAutorizacao,
} from "./api";

interface Props {
  guerreiro: GuerreiroVinculado;
  /** Leva a tela do termo à versão que valia numa decisão do histórico
   * (`RF-13-33`). */
  aoAbrirVersaoDoTermo?: (versao: string) => void;
}

const FORMATADOR_DE_DATA_HORA = new Intl.DateTimeFormat("pt-BR", {
  dateStyle: "short",
  timeStyle: "short",
});

function formatarDataHora(momentoISO: string): string {
  return FORMATADOR_DE_DATA_HORA.format(new Date(momentoISO));
}

const RESUMO_DO_ESTADO: Record<EstadoDaAutorizacao, string> = {
  vigente: "Vigente: o perfil aparece na vitrine e nos rankings públicos.",
  suspensa: "Suspensa por divergência entre os responsáveis.",
  nao_autorizada: "Ainda não autorizada.",
};

const CODIGO_DE_CONCESSAO_COLIDENTE = "autorizacao_suspensa_por_outro_responsavel";

// A tela da autorização única: o que ela libera e o que não depende dela,
// sempre antes de qualquer botão (`RF-13-13`, `RN-13-05`, `RN-13-06`);
// conceder e revogar dizendo o efeito no mesmo ato (`RF-13-14` a
// `RF-13-16`, `RN-13-08`); os três estados em linguagem simples, com quem
// motivou a suspensão e a alternativa equivalente enquanto não vigente
// (`RF-13-17`, `RF-13-18`, `RF-13-20`, `RN-13-09`); e o histórico, sem
// caminho de editar ou apagar (`RF-13-21`, `RN-13-10`).
export function TelaDeAutorizacao({ guerreiro, aoAbrirVersaoDoTermo }: Props) {
  const { sessao } = useSessao();
  const [autorizacao, definirAutorizacao] = useState<Autorizacao | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [decidindo, definirDecidindo] = useState(false);
  const [avisoDaDecisao, definirAvisoDaDecisao] = useState<{
    tipo: "sucesso" | "atencao" | "erro";
    texto: string;
  } | null>(null);

  const carregar = useCallback(() => {
    if (!sessao) return;
    return lerAutorizacao(guerreiro.id, sessao.token)
      .then(definirAutorizacao)
      .catch(() => definirErro("Não foi possível carregar a autorização. Tente novamente."));
  }, [guerreiro.id, sessao]);

  useEffect(() => {
    definirAutorizacao(null);
    definirErro(null);
    definirAvisoDaDecisao(null);
    carregar();
  }, [carregar]);

  async function decidir(decisao: "concede" | "nega") {
    if (!sessao) return;
    definirDecidindo(true);
    definirAvisoDaDecisao(null);
    try {
      await decidirAutorizacao(guerreiro.id, decisao, sessao.token);
      definirAvisoDaDecisao({
        tipo: "sucesso",
        texto:
          decisao === "concede"
            ? "Autorização concedida: o perfil passa a aparecer na vitrine e nos rankings públicos."
            : `Autorização revogada: perfil, criações e elenco do jogo saem do que é público agora. ` +
              `Nada foi apagado, e ${guerreiro.nick} continua participando de tudo normalmente.`,
      });
      await carregar();
    } catch (erroRecebido) {
      if (
        erroRecebido instanceof ErroDaApi &&
        erroRecebido.codigo === CODIGO_DE_CONCESSAO_COLIDENTE
      ) {
        // O 409 da concessão colidente vira orientação, nunca código de
        // erro cru (PRD-13 §§9, 10).
        definirAvisoDaDecisao({ tipo: "atencao", texto: erroRecebido.message });
        await carregar();
        return;
      }
      // Conceder e revogar exigem rede: a decisão nunca é dada por tomada
      // sem confirmação do núcleo (PRD-13 §10).
      definirAvisoDaDecisao({
        tipo: "erro",
        texto: "A decisão não foi registrada. Verifique sua conexão e tente novamente.",
      });
    } finally {
      definirDecidindo(false);
    }
  }

  if (erro) {
    return <Aviso tipo="erro">{erro}</Aviso>;
  }

  if (autorizacao === null) {
    return <EstadoDaLista>Carregando…</EstadoDaLista>;
  }

  return (
    <section aria-label={`Autorização de ${guerreiro.nick}`}>
      <AvisoDeColeta dado={`a decisão da autorização de ${guerreiro.nick}`} />

      <section>
        <h2>O que a autorização libera</h2>
        <ul>
          <li>Divulgação do perfil, do histórico e das criações</li>
          <li>Imagem em fotos e vídeos de eventos</li>
          <li>Captação da produção por foto do manuscrito ou áudio</li>
        </ul>
        <h3>O que não depende dela</h3>
        <ul>
          <li>A participação nas atividades, que é sempre livre</li>
          <li>A biometria do onboarding, que tem termo impresso próprio</li>
        </ul>
      </section>

      <section>
        <h2>Estado atual</h2>
        <p>{RESUMO_DO_ESTADO[autorizacao.estado]}</p>

        {autorizacao.estado === "suspensa" && autorizacao.suspensa_por && (
          <Aviso tipo="atencao">
            Motivada por outro responsável, em{" "}
            {formatarDataHora(autorizacao.suspensa_por.decidido_em)}. A gestão vai tratar o
            caso com a família.
          </Aviso>
        )}

        {autorizacao.estado !== "vigente" && (
          <Aviso tipo="atencao">
            Enquanto não houver autorização, {guerreiro.nick} entrega a produção ao Mestre no
            encontro e participa de tudo normalmente — só não aparece publicamente.
          </Aviso>
        )}

        {avisoDaDecisao && <Aviso tipo={avisoDaDecisao.tipo}>{avisoDaDecisao.texto}</Aviso>}

        <Botao onClick={() => decidir("concede")} desabilitado={decidindo}>
          Conceder
        </Botao>
        <Botao variante="secundaria" onClick={() => decidir("nega")} desabilitado={decidindo}>
          Revogar
        </Botao>
      </section>

      <section>
        <h2>Histórico</h2>
        {autorizacao.historico.length === 0 && (
          <EstadoDaLista>Nenhuma decisão registrada ainda.</EstadoDaLista>
        )}
        {autorizacao.historico.length > 0 && (
          <ul aria-label="Histórico da autorização">
            {autorizacao.historico.map((item) => (
              <li key={item.id}>
                {item.decisao === "concede" ? "Concedida" : "Revogada"}
                {item.responsavel_id === sessao?.persona_id
                  ? " por você"
                  : " por outro responsável"}{" "}
                em {formatarDataHora(item.registrado_em)} — versão {item.versao_do_termo} do
                termo
                {aoAbrirVersaoDoTermo && (
                  <button
                    type="button"
                    onClick={() => aoAbrirVersaoDoTermo(item.versao_do_termo)}
                  >
                    Ver o termo desta decisão
                  </button>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>
    </section>
  );
}
