import { ErroDaApi } from "comum/api";
import { Avatar } from "comum/avatar";
import { existeTranscricaoDeFala, iniciarTranscricao } from "comum/fala";
import {
  Aviso,
  Botao,
  Cabecalho,
  Campo,
  EstadoDaLista,
  MidiaDoNucleo,
  Moldura,
} from "comum/react";
import { useCallback, useEffect, useRef, useState } from "react";
import {
  type BemRecebido,
  capturarCustomizacao,
  enviarMidiaDaCustomizacao,
  type FonteDaPontuacao,
  julgarCustomizacao,
  lerFilaDoCuidado,
  lerMidiaDoRegistro,
  lerMidiaDoUltimoAprovado,
  type PresenteNaFila,
  validarConservacao,
} from "../api/cuidadoDoBem";

interface Props {
  tokenDeTrabalho: string;
  aulaId: string;
  aoVoltar: () => void;
}

const NOME_DA_FONTE: Record<FonteDaPontuacao, string> = {
  conservacao: "conservação",
  customizacao: "customização",
};

function tipoDaMidia(tipoDoArquivo: string | null): "imagem" | "video" | "audio" {
  if (tipoDoArquivo?.startsWith("video/")) return "video";
  if (tipoDoArquivo?.startsWith("audio/")) return "audio";
  return "imagem";
}

function mensagemDoErro(erro: unknown, padrao: string): string {
  // A recusa do núcleo já vem em linguagem simples — o bem que já pontuou no
  // encontro, o registro já julgado, a presença ausente — e a tela a
  // apresenta como ela vem (`RF-04-83`, design — decisão 7).
  return erro instanceof ErroDaApi ? erro.message : padrao;
}

