import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as sessaoApi from "comum/autenticacao/api";
import * as biometriaModulo from "comum/biometria";
import { ProvedorDeNarracao } from "comum/narracao";
import * as trilhaApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as descritorApi from "../api/descritor";
import * as equipesApi from "../api/equipes";
import * as presencasApi from "../api/presencas";
import * as sessoesDeGuerreiroApi from "../api/sessoesDeGuerreiro";
import { enfileirarPresenca, lerFilaDePresenca } from "../fila/filaDePresenca";
import { guardarVerificadorDeTeste, PIN_DE_TESTE } from "../pin/paraTestes";
import {
  estadoDoPinDe,
  guardarVerificadorDoPin,
  marcarPinBloqueado,
} from "../pin/pinDeConfirmacao";
import { ProvedorDeEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";
import { TelaInicial } from "./TelaInicial";

function mockarRegistrarPresencaEcoando() {
  return vi.spyOn(presencasApi, "registrarPresenca").mockImplementation((aulaId, entrada) =>
    Promise.resolve({
      id: "presenca-1",
      aula_id: aulaId,
      guerreiro_id: entrada.guerreiro_id,
      modo: entrada.modo,
      confirmador_id: entrada.modo === "confirmacao" ? "mestre-de-trabalho-1" : null,
      momento_do_fato: entrada.momento_do_fato,
    }),
  );
}

function mockarPresencaNoEncontro(presente: boolean) {
  return vi.spyOn(presencasApi, "lerMinhaPresenca").mockResolvedValue({
    presente,
    momento_do_fato: presente ? new Date().toISOString() : null,
    modo: presente ? "reconhecimento" : null,
  });
}

// O caminho das equipes abre a sessão e não registra presença: a guarda é
// que confere se ela existe (`RF-04-67`, `RF-04-68`).
async function entrarPorConfirmacao(
  usuario: ReturnType<typeof userEvent.setup>,
  nick = "zeferina",
) {
  await usuario.click(screen.getByRole("button", { name: /equipes —/i }));
  await usuario.type(await screen.findByLabelText(/nick/i), nick);
  await usuario.click(screen.getByRole("button", { name: /entrar/i }));
  await usuario.type(await screen.findByLabelText(/pin de quem confirma/i), "4821");
  await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
  localStorage.clear();
});

function renderizar(
  aoVoltarAoInicio = vi.fn(),
  props: Partial<{
    podeAbrirMomentoDeTroca: boolean;
    momentoDeTrocaAberto: boolean;
    abrindoMomentoDeTroca: boolean;
    erroDeAberturaDaTroca: string | null;
    papelDeTrabalho: string;
  }> = {},
  aoEncerrarSessaoDeTrabalho = vi.fn(),
) {
  return render(
    <ProvedorDeNarracao>
      <ProvedorDeEstadoDeRede>
        <ProvedorDeSessao chaveDeArmazenamento="teste:app-01:sessao-guerreiro">
          <TelaInicial
            tokenDeTrabalho="token-de-trabalho"
            personaIdDeTrabalho="mestre-de-trabalho-1"
            papelDeTrabalho={props.papelDeTrabalho ?? "mestre"}
            aulaId="aula-1"
            aoVoltarAoInicio={aoVoltarAoInicio}
            podeAbrirMomentoDeTroca={props.podeAbrirMomentoDeTroca ?? false}
            momentoDeTrocaAberto={props.momentoDeTrocaAberto ?? false}
            abrindoMomentoDeTroca={props.abrindoMomentoDeTroca ?? false}
            erroDeAberturaDaTroca={props.erroDeAberturaDaTroca ?? null}
            aoAbrirMomentoDeTroca={vi.fn()}
            aoFecharMomentoDeTroca={vi.fn()}
            aoEncerrarSessaoDeTrabalho={aoEncerrarSessaoDeTrabalho}
          />
        </ProvedorDeSessao>
      </ProvedorDeEstadoDeRede>
    </ProvedorDeNarracao>,
  );
}

