import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import * as autenticacaoApi from "comum/autenticacao/api";
import * as biometriaModulo from "comum/biometria";
import * as cartaApi from "comum/carta/api";
import * as trilhaComumApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as presencasApi from "../api/presencas";
import * as sessoesDeGuerreiroApi from "../api/sessoesDeGuerreiro";
import * as filaDePresenca from "../fila/filaDePresenca";
import { TelaInicial } from "../inicio/TelaInicial";
import { guardarVerificadorDeTeste, PIN_DE_TESTE } from "../pin/paraTestes";
import { estadoDoPinDe, pinBloqueadoNoAparelho } from "../pin/pinDeConfirmacao";
import { ProvedorDeEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";
import { type CaminhoDaEntrada, TelaDeEntradaDoGuerreiro } from "./TelaDeEntradaDoGuerreiro";

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

function renderizar(
  aoVoltar = vi.fn(),
  aoAbrirSessao = vi.fn(),
  caminho: CaminhoDaEntrada = "presenca",
  aoSeguirParaTrilhas?: () => void,
) {
  return render(
    <TelaDeEntradaDoGuerreiro
      tokenDeTrabalho="token-de-trabalho"
      aulaId="aula-1"
      caminho={caminho}
      aoVoltar={aoVoltar}
      aoAbrirSessao={aoAbrirSessao}
      aoSeguirParaTrilhas={aoSeguirParaTrilhas}
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
    // `RF-04-18`, `RF-01-73`: a aula do encontro vai junto, e é ela que
    // determina o ponto de apoio e o limiar. Quem opera não a digitou.
    expect(abrirSessao).toHaveBeenCalledWith({
      nick: "zeferina",
      descritor: [0.1, 0.2, 0.3],
      aula_id: "aula-1",
    });
    expect(Object.keys(abrirSessao.mock.calls[0][0])).toEqual([
      "nick",
      "descritor",
      "aula_id",
    ]);
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
  // `RF-04-64`, `RN-04-34`: o retorno do laço vale **enquanto** a tentativa
  // corre — sem este caso, passar sempre `null` ao visor também passaria nos
  // dois testes seguintes, e a tela ficaria muda.
  it("apresenta o retorno do laço enquanto a captura acontece", async () => {
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockImplementation(
      (aoMudarEstado) =>
        new Promise(() => {
          aoMudarEstado?.("procurando_rosto");
        }),
    );

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    expect(await screen.findByText(/procurando um rosto/i)).toBeInTheDocument();
  });

  // `RF-04-64`, `RN-04-34`: e **cala no desfecho**. Observado em produção em
  // 2026-09-18: "Pessoa confirmada." ao lado de "não foi possível reconhecer"
  // faz quem opera ler as duas frases como um julgamento só, contraditório.
  it("o retorno do laço não sobrevive à recusa do núcleo", async () => {
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockImplementation(async (aoMudarEstado) => {
      aoMudarEstado?.("vivacidade_confirmada");
      return true;
    });
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2]);
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

    expect(await screen.findByRole("alert")).toHaveTextContent(/não foi possível reconhecer/i);
    expect(screen.queryByText(/pessoa confirmada/i)).not.toBeInTheDocument();
  });

  // `RF-04-64`, `RF-04-65`, `RN-04-34`: vale para todo desfecho, não só para o
  // da recusa do núcleo.
  it("o retorno do laço não sobrevive à vivacidade reprovada nem à falha de preparo", async () => {
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockImplementation(async (aoMudarEstado) => {
      aoMudarEstado?.("rosto_encontrado");
      return false;
    });

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/não foi possível reconhecer/i);
    expect(screen.queryByText(/rosto encontrado/i)).not.toBeInTheDocument();

    cleanup();
    vi.spyOn(biometriaModulo, "prepararCaptura").mockRejectedValue(
      new biometriaModulo.ErroDePreparoDaCaptura("modelos não carregaram"),
    );

    renderizar();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      /câmera não pôde ser preparada/i,
    );
    expect(screen.queryByText(/rosto encontrado/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/pessoa confirmada/i)).not.toBeInTheDocument();
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
    await usuario.type(await screen.findByLabelText(/pin de quem confirma/i), "4821");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    expect(sessoesDeGuerreiroApi.confirmarSessaoDeGuerreiro).toHaveBeenCalledWith(
      "zeferina",
      "4821",
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
    await usuario.type(await screen.findByLabelText(/pin de quem confirma/i), "4821");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa.textContent).not.toMatch(/confirmacao_de_guerreiro_recusada/i);
    expect(recusa).toHaveTextContent(/não foi possível confirmar/i);
  });

  it("o botão de entrar não abre sem nick digitado", () => {
    configurarSessao();

    renderizar();

    expect(screen.getByRole("button", { name: /entrar/i })).toBeDisabled();
  });

  // `RF-04-64`: também aqui quem chega se vê no visor antes de a captura
  // julgar — a tela empresta o lugar, o módulo anexa o vídeo.
  it("empresta ao módulo o lugar do visor, e ele está na tela", async () => {
    configurarSessao();
    const acoplar = vi.spyOn(biometriaModulo, "acoplarEspelho");
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(false);

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    await vi.waitFor(() => expect(acoplar).toHaveBeenCalled());
    expect(document.body.contains(acoplar.mock.calls[0][0])).toBe(true);
  });

  // `RF-04-65`: a indistinguibilidade do `RF-04-20` cobre as três causas da
  // recusa do núcleo, não a câmera que nem chegou a funcionar.
  it("falha de preparo tem frase própria, distinta da recusa do reconhecimento", async () => {
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "prepararCaptura").mockRejectedValue(
      new biometriaModulo.ErroDePreparoDaCaptura("modelos não carregaram"),
    );
    const provar = vi.spyOn(biometriaModulo, "provarVivacidade");
    const abrirSessao = vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento");

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(/câmera não pôde ser preparada/i);
    expect(alerta).not.toHaveTextContent(/não foi possível reconhecer/i);
    expect(provar).not.toHaveBeenCalled();
    expect(abrirSessao).not.toHaveBeenCalled();
  });

  // `RF-04-20`, `RN-01-22`: o que a change não pode ter quebrado — a recusa
  // do núcleo continua a mesma frase da vivacidade reprovada.
  it("a recusa do núcleo e a vivacidade reprovada continuam indistinguíveis", async () => {
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(false);
    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));
    const porVivacidade = (await screen.findByRole("alert")).textContent;

    cleanup();
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2]);
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockRejectedValue(
      new ErroDaApi(401, {
        codigo: "autenticacao_biometrica_invalida",
        mensagem: "Não foi possível autenticar.",
      }),
    );
    renderizar();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));
    const porRecusaDoNucleo = (await screen.findByRole("alert")).textContent;

    expect(porRecusaDoNucleo).toEqual(porVivacidade);
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

  // `RN-04-36`, `RF-01-27`: erro que o núcleo declara no corpo único nunca
  // veste a frase da recusa do rosto — foi assim que um 422 de campo em falta
  // passou dias parecendo criança não reconhecida.
  it("erro de validação do núcleo não se disfarça de rosto que não confere", async () => {
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Field required",
        campo: "aula_id",
      }),
    );

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(/field required/i);
    expect(alerta).not.toHaveTextContent(/não foi possível reconhecer/i);
  });

  // `RN-04-36`: falha que não chega a produzir corpo tem frase própria.
  it("rede fora não se disfarça de rosto que não confere", async () => {
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockRejectedValue(
      new TypeError("Failed to fetch"),
    );

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(/não foi possível falar com a plataforma/i);
    expect(alerta).not.toHaveTextContent(/não foi possível reconhecer/i);
  });

  // `RN-04-36`, `RF-04-18`: depois da conferência o rosto já conferiu. A
  // armadilha inversa — presença gravada no núcleo e recusa na tela — morre
  // aqui.
  it("falha depois do reconhecimento não se disfarça de recusa", async () => {
    configurarSessao();
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
    vi.spyOn(presencasApi, "registrarPresenca").mockRejectedValue(
      new ErroDaApi(503, { codigo: "erro_http", mensagem: "Serviço indisponível." }),
    );

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(/rosto foi reconhecido/i);
    expect(alerta).not.toHaveTextContent(/não foi possível reconhecer\./i);
  });

  // `RF-04-20`, `RN-01-22`: a recusa que o núcleo declara continua com a
  // frase de sempre, e continua oferecendo o caminho humano.
  it("a recusa declarada pelo núcleo mantém a frase e o caminho do Mestre", async () => {
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockRejectedValue(
      new ErroDaApi(401, {
        codigo: "autenticacao_biometrica_invalida",
        mensagem: "Nick ou imagem não reconhecidos.",
      }),
    );

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(/não foi possível reconhecer/i);
    expect(screen.getByRole("button", { name: /chamar mestre ou admin/i })).toBeVisible();
  });
});

