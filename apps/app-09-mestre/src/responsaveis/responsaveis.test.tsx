import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { GuerreiroVinculavel, ResponsavelDaLista, VinculoCriado } from "./api";
import * as responsaveisApi from "./api";
import { FormularioDeResponsavel } from "./FormularioDeResponsavel";
import { TelaDeResponsaveis } from "./TelaDeResponsaveis";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

vi.mock("../direitos/ContextoDeDireitos", async () => {
  const real = await vi.importActual<typeof import("../direitos/ContextoDeDireitos")>(
    "../direitos/ContextoDeDireitos",
  );
  return { ...real, useDireitos: () => ({ irParaDireitos: vi.fn() }) };
});

import { useSessao } from "comum/autenticacao";

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
};

function configurarSessao() {
  vi.mocked(useSessao).mockReturnValue({
    sessao: SESSAO_DE_MESTRE,
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

const GUERREIRO = { id: "guerreiro-1", nick: "guerreira-teste", avatar: "avatar-1" };

afterEach(() => {
  vi.restoreAllMocks();
});

describe("cadastro do responsável", () => {
  it("declara que o cadastro pressupõe a apresentação presencial", () => {
    configurarSessao();
    render(<FormularioDeResponsavel onConcluido={vi.fn()} />);

    expect(screen.getByText(/apresentou pessoalmente/i)).toBeInTheDocument();
  });

  it("mostra o aviso de coleta do cadastro e do vínculo", () => {
    configurarSessao();
    render(<FormularioDeResponsavel onConcluido={vi.fn()} />);

    expect(screen.getByText(/coleta o cadastro e o vínculo do responsável/i)).toHaveAttribute(
      "role",
      "status",
    );
  });

  it("recusa o cadastro sem nome", async () => {
    configurarSessao();
    const cadastrarEspiado = vi.spyOn(responsaveisApi, "cadastrarResponsavel");
    render(<FormularioDeResponsavel onConcluido={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));

    expect(await screen.findByText(/informe o nome/i)).toBeInTheDocument();
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });
});

describe("vínculo com Guerreiro(a)", () => {
  it("escolhe o Guerreiro(a) por nick e avatar, e exige o grau de parentesco", async () => {
    configurarSessao();
    vi.spyOn(responsaveisApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-1",
      nome: "Maria",
    });
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: [GUERREIRO],
      proximo_cursor: null,
    });
    const criarVinculoEspiado = vi.spyOn(responsaveisApi, "criarVinculo");

    render(<FormularioDeResponsavel onConcluido={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Maria");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/responsável cadastrado/i);

    const opcao = await screen.findByRole("option", { name: /guerreira-teste — avatar-1/i });
    expect(opcao).toBeInTheDocument();
    expect(screen.queryByRole("img")).not.toBeInTheDocument();

    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), GUERREIRO.id);
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));
    expect(await screen.findByText(/informe o grau de parentesco/i)).toBeInTheDocument();
    expect(criarVinculoEspiado).not.toHaveBeenCalled();
  });

  it("cria dois vínculos, cada um com o seu grau de parentesco", async () => {
    configurarSessao();
    vi.spyOn(responsaveisApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-1",
      nome: "Maria",
    });
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: [GUERREIRO, { id: "guerreiro-2", nick: "guerreiro-dois", avatar: "avatar-2" }],
      proximo_cursor: null,
    });
    vi.spyOn(responsaveisApi, "criarVinculo")
      .mockResolvedValueOnce({
        id: "v1",
        responsavel_id: "resp-1",
        guerreiro_id: "guerreiro-1",
        grau_de_parentesco: "mãe",
        inicio: "2026-08-29T10:00:00-03:00",
      })
      .mockResolvedValueOnce({
        id: "v2",
        responsavel_id: "resp-1",
        guerreiro_id: "guerreiro-2",
        grau_de_parentesco: "tia",
        inicio: "2026-08-29T10:05:00-03:00",
      });

    render(<FormularioDeResponsavel onConcluido={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Maria");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/responsável cadastrado/i);

    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), GUERREIRO.id);
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "mãe");
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));
    await screen.findByText("guerreira-teste — mãe");

    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), "guerreiro-2");
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "tia");
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));

    expect(await screen.findByText("guerreiro-dois — tia")).toBeInTheDocument();
    expect(screen.getByText("guerreira-teste — mãe")).toBeInTheDocument();
  });

  it("o quarto vínculo é recusado com o teto de três, sem perder o que já foi criado", async () => {
    configurarSessao();
    vi.spyOn(responsaveisApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-1",
      nome: "Maria",
    });
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: [GUERREIRO],
      proximo_cursor: null,
    });
    vi.spyOn(responsaveisApi, "criarVinculo").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Este Guerreiro(a) já tem três responsáveis vigentes.",
        campo: "guerreiro_id",
      }),
    );

    render(<FormularioDeResponsavel onConcluido={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Maria");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/responsável cadastrado/i);

    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), GUERREIRO.id);
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "tio");
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));

    expect(await screen.findByText(/três responsáveis vigentes/i)).toBeInTheDocument();
    expect(screen.getByText(/responsável cadastrado/i)).toBeInTheDocument();
  });
});