describe("tela inicial da App 01", () => {
  it("os três caminhos aparecem, e os três estão habilitados", async () => {
    renderizar();

    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /onboarding/i })).toBeEnabled();
    expect(screen.getByRole("button", { name: /presença — entrar/i })).toBeEnabled();
    expect(screen.getByRole("button", { name: /equipes —/i })).toBeEnabled();
  });

  // O glifo entra ao lado do rótulo, nunca no lugar dele: os testes localizam
  // os caminhos pelo rótulo, e o desenho não pode roubar essa localização
  // (`RF-04-01`, documento 15 §§5, 11.1).
  it("cada caminho leva glifo ao lado do rótulo", async () => {
    renderizar(vi.fn(), { momentoDeTrocaAberto: true });

    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();

    const rotulos = [
      "Onboarding — cadastro do Guerreiro(a) e presença do dia",
      "Presença — entrar com o nick e registrar a presença de hoje",
      "Equipes — formar a equipe e trabalhar a trilha",
      "Quiz ao Vivo — entrar com o nick e responder pela equipe",
      "Medição do limiar — calibrar o reconhecimento facial deste ponto de apoio",
      "Troca por recompensa avulsa — entregar uma recompensa do encontro",
      "Trilhas e missões — ver o seu percurso e as atividades do encontro",
    ];

    for (const rotulo of rotulos) {
      // O rótulo continua sendo o nome acessível inteiro do botão: o glifo é
      // decorativo e não acrescenta nem substitui palavra alguma.
      const caminho = screen.getByRole("button", { name: rotulo });
      expect(caminho).toHaveTextContent(rotulo);
      // E o glifo está ali, junto do rótulo.
      expect(caminho.querySelector("svg")).not.toBeNull();
    }
  });

  it("nenhum caminho se identifica só pelo desenho", async () => {
    renderizar(vi.fn(), { momentoDeTrocaAberto: true, podeAbrirMomentoDeTroca: true });
    await screen.findByText(/o que você quer fazer/i);

    for (const caminho of screen.getAllByRole("button")) {
      const glifo = caminho.querySelector("svg");
      if (!glifo) continue;
      // O desenho não fala por si: é escondido da tecnologia assistiva, e o
      // botão que o leva tem rótulo — visível ou acessível, que é o que o
      // documento 15 §5 exige. O alternador do som é o único de glifo só, e o
      // rótulo dele vive em `aria-label`.
      expect(glifo).toHaveAttribute("aria-hidden", "true");
      const rotulo = caminho.getAttribute("aria-label") ?? caminho.textContent ?? "";
      expect(rotulo.trim()).not.toBe("");
    }
  });

  it("onboarding leva à tela de cadastro do Guerreiro(a)", async () => {
    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /onboarding/i }));

    expect(await screen.findByText(/novo guerreiro/i)).toBeInTheDocument();
  });

  it("equipes sem sessão leva à entrada do Guerreiro(a), nunca ao cadastro", async () => {
    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /equipes —/i }));

    // A entrada anuncia o caminho que serve, e não o da presença: quem escolheu
    // Equipes precisa reconhecer que chegou onde quis (`RF-04-01`, `RF-04-67`).
    expect(await screen.findByText(/quem vai formar equipe/i)).toBeInTheDocument();
    expect(screen.queryByText(/quem está chegando/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/cadastr/i)).not.toBeInTheDocument();
  });

  // Os quatro caminhos passam pela mesma tela de entrada: sem título próprio,
  // quem opera não distingue onde chegou (`RF-04-01`, `RF-04-67`, `RF-04-68`).
  it("a entrada anuncia o caminho que serve, e não o da presença", async () => {
    const usuario = userEvent.setup();

    const presenca = renderizar();
    await usuario.click(screen.getByRole("button", { name: /presença — entrar/i }));
    expect(await screen.findByText(/quem está chegando/i)).toBeInTheDocument();
    presenca.unmount();

    const quiz = renderizar();
    await usuario.click(screen.getByRole("button", { name: /quiz ao vivo/i }));
    expect(await screen.findByText(/quem vai jogar o quiz/i)).toBeInTheDocument();
    expect(screen.queryByText(/quem está chegando/i)).not.toBeInTheDocument();
    quiz.unmount();

    renderizar(vi.fn(), { momentoDeTrocaAberto: true });
    await usuario.click(screen.getByRole("button", { name: /troca por recompensa avulsa/i }));
    expect(await screen.findByText(/quem vai trocar recompensa/i)).toBeInTheDocument();
    expect(screen.queryByText(/quem está chegando/i)).not.toBeInTheDocument();
  });

  // A entrada por confirmação é a outra forma da mesma tela, e anuncia o
  // caminho do mesmo jeito (`RF-04-01`, design — decisão 2).
  it("a entrada por confirmação de Mestre também anuncia o caminho", async () => {
    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /equipes —/i }));
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));

    expect(await screen.findByLabelText(/pin de quem confirma/i)).toBeInTheDocument();
    expect(screen.getByText(/quem vai formar equipe/i)).toBeInTheDocument();
    expect(screen.queryByText(/quem está chegando/i)).not.toBeInTheDocument();
  });

  it("no caminho da presença, a confirmação do Mestre registra a presença e termina o atendimento", async () => {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    const listarEquipes = vi.spyOn(equipesApi, "listarEquipesDaAula");
    const registrarPresenca = mockarRegistrarPresencaEcoando();

    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /presença — entrar/i }));
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));
    await usuario.type(await screen.findByLabelText(/pin de quem confirma/i), "4821");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    expect(await screen.findByText(/presença registrada/i)).toBeInTheDocument();
    expect(registrarPresenca).toHaveBeenCalledWith(
      "aula-1",
      expect.objectContaining({ guerreiro_id: "guerreiro-1", modo: "confirmacao" }),
      "token-de-trabalho",
    );
    // `RF-04-67`: o caminho da presença não leva às equipes.
    expect(screen.queryByText(/equipes desta aula/i)).not.toBeInTheDocument();
    expect(listarEquipes).not.toHaveBeenCalled();
  });

  it("o caminho das equipes abre a sessão sem registrar presença e mostra as equipes", async () => {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const registrarPresenca = mockarRegistrarPresencaEcoando();
    mockarPresencaNoEncontro(true);

    renderizar();
    const usuario = userEvent.setup();
    await entrarPorConfirmacao(usuario);

    expect(await screen.findByText(/equipes desta aula/i)).toBeInTheDocument();
    expect(registrarPresenca).not.toHaveBeenCalled();
  });

  it("sem presença registrada, o caminho das equipes não abre e oferece o caminho da presença", async () => {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(sessaoApi, "encerrarSessao").mockResolvedValue(undefined);
    const listarEquipes = vi.spyOn(equipesApi, "listarEquipesDaAula");
    mockarPresencaNoEncontro(false);

    renderizar();
    const usuario = userEvent.setup();
    await entrarPorConfirmacao(usuario);

    expect(await screen.findByText(/registre a presença primeiro/i)).toBeInTheDocument();
    expect(listarEquipes).not.toHaveBeenCalled();

    // O encaminhamento encerra a sessão aberta aqui (`RF-04-28`).
    await usuario.click(screen.getByRole("button", { name: /registrar a presença/i }));
    expect(await screen.findByText(/quem está chegando/i)).toBeInTheDocument();
    expect(sessaoApi.encerrarSessao).toHaveBeenCalledWith("token-do-guerreiro");
  });

  it("sem presença registrada, o caminho do quiz recusa do mesmo modo", async () => {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    mockarPresencaNoEncontro(false);

    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /quiz ao vivo/i }));
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));
    await usuario.type(await screen.findByLabelText(/pin de quem confirma/i), "4821");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    expect(await screen.findByText(/registre a presença primeiro/i)).toBeInTheDocument();
  });

  // --- O caminho das trilhas e missões (`RF-04-72`, `RF-04-01`, `RN-04-40`)

  it("a tela inicial leva às trilhas de quem já tem presença", async () => {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    const registrarPresenca = mockarRegistrarPresencaEcoando();
    mockarPresencaNoEncontro(true);
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([]);
    vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([]);
    vi.spyOn(equipesApi, "listarMinhasEquipes").mockResolvedValue([]);

    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /trilhas e missões/i }));
    // A entrada anuncia o caminho que serve, como nos demais.
    expect(await screen.findByText(/quem vai ver as próprias trilhas/i)).toBeInTheDocument();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));
    await usuario.type(await screen.findByLabelText(/pin de quem confirma/i), "4821");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    expect(
      await screen.findByRole("heading", { name: /trilhas e missões/i }),
    ).toBeInTheDocument();
    // O caminho abre a sessão e NUNCA registra presença (`RF-04-72`).
    expect(registrarPresenca).not.toHaveBeenCalled();
  });

  it("sem presença, o caminho das trilhas não abre", async () => {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    mockarPresencaNoEncontro(false);
    const listarTrilhas = vi.spyOn(trilhaApi, "listarMinhasTrilhas");

    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /trilhas e missões/i }));
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));
    await usuario.type(await screen.findByLabelText(/pin de quem confirma/i), "4821");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    // A mesma recusa dos caminhos das equipes, do quiz e da troca
    // (`RN-04-40`), e o mesmo encaminhamento ao caminho da presença.
    expect(await screen.findByText(/registre a presença primeiro/i)).toBeInTheDocument();
    expect(listarTrilhas).not.toHaveBeenCalled();
  });

  it("o caminho da presença continua não levando às equipes", async () => {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    mockarRegistrarPresencaEcoando();
    mockarPresencaNoEncontro(true);
    const listarEquipes = vi.spyOn(equipesApi, "listarEquipesDaAula");
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([]);
    vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([]);
    vi.spyOn(equipesApi, "listarMinhasEquipes").mockResolvedValue([]);

    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /presença — entrar/i }));
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));
    await usuario.type(await screen.findByLabelText(/pin de quem confirma/i), "4821");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    // Registrada a presença, quem chegou segue às trilhas pelo desfecho — e
    // nenhuma tela de equipe da aula aparece nesse atendimento (`RF-04-67`).
    await usuario.click(
      await screen.findByRole("button", { name: /ver as minhas trilhas e missões/i }),
    );
    expect(
      await screen.findByRole("heading", { name: /trilhas e missões/i }),
    ).toBeInTheDocument();
    expect(screen.queryByText(/equipes desta aula/i)).not.toBeInTheDocument();
    expect(listarEquipes).not.toHaveBeenCalled();
  });

  it("voltar ao início encerra a sessão do Guerreiro(a) e limpa a tela", async () => {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(sessaoApi, "encerrarSessao").mockResolvedValue(undefined);
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    mockarPresencaNoEncontro(true);

    const aoVoltarAoInicio = vi.fn();
    renderizar(aoVoltarAoInicio);
    const usuario = userEvent.setup();
    await entrarPorConfirmacao(usuario);
    await screen.findByText(/equipes desta aula/i);

    await usuario.click(screen.getByRole("button", { name: /voltar ao início/i }));

    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
    expect(sessaoApi.encerrarSessao).toHaveBeenCalledWith("token-do-guerreiro");
    // A volta ao início relê a janela da aula — design decisão 3.
    expect(aoVoltarAoInicio).toHaveBeenCalled();
  });

  it("a sessão aberta por confirmação habilita o recadastro, com o identificador vindo dela", async () => {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    mockarPresencaNoEncontro(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.4, 0.5, 0.6]);
    const enviarDescritor = vi.spyOn(descritorApi, "enviarDescritor").mockResolvedValue({
      guerreiro_id: "guerreiro-1",
      gravado_em: new Date().toISOString(),
    });

    renderizar();
    const usuario = userEvent.setup();
    await entrarPorConfirmacao(usuario);
    await screen.findByText(/equipes desta aula/i);

    const botaoDeRecadastro = screen.getByRole("button", { name: /recadastrar imagem/i });
    await usuario.click(botaoDeRecadastro);
    await usuario.click(await screen.findByRole("button", { name: /iniciar captura/i }));

    await vi.waitFor(() =>
      expect(enviarDescritor).toHaveBeenCalledWith(
        "guerreiro-1",
        { descritor: [0.4, 0.5, 0.6] },
        "token-de-trabalho",
      ),
    );
    // Nenhuma rota de nick para identificador foi chamada — o identificador
    // veio da sessão aberta por confirmação presencial (`RN-01-22`).
    expect(sessoesDeGuerreiroApi.confirmarSessaoDeGuerreiro).toHaveBeenCalledTimes(1);
  });

  it("a sessão aberta por reconhecimento não oferece o recadastro", async () => {
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    mockarPresencaNoEncontro(true);

    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /equipes —/i }));
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));

    expect(await screen.findByText(/equipes desta aula/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /recadastrar imagem/i }),
    ).not.toBeInTheDocument();
  });

  it("o caminho da troca não aparece com o momento de troca fechado", async () => {
    renderizar(vi.fn(), { momentoDeTrocaAberto: false });

    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /troca por recompensa/i }),
    ).not.toBeInTheDocument();
  });

  it("o caminho da troca aparece com o momento aberto e leva à entrada, não ao cadastro", async () => {
    renderizar(vi.fn(), { momentoDeTrocaAberto: true });
    const usuario = userEvent.setup();

    const caminhoDeTroca = await screen.findByRole("button", {
      name: /troca por recompensa/i,
    });
    await usuario.click(caminhoDeTroca);

    expect(await screen.findByText(/quem vai trocar recompensa/i)).toBeInTheDocument();
    expect(screen.queryByText(/cadastr/i)).not.toBeInTheDocument();
  });

  it("o caminho do quiz está presente com o momento de troca fechado, e leva à entrada sem sessão aberta", async () => {
    renderizar(vi.fn(), { momentoDeTrocaAberto: false });
    const usuario = userEvent.setup();

    const caminhoDoQuiz = await screen.findByRole("button", { name: /quiz ao vivo/i });
    await usuario.click(caminhoDoQuiz);

    expect(await screen.findByText(/quem vai jogar o quiz/i)).toBeInTheDocument();
    expect(screen.queryByText(/cadastr/i)).not.toBeInTheDocument();
  });

  it("sem rede, o onboarding não abre e nenhum dado é coletado", async () => {
    renderizar();
    window.dispatchEvent(new Event("offline"));
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /onboarding/i }));

    expect(await screen.findByText(/onboarding indisponível sem rede/i)).toBeInTheDocument();
    expect(
      screen.getByText(/o cadastro de um novo guerreiro\(a\) exige rede/i),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /concluir cadastro/i }),
    ).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/^nome$/i)).not.toBeInTheDocument();
  });

  it("falha ao conferir a presença aparece como falha, nunca como falta de presença", async () => {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(presencasApi, "lerMinhaPresenca").mockRejectedValue(new Error("rede fora"));

    renderizar();
    const usuario = userEvent.setup();
    await entrarPorConfirmacao(usuario);

    // `RN-04-36`: quem não conseguiu perguntar não descobriu nada sobre a
    // criança, e não manda registrar presença.
    expect(await screen.findByText(/não deu para conferir/i)).toBeInTheDocument();
    expect(screen.queryByText(/registre a presença primeiro/i)).not.toBeInTheDocument();
  });

  it("sem rede, a entrada por reconhecimento não é oferecida e encaminha à confirmação humana", async () => {
    renderizar();
    window.dispatchEvent(new Event("offline"));
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /presença — entrar/i }));

    expect(
      await screen.findByText(/entrada por reconhecimento facial não funciona/i),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /confirmar identidade/i })).toBeInTheDocument();
    expect(screen.queryByText(/digite o nick e olhe para a câmera/i)).not.toBeInTheDocument();
  });
});

