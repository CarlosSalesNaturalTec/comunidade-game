import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as sessaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as descritorApi from "../api/descritor";
import * as equipesApi from "../api/equipes";
import * as presencasApi from "../api/presencas";
import * as sessoesDeGuerreiroApi from "../api/sessoesDeGuerreiro";
import * as biometriaModulo from "../biometria/biometria";
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

async function entrarPorConfirmacao(
  usuario: ReturnType<typeof userEvent.setup>,
  nick = "zeferina",
) {
  await usuario.click(screen.getByRole("button", { name: /trilhas/i }));
  await usuario.type(await screen.findByLabelText(/nick/i), nick);
  await usuario.click(screen.getByRole("button", { name: /entrar/i }));
  await usuario.click(await screen.findByRole("button", { name: /confirmar identidade/i }));
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
    <ProvedorDeSessao chaveDeArmazenamento="teste:app-01:sessao-guerreiro">
      <TelaInicial
        tokenDeTrabalho="token-de-trabalho"
        personaIdDeTrabalho="mestre-de-trabalho-1"
        aulaId="aula-1"
        aoVoltarAoInicio={aoVoltarAoInicio}
        podeAbrirMomentoDeTroca={propsDeTroca.podeAbrirMomentoDeTroca ?? false}
        momentoDeTrocaAberto={propsDeTroca.momentoDeTrocaAberto ?? false}
        abrindoMomentoDeTroca={propsDeTroca.abrindoMomentoDeTroca ?? false}
        erroDeAberturaDaTroca={propsDeTroca.erroDeAberturaDaTroca ?? null}
        aoAbrirMomentoDeTroca={vi.fn()}
        aoFecharMomentoDeTroca={vi.fn()}
      />
    </ProvedorDeSessao>,
  );
}

describe("tela inicial da App 01", () => {
  it("os dois caminhos aparecem, e os dois estão habilitados", async () => {
    renderizar();

    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /onboarding/i })).toBeEnabled();
    expect(screen.getByRole("button", { name: /trilhas/i })).toBeEnabled();
  });

  it("onboarding leva à tela de cadastro do Guerreiro(a)", async () => {
    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /onboarding/i }));

    expect(await screen.findByText(/novo guerreiro/i)).toBeInTheDocument();
  });

  it("trilhas sem sessão leva à entrada do Guerreiro(a), nunca ao cadastro", async () => {
    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /trilhas/i }));

    expect(await screen.findByText(/quem está chegando/i)).toBeInTheDocument();
    expect(screen.queryByText(/cadastr/i)).not.toBeInTheDocument();
  });

  it("a confirmação do Mestre abre a sessão do Guerreiro(a), registra a presença e leva às equipes", async () => {
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

    renderizar();
    const usuario = userEvent.setup();
    await entrarPorConfirmacao(usuario);

    expect(await screen.findByText(/equipes desta aula/i)).toBeInTheDocument();
    expect(registrarPresenca).toHaveBeenCalledWith(
      "aula-1",
      expect.objectContaining({ guerreiro_id: "guerreiro-1", modo: "confirmacao" }),
      "token-de-trabalho",
    );
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
    mockarRegistrarPresencaEcoando();

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
    mockarRegistrarPresencaEcoando();
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
    mockarRegistrarPresencaEcoando();

    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /trilhas/i }));
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    expect(await screen.findByText(/equipes desta aula/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /recadastrar imagem/i }),
    ).not.toBeInTheDocument();
  });

  it("o terceiro caminho não aparece com o momento de troca fechado", async () => {
    renderizar(vi.fn(), { momentoDeTrocaAberto: false });

    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /troca por recompensa/i }),
    ).not.toBeInTheDocument();
  });

  it("o terceiro caminho aparece com o momento de troca aberto e leva à entrada, não ao cadastro", async () => {
    renderizar(vi.fn(), { momentoDeTrocaAberto: true });
    const usuario = userEvent.setup();

    const caminhoDeTroca = await screen.findByRole("button", {
      name: /troca por recompensa/i,
    });
    await usuario.click(caminhoDeTroca);

    expect(await screen.findByText(/quem está chegando/i)).toBeInTheDocument();
    expect(screen.queryByText(/cadastr/i)).not.toBeInTheDocument();
  });
});
