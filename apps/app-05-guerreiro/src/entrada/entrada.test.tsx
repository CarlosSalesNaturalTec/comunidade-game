import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import * as biometriaModulo from "comum/biometria";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as sessoesDeGuerreiroApi from "../api/sessoesDeGuerreiro";
import { AparelhoDaAreaDoGuerreiro } from "./AparelhoDaAreaDoGuerreiro";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: ({
      aoReceberIdToken,
    }: {
      aoReceberIdToken: (token: string) => void;
    }) => (
      <button type="button" onClick={() => aoReceberIdToken("id-token-do-adulto")}>
        Entrar com Google
      </button>
    ),
  };
});

function renderizar() {
  return render(
    <ProvedorDeSessao chaveDeArmazenamento="app-05:sessao-guerreiro">
      <AparelhoDaAreaDoGuerreiro />
    </ProvedorDeSessao>,
  );
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("entrada do Guerreiro(a) por reconhecimento", () => {
  it("nick e imagem conferidos abrem a sessão, submetendo só o descritor", async () => {
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    const abrirSessao = vi
      .spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento")
      .mockResolvedValue({
        token: "token-do-guerreiro",
        expira_em: new Date().toISOString(),
        papel: "guerreiro",
      });
    vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    await vi.waitFor(() =>
      expect(abrirSessao).toHaveBeenCalledWith({
        nick: "zeferina",
        descritor: [0.1, 0.2, 0.3],
      }),
    );
    expect(Object.keys(abrirSessao.mock.calls[0][0])).toEqual(["nick", "descritor"]);
    expect(await screen.findByRole("heading", { name: /minha área/i })).toBeInTheDocument();
  });

  it("recusa não diz o que falhou, e oferece a sessão assistida", async () => {
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockRejectedValue(
      new ErroDaApi(401, {
        codigo: "autenticacao_biometrica_invalida",
        mensagem: "Não foi possível autenticar.",
      }),
    );

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/nick/i), "nick-que-nao-existe");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa).toHaveTextContent(/não foi possível reconhecer/i);
    expect(recusa.textContent).not.toMatch(/autenticacao_biometrica_invalida/i);

    await usuario.click(screen.getByRole("button", { name: /pedir ajuda a um adulto/i }));
    expect(screen.getByRole("button", { name: /entrar com google/i })).toBeInTheDocument();
  });

  it("vivacidade reprovada não chama o núcleo", async () => {
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(false);
    const gerarDescritor = vi.spyOn(biometriaModulo, "gerarDescritor");
    const abrirSessao = vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento");

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/não foi possível reconhecer/i);
    expect(gerarDescritor).not.toHaveBeenCalled();
    expect(abrirSessao).not.toHaveBeenCalled();
  });
});

describe("aparelho sem câmera", () => {
  it("recusa a entrada em linguagem simples, sem código de erro, e cai na sessão assistida", async () => {
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(false);

    renderizar();

    const aviso = await screen.findByRole("alert");
    expect(aviso).toHaveTextContent(/não tem câmera/i);
    expect(aviso.textContent).not.toMatch(/error|exception|c[oó]digo|getUserMedia/i);
    expect(screen.getByRole("button", { name: /entrar com google/i })).toBeInTheDocument();
  });
});

describe("sessão assistida pelo adulto — responsável, Mestre ou Admin", () => {
  it("o adulto se autentica, confirma a identidade e a sessão do Guerreiro(a) abre", async () => {
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockRejectedValue(
      new ErroDaApi(401, {
        codigo: "autenticacao_biometrica_invalida",
        mensagem: "Não foi possível autenticar.",
      }),
    );
    vi.spyOn(autenticacaoApi, "loginSocial").mockResolvedValue({
      token: "token-do-mestre",
      expira_em: new Date().toISOString(),
      papel: "mestre",
    });
    const confirmar = vi
      .spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro")
      .mockResolvedValue({
        token: "token-do-guerreiro",
        expira_em: new Date().toISOString(),
        papel: "guerreiro",
      });
    vi.spyOn(autenticacaoApi, "eu")
      .mockResolvedValueOnce({ persona_id: "mestre-1", papel: "mestre", permissoes: {} })
      .mockResolvedValueOnce({
        persona_id: "guerreiro-1",
        papel: "guerreiro",
        permissoes: {},
      });
    const encerrarSessaoDoAdulto = vi
      .spyOn(autenticacaoApi, "encerrarSessao")
      .mockResolvedValue(undefined);

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));
    await usuario.click(
      await screen.findByRole("button", { name: /pedir ajuda a um adulto/i }),
    );
    await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));
    await usuario.click(await screen.findByRole("button", { name: /confirmar identidade/i }));

    expect(confirmar).toHaveBeenCalledWith("zeferina", "token-do-mestre");
    await vi.waitFor(() =>
      expect(encerrarSessaoDoAdulto).toHaveBeenCalledWith("token-do-mestre"),
    );
    expect(await screen.findByRole("heading", { name: /minha área/i })).toBeInTheDocument();
  });

  it("sem adulto autenticado, o botão de confirmar não aparece", async () => {
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(false);

    renderizar();
    await screen.findByRole("button", { name: /entrar com google/i });

    expect(
      screen.queryByRole("button", { name: /confirmar identidade/i }),
    ).not.toBeInTheDocument();
  });
});