// A saída do aparelho, que nasce nesta fatia: só na tela inicial, atrás do PIN
// de quem abriu a sessão de trabalho, e com alternativa quando o PIN bloqueia
// (`RF-04-71`, `RN-04-41`).
describe("encerrar a sessão de trabalho pela tela inicial (RF-04-71, RN-04-41)", () => {
  const PERSONA_DE_TRABALHO = "mestre-de-trabalho-1";

  async function abrirOEncerramento(usuario: ReturnType<typeof userEvent.setup>) {
    await usuario.click(
      await screen.findByRole("button", { name: /encerrar a sessão de trabalho/i }),
    );
  }

  async function digitarOPin(usuario: ReturnType<typeof userEvent.setup>, pin = PIN_DE_TESTE) {
    await usuario.type(await screen.findByLabelText(/pin de quem abriu o aparelho/i), pin);
    await usuario.click(
      screen.getByRole("button", { name: /^encerrar a sessão de trabalho$/i }),
    );
  }

  it("a saída aparece na tela inicial e não nas telas de atendimento", async () => {
    await guardarVerificadorDeTeste(PERSONA_DE_TRABALHO);
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    mockarPresencaNoEncontro(true);

    renderizar();
    const usuario = userEvent.setup();
    expect(
      await screen.findByRole("button", { name: /encerrar a sessão de trabalho/i }),
    ).toBeInTheDocument();

    await entrarPorConfirmacao(usuario);
    await screen.findByText(/equipes desta aula/i);

    // No meio do atendimento, quem está com o aparelho é a criança: a saída
    // NEVER é oferecida ali (`RF-04-28`, design — decisão 2).
    expect(
      screen.queryByRole("button", { name: /encerrar a sessão de trabalho/i }),
    ).not.toBeInTheDocument();
  });

  it("encerra com o PIN de quem abriu o aparelho", async () => {
    await guardarVerificadorDeTeste(PERSONA_DE_TRABALHO);
    const encerrar = vi.fn();

    renderizar(vi.fn(), {}, encerrar);
    const usuario = userEvent.setup();
    await abrirOEncerramento(usuario);
    await digitarOPin(usuario);

    await waitFor(() => expect(encerrar).toHaveBeenCalled());
  });

  it("PIN errado recusa o encerramento e conta no contador de sempre", async () => {
    await guardarVerificadorDeTeste(PERSONA_DE_TRABALHO);
    const encerrar = vi.fn();

    renderizar(vi.fn(), {}, encerrar);
    const usuario = userEvent.setup();
    await abrirOEncerramento(usuario);
    await digitarOPin(usuario, "0000");

    expect(await screen.findByText(/pin errado/i)).toBeInTheDocument();
    expect(encerrar).not.toHaveBeenCalled();
    // O mesmo contador da confirmação de identidade e da bancada (`RN-04-41`).
    expect(estadoDoPinDe(PERSONA_DE_TRABALHO)?.erros).toBe(1);
  });

  it("PIN bloqueado recusa, e a recusa diz que fechar a aba encerra a sessão", async () => {
    await guardarVerificadorDeTeste(PERSONA_DE_TRABALHO);
    marcarPinBloqueado();
    const encerrar = vi.fn();

    renderizar(vi.fn(), {}, encerrar);
    const usuario = userEvent.setup();
    await abrirOEncerramento(usuario);

    expect(await screen.findByText(/pin bloqueado neste aparelho/i)).toBeInTheDocument();
    expect(
      screen.getByText(/fechar a aba do navegador encerra a sessão/i),
    ).toBeInTheDocument();
    expect(screen.queryByLabelText(/pin de quem abriu o aparelho/i)).not.toBeInTheDocument();
    expect(encerrar).not.toHaveBeenCalled();
  });

  it("quem abriu o aparelho sem PIN cadastrado encerra sem PIN, com o aviso", async () => {
    guardarVerificadorDoPin(PERSONA_DE_TRABALHO, null);
    const encerrar = vi.fn();

    renderizar(vi.fn(), {}, encerrar);
    const usuario = userEvent.setup();
    await abrirOEncerramento(usuario);

    expect(await screen.findByText(/ainda não tem pin de confirmação/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/pin de quem abriu o aparelho/i)).not.toBeInTheDocument();

    await usuario.click(
      screen.getByRole("button", { name: /^encerrar a sessão de trabalho$/i }),
    );
    await waitFor(() => expect(encerrar).toHaveBeenCalled());
  });

  it("a fila local pendente é anunciada antes de encerrar, e sobrevive ao encerramento", async () => {
    await guardarVerificadorDeTeste(PERSONA_DE_TRABALHO);
    // A fila não sincroniza neste teste: sem resposta do núcleo, o item fica
    // onde está (`RF-04-25`).
    vi.spyOn(presencasApi, "registrarPresencaSemRede").mockRejectedValue(
      new Error("rede fora"),
    );
    enfileirarPresenca({
      aula_id: "aula-1",
      nick: "zeferina",
      momento_do_fato: "2026-09-25T14:00:00Z",
    });
    enfileirarPresenca({
      aula_id: "aula-1",
      nick: "joao",
      momento_do_fato: "2026-09-25T14:01:00Z",
    });
    const encerrar = vi.fn();

    renderizar(vi.fn(), {}, encerrar);
    const usuario = userEvent.setup();
    await abrirOEncerramento(usuario);

    expect(await screen.findByText(/2 presenças aguardam sincronização/i)).toBeInTheDocument();
    expect(screen.getByText(/aberto nesta mesma aula/i)).toBeInTheDocument();

    await digitarOPin(usuario);

    await waitFor(() => expect(encerrar).toHaveBeenCalled());
    // Nada se perde: a fila vive em `localStorage` e não sai com a sessão
    // (`RF-04-23`, `RF-04-25`).
    expect(lerFilaDePresenca("aula-1")).toHaveLength(2);
  });
});

