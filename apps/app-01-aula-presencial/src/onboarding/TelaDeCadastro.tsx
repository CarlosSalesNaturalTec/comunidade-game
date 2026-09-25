import { ErroDaApi } from "comum/api";
import {
  Avatar,
  type AvatarDoGuerreiro,
  CAMADAS_DO_AVATAR,
  escreverAvatar,
} from "comum/avatar";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import { cadastrarGuerreiroNoEncontro, type GuerreiroCadastrado } from "../api/guerreiros";

interface Props {
  tokenDeTrabalho: string;
  aulaId: string;
  aoConcluir: (guerreiro: GuerreiroCadastrado) => void;
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
// recusa.
//
// O avatar se **compõe no catálogo fechado** da camada comum, camada por
// camada, pelo nome dizível de cada traço — nunca por texto livre, que ninguém
// desenha depois (`RF-04-07`, documento 15 §7). Ele nasce no avatar padrão do
// projeto, para a criança ver um avatar completo desde o primeiro toque e
// trocar só o que quiser (design — decisão 4), e a composição acontece toda no
// aparelho: nenhuma requisição sai por causa dela.
//
// No campo `avatar`, opaco ao núcleo, viajam duas coisas: o **objeto versionado
// do documento 15 §7.2**, aninhado, e a **forma de tratamento** ao lado dele —
// campo próprio, como o §7 exige, sem coluna própria no núcleo (design —
// decisão 3).
export function TelaDeCadastro({ tokenDeTrabalho, aulaId, aoConcluir, aoVoltar }: Props) {
  const idDaFormaDeTratamento = useId();
  const idDaEscolhaDeAvatar = useId();
  const [nome, definirNome] = useState("");
  const [nick, definirNick] = useState("");
  const [formaDeTratamento, definirFormaDeTratamento] =
    useState<FormaDeTratamento>("guerreira");
  const [nascimento, definirNascimento] = useState("");
  const [avatar, definirAvatar] = useState<AvatarDoGuerreiro>(() => escreverAvatar({}));
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [variacoesDeNick, definirVariacoesDeNick] = useState<string[]>([]);
  const [idadeForaDaFaixa, definirIdadeForaDaFaixa] = useState(false);
  const [enviando, definirEnviando] = useState(false);

  function escolherTraco(camada: string, tracoId: string) {
    definirAvatar((atual) => escreverAvatar({ ...atual, [camada]: tracoId }));
  }

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
    const idade = idadeEm(nascimento, new Date());
    if (idade === null || idade < IDADE_MINIMA || idade > IDADE_MAXIMA) {
      definirIdadeForaDaFaixa(true);
      return;
    }

    definirEnviando(true);
    try {
      const guerreiro = await cadastrarGuerreiroNoEncontro(
        {
          nome: nome.trim(),
          nascimento,
          nick: nick.trim(),
          avatar: JSON.stringify({ formaDeTratamento, avatar }),
          aula_id: aulaId,
        },
        tokenDeTrabalho,
      );
      aoConcluir(guerreiro);
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
          focoInicial
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
        <fieldset className="cg-escolha-de-avatar">
          <legend>Monte o seu avatar</legend>
          <Avatar avatar={avatar} tamanho={96} />
          {CAMADAS_DO_AVATAR.map((camada) => (
            <div className="cg-campo" key={camada.nome}>
              <label htmlFor={`${idDaEscolhaDeAvatar}-${camada.nome}`}>{camada.rotulo}</label>
              <select
                id={`${idDaEscolhaDeAvatar}-${camada.nome}`}
                value={avatar[camada.nome]}
                onChange={(evento) => escolherTraco(camada.nome, evento.target.value)}
              >
                {camada.tracos.map((traco) => (
                  <option key={traco.id} value={traco.id}>
                    {traco.nome}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </fieldset>
        {erroDeCampo?.campo === "geral" && <Aviso tipo="erro">{erroDeCampo.mensagem}</Aviso>}
        <Botao tipo="submit" desabilitado={enviando}>
          {enviando ? "Cadastrando…" : "Concluir cadastro"}
        </Botao>
      </form>
    </Moldura>
  );
}
