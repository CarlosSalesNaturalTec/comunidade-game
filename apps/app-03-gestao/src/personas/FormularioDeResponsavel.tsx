import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useEffect, useId, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import {
  cadastrarResponsavel,
  criarCredencialProvisoria,
  criarVinculo,
  type GuerreiroDaLista,
  listarGuerreiros,
  type VinculoCriado,
} from "./api";

interface Props {
  onConcluido: () => void;
  onCancelar: () => void;
}

const TETO_DE_RESPONSAVEIS_POR_MENSAGEM =
  "Este Guerreiro(a) já tem três responsáveis vigentes — o teto por criança.";

const DADO_COLETADO =
  "o nome do responsável, o vínculo dele com o Guerreiro(a) e o usuário de acesso dele";

const SEM_NICK = "Guerreiro(a) sem nick";

// O grau de parentesco sozinho não identifica o vínculo: ele se repete entre
// irmãos, e duas linhas de "Pai" não dizem ao Admin a quem cada uma se refere.
// O nick sai do mesmo estado que alimenta o seletor e o `guerreiro_id` vem na
// resposta do vínculo, então o cruzamento é local — nenhuma consulta nova
// (`RF-02-06`, design — decisões 1 e 2).
//
// Sem correspondência no estado carregado, a linha marca o Guerreiro(a) como
// não identificado em vez de cair no rótulo mudo de antes: o silêncio é o
// próprio defeito que esta correção fecha (design — decisão 3).
function rotuloDoVinculo(vinculo: VinculoCriado, guerreiros: GuerreiroDaLista[]): string {
  const nick = guerreiros
    .find((guerreiro) => guerreiro.id === vinculo.guerreiro_id)
    ?.nick.trim();
  return `${nick || SEM_NICK} — ${vinculo.grau_de_parentesco}`;
}

// Cadastro, vínculo e credencial provisória em um só fluxo: o responsável
// nasce sem nenhum acesso a Guerreiro(a) algum, o vínculo declara o grau de
// parentesco, e o teto de três é do núcleo (`RF-02-06`, `RF-02-07`,
// `RN-02-08`, invariante 3 do documento 99 §6).
//
// O cadastro declara o **nome**: é sobre ele que se apoia o consentimento que
// autoriza a captura da imagem da criança, e o núcleo o exige. A tela nascera
// sem o campo e mandava o cadastro **sem corpo**, o que respondia 422 a toda
// tentativa — as Apps 09 e 01 já o mandavam.
export function FormularioDeResponsavel({ onConcluido, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoCampoDeGuerreiro = useId();
  const [nome, definirNome] = useState("");
  const [responsavelId, definirResponsavelId] = useState<string | null>(null);
  const [guerreiros, definirGuerreiros] = useState<GuerreiroDaLista[]>([]);
  const [guerreiroId, definirGuerreiroId] = useState("");
  const [grauDeParentesco, definirGrauDeParentesco] = useState("");
  const [vinculos, definirVinculos] = useState<VinculoCriado[]>([]);
  const [usuario, definirUsuario] = useState("");
  const [senhaProvisoria, definirSenhaProvisoria] = useState<string | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  useEffect(() => {
    if (!sessao || responsavelId === null) return;
    listarGuerreiros(sessao.token)
      .then((pagina) => definirGuerreiros(pagina.itens))
      .catch(() => definirGuerreiros([]));
  }, [sessao, responsavelId]);

  async function aoCadastrarResponsavel(evento: FormEvent<HTMLFormElement>) {
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
      definirResponsavelId(criado.id);
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
    if (!sessao || !responsavelId) return;

    definirEnviando(true);
    try {
      const vinculo = await criarVinculo(
        responsavelId,
        { guerreiro_id: guerreiroId, grau_de_parentesco: grauDeParentesco },
        sessao.token,
      );
      definirVinculos((atual) => [...atual, vinculo]);
      definirGrauDeParentesco("");
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "erro_de_validacao") {
        definirErro(TETO_DE_RESPONSAVEIS_POR_MENSAGEM);
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
    if (!sessao || !responsavelId) return;

    definirEnviando(true);
    try {
      const credencial = await criarCredencialProvisoria(
        { persona_id: responsavelId, usuario },
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

  if (responsavelId === null) {
    return (
      <div>
        <AvisoDeColeta dado={DADO_COLETADO} />
        <form onSubmit={aoCadastrarResponsavel} aria-label="Cadastrar responsável">
          <Campo rotulo="Nome do responsável" valor={nome} aoAlterar={definirNome} />
          {erro && <Aviso tipo="erro">{erro}</Aviso>}
          <Botao tipo="submit" desabilitado={enviando}>
            Cadastrar responsável
          </Botao>
        </form>
        <Botao variante="secundaria" onClick={onCancelar}>
          Cancelar
        </Botao>
      </div>
    );
  }

  return (
    <div>
      <AvisoDeColeta dado={DADO_COLETADO} />
      <Aviso tipo="sucesso">
        Responsável cadastrado. Vincule os Guerreiros e Guerreiras dele.
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
                {guerreiro.nick}
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
