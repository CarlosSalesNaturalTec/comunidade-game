import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { TipoDeRecurso } from "../recursos/api";
import * as recursosApi from "../recursos/api";
import type { TipoDeColeta } from "./api";
import * as catalogosApi from "./api";
import { TelaDeCatalogos } from "./TelaDeCatalogos";

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
  persona_id: "admin-1",
};

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
};

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return { ...real, useSessao: vi.fn() };
});

import { useSessao } from "comum/autenticacao";

function configurarSessao(sessao: SessaoAberta | null) {
  vi.mocked(useSessao).mockReturnValue({
    sessao,
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
  });
}

function tipoDeRecurso(sobrescreve: Partial<TipoDeRecurso> = {}): TipoDeRecurso {
  return {
    id: "tipo-recurso-1",
    nome: "Lanche",
    natureza: "consumivel",
    unidade: "kit",
    exige_comprovante: false,
    valor_em_moedas: "12.50",
    vigencia_inicio: "2026-08-01",
    ...sobrescreve,
  };
}

function tipoDeColeta(sobrescreve: Partial<TipoDeColeta> = {}): TipoDeColeta {
  return {
    id: "tipo-coleta-1",
    nome: "Temperatura",
    forma_de_registro: "numero",
    unidade: "°C",
    faixa_minima: -10,
    faixa_maxima: 55,
    ativo: true,
    ...sobrescreve,
  };
}

function dublarCatalogos(recursos: TipoDeRecurso[], coletas: TipoDeColeta[]) {
  vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue(recursos);
  vi.spyOn(catalogosApi, "listarTodosOsTiposDeColeta").mockResolvedValue(coletas);
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("A App 03 abre a área Catálogos, fora do escopo de comunidade", () => {
  it("reúne os dois catálogos", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([tipoDeRecurso()], [tipoDeColeta()]);

    render(<TelaDeCatalogos />);

    expect(
      await screen.findByRole("list", { name: "Catálogo de tipos de recurso" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("list", { name: "Catálogo de tipos de coleta" }),
    ).toBeInTheDocument();
  });

  it("não pede comunidade", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([tipoDeRecurso()], [tipoDeColeta()]);

    render(<TelaDeCatalogos />);
    await screen.findByRole("list", { name: "Catálogo de tipos de recurso" });

    expect(screen.queryByLabelText(/comunidade/i)).not.toBeInTheDocument();
  });

  it("apresenta catálogo vazio como informação, não como erro", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([], []);

    render(<TelaDeCatalogos />);

    expect(
      await screen.findByText(/Nenhum tipo de recurso cadastrado ainda/),
    ).toBeInTheDocument();
    expect(screen.getByText(/Nenhum tipo de coleta cadastrado ainda/)).toBeInTheDocument();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});

describe("A área Catálogos apresenta os tipos de recurso com o valor vigente", () => {
  it("traz o valor da vigência corrente", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos(
      [
        tipoDeRecurso({
          nome: "Hora-aula",
          exige_comprovante: true,
          valor_em_moedas: "30.00",
        }),
      ],
      [],
    );

    render(<TelaDeCatalogos />);

    const lista = await screen.findByRole("list", { name: "Catálogo de tipos de recurso" });
    expect(within(lista).getByText("Hora-aula")).toBeInTheDocument();
    expect(within(lista).getByText("Consumível")).toBeInTheDocument();
    expect(within(lista).getByText("Unidade: kit")).toBeInTheDocument();
    expect(within(lista).getByText("30.00 moedas")).toBeInTheDocument();
    expect(within(lista).getByText("Exige comprovante")).toBeInTheDocument();
  });

  it("diz que mostra apenas o que tem valor vigente", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([tipoDeRecurso()], []);

    render(<TelaDeCatalogos />);

    expect(
      await screen.findByText(/valor de referência vigente na data de hoje/),
    ).toBeInTheDocument();
  });
});