describe("PIN de quem confirma (RF-04-21, RN-04-37, RN-04-38)", () => {
  afterEach(() => {
    sessionStorage.clear();
    localStorage.clear();
  });

  async function abrirConfirmacao(usuario: ReturnType<typeof userEvent.setup>) {
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(false);
    renderizar();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));
    await screen.findByRole("button", { name: /confirmar identidade/i });
  }

  it("sem o PIN, a confirmação não acontece", async () => {
    configurarSessao();
    const confirmar = vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro");
    const usuario = userEvent.setup();
    await abrirConfirmacao(usuario);

    const botao = screen.getByRole("button", { name: /confirmar identidade/i });
    expect(botao).toBeDisabled();
    await usuario.type(screen.getByLabelText(/pin de quem confirma/i), "48");
    expect(botao).toBeDisabled();
    expect(confirmar).not.toHaveBeenCalled();
  });

  it("PIN errado é dito como tal, limpa o PIN e mantém o nick", async () => {
    configurarSessao();
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockRejectedValue(
      new ErroDaApi(401, { codigo: "pin_recusado", mensagem: "PIN errado." }),
    );
    const usuario = userEvent.setup();
    await abrirConfirmacao(usuario);

    await usuario.type(screen.getByLabelText(/pin de quem confirma/i), "0000");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    expect(await screen.findByText(/pin errado/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/pin de quem confirma/i)).toHaveValue("");
    expect(screen.getByLabelText(/nick/i)).toHaveValue("zeferina");
  });

  it("PIN bloqueado manda entrar de novo pelo Google e não oferece nova tentativa", async () => {
    configurarSessao();
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockRejectedValue(
      new ErroDaApi(403, { codigo: "pin_bloqueado", mensagem: "PIN bloqueado." }),
    );
    await guardarVerificadorDeTeste();
    const usuario = userEvent.setup();
    await abrirConfirmacao(usuario);

    await usuario.type(screen.getByLabelText(/pin de quem confirma/i), "0000");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    expect(await screen.findByText(/entre outra vez pelo google/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /confirmar identidade/i })).toBeDisabled();
    expect(pinBloqueadoNoAparelho()).toBe(true);
  });

  it("o PIN não fica no aparelho depois de uma confirmação", async () => {
    configurarSessao(vi.fn().mockResolvedValue(undefined));
    await guardarVerificadorDeTeste();
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
    mockarRegistrarPresencaEcoando();
    const usuario = userEvent.setup();
    await abrirConfirmacao(usuario);

    await usuario.type(screen.getByLabelText(/pin de quem confirma/i), "4821");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    await vi.waitFor(() =>
      expect(sessoesDeGuerreiroApi.confirmarSessaoDeGuerreiro).toHaveBeenCalled(),
    );
    const armazenado =
      JSON.stringify({ ...sessionStorage }) + JSON.stringify({ ...localStorage });
    expect(armazenado).not.toContain("4821");
  });
});