describe("a entrada fora do encontro e o erro que não se disfarça", () => {
  function prepararCapturaQuePassa() {
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
  }

  // `RF-05-01`, `RN-01-57`: fora do encontro não há aula, e é a ausência dela
  // que faz o núcleo emprestar o limiar da comunidade.
  it("a conferência é submetida sem aula", async () => {
    prepararCapturaQuePassa();
    const abrirSessao = vi
      .spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento")
      .mockResolvedValue({
        token: "token-do-guerreiro",
        expira_em: new Date().toISOString(),
        papel: "guerreiro",
      });
    vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    await vi.waitFor(() => expect(abrirSessao).toHaveBeenCalled());
    expect(abrirSessao).toHaveBeenCalledWith({
      nick: "zeferina",
      descritor: [0.1, 0.2, 0.3],
    });
    expect(Object.keys(abrirSessao.mock.calls[0][0])).toEqual(["nick", "descritor"]);
  });

  // `RN-05-48`, `RF-01-27`: é o 422 que quebrou a App 01, e que aqui nunca
  // pode chegar à criança como rosto que não confere.
  it("erro de validação do núcleo não vira rosto que não confere", async () => {
    prepararCapturaQuePassa();
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Field required",
        campo: "aula_id",
      }),
    );

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta).not.toHaveTextContent(/não foi possível reconhecer/i);
    expect(alerta).not.toHaveTextContent(/field required/i);
    expect(alerta).not.toHaveTextContent(/aula_id/i);
  });

  it("rede fora não vira rosto que não confere", async () => {
    prepararCapturaQuePassa();
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockRejectedValue(
      new TypeError("Failed to fetch"),
    );

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(/não consegui falar com a plataforma/i);
    expect(alerta).not.toHaveTextContent(/não foi possível reconhecer/i);
  });

  // `RN-05-48`, `RF-05-02`: a falha de camada chega em linguagem de criança,
  // sem código de erro nem nome de biblioteca.
  it("nenhum código técnico chega à criança na falha de camada", async () => {
    prepararCapturaQuePassa();
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockRejectedValue(
      new ErroDaApi(429, {
        codigo: "freio_por_origem",
        mensagem: "Too many requests from origin 10.0.0.1",
      }),
    );

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta.textContent).not.toMatch(/freio_por_origem|429|10\.0\.0\.1/);
  });

  // `RN-05-48`: depois da conferência o rosto já conferiu.
  it("falha depois do reconhecimento não vira recusa", async () => {
    prepararCapturaQuePassa();
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(autenticacaoApi, "eu").mockRejectedValue(new TypeError("Failed to fetch"));

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta).not.toHaveTextContent(/não foi possível reconhecer/i);
  });
});