describe("o alternador do som no canto do cabeçalho (documento 15 §5.1)", () => {
  class EnunciadoFalso {
    lang = "";
    voice: SpeechSynthesisVoice | null = null;
    text: string;

    constructor(text: string) {
      this.text = text;
    }
  }

  class MotorDeFalaFalso {
    ditos: EnunciadoFalso[] = [];

    getVoices() {
      return [
        {
          lang: "pt-BR",
          localService: true,
          name: "local",
          default: true,
          voiceURI: "local",
        } as SpeechSynthesisVoice,
      ];
    }

    speak(dito: EnunciadoFalso) {
      this.ditos.push(dito);
    }

    cancel() {}

    addEventListener() {}

    removeEventListener() {}
  }

  function instalarMotorDeFalaFalso() {
    const motor = new MotorDeFalaFalso();
    vi.stubGlobal("speechSynthesis", motor);
    vi.stubGlobal("SpeechSynthesisUtterance", EnunciadoFalso);
    return motor;
  }

  const ROTULO_LIGAR = "Ligar a leitura das telas em voz alta";
  const ROTULO_DESLIGAR = "Desligar a leitura das telas em voz alta";

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("o alternador aparece no canto do cabeçalho, só pelo glifo, e nasce desligado", async () => {
    renderizar();

    const alternador = await screen.findByRole("button", { name: ROTULO_LIGAR });
    // Está no cabeçalho, ao lado do título — não numa faixa própria.
    expect(alternador.closest("header")).not.toBeNull();
    // É só o glifo: nenhum texto visível, e o estado em `aria-pressed`.
    expect(alternador.textContent).toBe("");
    expect(alternador.querySelector("svg")).not.toBeNull();
    expect(alternador).toHaveAttribute("aria-pressed", "false");
    // A frase que descrevia o estado por escrito saiu da tela.
    expect(screen.queryByText(/a narração está/i)).not.toBeInTheDocument();
  });

  it("ligar troca o glifo e o rótulo, e marca o pressionado", async () => {
    renderizar();
    const usuario = userEvent.setup();

    const desligado = await screen.findByRole("button", { name: ROTULO_LIGAR });
    const glifoDesligado = desligado.querySelector("svg")?.innerHTML;
    await usuario.click(desligado);

    const ligado = screen.getByRole("button", { name: ROTULO_DESLIGAR });
    expect(ligado).toHaveAttribute("aria-pressed", "true");
    // O estado se reconhece pela forma, não pela cor.
    expect(ligado.querySelector("svg")?.innerHTML).not.toBe(glifoDesligado);
  });

  it("a escolha sobrevive ao atendimento seguinte no mesmo aparelho", async () => {
    const aoVoltarAoInicio = vi.fn();
    renderizar(aoVoltarAoInicio);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: ROTULO_LIGAR }));
    // O atendimento seguinte é a volta ao início, dentro da mesma sessão do
    // aparelho: a escolha é do aparelho, não do atendimento.
    await usuario.click(screen.getByRole("button", { name: /presença — entrar/i }));
    await usuario.click(await screen.findByRole("button", { name: /^voltar$/i }));

    expect(await screen.findByRole("button", { name: ROTULO_DESLIGAR })).toBeInTheDocument();
  });

  it("a recarga da aplicação devolve o som ao desligado", async () => {
    const primeira = renderizar();
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: ROTULO_LIGAR }));
    // Recarregar monta o provedor de novo, e nada foi gravado de onde ler a
    // escolha anterior (decisão do fundador de 2026-10-14).
    primeira.unmount();
    renderizar();

    expect(await screen.findByRole("button", { name: ROTULO_LIGAR })).toBeInTheDocument();
  });

  it("a escolha não é gravada no aparelho", async () => {
    renderizar();
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: ROTULO_LIGAR }));

    expect(localStorage.getItem("cg:narracao")).toBeNull();
  });

  it("nenhuma outra tela apresenta o alternador", async () => {
    renderizar();
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /presença — entrar/i }));

    await screen.findByRole("button", { name: /^voltar$/i });
    expect(screen.queryByRole("button", { name: ROTULO_LIGAR })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: ROTULO_DESLIGAR })).not.toBeInTheDocument();
  });

  it("a tela inicial fala o título dela, e nenhum rótulo de botão", async () => {
    const motor = instalarMotorDeFalaFalso();
    renderizar();
    const usuario = userEvent.setup();

    // Ligar é o gesto que arma, e a tela já montada passa a ser falada.
    await usuario.click(await screen.findByRole("button", { name: ROTULO_LIGAR }));

    // O que fala é o título da tela — nunca o subtítulo, nunca o rótulo de um
    // caminho, nunca o do cartão de encerrar (documento 15 §5.1).
    const ditos = motor.ditos.map((dito) => dito.text).filter((texto) => texto !== "");
    expect(ditos.join(" | ")).not.toMatch(/onboarding —|equipes —|quiz ao vivo —/i);
    expect(ditos.join(" | ")).not.toMatch(/encerrar a sessão de trabalho/i);
    expect(ditos.join(" | ")).not.toMatch(/o que você quer fazer/i);
    expect(ditos).toContain("Comunidade Game — Aula");
  });

  it("encerrar a sessão de trabalho não mexe na escolha do aparelho", async () => {
    await guardarVerificadorDeTeste("mestre-de-trabalho-1");
    const encerrar = vi.fn();

    renderizar(vi.fn(), {}, encerrar);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: ROTULO_LIGAR }));
    await usuario.click(
      screen.getByRole("button", { name: /encerrar a sessão de trabalho/i }),
    );
    await usuario.type(
      await screen.findByLabelText(/pin de quem abriu o aparelho/i),
      PIN_DE_TESTE,
    );
    await usuario.click(
      screen.getByRole("button", { name: /^encerrar a sessão de trabalho$/i }),
    );

    await waitFor(() => expect(encerrar).toHaveBeenCalled());
    // A narração não é dado da sessão de trabalho nem do Guerreiro(a).
    expect(screen.queryByText(/a narração está/i)).not.toBeInTheDocument();
  });
});