describe("o caminho decide quem registra a presença (RF-04-67)", () => {
  it("no caminho das equipes, o reconhecimento abre a sessão e não registra presença", async () => {
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
    const quemSou = vi.spyOn(autenticacaoApi, "eu");
    const registrarPresenca = mockarRegistrarPresencaEcoando();

    renderizar(vi.fn(), vi.fn(), "equipes");
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));

    await vi.waitFor(() => expect(entrarComToken).toHaveBeenCalledWith("token-do-guerreiro"));
    expect(registrarPresenca).not.toHaveBeenCalled();
    expect(quemSou).not.toHaveBeenCalled();
  });

  it("no caminho das equipes, a confirmação com PIN abre a sessão e não registra presença", async () => {
    const entrarComToken = vi.fn().mockResolvedValue(undefined);
    configurarSessao(entrarComToken);
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    const registrarPresenca = mockarRegistrarPresencaEcoando();

    // Sem câmera, a entrada já abre na confirmação humana (`RN-04-09`).
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(false);
    renderizar(vi.fn(), vi.fn(), "equipes");
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));
    await usuario.type(await screen.findByLabelText(/pin de quem confirma/i), "4821");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    await vi.waitFor(() => expect(entrarComToken).toHaveBeenCalledWith("token-do-guerreiro"));
    expect(registrarPresenca).not.toHaveBeenCalled();
  });

  it("no caminho da presença, o atendimento termina na confirmação do registro", async () => {
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
    mockarRegistrarPresencaEcoando();

    renderizar(vi.fn(), vi.fn(), "presenca");
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));

    expect(await screen.findByText(/presença registrada/i)).toBeInTheDocument();
    expect(screen.getByText(/a presença de hoje está registrada/i)).toBeInTheDocument();
  });
});

