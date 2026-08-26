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

    await usuario.click(screen.getByRole("button", { name: /chamar mestre ou admin/i }));
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

describe("sessão assistida por Mestre ou Admin", () => {
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
      await screen.findByRole("button", { name: /chamar mestre ou admin/i }),
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