// A fila do cuidado do encontro: só quem tem presença registrada nesta aula,
// por nick e avatar, com os bens que recebeu. Em cada kit, o registro novo ao
// lado do último aprovado; o Mestre aprova, reprova com motivo, captura na
// hora ou valida a conservação — por bem, uma coisa ou outra (`RF-04-81` a
// `RF-04-84`, `RN-01-66`, PRD-04 §5.13). Ato de quem opera: tudo vai sob o
// `tokenDeTrabalho`, e a fila é **relida** do núcleo depois de cada ato, bem
// ou malsucedido — o mesmo kit pode ter sido julgado em outro aparelho.
export function TelaDoCuidadoNoEncontro({ tokenDeTrabalho, aulaId, aoVoltar }: Props) {
  const [fila, definirFila] = useState<PresenteNaFila[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [sucesso, definirSucesso] = useState<string | null>(null);
  const [ocupado, definirOcupado] = useState(false);

  const carregar = useCallback(async () => {
    try {
      definirFila(await lerFilaDoCuidado(aulaId, tokenDeTrabalho));
    } catch (erroCapturado) {
      definirFila((atual) => atual ?? []);
      definirErro(
        mensagemDoErro(
          erroCapturado,
          "Não foi possível carregar a fila do encontro. Tente novamente em instantes.",
        ),
      );
    }
  }, [aulaId, tokenDeTrabalho]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  async function executar(ato: () => Promise<unknown>, confirmacao: string, padrao: string) {
    definirErro(null);
    definirSucesso(null);
    definirOcupado(true);
    try {
      await ato();
      definirSucesso(confirmacao);
    } catch (erroCapturado) {
      definirErro(mensagemDoErro(erroCapturado, padrao));
    } finally {
      await carregar();
      definirOcupado(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Customizações a julgar"
        subtitulo="Quem chegou hoje e os bens que recebeu. Cada bem pontua uma vez por encontro: pela conservação ou pela customização."
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {sucesso && <Aviso tipo="sucesso">{sucesso}</Aviso>}
      {fila === null && <EstadoDaLista>Carregando a fila do encontro…</EstadoDaLista>}
      {fila !== null && fila.length === 0 && (
        <EstadoDaLista>Nada a julgar neste encontro.</EstadoDaLista>
      )}
      {fila !== null && fila.length > 0 && (
        <ul className="cg-cuidado-do-encontro" aria-label="Fila do cuidado do encontro">
          {fila.map((presente) => {
            const nick = presente.guerreiro?.nick ?? "Guerreiro(a)";
            return (
              <li key={presente.guerreiro_id} className="cg-cuidado-do-encontro__presente">
                <p>
                  {/* Avatar desenhado e nick, e nada além disso (invariante 12). */}
                  <Avatar avatar={presente.guerreiro?.avatar ?? null} tamanho={32} />{" "}
                  <strong>{nick}</strong>
                </p>
                {presente.bens.length === 0 ? (
                  <p>Nenhum bem recebido.</p>
                ) : (
                  <ul aria-label={`Bens recebidos por ${nick}`}>
                    {presente.bens.map((bem) => (
                      <BlocoDoBem
                        key={bem.entrega_de_recompensa_id}
                        bem={bem}
                        nick={nick}
                        guerreiroId={presente.guerreiro_id}
                        aulaId={aulaId}
                        token={tokenDeTrabalho}
                        ocupado={ocupado}
                        executar={executar}
                        aoCapturar={carregar}
                      />
                    ))}
                  </ul>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </Moldura>
  );
}

interface PropsDoBem {
  bem: BemRecebido;
  nick: string;
  guerreiroId: string;
  aulaId: string;
  token: string;
  ocupado: boolean;
  executar: (
    ato: () => Promise<unknown>,
    confirmacao: string,
    padrao: string,
  ) => Promise<void>;
  aoCapturar: () => Promise<void>;
}

function BlocoDoBem({
  bem,
  nick,
  guerreiroId,
  aulaId,
  token,
  ocupado,
  executar,
  aoCapturar,
}: PropsDoBem) {
  const [reprovando, definirReprovando] = useState(false);
  const [motivo, definirMotivo] = useState("");
  const [erroDoMotivo, definirErroDoMotivo] = useState<string | null>(null);
  const [capturando, definirCapturando] = useState(false);

  const titulo = `${bem.tipo_de_recurso_nome} — ${bem.trilha_nome}`;
  const pendente = bem.pendente;

  // O bem que já pontuou neste encontro diz por qual caminho e não oferece
  // nada: conservação ou customização, nunca as duas (`RN-01-66`).
  if (bem.pontuado_na_aula) {
    return (
      <li className="cg-cuidado-do-encontro__bem">
        <p>
          <strong>{titulo}</strong>
        </p>
        <p>Já pontuou neste encontro pela {NOME_DA_FONTE[bem.pontuado_na_aula]}.</p>
      </li>
    );
  }

  function conservar() {
    return executar(
      () =>
        validarConservacao(
          aulaId,
          {
            guerreiro_id: guerreiroId,
            entrega_de_recompensa_id: bem.entrega_de_recompensa_id,
          },
          token,
        ),
      `Conservação validada: 1 ponto extra para ${nick}.`,
      "Não foi possível validar a conservação. Tente novamente em instantes.",
    );
  }

  function aprovar(registroId: string) {
    return executar(
      () => julgarCustomizacao(registroId, { aula_id: aulaId, aprovado: true }, token),
      `Customização aprovada: 1 ponto extra para ${nick}, e o registro entrou no acervo.`,
      "Não foi possível aprovar a customização. Tente novamente em instantes.",
    );
  }

  async function reprovar(registroId: string) {
    if (!motivo.trim()) {
      definirErroDoMotivo("Escreva o motivo, em linguagem simples, antes de reprovar.");
      return;
    }
    definirErroDoMotivo(null);
    await executar(
      () =>
        julgarCustomizacao(
          registroId,
          { aula_id: aulaId, aprovado: false, motivo: motivo.trim() },
          token,
        ),
      `Customização reprovada. ${nick} vai ler o motivo e pode registrar de novo.`,
      "Não foi possível reprovar a customização. Tente novamente em instantes.",
    );
    definirReprovando(false);
    definirMotivo("");
  }

  return (
    <li className="cg-cuidado-do-encontro__bem">
      <p>
        <strong>{titulo}</strong>
      </p>

      {bem.customizacao_aberta && pendente && (
        <div className="cg-cuidado-do-encontro__comparacao">
          <section aria-label="Registro novo">
            <h4>Registro novo</h4>
            {pendente.tem_midia ? (
              <MidiaDoNucleo
                id={pendente.id}
                buscar={lerMidiaDoRegistro}
                token={token}
                tipo={tipoDaMidia(pendente.tipo_do_arquivo)}
                alt={`Registro novo do kit de ${nick}`}
                textoDeErro="Não foi possível abrir o registro novo."
                ampliavel
              />
            ) : (
              <p>Aguardando o envio da foto ou do vídeo.</p>
            )}
            <p>{pendente.descricao}</p>
          </section>
          <section aria-label="Último registro aprovado">
            <h4>Último registro aprovado</h4>
            {bem.ultimo_aprovado?.tipo_do_arquivo ? (
              <MidiaDoNucleo
                id={bem.entrega_de_recompensa_id}
                buscar={lerMidiaDoUltimoAprovado}
                token={token}
                tipo={tipoDaMidia(bem.ultimo_aprovado.tipo_do_arquivo)}
                alt={`Último registro aprovado do kit de ${nick}`}
                textoDeErro="Não foi possível abrir o último registro aprovado."
                ampliavel
              />
            ) : (
              <p>O último registro aprovado não tem foto nem vídeo.</p>
            )}
            {bem.ultimo_aprovado?.descricao && <p>{bem.ultimo_aprovado.descricao}</p>}
          </section>
        </div>
      )}

      <div className="cg-cuidado-do-encontro__acoes">
        <Botao variante="secundaria" onClick={conservar} desabilitado={ocupado}>
          Validar a conservação
        </Botao>
        {bem.customizacao_aberta && pendente?.tem_midia && !reprovando && (
          <>
            <Botao onClick={() => aprovar(pendente.id)} desabilitado={ocupado}>
              Aprovar a customização
            </Botao>
            <Botao
              variante="secundaria"
              onClick={() => definirReprovando(true)}
              desabilitado={ocupado}
            >
              Reprovar a customização
            </Botao>
          </>
        )}
        {bem.customizacao_aberta && !pendente && !capturando && (
          <Botao
            variante="secundaria"
            onClick={() => definirCapturando(true)}
            desabilitado={ocupado}
          >
            Registrar a customização agora
          </Botao>
        )}
        {bem.customizacao_aberta && pendente && !pendente.tem_midia && !capturando && (
          <Botao
            variante="secundaria"
            onClick={() => definirCapturando(true)}
            desabilitado={ocupado}
          >
            Enviar a foto ou o vídeo
          </Botao>
        )}
      </div>

      {reprovando && pendente && (
        <div className="cg-cuidado-do-encontro__reprovacao">
          <Campo
            rotulo="Motivo da reprovação"
            valor={motivo}
            aoAlterar={definirMotivo}
            erro={erroDoMotivo}
            focoInicial
          />
          <Botao onClick={() => reprovar(pendente.id)} desabilitado={ocupado}>
            Confirmar a reprovação
          </Botao>
          <Botao
            variante="secundaria"
            onClick={() => {
              definirReprovando(false);
              definirErroDoMotivo(null);
            }}
          >
            Cancelar
          </Botao>
        </div>
      )}

      {capturando && bem.customizacao_aberta && !pendente?.tem_midia && (
        <CapturaNaHora
          registroIdInicial={pendente?.id ?? null}
          bem={bem}
          nick={nick}
          guerreiroId={guerreiroId}
          aulaId={aulaId}
          token={token}
          aoConcluir={async () => {
            definirCapturando(false);
            await aoCapturar();
          }}
          aoCancelar={() => definirCapturando(false)}
        />
      )}
    </li>
  );
}

const MENSAGEM_SEM_TRANSCRICAO = "Este aparelho não transcreve fala. Escreva a descrição.";
const MENSAGEM_DE_FALHA_NA_FALA = "Não foi possível entender a fala. Fale de novo ou escreva.";

interface PropsDaCaptura {
  /** O pendente sem mídia: a captura só retoma o envio dele. */
  registroIdInicial: string | null;
  bem: BemRecebido;
  nick: string;
  guerreiroId: string;
  aulaId: string;
  token: string;
  aoConcluir: () => Promise<void>;
  aoCancelar: () => void;
}

// A captura na hora, em nome da criança presente: a foto ou o vídeo **só do
// kit** e a descrição dela, dita ou escrita. A fala é transcrita no próprio
// aparelho e cai no campo, editável; ao núcleo vai só o texto. Registro
// gravado com o envio interrompido — aqui ou antes, no pendente sem mídia —
// retoma o envio do **mesmo** registro, sem criar outro (`RF-04-82`, PRD-04
// §5.13.3, design — decisão 5).
function CapturaNaHora({
  registroIdInicial,
  bem,
  nick,
  guerreiroId,
  aulaId,
  token,
  aoConcluir,
  aoCancelar,
}: PropsDaCaptura) {
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
  const idDoArquivo = `captura-${bem.entrega_de_recompensa_id}`;

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

  async function registrar() {
    definirErro(null);
    if (!registroId && !descricao.trim()) {
      definirErro("Escreva ou fale a descrição da customização antes de registrar.");
      return;
    }
    if (!arquivo) {
      definirErro("Escolha a foto ou o vídeo do kit antes de registrar.");
      return;
    }
    definirEnviando(true);
    try {
      let id = registroId;
      if (!id) {
        const registro = await capturarCustomizacao(
          aulaId,
          {
            guerreiro_id: guerreiroId,
            entrega_de_recompensa_id: bem.entrega_de_recompensa_id,
            descricao: descricao.trim(),
          },
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
      definirErro(
        mensagemDoErro(
          erroCapturado,
          "A conexão caiu no meio do envio. Quando ela voltar, toque em Enviar a foto ou o vídeo.",
        ),
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <div className="cg-cuidado-do-encontro__captura">
      <p>
        Registro da customização de {nick}: foto ou vídeo <strong>só do kit, sem rosto</strong>
        , e a descrição dita ou escrita pela criança.
      </p>
      {!registroId && (
        <>
          <Campo
            rotulo="Descrição da customização"
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
      <Botao onClick={registrar} desabilitado={enviando || ouvindo}>
        {registroId ? "Enviar a foto ou o vídeo" : "Registrar a customização"}
      </Botao>
      <Botao variante="secundaria" onClick={aoCancelar} desabilitado={enviando}>
        Cancelar
      </Botao>
    </div>
  );
}
