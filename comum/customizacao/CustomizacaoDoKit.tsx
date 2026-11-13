import { type ReactNode, useState } from "react";
import { ErroDaApi } from "../api/cliente";
import { Aviso } from "../react/Aviso";
import { Botao } from "../react/Botao";
import { cancelarCustomizacao, type KitAberto, type RegistroDeCustomizacao } from "./api";
import { RegistroDaCustomizacao } from "./RegistroDaCustomizacao";

/** O registro mais recente do kit, pela data em que foi registrado — é ele
 * que decide a ação do bloco (`RF-05-103`, `RF-04-80`). */
export function ultimoRegistroDoKit(
  kit: KitAberto,
  registros: RegistroDeCustomizacao[],
): RegistroDeCustomizacao | null {
  const doKit = registros.filter(
    (registro) => registro.entrega_de_recompensa_id === kit.entrega_de_recompensa_id,
  );
  if (doKit.length === 0) return kit.pendente;
  return doKit.reduce((maisRecente, registro) =>
    registro.registrado_em > maisRecente.registrado_em ? registro : maisRecente,
  );
}

/** Qual formulário está aberto: um por vez, guardado por quem consome. */
export interface FormularioAberto {
  entregaId: string;
  registroId: string | null;
}

interface Props {
  kit: KitAberto;
  ultimo: RegistroDeCustomizacao | null;
  token: string;
  formularioAberto: FormularioAberto | null;
  abrirFormulario: (formulario: FormularioAberto) => void;
  fecharFormulario: () => void;
  aoMudar: () => Promise<void>;
}

// A situação do último registro do kit aberto e a ação que cabe — registrar,
// retomar o envio, aguardar a aula e cancelar, ler o motivo e enviar de novo.
// Mora no `comum` para a App 05, em casa, e a App 01, no encontro, mostrarem o
// mesmo com as mesmas palavras (`RF-05-103`, `RF-04-80`, design — decisão 1).
export function CustomizacaoDoKit({
  kit,
  ultimo,
  token,
  formularioAberto,
  abrirFormulario,
  fecharFormulario,
  aoMudar,
}: Props) {
  const [erro, definirErro] = useState<string | null>(null);
  const [cancelando, definirCancelando] = useState(false);
  const entregaId = kit.entrega_de_recompensa_id;

  if (formularioAberto?.entregaId === entregaId) {
    return (
      <RegistroDaCustomizacao
        entregaDeRecompensaId={entregaId}
        registroIdInicial={formularioAberto.registroId}
        token={token}
        aoConcluir={async () => {
          fecharFormulario();
          await aoMudar();
        }}
        aoCancelar={fecharFormulario}
      />
    );
  }

  async function cancelar(registroId: string) {
    definirErro(null);
    definirCancelando(true);
    try {
      await cancelarCustomizacao(registroId, token);
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível cancelar agora. Tente de novo em instantes.",
      );
    } finally {
      definirCancelando(false);
    }
    await aoMudar();
  }

  const registrarNovo = (rotulo: string) => (
    <Botao
      variante="secundaria"
      onClick={() => abrirFormulario({ entregaId, registroId: null })}
    >
      {rotulo}
    </Botao>
  );

  let conteudo: ReactNode;
  if (ultimo === null || ultimo.situacao === "cancelado" || ultimo.situacao === "expirado") {
    conteudo = registrarNovo("Registrar a customização");
  } else if (ultimo.situacao === "pendente" && !ultimo.tem_midia) {
    conteudo = (
      <>
        <p>Falta enviar a foto ou o vídeo da sua customização.</p>
        <Botao onClick={() => abrirFormulario({ entregaId, registroId: ultimo.id })}>
          Enviar a foto ou o vídeo
        </Botao>
        <Botao
          variante="secundaria"
          onClick={() => cancelar(ultimo.id)}
          desabilitado={cancelando}
        >
          Cancelar
        </Botao>
      </>
    );
  } else if (ultimo.situacao === "pendente") {
    conteudo = (
      <>
        <Aviso tipo="andamento">
          Aguardando a aula: mostre o kit ao Mestre no encontro. Se não for apresentado até o
          fim do ciclo, este registro expira.
        </Aviso>
        <Botao
          variante="secundaria"
          onClick={() => cancelar(ultimo.id)}
          desabilitado={cancelando}
        >
          Cancelar
        </Botao>
      </>
    );
  } else if (ultimo.situacao === "reprovado") {
    conteudo = (
      <>
        <Aviso tipo="atencao">O Mestre pediu um ajuste: {ultimo.motivo_do_julgamento}</Aviso>
        {registrarNovo("Enviar de novo")}
      </>
    );
  } else {
    conteudo = (
      <>
        <Aviso tipo="sucesso">Aprovado pelo Mestre.</Aviso>
        {registrarNovo("Registrar a customização")}
      </>
    );
  }

  return (
    <div className="cg-customizacao__kit">
      {conteudo}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
    </div>
  );
}
