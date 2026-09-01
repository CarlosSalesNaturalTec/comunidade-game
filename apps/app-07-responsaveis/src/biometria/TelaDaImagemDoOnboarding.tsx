import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import type { GuerreiroVinculado } from "../vinculados/api";
import {
  type EstadoDaBiometria,
  type GatilhoDoApagamento,
  lerEstadoDaBiometria,
  recusarBiometria,
} from "./api";

interface Props {
  guerreiro: GuerreiroVinculado;
}

const FORMATADOR_DE_DATA = new Intl.DateTimeFormat("pt-BR", { dateStyle: "short" });

function formatarData(momentoISO: string): string {
  return FORMATADOR_DE_DATA.format(new Date(momentoISO));
}

const ROTULO_DO_GATILHO: Record<GatilhoDoApagamento, string> = {
  exclusao_deferida: "o pedido de exclusão deferido",
  recusa_biometria: "a recusa da biometria",
  fim_do_vinculo: "o fim do vínculo com o projeto",
};

// A imagem captada no onboarding: termo próprio e finalidade antes do ato,
// recusa sem caminho de concessão — essa é o termo impresso assinado no
// encontro —, a alternativa equivalente dita junto e o aviso do apagamento
// com a data, quando existir (`RF-13-27`, `RF-13-28`, `RF-13-43`,
// `RF-13-44`, `RN-13-05`, `RN-13-06`, `RN-13-09`, `RN-13-15`).
export function TelaDaImagemDoOnboarding({ guerreiro }: Props) {
  const { sessao } = useSessao();
  const [estado, definirEstado] = useState<EstadoDaBiometria | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [recusando, definirRecusando] = useState(false);
  const [avisoDaRecusa, definirAvisoDaRecusa] = useState<string | null>(null);

  const carregar = useCallback(() => {
    if (!sessao) return;
    return lerEstadoDaBiometria(guerreiro.id, sessao.token)
      .then(definirEstado)
      .catch(() => definirErro("Não foi possível carregar o estado da biometria."));
  }, [guerreiro.id, sessao]);

  useEffect(() => {
    definirEstado(null);
    definirErro(null);
    definirAvisoDaRecusa(null);
    carregar();
  }, [carregar]);

  async function recusar() {
    if (!sessao) return;
    definirRecusando(true);
    definirAvisoDaRecusa(null);
    try {
      const resposta = await recusarBiometria(guerreiro.id, sessao.token);
      definirAvisoDaRecusa(
        resposta.apagar_em
          ? `Recusa registrada. O template será apagado em ${formatarData(resposta.apagar_em)}.`
          : "Recusa registrada.",
      );
      await carregar();
    } catch (erroCapturado) {
      definirAvisoDaRecusa(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "A recusa não foi registrada. Verifique sua conexão e tente novamente.",
      );
    } finally {
      definirRecusando(false);
    }
  }

  if (erro) {
    return <Aviso tipo="erro">{erro}</Aviso>;
  }

  if (estado === null) {
    return <EstadoDaLista>Carregando…</EstadoDaLista>;
  }

  return (
    <section aria-label={`Imagem do onboarding de ${guerreiro.nick}`}>
      <section>
        <h2>Para que serve a imagem</h2>
        <p>
          A imagem captada no onboarding identifica {guerreiro.nick} na presença e na entrada —
          e nada mais. É um termo próprio, distinto da autorização de divulgação.
        </p>
        <p>
          Esta tela só recusa. Conceder a biometria é ato do termo impresso, assinado no
          encontro com Admin ou Mestre.
        </p>
      </section>

      <section>
        <h2>Se você recusar</h2>
        <p>
          {guerreiro.nick} não fica de fora de nada: sem captura, entra por nick e confirmação
          do Mestre ou de um Admin no encontro, e participa de tudo normalmente.
        </p>

        {avisoDaRecusa && <Aviso tipo="sucesso">{avisoDaRecusa}</Aviso>}

        <Botao variante="secundaria" onClick={recusar} desabilitado={recusando}>
          Recusar a imagem
        </Botao>
      </section>

      {estado.apagar_em && (
        <Aviso tipo="atencao">
          O <em>template</em> biométrico será apagado em {formatarData(estado.apagar_em)}, por{" "}
          {ROTULO_DO_GATILHO[estado.gatilho_do_apagamento as GatilhoDoApagamento]}. Se{" "}
          {guerreiro.nick} voltar depois disso, a captura é feita de novo, com novo termo.
        </Aviso>
      )}
    </section>
  );
}