describe("os atos de quem opera fecham o menu (RF-04-71, RF-04-49, RF-04-63)", () => {
  it("o encerramento é o último cartão, sob o rótulo do grupo", async () => {
    renderizar();

    await screen.findByText(/o que você quer fazer/i);
    expect(screen.getByText("Para quem opera o aparelho")).toBeInTheDocument();

    const cartoes = Array.from(document.querySelectorAll(".cg-caminho"));
    const ultimo = cartoes[cartoes.length - 1];
    expect(ultimo.textContent).toMatch(/encerrar a sessão de trabalho/i);
    // No mesmo padrão dos demais caminhos, com glifo ao lado do rótulo.
    expect(ultimo.querySelector("svg")).not.toBeNull();
  });

  it("o grupo é declarado, não só desenhado: a legend o nomeia", async () => {
    renderizar(vi.fn(), { podeAbrirMomentoDeTroca: true });

    await screen.findByText(/o que você quer fazer/i);
    // `fieldset` com `legend`: quem navega por leitor de tela ouve a fronteira
    // que quem olha vê no separador.
    const grupo = screen.getByRole("group", { name: "Para quem opera o aparelho" });
    expect(grupo).toContainElement(
      screen.getByRole("button", { name: /encerrar a sessão de trabalho/i }),
    );
    expect(grupo).toContainElement(
      screen.getByRole("button", { name: /abrir o momento de troca/i }),
    );
    // Os caminhos da criança ficam fora dele.
    expect(grupo).not.toContainElement(
      screen.getByRole("button", { name: /presença — entrar/i }),
    );
  });

  it("o aparelho que não abre a troca mostra só o encerramento", async () => {
    renderizar(vi.fn(), { podeAbrirMomentoDeTroca: false });

    await screen.findByText(/o que você quer fazer/i);
    expect(
      screen.getByRole("button", { name: /encerrar a sessão de trabalho/i }),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /abrir o momento de troca/i }),
    ).not.toBeInTheDocument();
  });

  it("a chave da troca, as entregas e o encerramento fecham o grupo nesta ordem", async () => {
    renderizar(vi.fn(), { podeAbrirMomentoDeTroca: true });

    await screen.findByText(/o que você quer fazer/i);
    const cartoes = Array.from(document.querySelectorAll(".cg-caminho"));
    expect(cartoes[cartoes.length - 3].textContent).toMatch(/abrir o momento de troca/i);
    expect(cartoes[cartoes.length - 2].textContent).toMatch(/entregas pendentes do encontro/i);
    expect(cartoes[cartoes.length - 1].textContent).toMatch(/encerrar a sessão de trabalho/i);
  });

  it("o cartão da chave da troca não repete o glifo do caminho da troca", async () => {
    renderizar(vi.fn(), { podeAbrirMomentoDeTroca: true, momentoDeTrocaAberto: true });

    await screen.findByText(/o que você quer fazer/i);
    const caminhoDaTroca = screen.getByRole("button", {
      name: /troca por recompensa avulsa/i,
    });
    const chaveDaTroca = screen.getByRole("button", { name: /fechar o momento de troca/i });

    expect(chaveDaTroca.querySelector("svg")?.innerHTML).not.toBe(
      caminhoDaTroca.querySelector("svg")?.innerHTML,
    );
  });

  it("abrindo, o cartão fica desabilitado e diz que está abrindo", async () => {
    renderizar(vi.fn(), { podeAbrirMomentoDeTroca: true, abrindoMomentoDeTroca: true });

    await screen.findByText(/o que você quer fazer/i);
    const cartao = screen.getByRole("button", { name: /abrindo/i });
    expect(cartao).toBeDisabled();
  });

  it("a falha da abertura aparece abaixo da lista, não entre os cartões", async () => {
    renderizar(vi.fn(), {
      podeAbrirMomentoDeTroca: true,
      erroDeAberturaDaTroca: "A troca exige rede.",
    });

    const aviso = await screen.findByRole("alert");
    expect(aviso).toHaveTextContent("A troca exige rede.");
    // Fora da coluna de alvos de toque: nenhum cartão se desloca sob o dedo.
    expect(aviso.closest(".cg-caminhos")).toBeNull();
  });
});