describe("o desfecho da presença e o caminho das trilhas (RF-04-67, RF-04-72)", () => {
  async function registrarPresencaPorReconhecimento(aoSeguirParaTrilhas?: () => void) {
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
    mockarRegistrarPresencaEcoando();

    renderizar(vi.fn(), vi.fn(), "presenca", aoSeguirParaTrilhas);
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));
    await screen.findByText(/presença registrada/i);
    return { usuario, entrarComToken };
  }

  it("o desfecho da presença oferece as trilhas ao lado de voltar ao início", async () => {
    const aoSeguirParaTrilhas = vi.fn();
    const { usuario, entrarComToken } =
      await registrarPresencaPorReconhecimento(aoSeguirParaTrilhas);

    expect(screen.getByRole("button", { name: /voltar ao início/i })).toBeInTheDocument();
    await usuario.click(
      screen.getByRole("button", { name: /ver as minhas trilhas e missões/i }),
    );

    expect(aoSeguirParaTrilhas).toHaveBeenCalled();
    // A sessão do Guerreiro(a) já está aberta quando o desfecho aparece:
    // seguir às trilhas NUNCA pede nick nem imagem de novo (`RF-04-72`).
    expect(entrarComToken).toHaveBeenCalledWith("token-do-guerreiro");
    expect(screen.queryByLabelText(/nick/i)).not.toBeInTheDocument();
  });

  it("sem o desfecho ligado, a presença registrada só volta ao início", async () => {
    await registrarPresencaPorReconhecimento();

    expect(screen.getByRole("button", { name: /voltar ao início/i })).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /trilhas e missões/i }),
    ).not.toBeInTheDocument();
  });

  it("o caminho das trilhas tem título próprio nas duas formas da entrada", async () => {
    configurarSessao();
    renderizar(vi.fn(), vi.fn(), "trilhas");

    // A forma por nick e imagem.
    expect(screen.getByText(/quem vai ver as próprias trilhas/i)).toBeInTheDocument();
    expect(screen.queryByText(/quem está chegando/i)).not.toBeInTheDocument();

    // A forma por confirmação de Mestre ou Admin, alcançada sem câmera.
    cleanup();
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(false);
    renderizar(vi.fn(), vi.fn(), "trilhas");
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));

    expect(await screen.findByLabelText(/pin de quem confirma/i)).toBeInTheDocument();
    expect(screen.getByText(/quem vai ver as próprias trilhas/i)).toBeInTheDocument();
    expect(screen.queryByText(/quem está chegando/i)).not.toBeInTheDocument();
  });

  it("no caminho das trilhas a entrada não registra presença", async () => {
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
    const registrarPresenca = vi.spyOn(presencasApi, "registrarPresenca");

    renderizar(vi.fn(), vi.fn(), "trilhas");
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));

    await vi.waitFor(() => expect(entrarComToken).toHaveBeenCalledWith("token-do-guerreiro"));
    expect(registrarPresenca).not.toHaveBeenCalled();
  });
});