describe("O Admin cadastra o tipo de recurso pela aplicação", () => {
  it("cadastra o tipo com a primeira vigência no mesmo ato", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([], []);
    const cadastrar = vi
      .spyOn(recursosApi, "cadastrarTipoDeRecurso")
      .mockResolvedValue(tipoDeRecurso());

    render(<TelaDeCatalogos />);
    await userEvent.click(await screen.findByRole("button", { name: "Novo tipo de recurso" }));

    await userEvent.type(screen.getByLabelText("Nome"), "Lanche");
    await userEvent.selectOptions(screen.getByLabelText("Natureza"), "consumivel");
    await userEvent.type(screen.getByLabelText("Unidade"), "kit");
    await userEvent.type(screen.getByLabelText("Valor de referência em moedas"), "12.50");
    await userEvent.click(screen.getByRole("button", { name: "Cadastrar" }));

    await waitFor(() => expect(cadastrar).toHaveBeenCalledTimes(1));
    const [entrada] = cadastrar.mock.calls[0];
    expect(entrada.nome).toBe("Lanche");
    expect(entrada.valor_em_moedas).toBe("12.50");
    expect(entrada.vigencia_inicio).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  });

  it("oferece a natureza como escolha, nunca como texto livre", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([], []);

    render(<TelaDeCatalogos />);
    await userEvent.click(await screen.findByRole("button", { name: "Novo tipo de recurso" }));

    const natureza = screen.getByLabelText("Natureza");
    expect(natureza.tagName).toBe("SELECT");
    expect(
      within(natureza)
        .getAllByRole("option")
        .map((o) => o.textContent),
    ).toEqual(["Consumível", "Durável", "Serviço", "Financeiro"]);
  });

  it("nasce sem exigir comprovante quando a marca não é declarada", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([], []);
    const cadastrar = vi
      .spyOn(recursosApi, "cadastrarTipoDeRecurso")
      .mockResolvedValue(tipoDeRecurso());

    render(<TelaDeCatalogos />);
    await userEvent.click(await screen.findByRole("button", { name: "Novo tipo de recurso" }));
    await userEvent.type(screen.getByLabelText("Nome"), "Lanche");
    await userEvent.type(screen.getByLabelText("Unidade"), "kit");
    await userEvent.type(screen.getByLabelText("Valor de referência em moedas"), "12.50");
    await userEvent.click(screen.getByRole("button", { name: "Cadastrar" }));

    await waitFor(() => expect(cadastrar).toHaveBeenCalledTimes(1));
    expect(cadastrar.mock.calls[0][0].exige_comprovante).toBe(false);
  });

  it("apresenta a recusa do núcleo no campo que a originou", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([], []);
    vi.spyOn(recursosApi, "cadastrarTipoDeRecurso").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "O valor em moedas tem no máximo duas casas decimais.",
        campo: "valor_em_moedas",
      }),
    );

    render(<TelaDeCatalogos />);
    await userEvent.click(await screen.findByRole("button", { name: "Novo tipo de recurso" }));
    await userEvent.type(screen.getByLabelText("Nome"), "Lanche");
    await userEvent.type(screen.getByLabelText("Unidade"), "kit");
    await userEvent.type(screen.getByLabelText("Valor de referência em moedas"), "12.505");
    await userEvent.click(screen.getByRole("button", { name: "Cadastrar" }));

    expect(
      await screen.findByText("O valor em moedas tem no máximo duas casas decimais."),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Valor de referência em moedas")).toHaveAttribute(
      "aria-invalid",
      "true",
    );
  });

  it("não oferece o cadastro a quem não é Admin", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    dublarCatalogos([tipoDeRecurso()], [tipoDeColeta()]);

    render(<TelaDeCatalogos />);
    await screen.findByRole("list", { name: "Catálogo de tipos de recurso" });

    expect(
      screen.queryByRole("button", { name: "Novo tipo de recurso" }),
    ).not.toBeInTheDocument();
  });
});

describe("A área Catálogos apresenta os tipos de coleta com a marca de ativo", () => {
  it("traz os tipos cadastrados", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([], [tipoDeColeta()]);

    render(<TelaDeCatalogos />);

    const lista = await screen.findByRole("list", { name: "Catálogo de tipos de coleta" });
    expect(within(lista).getByText("Temperatura")).toBeInTheDocument();
    expect(within(lista).getByText("Número")).toBeInTheDocument();
    expect(within(lista).getByText("Unidade: °C")).toBeInTheDocument();
    expect(within(lista).getByText("Faixa: -10 a 55")).toBeInTheDocument();
  });

  it("apresenta o tipo por evidência sem unidade e sem faixa", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos(
      [],
      [
        tipoDeColeta({
          nome: "Foto do córrego",
          forma_de_registro: "foto",
          unidade: null,
          faixa_minima: null,
          faixa_maxima: null,
        }),
      ],
    );

    render(<TelaDeCatalogos />);

    const lista = await screen.findByRole("list", { name: "Catálogo de tipos de coleta" });
    expect(within(lista).getByText("Foto")).toBeInTheDocument();
    expect(within(lista).queryByText(/Unidade:/)).not.toBeInTheDocument();
    expect(within(lista).queryByText(/Faixa:/)).not.toBeInTheDocument();
  });

  it("assinala o tipo desativado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos(
      [],
      [
        tipoDeColeta({ id: "ativo", nome: "Temperatura", ativo: true }),
        tipoDeColeta({ id: "inativo", nome: "Descontinuado", ativo: false }),
      ],
    );

    render(<TelaDeCatalogos />);

    const lista = await screen.findByRole("list", { name: "Catálogo de tipos de coleta" });
    expect(within(lista).getByText("Inativo")).toBeInTheDocument();
    expect(within(lista).getByText("Ativo")).toBeInTheDocument();
  });

  it("segue a paginação do núcleo até o fim", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([]);
    vi.spyOn(catalogosApi, "listarTodosOsTiposDeColeta").mockResolvedValue([
      tipoDeColeta({ id: "pagina-1", nome: "Temperatura" }),
      tipoDeColeta({ id: "pagina-2", nome: "Ruído" }),
    ]);

    render(<TelaDeCatalogos />);

    const lista = await screen.findByRole("list", { name: "Catálogo de tipos de coleta" });
    expect(within(lista).getAllByRole("listitem")).toHaveLength(2);
  });
});

