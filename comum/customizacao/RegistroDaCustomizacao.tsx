import { useEffect, useId, useRef, useState } from "react";
import { ErroDaApi } from "../api/cliente";
import { existeTranscricaoDeFala, iniciarTranscricao } from "../fala/fala";
import { Aviso } from "../react/Aviso";
import { Botao } from "../react/Botao";
import { Campo } from "../react/Campo";
import { enviarMidiaDaCustomizacao, registrarMinhaCustomizacao } from "./api";

/** O aviso antes do envio, no texto aprovado pelo fundador em 2026-11-13
 * (`RF-05-102`, PRD-05 §11). */
export const AVISO_DA_CUSTOMIZACAO =
  "Foto ou vídeo só do kit, sem o seu rosto. Se o Mestre aprovar no encontro, o registro fica " +
  "guardado no seu acervo e pode ir à vitrine, com o seu nick, se o seu responsável autorizar.";

const MENSAGEM_SEM_TRANSCRICAO = "Este aparelho não transcreve fala. Escreva a descrição.";
const MENSAGEM_DE_FALHA_NA_FALA = "Não foi possível entender a fala. Fale de novo ou escreva.";
const MENSAGEM_DE_QUEDA_DE_REDE =
  "A conexão caiu no meio do envio. Quando ela voltar, toque em Tentar novamente.";

function mensagemDoErro(erro: unknown): string {
  // A recusa do núcleo já vem em linguagem simples; a queda de rede não tem
  // corpo, e por isso ganha a frase própria.
  return erro instanceof ErroDaApi ? erro.message : MENSAGEM_DE_QUEDA_DE_REDE;
}

// O aviso vem **antes** do controle de envio, nunca depois: é o que dá
// sentido ao "só do kit, sem rosto". O Saber mais é o acesso à área
// detalhada que o PRD-05 §11 exige de toda tela que coleta dado.
function AvisoDaCustomizacao() {
  const [aberto, definirAberto] = useState(false);

  return (
    <div className="cg-customizacao__aviso">
      <p>
        {AVISO_DA_CUSTOMIZACAO}{" "}
        <button
          type="button"
          className="cg-customizacao__aviso-botao"
          aria-expanded={aberto}
          onClick={() => definirAberto((valor) => !valor)}
        >
          {aberto ? "Ver menos" : "Saber mais"}
        </button>
      </p>
      {aberto && (
        <p className="cg-customizacao__aviso-detalhe">
          Só você e o Mestre da sua comunidade veem o que você enviou, para conferir a
          customização no encontro. Se ele aprovar e o seu responsável autorizar, o registro
          aparece na vitrine com o seu nick — nunca com o seu nome nem com a sua foto de rosto.
          É por isso que a foto é só do kit.
        </p>
      )}
    </div>
  );
}

interface Props {
  entregaDeRecompensaId: string;
  /** O pendente sem mídia recebida: só falta o envio, do mesmo registro. */
  registroIdInicial?: string | null;
  token: string;
  aoConcluir: () => void | Promise<void>;
  aoCancelar: () => void;
}

/** O registro da customização do kit feito pelo próprio Guerreiro(a): a
 * descrição por voz ou texto, a foto ou o vídeo só do kit, o aviso e o envio
 * retomável com progresso. Registro gravado com o envio interrompido retoma o
 * envio do **mesmo** registro, sem criar outro (`RF-05-102`, `RF-04-80`,
 * design — decisão 2). */
export function RegistroDaCustomizacao({
  entregaDeRecompensaId,
  registroIdInicial = null,
  token,
  aoConcluir,
  aoCancelar,
}: Props) {
  const [descricao, definirDescricao] = useState("");
  const [arquivo, definirArquivo] = useState<File | null>(null);
  const [registroId, definirRegistroId] = useState<string | null>(registroIdInicial);
  const [progresso, definirProgresso] = useState<number | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [ouvindo, definirOuvindo] = useState(false);
  const [avisoDeFala, definirAvisoDeFala] = useState<string | null>(null);
  const encerradorRef = useRef<(() => void) | null>(null);
  const transcreve = existeTranscricaoDeFala();
  const idDoArquivo = useId();

  // O microfone fecha junto com a tela: nunca fica captando sozinho.
  useEffect(() => {
    return () => encerradorRef.current?.();
  }, []);

  function alternarFala() {
    if (ouvindo) {
      encerradorRef.current?.();
      return;
    }
    definirAvisoDeFala(null);
    definirOuvindo(true);
    encerradorRef.current = iniciarTranscricao({
      aoTranscrever: (transcricao) => definirDescricao(transcricao),
      aoFalhar: () => definirAvisoDeFala(MENSAGEM_DE_FALHA_NA_FALA),
      aoEncerrar: () => {
        definirOuvindo(false);
        encerradorRef.current = null;
      },
    });
  }

  const faltaAlgo = arquivo === null || (registroId === null && !descricao.trim());

  async function registrar() {
    if (faltaAlgo || arquivo === null) return;
    definirErro(null);
    definirEnviando(true);
    try {
      let id = registroId;
      if (id === null) {
        const registro = await registrarMinhaCustomizacao(
          { entrega_de_recompensa_id: entregaDeRecompensaId, descricao: descricao.trim() },
          token,
        );
        id = registro.id;
        definirRegistroId(id);
      }
      definirProgresso(0);
      await enviarMidiaDaCustomizacao(id, arquivo, token, (enviados, total) =>
        definirProgresso(total > 0 ? Math.round((enviados / total) * 100) : 100),
      );
      await aoConcluir();
    } catch (erroCapturado) {
      definirErro(mensagemDoErro(erroCapturado));
    } finally {
      definirEnviando(false);
    }
  }

  const rotuloDoEnvio =
    erro !== null && registroId !== null
      ? "Tentar novamente"
      : registroId !== null
        ? "Enviar a foto ou o vídeo"
        : "Registrar a customização";

  return (
    <div className="cg-customizacao">
      {registroId === null && (
        <>
          <Campo
            rotulo="O que você customizou no kit"
            valor={descricao}
            aoAlterar={definirDescricao}
          />
          {transcreve ? (
            <>
              <Botao variante="secundaria" onClick={alternarFala} desabilitado={enviando}>
                {ouvindo ? "Parar de ouvir" : "Falar a descrição"}
              </Botao>
              {ouvindo && <p role="status">Ouvindo…</p>}
              {avisoDeFala && <Aviso tipo="atencao">{avisoDeFala}</Aviso>}
            </>
          ) : (
            <p>{MENSAGEM_SEM_TRANSCRICAO}</p>
          )}
        </>
      )}
      <AvisoDaCustomizacao />
      <div className="cg-campo">
        <label htmlFor={idDoArquivo}>Foto ou vídeo do kit</label>
        <input
          id={idDoArquivo}
          type="file"
          accept="image/*,video/*"
          capture="environment"
          onChange={(evento) => definirArquivo(evento.target.files?.[0] ?? null)}
        />
      </div>
      {progresso !== null && enviando && <p role="status">Enviando… {progresso}%</p>}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Botao onClick={registrar} desabilitado={enviando || ouvindo || faltaAlgo}>
        {rotuloDoEnvio}
      </Botao>
      <Botao variante="secundaria" onClick={aoCancelar} desabilitado={enviando}>
        Voltar
      </Botao>
    </div>
  );
}
