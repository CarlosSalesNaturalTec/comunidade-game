import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useEffect, useId, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import {
  cadastrarResponsavel,
  criarCredencialProvisoria,
  criarVinculo,
  type GuerreiroVinculavel,
  listarGuerreirosVinculaveis,
  type ResponsavelDaLista,
  type VinculoCriado,
} from "./api";

const MENSAGEM_DO_TETO =
  "Este Guerreiro(a) já tem três responsáveis vigentes — o teto por criança.";

const DADO_COLETADO =
  "o cadastro e o vínculo do responsável, e a credencial de acesso dele quando criada";

const SEM_NICK = "Guerreiro(a) sem nick";

// O grau de parentesco sozinho não identifica o vínculo: ele se repete entre
// irmãos, e duas linhas de "Pai" não dizem ao Mestre a quem cada uma se
// refere — enquanto o seletor logo acima já apresenta cada Guerreiro(a) por
// nick e avatar. O nick sai desse mesmo estado e o `guerreiro_id` vem na
// resposta do vínculo, então o cruzamento é local (`RF-09-63`, design —
// decisões 1 e 2).
//
// O avatar fica de fora: na confirmação o que distingue é o nick, e repeti-lo
// alongaria a linha sem ganho (design — decisão 2). Sem correspondência no
// estado carregado, a linha marca a ausência do nick em vez de cair no rótulo
// mudo de antes (design — decisão 3).
function rotuloDoVinculo(vinculo: VinculoCriado, guerreiros: GuerreiroVinculavel[]): string {
  const nick = guerreiros
    .find((guerreiro) => guerreiro.id === vinculo.guerreiro_id)
    ?.nick.trim();
  return `${nick || SEM_NICK} — ${vinculo.grau_de_parentesco}`;
}

interface Props {
  // Quando vem preenchido, abre direto no passo de vínculo de um responsável
  // já cadastrado, sem passar pelo cadastro: é a retomada que a lista da área
  // oferece (`RF-09-122`, design — decisão 2).
  responsavelExistente?: ResponsavelDaLista | null;
  onConcluido: () => void;
}