describe("sem rede, só o caminho da presença tem desfecho (RF-04-23, RF-04-58)", () => {
  it("o caminho das equipes não abre sem rede e nada é enfileirado", async () => {
    configurarSessao();
    const enfileirar = vi.spyOn(filaDePresenca, "enfileirarPresenca");

    render(
      <ProvedorDeEstadoDeRede>
        <TelaDeEntradaDoGuerreiro
          tokenDeTrabalho="token-de-trabalho"
          aulaId="aula-1"
          caminho="equipes"
          aoVoltar={vi.fn()}
        />
      </ProvedorDeEstadoDeRede>,
    );
    window.dispatchEvent(new Event("offline"));

    expect(await screen.findByText(/este caminho precisa de rede/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/pin de quem confirma/i)).not.toBeInTheDocument();
    expect(enfileirar).not.toHaveBeenCalled();
  });

  it("o caminho das trilhas não abre sem rede e nada é enfileirado", async () => {
    configurarSessao();
    const enfileirar = vi.spyOn(filaDePresenca, "enfileirarPresenca");

    render(
      <ProvedorDeEstadoDeRede>
        <TelaDeEntradaDoGuerreiro
          tokenDeTrabalho="token-de-trabalho"
          aulaId="aula-1"
          caminho="trilhas"
          aoVoltar={vi.fn()}
        />
      </ProvedorDeEstadoDeRede>,
    );
    window.dispatchEvent(new Event("offline"));

    expect(await screen.findByText(/este caminho precisa de rede/i)).toBeInTheDocument();
    expect(enfileirar).not.toHaveBeenCalled();
  });
});

describe("o foco inicial da entrada (RF-04-18, RF-04-21, RF-04-29)", () => {
  it("a entrada abre com o nick focado nos cinco caminhos", () => {
    const caminhos: CaminhoDaEntrada[] = ["presenca", "equipes", "quiz", "troca", "trilhas"];

    for (const caminho of caminhos) {
      configurarSessao();
      renderizar(vi.fn(), vi.fn(), caminho);

      expect(document.activeElement).toBe(screen.getByLabelText(/nick/i));

      cleanup();
    }
  });

  it("a confirmação por PIN também começa no nick, e o PIN não toma o foco", async () => {
    configurarSessao();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(false);

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));
    await screen.findByRole("button", { name: /confirmar identidade/i });

    expect(document.activeElement).toBe(screen.getByLabelText(/nick/i));
    expect(document.activeElement).not.toBe(screen.getByLabelText(/pin de quem confirma/i));
  });
});

