import { ErroDaApi } from "comum/api";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import { cadastrarGuerreiroNoEncontro } from "../api/guerreiros";

interface Props {
  tokenDeTrabalho: string;
  aulaId: string;
  aoConcluir: () => void;
  aoVoltar: () => void;
}

type FormaDeTratamento = "guerreiro" | "guerreira";

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const IDADE_MINIMA = 6;
const IDADE_MAXIMA = 16;

// A idade é conta local, sem oráculo algum envolvido — ao contrário do
// nick, não há dado de outra persona em jogo (`RF-04-09`, `RN-04-11`).
function idadeEm(nascimentoIso: string, referencia: Date): number | null {
  if (!nascimentoIso) return null;
  const nascimento = new Date(`${nascimentoIso}T00:00:00`);
  if (Number.isNaN(nascimento.getTime())) return null;
  let idade = referencia.getFullYear() - nascimento.getFullYear();
  const aniversarioAindaNaoChegou =
    referencia.getMonth() < nascimento.getMonth() ||
    (referencia.getMonth() === nascimento.getMonth() &&
      referencia.getDate() < nascimento.getDate());
  if (aniversarioAindaNaoChegou) idade -= 1;
  return idade;
}

// Cadastro do encontro: formulário guiado, sem IA — a conversa conduzida
// por modelo é de fatia posterior. A tela nunca consulta disponibilidade de
// nick antes de enviar (design — decisão 6): envia o cadastro e trata a
// recusa. "Forma de tratamento" e "características do avatar" viajam
// juntas no campo `avatar`, opaco ao núcleo (`RF-04-07`).
export function TelaDeCadastro({ tokenDeTrabalho, aulaId, aoConcluir, aoVoltar }: Props) {
  const idDaFormaDeTratamento = useId();
  const [nome, definirNome] = useState("");
  const [nick, definirNick] = useState("");
  const [formaDeTratamento, definirFormaDeTratamento] =
    useState<FormaDeTratamento>("guerreira");
  const [nascimento, definirNascimento] = useState("");
  const [caracteristicasDoAvatar, definirCaracteristicasDoAvatar] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [variacoesDeNick, definirVariacoesDeNick] = useState<string[]>([]);
  const [idadeForaDaFaixa, definirIdadeForaDaFaixa] = useState(false);
  const [enviando, definirEnviando] = useState(false);

  function usarVariacao(variacao: string) {
    definirNick(variacao);
    definirVariacoesDeNick([]);
    definirErroDeCampo(null);
  }

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirVariacoesDeNick([]);

    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome." });
      return;
    }
    if (!nick.trim()) {
      definirErroDeCampo({ campo: "nick", mensagem: "Informe o nick." });
      return;
    }
    if (!nascimento) {
      definirErroDeCampo({ campo: "nascimento", mensagem: "Informe a data de nascimento." });
      return;
    }
    if (!caracteristicasDoAvatar.trim()) {
      definirErroDeCampo({
        campo: "avatar",
        mensagem: "Escolha as características do avatar.",
      });
      return;
    }

    const idade = idadeEm(nascimento, new Date());
    if (idade === null || idade < IDADE_MINIMA || idade > IDADE_MAXIMA) {
      definirIdadeForaDaFaixa(true);
      return;
    }

    definirEnviando(true);
    try {
      await cadastrarGuerreiroNoEncontro(
        {
          nome: nome.trim(),
          nascimento,
          nick: nick.trim(),
          avatar: JSON.stringify({ formaDeTratamento, caracteristicasDoAvatar }),
          aula_id: aulaId,
        },
        tokenDeTrabalho,
      );
      aoConcluir();
    } catch (erroCapturado) {
      if (erroCapturado instanceof ErroDaApi && erroCapturado.campo === "nascimento") {
        definirIdadeForaDaFaixa(true);
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.campo === "nick") {
        definirErroDeCampo({
          campo: "nick",
          mensagem: "Este nick já está em uso. Escolha uma das opções abaixo.",
        });
        definirVariacoesDeNick(erroCapturado.sugestoes ?? []);
        return;
      }
      definirErroDeCampo({
        campo: "geral",
        mensagem: "Não foi possível concluir o cadastro. Tente novamente.",
      });
    } finally {
      definirEnviando(false);
    }
  }

  if (idadeForaDaFaixa) {
    return (
      <Moldura>
        <Cabecalho
          titulo="Chame o Mestre ou o Admin"
          acao={{ rotulo: "Voltar ao início", aoAcionar: aoVoltar }}
        />
        <Aviso tipo="atencao">
          A idade informada está fora da faixa que a plataforma atende. Peça ajuda a um adulto
          da equipe.
        </Aviso>
      </Moldura>
    );
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Novo Guerreiro(a)"
        subtitulo="Vamos te conhecer! Um adulto da equipe pode ajudar a preencher."
        acao={{ rotulo: "Voltar ao início", aoAcionar: aoVoltar }}
      />
      <form onSubmit={aoSubmeter} aria-label="Cadastro do Guerreiro(a)">
        <Campo
          rotulo="Nome"
          valor={nome}
          aoAlterar={definirNome}
          erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
        />
        <Campo
          rotulo="Nick"
          valor={nick}
          aoAlterar={definirNick}
          erro={erroDeCampo?.campo === "nick" ? erroDeCampo.mensagem : null}
        />
        {variacoesDeNick.length > 0 && (
          <div className="cg-variacoes-de-nick">
            {variacoesDeNick.map((variacao) => (
              <Botao
                key={variacao}
                variante="secundaria"
                onClick={() => usarVariacao(variacao)}
              >
                {variacao}
              </Botao>
            ))}
          </div>
        )}
        <div className="cg-campo">
          <label htmlFor={idDaFormaDeTratamento}>Forma de tratamento</label>
          <select
            id={idDaFormaDeTratamento}
            value={formaDeTratamento}
            onChange={(evento) =>
              definirFormaDeTratamento(evento.target.value as FormaDeTratamento)
            }
          >
            <option value="guerreira">Guerreira</option>
            <option value="guerreiro">Guerreiro</option>
          </select>
        </div>
        <Campo
          rotulo="Data de nascimento"
          tipo="date"
          valor={nascimento}
          aoAlterar={definirNascimento}
          erro={erroDeCampo?.campo === "nascimento" ? erroDeCampo.mensagem : null}
        />
        <Campo
          rotulo="Características do avatar"
          valor={caracteristicasDoAvatar}
          aoAlterar={definirCaracteristicasDoAvatar}
          erro={erroDeCampo?.campo === "avatar" ? erroDeCampo.mensagem : null}
        />
        {erroDeCampo?.campo === "geral" && <Aviso tipo="erro">{erroDeCampo.mensagem}</Aviso>}
        <Botao tipo="submit" desabilitado={enviando}>
          {enviando ? "Cadastrando…" : "Concluir cadastro"}
        </Botao>
      </form>
    </Moldura>
  );
}