// A lista de vínculos já criados imprimia só o grau de parentesco, enquanto o
// seletor logo acima já mostrava `nick — avatar`: dois vínculos de "Pai"
// viravam duas linhas idênticas (`RF-09-63`).
describe("o vínculo já criado identifica o Guerreiro(a) pelo nick", () => {
  function vinculoDe(id: string, guerreiroId: string, grau: string): VinculoCriado {
    return {
      id,
      responsavel_id: "resp-1",
      guerreiro_id: guerreiroId,
      grau_de_parentesco: grau,
      inicio: "2026-09-27T10:00:00-03:00",
    };
  }

  async function abrirOPassoDeVinculo(guerreiros: GuerreiroVinculavel[]) {
    configurarSessao();
    vi.spyOn(responsaveisApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-1",
      nome: "Maria",
    });
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: guerreiros,
      proximo_cursor: null,
    });

    render(<FormularioDeResponsavel onConcluido={vi.fn()} />);
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Maria");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/responsável cadastrado/i);
    return usuario;
  }

  async function vincular(
    usuario: ReturnType<typeof userEvent.setup>,
    guerreiroId: string,
    grau: string,
  ) {
    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), guerreiroId);
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), grau);
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));
  }

  function linhasDosVinculos() {
    const lista = screen.getByRole("list", { name: /vínculos já criados/i });
    return within(lista)
      .getAllByRole("listitem")
      .map((item) => item.textContent);
  }

  it("traz o nick ao lado do grau de parentesco", async () => {
    const usuario = await abrirOPassoDeVinculo([GUERREIRO]);
    vi.spyOn(responsaveisApi, "criarVinculo").mockResolvedValue(
      vinculoDe("v-1", GUERREIRO.id, "Pai"),
    );

    await vincular(usuario, GUERREIRO.id, "Pai");

    await screen.findByRole("list", { name: /vínculos já criados/i });
    expect(linhasDosVinculos()).toEqual([`${GUERREIRO.nick} — Pai`]);
  });

  it("dois vínculos de mesmo parentesco continuam distinguíveis", async () => {
    const OUTRO: GuerreiroVinculavel = {
      id: "guerreiro-2",
      nick: "guerreiro-dois",
      avatar: "avatar-2",
    };
    const usuario = await abrirOPassoDeVinculo([GUERREIRO, OUTRO]);
    vi.spyOn(responsaveisApi, "criarVinculo")
      .mockResolvedValueOnce(vinculoDe("v-1", GUERREIRO.id, "Pai"))
      .mockResolvedValueOnce(vinculoDe("v-2", OUTRO.id, "Pai"));

    await vincular(usuario, GUERREIRO.id, "Pai");
    await screen.findByRole("list", { name: /vínculos já criados/i });
    await vincular(usuario, OUTRO.id, "Pai");
    await waitFor(() => expect(linhasDosVinculos()).toHaveLength(2));

    const linhas = linhasDosVinculos();
    expect(linhas).toEqual([`${GUERREIRO.nick} — Pai`, `${OUTRO.nick} — Pai`]);
    expect(new Set(linhas).size).toBe(2);
  });

  it("Guerreiro(a) sem nick gravado não apaga a linha", async () => {
    const semNick: GuerreiroVinculavel = { id: "guerreiro-9", nick: "", avatar: "avatar-9" };
    const usuario = await abrirOPassoDeVinculo([semNick]);
    vi.spyOn(responsaveisApi, "criarVinculo").mockResolvedValue(
      vinculoDe("v-1", semNick.id, "Mãe"),
    );

    await vincular(usuario, semNick.id, "Mãe");

    await screen.findByRole("list", { name: /vínculos já criados/i });
    const [linha] = linhasDosVinculos();
    expect(linha).toMatch(/sem nick/i);
    expect(linha).toMatch(/Mãe/);
  });
});