// A conferência do PIN passou a viver num lugar só, alcançada pelos três atos
// que a pedem. A confirmação de identidade continua recusando e concluindo do
// mesmo jeito, e o contador de cinco erros é o mesmo dos três (`RF-04-21`,
// `RN-04-37`, `RN-04-41`, design — decisão 1).
describe("a conferência comum do PIN, vista da confirmação de identidade (RN-04-41)", () => {
  const PERSONA_DE_TRABALHO = "mestre-de-trabalho-1";

  afterEach(() => {
    sessionStorage.clear();
    localStorage.clear();
  });

  async function abrirConfirmacaoSemRede(usuario: ReturnType<typeof userEvent.setup>) {
    render(
      <ProvedorDeEstadoDeRede>
        <TelaDeEntradaDoGuerreiro
          tokenDeTrabalho="token-de-trabalho"
          aulaId="aula-1"
          caminho="presenca"
          aoVoltar={vi.fn()}
        />
      </ProvedorDeEstadoDeRede>,
    );
    window.dispatchEvent(new Event("offline"));
    await screen.findByText(/entrada por reconhecimento facial não funciona/i);
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
  }

  async function confirmarComOPin(
    usuario: ReturnType<typeof userEvent.setup>,
    pin: string,
    rotuloDoCampo: RegExp,
    rotuloDaAcao: RegExp,
  ) {
    await usuario.type(screen.getByLabelText(rotuloDoCampo), pin);
    await usuario.click(screen.getByRole("button", { name: rotuloDaAcao }));
  }

  it("a recusa e o desfecho da confirmação sem rede continuam os mesmos", async () => {
    configurarSessao();
    await guardarVerificadorDeTeste(PERSONA_DE_TRABALHO);
    const usuario = userEvent.setup();
    await abrirConfirmacaoSemRede(usuario);

    await confirmarComOPin(usuario, "0000", /pin de quem confirma/i, /confirmar identidade/i);

    expect(await screen.findByText(/pin errado/i)).toBeInTheDocument();
    expect(filaDePresenca.lerFilaDePresenca("aula-1")).toHaveLength(0);
    expect(estadoDoPinDe(PERSONA_DE_TRABALHO)?.erros).toBe(1);

    await confirmarComOPin(
      usuario,
      PIN_DE_TESTE,
      /pin de quem confirma/i,
      /confirmar identidade/i,
    );

    // Mesmo desfecho de antes: a presença entra na fila e a tela diz isso.
    expect(await screen.findByText(/guardada neste aparelho/i)).toBeInTheDocument();
    expect(filaDePresenca.lerFilaDePresenca("aula-1")).toHaveLength(1);
    // PIN que confere zera os erros seguidos, como sempre (`RN-04-38`).
    expect(estadoDoPinDe(PERSONA_DE_TRABALHO)?.erros).toBe(0);
  });

  it("errar na entrada e depois no encerramento soma no mesmo contador", async () => {
    configurarSessao();
    await guardarVerificadorDeTeste(PERSONA_DE_TRABALHO);
    const usuario = userEvent.setup();

    render(
      <ProvedorDeEstadoDeRede>
        <TelaInicial
          tokenDeTrabalho="token-de-trabalho"
          personaIdDeTrabalho={PERSONA_DE_TRABALHO}
          papelDeTrabalho="mestre"
          aulaId="aula-1"
          aoVoltarAoInicio={vi.fn()}
          podeAbrirMomentoDeTroca={false}
          momentoDeTrocaAberto={false}
          abrindoMomentoDeTroca={false}
          erroDeAberturaDaTroca={null}
          aoAbrirMomentoDeTroca={vi.fn()}
          aoFecharMomentoDeTroca={vi.fn()}
          aoEncerrarSessaoDeTrabalho={vi.fn()}
        />
      </ProvedorDeEstadoDeRede>,
    );
    window.dispatchEvent(new Event("offline"));

    // Três erros na confirmação de identidade, conferida no aparelho.
    await usuario.click(await screen.findByRole("button", { name: /presença — entrar/i }));
    await screen.findByText(/entrada por reconhecimento facial não funciona/i);
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    for (let tentativa = 0; tentativa < 3; tentativa += 1) {
      await confirmarComOPin(
        usuario,
        "0000",
        /pin de quem confirma/i,
        /confirmar identidade/i,
      );
      await vi.waitFor(() =>
        expect(screen.getByLabelText(/pin de quem confirma/i)).toHaveValue(""),
      );
    }
    expect(estadoDoPinDe(PERSONA_DE_TRABALHO)?.erros).toBe(3);

    // Mais dois no encerramento: o quinto bloqueia os três atos.
    await usuario.click(screen.getByRole("button", { name: /^voltar$/i }));
    await usuario.click(
      await screen.findByRole("button", { name: /encerrar a sessão de trabalho/i }),
    );
    for (let tentativa = 0; tentativa < 2; tentativa += 1) {
      await confirmarComOPin(
        usuario,
        "0000",
        /pin de quem abriu o aparelho/i,
        /^encerrar a sessão de trabalho$/i,
      );
      if (tentativa === 0) {
        await vi.waitFor(() =>
          expect(screen.getByLabelText(/pin de quem abriu o aparelho/i)).toHaveValue(""),
        );
      }
    }

    expect(await screen.findByText(/pin bloqueado neste aparelho/i)).toBeInTheDocument();
    expect(
      screen.getByText(/fechar a aba do navegador encerra a sessão/i),
    ).toBeInTheDocument();
    expect(pinBloqueadoNoAparelho()).toBe(true);
    expect(estadoDoPinDe(PERSONA_DE_TRABALHO)?.erros).toBe(5);
  });
});

