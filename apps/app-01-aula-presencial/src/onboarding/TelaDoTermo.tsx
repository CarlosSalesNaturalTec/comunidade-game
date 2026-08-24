import { ErroDaApi } from "comum/api";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useState } from "react";
import { registrarConsentimento } from "../api/consentimentos";

interface Props {
  tokenDeTrabalho: string;
  personaIdDeTrabalho: string;
  responsavelId: string;
  guerreiroId: string;
  aoConcluir: () => void;
  aoVoltar: () => void;
}

// O termo na tela, antes de qualquer captura — a câmera só abre depois de o
// consentimento estar registrado no núcleo, com quem confirma a assinatura
// registrado como testemunha (`RF-04-11`, `RF-04-12`, `RF-04-13`,
// `RN-04-07`, design — decisão 3). A leitura em voz alta depende da
// modalidade áudio, que ainda não existe (`RF-04-06`).
export function TelaDoTermo({
  tokenDeTrabalho,
  personaIdDeTrabalho,
  responsavelId,
  guerreiroId,
  aoConcluir,
  aoVoltar,
}: Props) {
  const [erro, definirErro] = useState<string | null>(null);
  const [confirmando, definirConfirmando] = useState(false);

  async function confirmarAssinatura() {
    definirErro(null);
    definirConfirmando(true);
    try {
      await registrarConsentimento(
        {
          responsavel_id: responsavelId,
          guerreiro_id: guerreiroId,
          tipo: "biometria",
          decisao: "concede",
          origem: "impressa",
          testemunha_id: personaIdDeTrabalho,
        },
        tokenDeTrabalho,
      );
      aoConcluir();
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível registrar o consentimento. Tente novamente.",
      );
    } finally {
      definirConfirmando(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Termo de consentimento"
        subtitulo="Captura e tratamento biométrico do onboarding — termo impresso, próprio da imagem."
        acao={{ rotulo: "Voltar ao início", aoAcionar: aoVoltar }}
      />
      <p>
        Ao assinar o termo impresso, o responsável autoriza a captura da imagem do Guerreiro(a)
        para identificação nas próximas atividades. A fotografia nunca sai deste aparelho: só o
        descritor gerado por ela é enviado.
      </p>
      <p>
        O Mestre ou o Admin presente confirma abaixo que o responsável assinou o termo impresso
        — essa confirmação fica registrada como testemunha do consentimento.
      </p>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Botao onClick={confirmarAssinatura} desabilitado={confirmando}>
        {confirmando ? "Registrando…" : "Confirmo: o termo impresso foi assinado"}
      </Botao>
    </Moldura>
  );
}