// A ordem do menu é decisão do fundador de 2026-10-15 e está fixada em spec:
// até esta fatia nenhum teste a protegia — o teste dos glifos lista os
// rótulos e itera, sem asserir sequência alguma (`RF-04-01`).
describe("a ordem do menu inicial (RF-04-01)", () => {
  it("os caminhos vêm na ordem decidida, e o grupo de quem opera fecha a lista", async () => {
    renderizar(vi.fn(), { momentoDeTrocaAberto: true, podeAbrirMomentoDeTroca: true });

    await screen.findByText(/o que você quer fazer/i);

    const cartoes = Array.from(document.querySelectorAll(".cg-caminho")).map((cartao) =>
      cartao.textContent?.trim(),
    );

    expect(cartoes).toEqual([
      "Onboarding — cadastro do Guerreiro(a) e presença do dia",
      "Presença — entrar com o nick e registrar a presença de hoje",
      "Trilhas e missões — ver o seu percurso e as atividades do encontro",
      "Equipes — formar a equipe e trabalhar a trilha",
      "Quiz ao Vivo — entrar com o nick e responder pela equipe",
      "Troca por recompensa avulsa — entregar uma recompensa do encontro",
      "Medição do limiar — calibrar o reconhecimento facial deste ponto de apoio",
      "Fechar o momento de troca",
      "Entregas pendentes do encontro — confirmar a recompensa conquistada",
      "Encerrar a sessão de trabalho",
    ]);
  });

  it("sem o momento de troca aberto, a ordem dos caminhos não muda", async () => {
    renderizar();

    await screen.findByText(/o que você quer fazer/i);

    const caminhos = Array.from(document.querySelectorAll(".cg-caminho"))
      .map((cartao) => cartao.textContent?.trim() ?? "")
      .filter(
        (rotulo) =>
          !rotulo.startsWith("Medição") &&
          !rotulo.startsWith("Entregas") &&
          !rotulo.startsWith("Encerrar"),
      );

    expect(caminhos).toEqual([
      "Onboarding — cadastro do Guerreiro(a) e presença do dia",
      "Presença — entrar com o nick e registrar a presença de hoje",
      "Trilhas e missões — ver o seu percurso e as atividades do encontro",
      "Equipes — formar a equipe e trabalhar a trilha",
      "Quiz ao Vivo — entrar com o nick e responder pela equipe",
    ]);
  });
});