// A fatia "Arena em primeiro plano": o desfecho da presença é o único momento
// em que esta aplicação apresenta o Guerreiro(a) a ele mesmo, e por isso é
// onde a carta domina a tela (documento 15 §6, decisão do fundador de
// 2026-09-25).
describe("a carta domina a tela da Arena (documento 15 §6)", () => {
  function mockarCarta() {
    vi.spyOn(cartaApi, "listarMinhasSeriesDaCarta").mockResolvedValue({
      itens: [{ comunidade_virtual_id: "comunidade-1" }],
    });
    vi.spyOn(cartaApi, "obterMinhaPosicaoNoRanking").mockResolvedValue({
      minha_posicao: {
        avatar: null,
        nick: "Zeferina",
        posicao: 2,
        pontos_regulares: 40,
      },
    });
    vi.spyOn(cartaApi, "obterProgressoDaCarta").mockResolvedValue([
      {
        trilha_id: "trilha-1",
        trilha_nome: "Robô Educa",
        nivel_atual: 3,
        badges: ["de_nivel"],
      },
    ]);
    vi.spyOn(cartaApi, "obterPortfolioDaCarta").mockResolvedValue([
      { producao: "Mapa das águas do bairro" },
    ]);
    vi.spyOn(trilhaComumApi, "listarPoderesDoCatalogo").mockResolvedValue([]);
  }

  /** A sessão do Guerreiro(a) já aberta, que é o estado do desfecho. */
  function configurarSessaoAberta() {
    vi.mocked(useSessao).mockReturnValue({
      sessao: {
        token: "token-do-guerreiro",
        persona_id: "guerreiro-1",
        papel: "guerreiro",
      },
      restaurando: false,
      entrando: false,
      erroDeEntrada: null,
      entrarComGoogle: vi.fn(),
      entrarComToken: vi.fn(),
      sair: vi.fn(),
      tratarRecusaDeSessao: vi.fn(),
      entrarComCredencial: vi.fn(),
      trocaDeSenhaPendente: false,
      trocandoSenha: false,
      erroDeTrocaDeSenha: null,
      trocarSenhaProvisoria: vi.fn(),
    } as unknown as ReturnType<typeof useSessao>);
  }

  async function chegarAoDesfecho() {
    configurarSessaoAberta();
    mockarCarta();
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "prepararCaptura").mockResolvedValue(undefined);
    vi.spyOn(biometriaModulo, "acoplarEspelho").mockImplementation(() => {});
    vi.spyOn(biometriaModulo, "encerrarCaptura").mockImplementation(() => {});
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
    mockarRegistrarPresencaEcoando();

    const { container } = renderizar(vi.fn(), vi.fn(), "presenca", vi.fn());
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));
    await screen.findByText(/presença registrada/i);
    return container;
  }

  it("a carta é o elemento maior do desfecho da presença, com uma decisão só", async () => {
    const container = await chegarAoDesfecho();

    // A carta chega e ocupa o primeiro plano do palco.
    const carta = await screen.findByRole("article", { name: /carta de zeferina/i });
    expect(container.querySelector(".cg-palco__personagem")).toContainElement(carta);

    // Uma decisão por tela: seguir às trilhas. Voltar ao início continua
    // oferecido, mas como saída, na ação do cabeçalho — os dois caminhos do
    // `RF-04-67` seguem inteiros, sem empilhar decisões.
    const decisao = container.querySelector(".cg-palco__decisao");
    expect(decisao?.querySelectorAll("button")).toHaveLength(1);
    expect(decisao?.textContent).toMatch(/ver as minhas trilhas e missões/i);
    expect(screen.getByRole("button", { name: /voltar ao início/i })).toBeInTheDocument();

    // A frase da presença registrada não se perde: fica no apoio, abaixo da
    // carta.
    expect(container.querySelector(".cg-palco__apoio")?.textContent).toMatch(
      /a presença de hoje está registrada/i,
    );
  });

  it("sem foto escolhida, o desfecho é a cor chapada, e nenhuma imagem é pedida", async () => {
    const container = await chegarAoDesfecho();

    // `ComunidadeVirtual` ainda não tem campo de foto, e a tela não perde
    // nada por isso (documento 15 §6.3).
    expect(container.querySelector(".cg-fundo-de-comunidade")).not.toBeNull();
    expect(container.querySelector("img")).toBeNull();
  });
});
