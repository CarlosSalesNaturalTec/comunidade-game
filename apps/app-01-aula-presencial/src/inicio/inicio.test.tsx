import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as sessaoApi from "comum/autenticacao/api";
import * as biometriaModulo from "comum/biometria";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as descritorApi from "../api/descritor";
import * as equipesApi from "../api/equipes";
import * as presencasApi from "../api/presencas";
import * as sessoesDeGuerreiroApi from "../api/sessoesDeGuerreiro";
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
});

function renderizar(
  aoVoltarAoInicio = vi.fn(),
  propsDeTroca: Partial<{
    podeAbrirMomentoDeTroca: boolean;
    momentoDeTrocaAberto: boolean;
    abrindoMomentoDeTroca: boolean;
    erroDeAberturaDaTroca: string | null;
  }> = {},
) {
  return render(
    <ProvedorDeEstadoDeRede>
      <ProvedorDeSessao chaveDeArmazenamento="teste:app-01:sessao-guerreiro">
        <TelaInicial
          tokenDeTrabalho="token-de-trabalho"
          personaIdDeTrabalho="mestre-de-trabalho-1"
          papelDeTrabalho="mestre"
          aulaId="aula-1"
          aoVoltarAoInicio={aoVoltarAoInicio}
          podeAbrirMomentoDeTroca={propsDeTroca.podeAbrirMomentoDeTroca ?? false}
          momentoDeTrocaAberto={propsDeTroca.momentoDeTrocaAberto ?? false}
          abrindoMomentoDeTroca={propsDeTroca.abrindoMomentoDeTroca ?? false}
          erroDeAberturaDaTroca={propsDeTroca.erroDeAberturaDaTroca ?? null}
          aoAbrirMomentoDeTroca={vi.fn()}
          aoFecharMomentoDeTroca={vi.fn()}
        />
      </ProvedorDeSessao>
    </ProvedorDeEstadoDeRede>,
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
    renderizar(vi.fn(), { momentoDeTrocaAberto: true });
    await screen.findByText(/o que você quer fazer/i);

    for (const caminho of screen.getAllByRole("button")) {
      const glifo = caminho.querySelector("svg");
      if (!glifo) continue;
      // O desenho não fala por si: é escondido da tecnologia assistiva, e o
      // botão que o leva tem texto visível.
      expect(glifo).toHaveAttribute("aria-hidden", "true");
      expect(caminho.textContent?.trim()).not.toBe("");
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