describe("O Admin cadastra o tipo de coleta pela aplicação", () => {
  async function abrirFormularioDeColeta() {
    render(<TelaDeCatalogos />);
    await userEvent.click(await screen.findByRole("button", { name: "Novo tipo de coleta" }));
  }

  it("cadastra o tipo que se mede por número", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([], []);
    const cadastrar = vi
      .spyOn(catalogosApi, "cadastrarTipoDeColeta")
      .mockResolvedValue(tipoDeColeta());

    await abrirFormularioDeColeta();
    await userEvent.type(screen.getByLabelText("Nome"), "Temperatura");
    await userEvent.type(screen.getByLabelText("Unidade"), "°C");
    await userEvent.type(screen.getByLabelText("Faixa esperada — mínimo"), "-10");
    await userEvent.type(screen.getByLabelText("Faixa esperada — máximo"), "55");
    await userEvent.click(screen.getByRole("button", { name: "Cadastrar" }));

    await waitFor(() => expect(cadastrar).toHaveBeenCalledTimes(1));
    expect(cadastrar.mock.calls[0][0]).toMatchObject({
      nome: "Temperatura",
      forma_de_registro: "numero",
      unidade: "°C",
      faixa_minima: -10,
      faixa_maxima: 55,
    });
  });

  it("exige unidade e faixa antes de confirmar, na forma número", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([], []);
    const cadastrar = vi.spyOn(catalogosApi, "cadastrarTipoDeColeta");

    await abrirFormularioDeColeta();
    await userEvent.type(screen.getByLabelText("Nome"), "Temperatura");
    await userEvent.click(screen.getByRole("button", { name: "Cadastrar" }));

    expect(
      await screen.findByText("O tipo que se mede por número exige unidade."),
    ).toBeInTheDocument();
    expect(cadastrar).not.toHaveBeenCalled();
  });

  it("dispensa unidade e faixa na forma por evidência", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([], []);
    const cadastrar = vi
      .spyOn(catalogosApi, "cadastrarTipoDeColeta")
      .mockResolvedValue(tipoDeColeta());

    await abrirFormularioDeColeta();
    await userEvent.type(screen.getByLabelText("Nome"), "Foto do córrego");
    await userEvent.selectOptions(screen.getByLabelText("Forma de registro"), "foto");

    expect(screen.queryByLabelText("Unidade")).not.toBeInTheDocument();
    expect(screen.queryByLabelText("Faixa esperada — mínimo")).not.toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Cadastrar" }));

    await waitFor(() => expect(cadastrar).toHaveBeenCalledTimes(1));
    expect(cadastrar.mock.calls[0][0]).toEqual({
      nome: "Foto do córrego",
      forma_de_registro: "foto",
    });
  });

  it("oferece a forma de registro como escolha, nunca como texto livre", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([], []);

    await abrirFormularioDeColeta();

    const forma = screen.getByLabelText("Forma de registro");
    expect(forma.tagName).toBe("SELECT");
    expect(
      within(forma)
        .getAllByRole("option")
        .map((o) => o.textContent),
    ).toEqual(["Número", "Foto", "Vídeo"]);
  });

  it("apresenta a recusa da faixa no campo da faixa", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    dublarCatalogos([], []);
    vi.spyOn(catalogosApi, "cadastrarTipoDeColeta").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "A faixa mínima não pode ser maior que a máxima.",
        campo: "faixa_minima",
      }),
    );

    await abrirFormularioDeColeta();
    await userEvent.type(screen.getByLabelText("Nome"), "Temperatura");
    await userEvent.type(screen.getByLabelText("Unidade"), "°C");
    await userEvent.type(screen.getByLabelText("Faixa esperada — mínimo"), "80");
    await userEvent.type(screen.getByLabelText("Faixa esperada — máximo"), "10");
    await userEvent.click(screen.getByRole("button", { name: "Cadastrar" }));

    expect(
      await screen.findByText("A faixa mínima não pode ser maior que a máxima."),
    ).toBeInTheDocument();
  });

  it("não oferece o cadastro a quem não é Admin", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    dublarCatalogos([tipoDeRecurso()], [tipoDeColeta()]);

    render(<TelaDeCatalogos />);
    await screen.findByRole("list", { name: "Catálogo de tipos de coleta" });

    expect(
      screen.queryByRole("button", { name: "Novo tipo de coleta" }),
    ).not.toBeInTheDocument();
  });
});