describe("o responsável abre a sessão em casa", () => {
  function recusarOReconhecimento() {
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockRejectedValue(
      new ErroDaApi(401, {
        codigo: "autenticacao_biometrica_invalida",
        mensagem: "Não foi possível autenticar.",
      }),
    );
  }

  async function chegarNaConfirmacao() {
    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));
    await usuario.click(
      await screen.findByRole("button", { name: /pedir ajuda a um adulto/i }),
    );
    return usuario;
  }

  // `RF-05-03`, `RF-05-04`: o documento 03 §1.1 dá dois caminhos ao adulto.
  // Oferecer só um trancaria fora quem tem o outro.
  it("a tela oferece os dois caminhos de login", async () => {
    recusarOReconhecimento();
    await chegarNaConfirmacao();

    expect(await screen.findByRole("button", { name: /entrar com google/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /entrar com usuário e senha/i })).toBeVisible();
  });

  it("o responsável entra por usuário e senha e confirma a criança", async () => {
    recusarOReconhecimento();
    vi.spyOn(autenticacaoApi, "loginPorCredencial").mockResolvedValue({
      token: "token-do-responsavel",
      expira_em: new Date().toISOString(),
      papel: "responsavel",
    });
    const confirmar = vi
      .spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro")
      .mockResolvedValue({
        token: "token-do-guerreiro",
        expira_em: new Date().toISOString(),
        papel: "guerreiro",
      });
    vi.spyOn(autenticacaoApi, "eu")
      .mockResolvedValueOnce({
        persona_id: "responsavel-1",
        papel: "responsavel",
        permissoes: {},
      })
      .mockResolvedValueOnce({
        persona_id: "guerreiro-1",
        papel: "guerreiro",
        permissoes: {},
      });
    vi.spyOn(autenticacaoApi, "encerrarSessao").mockResolvedValue(undefined);

    const usuario = await chegarNaConfirmacao();
    await usuario.type(await screen.findByLabelText(/^usuário$/i), "Mae_da_Zeferina");
    await usuario.type(screen.getByLabelText(/^senha$/i), "segredo-forte");
    await usuario.click(screen.getByRole("button", { name: /entrar com usuário e senha/i }));
    await usuario.click(await screen.findByRole("button", { name: /confirmar identidade/i }));

    expect(confirmar).toHaveBeenCalledWith("zeferina", "token-do-responsavel");
    expect(await screen.findByRole("heading", { name: /minha área/i })).toBeInTheDocument();
  });

  // `RF-01-12`: o primeiro uso da credencial costuma ser o resgate da criança.
  // Terminar ali deixaria os dois sem porta.
  it("a senha provisória se troca ali mesmo, sem sair do fluxo", async () => {
    recusarOReconhecimento();
    vi.spyOn(autenticacaoApi, "loginPorCredencial").mockResolvedValue({
      token: "token-provisorio",
      expira_em: new Date().toISOString(),
      papel: "responsavel",
    });
    vi.spyOn(autenticacaoApi, "eu")
      .mockRejectedValueOnce(
        new ErroDaApi(403, {
          codigo: "troca_de_senha_pendente",
          mensagem: "Troque a senha provisória.",
        }),
      )
      .mockResolvedValueOnce({
        persona_id: "responsavel-1",
        papel: "responsavel",
        permissoes: {},
      });
    const trocar = vi.spyOn(autenticacaoApi, "trocarSenha").mockResolvedValue(undefined);

    const usuario = await chegarNaConfirmacao();
    await usuario.type(await screen.findByLabelText(/^usuário$/i), "Mae_da_Zeferina");
    await usuario.type(screen.getByLabelText(/^senha$/i), "provisoria");
    await usuario.click(screen.getByRole("button", { name: /entrar com usuário e senha/i }));

    // Em vez de beco sem saída, a troca aparece no mesmo fluxo.
    await usuario.type(await screen.findByLabelText(/^senha nova$/i), "segredo-forte");
    await usuario.type(screen.getByLabelText(/confirme a senha nova/i), "segredo-forte");
    await usuario.click(screen.getByRole("button", { name: /trocar senha/i }));

    await vi.waitFor(() =>
      expect(trocar).toHaveBeenCalledWith("token-provisorio", "segredo-forte"),
    );
    expect(await screen.findByRole("button", { name: /confirmar identidade/i })).toBeVisible();
  });

  // `RN-01-58`, `RN-01-22`: o núcleo devolve resposta indistinguível, e a tela
  // não pode desfazer isso escrevendo "essa criança não é sua".
  it("criança alheia recusa com a frase que o núcleo declarou, sem dizer que ela existe", async () => {
    recusarOReconhecimento();
    vi.spyOn(autenticacaoApi, "loginPorCredencial").mockResolvedValue({
      token: "token-do-responsavel",
      expira_em: new Date().toISOString(),
      papel: "responsavel",
    });
    vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
      persona_id: "responsavel-1",
      papel: "responsavel",
      permissoes: {},
    });
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockRejectedValue(
      new ErroDaApi(401, {
        codigo: "confirmacao_de_guerreiro_recusada",
        mensagem: "Não foi possível confirmar esse nick.",
      }),
    );

    const usuario = await chegarNaConfirmacao();
    await usuario.type(await screen.findByLabelText(/^usuário$/i), "Mae_da_Zeferina");
    await usuario.type(screen.getByLabelText(/^senha$/i), "segredo-forte");
    await usuario.click(screen.getByRole("button", { name: /entrar com usuário e senha/i }));
    await usuario.click(await screen.findByRole("button", { name: /confirmar identidade/i }));

    const alerta = await screen.findByText(/não foi possível confirmar esse nick/i);
    expect(alerta).toBeVisible();
    expect(alerta.textContent).not.toMatch(/não é sua|de outra|alheia/i);
  });
});