// A medição é diagnóstico do ponto de apoio, não caminho da criança: `RF-04-63`
// a atribui a Mestre ou Admin, ela mede só quem opera fora do onboarding
// (`RN-04-33`) e pede o mesmo PIN do aparelho que o encerramento (`RN-04-41`).
// Até esta fatia estava entre os caminhos.
describe("a medição do limiar fica com quem opera (RF-04-63, RN-04-33)", () => {
  it("a medição está dentro do grupo, e nenhum caminho da criança vem depois dela", async () => {
    renderizar(vi.fn(), { momentoDeTrocaAberto: true, podeAbrirMomentoDeTroca: true });

    await screen.findByText(/o que você quer fazer/i);

    const grupo = screen.getByRole("group", { name: "Para quem opera o aparelho" });
    const medicao = screen.getByRole("button", { name: /medição do limiar/i });
    expect(grupo).toContainElement(medicao);

    // Os caminhos da criança ficam todos antes dela — inclusive o da troca,
    // que é o último deles quando o momento está aberto.
    for (const rotulo of [
      /onboarding/i,
      /presença — entrar/i,
      /trilhas e missões/i,
      /equipes —/i,
      /quiz ao vivo/i,
      /troca por recompensa avulsa/i,
    ]) {
      const caminho = screen.getByRole("button", { name: rotulo });
      expect(grupo).not.toContainElement(caminho);
      expect(
        caminho.compareDocumentPosition(medicao) & Node.DOCUMENT_POSITION_FOLLOWING,
      ).toBeTruthy();
    }
  });

  it("a medição abre o grupo, antes da chave da troca e do encerramento", async () => {
    renderizar(vi.fn(), { podeAbrirMomentoDeTroca: true });

    await screen.findByText(/o que você quer fazer/i);

    const grupo = screen.getByRole("group", { name: "Para quem opera o aparelho" });
    // A `legend` continua sendo o primeiro filho: é ela que carrega o
    // `border-top` do separador, e um cartão antes dela jogaria a linha para o
    // meio do grupo (design — decisão 2).
    expect(grupo.firstElementChild?.tagName).toBe("LEGEND");

    const naOrdem = Array.from(grupo.querySelectorAll(".cg-caminho")).map((cartao) =>
      cartao.textContent?.trim(),
    );

    expect(naOrdem).toEqual([
      "Medição do limiar — calibrar o reconhecimento facial deste ponto de apoio",
      "Abrir o momento de troca",
      "Entregas pendentes do encontro — confirmar a recompensa conquistada",
      "Encerrar a sessão de trabalho",
    ]);
  });

  it("o papel não guarda a medição: ela aparece em toda sessão de trabalho", async () => {
    // O delta afirma que a medição aparece em toda sessão de trabalho, guardada
    // pelo PIN do aparelho e não pelo papel (`RN-04-41`) — diferente da chave
    // da troca, que é só do Mestre. Sem este caso a afirmação ficaria sem
    // prova, porque os demais testes montam sempre com o papel `mestre`.
    renderizar(vi.fn(), { papelDeTrabalho: "admin" });

    await screen.findByText(/o que você quer fazer/i);

    const grupo = screen.getByRole("group", { name: "Para quem opera o aparelho" });
    expect(grupo).toContainElement(screen.getByRole("button", { name: /medição do limiar/i }));
  });

  it("o aparelho que não abre a troca mostra a medição e o encerramento", async () => {
    renderizar(vi.fn(), { podeAbrirMomentoDeTroca: false });

    await screen.findByText(/o que você quer fazer/i);

    const grupo = screen.getByRole("group", { name: "Para quem opera o aparelho" });
    const naOrdem = Array.from(grupo.querySelectorAll(".cg-caminho")).map((cartao) =>
      cartao.textContent?.trim(),
    );

    expect(naOrdem).toEqual([
      "Medição do limiar — calibrar o reconhecimento facial deste ponto de apoio",
      "Entregas pendentes do encontro — confirmar a recompensa conquistada",
      "Encerrar a sessão de trabalho",
    ]);
    expect(
      screen.queryByRole("button", { name: /abrir o momento de troca/i }),
    ).not.toBeInTheDocument();
  });
});

describe("a tela inicial usa o cartão do comum, em coluna (documento 15 §§5, 11.1)", () => {
  it("dispõe os caminhos em coluna, com o glifo ao lado do rótulo", async () => {
    renderizar();

    await screen.findByText(/o que você quer fazer/i);

    // A lista são 5 a 7 cartões mais o grupo de operação, em coluna — a única
    // disposição que a camada comum tem desde 2026-10-31 (design —
    // Non-Goals).
    const lista = document.querySelector(".cg-caminhos");
    expect(lista).not.toBeNull();

    // O glifo é o primeiro filho do cartão, e o rótulo segue sendo o nome
    // acessível do botão.
    const cartao = document.querySelector(".cg-caminho") as HTMLElement;
    expect(cartao.firstElementChild).toHaveClass("cg-icone");
    screen.getByRole("button", {
      name: "Onboarding — cadastro do Guerreiro(a) e presença do dia",
    });
  });
});
