import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import * as autenticacaoApi from "comum/autenticacao/api";
import * as biometriaModulo from "comum/biometria";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as presencasApi from "../api/presencas";
import * as sessoesDeGuerreiroApi from "../api/sessoesDeGuerreiro";
import { TelaDeEntradaDoGuerreiro } from "./TelaDeEntradaDoGuerreiro";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

import { useSessao } from "comum/autenticacao";

function configurarSessao(entrarComToken = vi.fn()) {
  vi.mocked(useSessao).mockReturnValue({
    sessao: null,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    entrarComToken,
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
    entrarComCredencial: vi.fn(),
    trocaDeSenhaPendente: false,
    trocandoSenha: false,
    erroDeTrocaDeSenha: null,
    trocarSenhaProvisoria: vi.fn(),
  });
}

function renderizar(aoVoltar = vi.fn(), aoAbrirSessao = vi.fn()) {
  return render(
    <TelaDeEntradaDoGuerreiro
      tokenDeTrabalho="token-de-trabalho"
      aulaId="aula-1"
      aoVoltar={aoVoltar}
      aoAbrirSessao={aoAbrirSessao}
    />,
  );
}

function mockarRegistrarPresencaEcoando() {
  return vi.spyOn(presencasApi, "registrarPresenca").mockImplementation((aulaId, entrada) =>
    Promise.resolve({
      id: "presenca-1",
      aula_id: aulaId,
      guerreiro_id: entrada.guerreiro_id,
      modo: entrada.modo,
      confirmador_id: entrada.modo === "confirmacao" ? "adulto-1" : null,
      momento_do_fato: entrada.momento_do_fato,
    }),
  );
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("entrada do Guerreiro(a) por reconhecimento", () => {
  it("nick, vivacidade e descritor abrem a sessão e registram a presença no mesmo ato", async () => {
    const entrarComToken = vi.fn().mockResolvedValue(undefined);
    const aoAbrirSessao = vi.fn();
    configurarSessao(entrarComToken);
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
    const registrarPresenca = mockarRegistrarPresencaEcoando();

    renderizar(vi.fn(), aoAbrirSessao);
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    await vi.waitFor(() => expect(entrarComToken).toHaveBeenCalledWith("token-do-guerreiro"));
    expect(abrirSessao).toHaveBeenCalledWith({ nick: "zeferina", descritor: [0.1, 0.2, 0.3] });
    expect(Object.keys(abrirSessao.mock.calls[0][0])).toEqual(["nick", "descritor"]);
    expect(registrarPresenca).toHaveBeenCalledWith(
      "aula-1",
      expect.objectContaining({ guerreiro_id: "guerreiro-1", modo: "reconhecimento" }),
      "token-de-trabalho",
    );
    expect(aoAbrirSessao).toHaveBeenCalledWith("reconhecimento");
  });

  it("presença já registrada avisa e não entra nas trilhas", async () => {
    const entrarComToken = vi.fn().mockResolvedValue(undefined);
    configurarSessao(entrarComToken);
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(presencasApi, "registrarPresenca").mockResolvedValue({
      id: "presenca-1",
      aula_id: "aula-1",
      guerreiro_id: "guerreiro-1",
      modo: "reconhecimento",
      confirmador_id: null,
      momento_do_fato: "2026-08-01T10:00:00Z",
    });
    const aoVoltar = vi.fn();

    renderizar(aoVoltar);
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    expect(await screen.findByText(/presença já registrada/i)).toBeInTheDocument();
    expect(entrarComToken).not.toHaveBeenCalled();

    await usuario.click(screen.getByRole("button", { name: /voltar ao início/i }));
    expect(aoVoltar).toHaveBeenCalled();
  });

  it("a recusa do núcleo oferece nova tentativa e o caminho da confirmação", async () => {
    configurarSessao();
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
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa).toHaveTextContent(/não foi possível reconhecer/i);
    expect(recusa.textContent).not.toMatch(/autenticacao_biometrica_invalida/i);

    await usuario.click(screen.getByRole("button", { name: /chamar mestre ou admin/i }));
    expect(screen.getByRole("button", { name: /confirmar identidade/i })).toBeInTheDocument();
  });

  it("vivacidade reprovada não chama o núcleo e oferece a mesma recusa", async () => {
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(false);
    const gerarDescritor = vi.spyOn(biometriaModulo, "gerarDescritor");
    const abrirSessao = vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento");

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/não foi possível reconhecer/i);
    expect(gerarDescritor).not.toHaveBeenCalled();
    expect(abrirSessao).not.toHaveBeenCalled();
  });

  it("sem câmera, a entrada cai direto na confirmação humana, sem tentar captura", async () => {
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(false);
    const provarVivacidade = vi.spyOn(biometriaModulo, "provarVivacidade");
    const abrirSessao = vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento");

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    expect(
      await screen.findByRole("button", { name: /confirmar identidade/i }),
    ).toBeInTheDocument();
    expect(provarVivacidade).not.toHaveBeenCalled();
    expect(abrirSessao).not.toHaveBeenCalled();
  });
});

describe("entrada do Guerreiro(a) por confirmação", () => {
  it("confirma pelo nick informado, registra a presença por confirmação e entra", async () => {
    const entrarComToken = vi.fn().mockResolvedValue(undefined);
    const aoAbrirSessao = vi.fn();
    configurarSessao(entrarComToken);
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(false);
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    const registrarPresenca = mockarRegistrarPresencaEcoando();

    renderizar(vi.fn(), aoAbrirSessao);
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));
    await usuario.click(await screen.findByRole("button", { name: /confirmar identidade/i }));

    expect(sessoesDeGuerreiroApi.confirmarSessaoDeGuerreiro).toHaveBeenCalledWith(
      "zeferina",
      "token-de-trabalho",
    );
    await vi.waitFor(() => expect(entrarComToken).toHaveBeenCalledWith("token-do-guerreiro"));
    expect(registrarPresenca).toHaveBeenCalledWith(
      "aula-1",
      expect.objectContaining({ guerreiro_id: "guerreiro-1", modo: "confirmacao" }),
      "token-de-trabalho",
    );
    expect(aoAbrirSessao).toHaveBeenCalledWith("confirmacao");
  });

  it("nick sem correspondência é recusado sem revelar o motivo", async () => {
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(false);
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockRejectedValue(
      new ErroDaApi(401, {
        codigo: "confirmacao_de_guerreiro_recusada",
        mensagem:
          "Não foi possível confirmar esse nick. Confira com o Guerreiro(a) e tente de novo.",
      }),
    );

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "nick-que-nao-existe");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));
    await usuario.click(await screen.findByRole("button", { name: /confirmar identidade/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa.textContent).not.toMatch(/confirmacao_de_guerreiro_recusada/i);
    expect(recusa).toHaveTextContent(/não foi possível confirmar/i);
  });

  it("o botão de entrar não abre sem nick digitado", () => {
    configurarSessao();

    renderizar();

    expect(screen.getByRole("button", { name: /entrar/i })).toBeDisabled();
  });

  it("voltar aciona aoVoltar sem chamar reconhecimento nem confirmação", async () => {
    configurarSessao();
    const aoVoltar = vi.fn();
    const abrirSessao = vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento");
    const confirmar = vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro");

    renderizar(aoVoltar);
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /voltar/i }));

    expect(aoVoltar).toHaveBeenCalled();
    expect(abrirSessao).not.toHaveBeenCalled();
    expect(confirmar).not.toHaveBeenCalled();
  });
});