// Cadastro, vínculo e credencial provisória em um só fluxo — o mesmo que a
// gestão já resolve na App 03, aqui recortado pelo que o Mestre alcança: os
// Guerreiros e Guerreiras que ele pode vincular vêm do núcleo, por nick e
// avatar, nunca por identificador digitado (`RF-09-62` a `RF-09-65`,
// `RN-09-15`, `RN-09-23`, design — decisões 1 e 4).
//
// Quem emoldura é a tela da área: aqui não há `Moldura` nem `Cabecalho`,
// senão a página ganharia duas (design — decisão 3).
export function FormularioDeResponsavel({ responsavelExistente = null, onConcluido }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoCampoDeGuerreiro = useId();
  const [nome, definirNome] = useState("");
  const [responsavel, definirResponsavel] = useState<{ id: string; nome: string } | null>(
    responsavelExistente,
  );
  const [guerreiros, definirGuerreiros] = useState<GuerreiroVinculavel[]>([]);
  const [guerreiroId, definirGuerreiroId] = useState("");
  const [grauDeParentesco, definirGrauDeParentesco] = useState("");
  const [vinculos, definirVinculos] = useState<VinculoCriado[]>([]);
  const [usuario, definirUsuario] = useState("");
  const [senhaProvisoria, definirSenhaProvisoria] = useState<string | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  useEffect(() => {
    if (!sessao || responsavel === null) return;
    listarGuerreirosVinculaveis(sessao.token)
      .then((pagina) => definirGuerreiros(pagina.itens))
      .catch(() => definirGuerreiros([]));
  }, [sessao, responsavel]);

  async function aoCadastrar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErro(null);

    if (!nome.trim()) {
      definirErro("Informe o nome do responsável.");
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      const criado = await cadastrarResponsavel(nome.trim(), sessao.token);
      definirResponsavel(criado);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível cadastrar o responsável. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  async function aoVincular(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErro(null);

    if (!guerreiroId) {
      definirErro("Escolha o Guerreiro(a).");
      return;
    }
    if (!grauDeParentesco.trim()) {
      definirErro("Informe o grau de parentesco.");
      return;
    }
    if (!sessao || !responsavel) return;

    definirEnviando(true);
    try {
      const vinculo = await criarVinculo(
        responsavel.id,
        { guerreiro_id: guerreiroId, grau_de_parentesco: grauDeParentesco.trim() },
        sessao.token,
      );
      definirVinculos((atual) => [...atual, vinculo]);
      definirGuerreiroId("");
      definirGrauDeParentesco("");
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "erro_de_validacao") {
        definirErro(MENSAGEM_DO_TETO);
        return;
      }
      definirErro("Não foi possível vincular. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  async function aoCriarCredencial(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErro(null);

    if (!usuario.trim()) {
      definirErro("Informe o usuário.");
      return;
    }
    if (!sessao || !responsavel) return;

    definirEnviando(true);
    try {
      const credencial = await criarCredencialProvisoria(
        { persona_id: responsavel.id, usuario: usuario.trim() },
        sessao.token,
      );
      definirSenhaProvisoria(credencial.senha_provisoria);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível criar a credencial. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  if (responsavel === null) {
    return (
      <div>
        <p>Cadastre o responsável que se apresentou pessoalmente no encontro.</p>
        <AvisoDeColeta dado={DADO_COLETADO} />
        <form onSubmit={aoCadastrar} aria-label="Cadastro do responsável">
          <Campo rotulo="Nome do responsável" valor={nome} aoAlterar={definirNome} />
          {erro && <Aviso tipo="erro">{erro}</Aviso>}
          <Botao tipo="submit" desabilitado={enviando}>
            Cadastrar responsável
          </Botao>
        </form>
        <Botao variante="secundaria" onClick={onConcluido}>
          Voltar à lista
        </Botao>
      </div>
    );
  }

  return (
    <div>
      <AvisoDeColeta dado={DADO_COLETADO} />
      <Aviso tipo="sucesso">
        {responsavelExistente === null
          ? `Responsável cadastrado. Vincule os Guerreiros e Guerreiras de ${responsavel.nome}.`
          : `Vincule mais Guerreiros e Guerreiras a ${responsavel.nome}.`}
      </Aviso>

      {vinculos.length > 0 && (
        <ul aria-label="Vínculos já criados">
          {vinculos.map((vinculo) => (
            <li key={vinculo.id}>{rotuloDoVinculo(vinculo, guerreiros)}</li>
          ))}
        </ul>
      )}

      <form onSubmit={aoVincular} aria-label="Vincular Guerreiro(a)">
        <div className="cg-campo">
          <label htmlFor={idDoCampoDeGuerreiro}>Guerreiro(a)</label>
          <select
            id={idDoCampoDeGuerreiro}
            value={guerreiroId}
            onChange={(evento) => definirGuerreiroId(evento.target.value)}
          >
            <option value="">Selecione</option>
            {guerreiros.map((guerreiro) => (
              <option key={guerreiro.id} value={guerreiro.id}>
                {guerreiro.nick} — {guerreiro.avatar}
              </option>
            ))}
          </select>
        </div>
        <Campo
          rotulo="Grau de parentesco"
          valor={grauDeParentesco}
          aoAlterar={definirGrauDeParentesco}
        />
        {erro && <Aviso tipo="erro">{erro}</Aviso>}
        <Botao tipo="submit" desabilitado={enviando}>
          Vincular
        </Botao>
      </form>

      {senhaProvisoria === null ? (
        <form onSubmit={aoCriarCredencial} aria-label="Criar credencial de usuário e senha">
          <Campo
            rotulo="Usuário (para quem não tem conta Google)"
            valor={usuario}
            aoAlterar={definirUsuario}
          />
          <Botao tipo="submit" desabilitado={enviando}>
            Criar credencial provisória
          </Botao>
        </form>
      ) : (
        <Aviso tipo="atencao">
          Senha provisória: {senhaProvisoria} — anote agora, ela não aparece de novo.
        </Aviso>
      )}

      <Botao variante="secundaria" onClick={onConcluido}>
        Concluir
      </Botao>
    </div>
  );
}