// A área abria direto no cadastro, e responsável cadastrado ficava
// inalcançável — pior no Mestre, que cadastra presencialmente e é quem mais
// interrompe o cadastro antes do vínculo (`RF-09-122`).
describe("área de responsáveis do Mestre", () => {
  const COM_VINCULO: ResponsavelDaLista = {
    id: "resp-1",
    nome: "Dona Maria",
    vinculados: [
      { guerreiro_id: GUERREIRO.id, nick: GUERREIRO.nick, grau_de_parentesco: "mãe" },
    ],
  };

  const SEM_VINCULO: ResponsavelDaLista = { id: "resp-2", nome: "Seu João", vinculados: [] };

  function configurarArea(itens: ResponsavelDaLista[]) {
    configurarSessao();
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: [GUERREIRO],
      proximo_cursor: null,
    });
    return vi.spyOn(responsaveisApi, "listarResponsaveis").mockResolvedValue({
      itens,
      proximo_cursor: null,
    });
  }

  it("abre na lista dos responsáveis que o Mestre alcança, não no cadastro", async () => {
    configurarArea([COM_VINCULO]);

    render(<TelaDeResponsaveis />);

    expect(await screen.findByText("Dona Maria")).toBeInTheDocument();
    expect(screen.queryByLabelText(/nome do responsável/i)).not.toBeInTheDocument();
    const tabela = screen.getByRole("table", { name: /responsáveis cadastrados/i });
    expect(within(tabela).getByText(/guerreira-teste \(mãe\)/)).toBeInTheDocument();
  });

  it("sinaliza o cadastro interrompido, sem Guerreiro(a) vinculado", async () => {
    configurarArea([SEM_VINCULO]);

    render(<TelaDeResponsaveis />);

    expect(await screen.findByText("Seu João")).toBeInTheDocument();
    expect(screen.getByText(/cadastro por concluir/i)).toBeInTheDocument();
  });

  it("lista vazia é dita, e o cadastro continua oferecido", async () => {
    configurarArea([]);

    render(<TelaDeResponsaveis />);

    expect(await screen.findByText(/nenhum responsável cadastrado/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /cadastrar responsável/i })).toBeInTheDocument();
  });

  it("o cadastro é alcançável a partir da lista", async () => {
    const listar = configurarArea([]);
    vi.spyOn(responsaveisApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-3",
      nome: "Nova",
    });

    render(<TelaDeResponsaveis />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /cadastrar responsável/i }));

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Nova");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/vincule os guerreiros e guerreiras de nova/i);

    await usuario.click(screen.getByRole("button", { name: /^concluir$/i }));
    await waitFor(() => expect(listar).toHaveBeenCalledTimes(2));
  });

  it("retoma um responsável e vincula outro Guerreiro(a), sem cadastrar ninguém", async () => {
    configurarArea([SEM_VINCULO]);
    const cadastrar = vi.spyOn(responsaveisApi, "cadastrarResponsavel");
    const criarVinculo = vi.spyOn(responsaveisApi, "criarVinculo").mockResolvedValue({
      id: "v-1",
      responsavel_id: SEM_VINCULO.id,
      guerreiro_id: GUERREIRO.id,
      grau_de_parentesco: "Pai",
      inicio: "2026-09-27T10:00:00-03:00",
    });

    render(<TelaDeResponsaveis />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: "Seu João" }));

    expect(
      await screen.findByText(/vincule mais guerreiros e guerreiras a seu joão/i),
    ).toBeInTheDocument();
    expect(screen.queryByLabelText(/nome do responsável/i)).not.toBeInTheDocument();

    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), GUERREIRO.id);
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "Pai");
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));

    await waitFor(() => expect(criarVinculo).toHaveBeenCalledTimes(1));
    expect(criarVinculo.mock.calls[0][0]).toBe(SEM_VINCULO.id);
    expect(cadastrar).not.toHaveBeenCalled();
    expect(await screen.findByText(`${GUERREIRO.nick} — Pai`)).toBeInTheDocument();
  });

  it("o teto de três continua explicado na retomada", async () => {
    configurarArea([SEM_VINCULO]);
    vi.spyOn(responsaveisApi, "criarVinculo").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Este Guerreiro(a) já tem três responsáveis vigentes.",
        campo: "guerreiro_id",
      }),
    );

    render(<TelaDeResponsaveis />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: "Seu João" }));
    await screen.findByText(/vincule mais guerreiros/i);

    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), GUERREIRO.id);
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "tio");
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));

    expect(await screen.findByText(/três responsáveis vigentes/i)).toBeInTheDocument();
  });

  it("não expõe credencial nem dado civil da criança", async () => {
    // Nick escolhido para não conter nome civil algum, para a asserção não
    // passar por acidente.
    configurarArea([
      {
        id: "resp-4",
        nome: "Dona Maria",
        vinculados: [
          { guerreiro_id: GUERREIRO.id, nick: "NickSemNomeCivil", grau_de_parentesco: "mãe" },
        ],
      },
    ]);

    render(<TelaDeResponsaveis />);
    await screen.findByText("Dona Maria");

    const tabela = screen.getByRole("table", { name: /responsáveis cadastrados/i });
    expect(tabela.textContent).not.toMatch(/senha|usuário|credencial/i);
    expect(tabela.textContent).not.toMatch(/nascimento|\d{4}-\d{2}-\d{2}/);
  });
});

describe("credencial provisória", () => {
  it("mostra a senha provisória uma vez, sem caminho para recuperá-la", async () => {
    configurarSessao();
    vi.spyOn(responsaveisApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-1",
      nome: "Maria",
    });
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(responsaveisApi, "criarCredencialProvisoria").mockResolvedValue({
      id: "cred-1",
      usuario: "maria",
      senha_provisoria: "abc123",
    });

    render(<FormularioDeResponsavel onConcluido={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Maria");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/responsável cadastrado/i);

    await usuario.type(screen.getByLabelText(/usuário \(para quem/i), "maria");
    await usuario.click(screen.getByRole("button", { name: /criar credencial provisória/i }));

    expect(await screen.findByText(/abc123/)).toBeInTheDocument();
    expect(screen.getByText(/não aparece de novo/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /criar credencial provisória/i }),
    ).not.toBeInTheDocument();
  });
});
