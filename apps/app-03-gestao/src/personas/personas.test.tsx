import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { configurarAcessoAoNucleo, ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as agendaApi from "../agenda/api";
import type { AdultoDaLista, GuerreiroDaLista, VinculoCriado } from "./api";
import * as personasApi from "./api";
import { FichaDoAdulto } from "./FichaDoAdulto";
import { FormularioDeAdmin } from "./FormularioDeAdmin";
import { FormularioDeAdulto } from "./FormularioDeAdulto";
import { FormularioDeGuerreiro } from "./FormularioDeGuerreiro";
import { FormularioDeResponsavel } from "./FormularioDeResponsavel";
import { ListaDeAdultos } from "./ListaDeAdultos";
import { ListaDeGuerreiros } from "./ListaDeGuerreiros";
import { TelaDeAdultos } from "./TelaDeAdultos";

vi.mock("../direitos/ContextoDeDireitos", async () => {
  const real = await vi.importActual<typeof import("../direitos/ContextoDeDireitos")>(
    "../direitos/ContextoDeDireitos",
  );
  return { ...real, useDireitos: () => ({ irParaDireitos: vi.fn() }) };
});

const COMUNIDADE = {
  id: "c1",
  nome: "Comunidade",
  localizacao: "x",
  series_abertas: null,
  series_ativas: null,
  registros_validos: null,
  continuidade: null,
};

const AULA = {
  id: "aula-1",
  comunidade_virtual_id: COMUNIDADE.id,
  ponto_de_apoio_id: "ponto-1",
  inicio_em: "2026-08-21T10:00:00-03:00",
  fim_em: "2026-08-21T12:00:00-03:00",
  situacao: "confirmada",
  cancelamento_motivo: null,
  recursos_faltantes: [],
};

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
  persona_id: "admin-1",
};

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
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

const GUERREIRO: GuerreiroDaLista = {
  id: "guerreiro-1",
  nome: "Zeferina",
  nascimento: "2015-03-20",
  nick: "ZeferinaGuerreira",
  avatar: "avatar-opaco",
  comunidade_virtual_id: COMUNIDADE.id,
  vinculo_iniciado_em: "2026-08-01T10:00:00-03:00",
};

const GUERREIRO_SEM_VINCULO: GuerreiroDaLista = {
  id: "guerreiro-2",
  nome: "Sem Vínculo",
  nascimento: "2015-03-20",
  nick: "SemVinculo",
  avatar: "avatar-opaco",
  comunidade_virtual_id: null,
  vinculo_iniciado_em: null,
};

const MESTRE_COM_ARTEFATO: AdultoDaLista = {
  id: "mestre-1",
  nome: "Mestre de Tal",
  email: "mestre@example.org",
  whatsapp: "11999990000",
  nick: "MestreDeTal",
  artefatos: [{ rotulo: "Certificado de curso", endereco: "https://exemplo.org/certificado" }],
};

const ADULTO_SEM_NICK: AdultoDaLista = {
  id: "a1",
  nome: "Apoiador de Tal",
  email: "a@example.org",
  whatsapp: null,
  nick: null,
  artefatos: [],
};

afterEach(() => {
  vi.restoreAllMocks();
});

describe("cadastro do Guerreiro(a)", () => {
  async function preencherFormularioDeCadastro(usuario: ReturnType<typeof userEvent.setup>) {
    await usuario.type(screen.getByLabelText(/^nome$/i), "Zeferina");
    await usuario.type(screen.getByLabelText(/data de nascimento/i), "2015-03-20");
    await usuario.type(screen.getByLabelText(/^nick$/i), "ZeferinaGuerreira");
    await usuario.type(screen.getByLabelText(/^avatar$/i), "avatar-opaco");
    await usuario.selectOptions(screen.getByLabelText(/^comunidade$/i), COMUNIDADE.id);
    await usuario.selectOptions(
      await screen.findByLabelText(/aula em que se cadastra/i),
      AULA.id,
    );
  }

  it("Admin cadastra o Guerreiro(a) informando os quatro campos", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "cadastrarGuerreiro").mockResolvedValue(GUERREIRO);
    vi.spyOn(agendaApi, "listarAgenda").mockResolvedValue({
      itens: [AULA],
      proximo_cursor: null,
    });

    render(
      <FormularioDeGuerreiro
        comunidades={[COMUNIDADE]}
        onSalvo={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();

    await preencherFormularioDeCadastro(usuario);
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    await waitFor(() => expect(personasApi.cadastrarGuerreiro).toHaveBeenCalled());
  });

  it("mostra o aviso de coleta do dado do Guerreiro(a), sem bloquear o envio", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "cadastrarGuerreiro").mockResolvedValue(GUERREIRO);
    vi.spyOn(agendaApi, "listarAgenda").mockResolvedValue({
      itens: [AULA],
      proximo_cursor: null,
    });

    render(
      <FormularioDeGuerreiro
        comunidades={[COMUNIDADE]}
        onSalvo={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );

    expect(
      screen.getByText(/nome, a data de nascimento, o nick e o avatar do guerreiro/i),
    ).toHaveAttribute("role", "status");

    const usuario = userEvent.setup();
    await preencherFormularioDeCadastro(usuario);
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    await waitFor(() => expect(personasApi.cadastrarGuerreiro).toHaveBeenCalled());
  });

  it("nick em uso é explicado sem revelar o dono", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "cadastrarGuerreiro").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Nick em uso.",
        campo: "nick",
      }),
    );
    vi.spyOn(agendaApi, "listarAgenda").mockResolvedValue({
      itens: [AULA],
      proximo_cursor: null,
    });

    render(
      <FormularioDeGuerreiro
        comunidades={[COMUNIDADE]}
        onSalvo={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();
    await preencherFormularioDeCadastro(usuario);
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    const mensagem = await screen.findByText(/nick já está em uso/i);
    expect(mensagem.textContent?.toLowerCase()).not.toContain("guerreiro");
    expect(mensagem.textContent?.toLowerCase()).not.toContain("mestre");
    expect(mensagem.textContent?.toLowerCase()).not.toContain("apoiador");
  });

  it("a gestão não vê a imagem do Guerreiro(a) — só nick e avatar", () => {
    render(
      <ListaDeGuerreiros
        guerreiros={[GUERREIRO]}
        comunidades={[COMUNIDADE]}
        onEditar={vi.fn()}
      />,
    );

    expect(screen.getByText("ZeferinaGuerreira")).toBeInTheDocument();
    expect(screen.queryByRole("img")).not.toBeInTheDocument();
  });
});

describe("o vínculo de comunidade na lista de Guerreiros e Guerreiras", () => {
  it("apresenta a comunidade herdada da aula e a data de início do vínculo", () => {
    render(
      <ListaDeGuerreiros
        guerreiros={[GUERREIRO]}
        comunidades={[COMUNIDADE]}
        onEditar={vi.fn()}
      />,
    );

    expect(screen.getByRole("cell", { name: /comunidade/i })).toBeInTheDocument();
    expect(screen.getByText(/desde/i)).toBeInTheDocument();
  });

  it("Guerreiro(a) sem vínculo vigente é informado, não acusado", () => {
    render(
      <ListaDeGuerreiros
        guerreiros={[GUERREIRO_SEM_VINCULO]}
        comunidades={[COMUNIDADE]}
        onEditar={vi.fn()}
      />,
    );

    const ausencia = screen.getByText(/ainda sem vínculo de comunidade/i);
    expect(ausencia).toHaveAttribute("role", "status");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("não existe caminho para mudar a comunidade do Guerreiro(a) na edição", () => {
    render(
      <FormularioDeGuerreiro
        comunidades={[COMUNIDADE]}
        guerreiroExistente={GUERREIRO}
        onSalvo={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );

    expect(screen.queryByLabelText(/^comunidade$/i)).not.toBeInTheDocument();
  });
});

describe("cadastro de Mestre e de Apoiador", () => {
  it("sem artefato a aplicação não deixa confirmar", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const cadastrarEspiado = vi.spyOn(personasApi, "cadastrarMestre");

    render(<FormularioDeAdulto papel="mestre" onSalvo={vi.fn()} onCancelar={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/^nome$/i), "Mestre de Tal");
    await usuario.type(screen.getByLabelText(/e-mail/i), "mestre@example.org");
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    expect(await screen.findByText(/ao menos um artefato/i)).toBeInTheDocument();
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });

  it("a tela de adulto não pede nick ao Admin", () => {
    render(<FormularioDeAdulto papel="mestre" onSalvo={vi.fn()} onCancelar={vi.fn()} />);

    expect(screen.queryByLabelText(/^nick$/i)).not.toBeInTheDocument();
  });

  it("mostra o aviso de coleta dos artefatos comprobatórios do adulto", () => {
    render(<FormularioDeAdulto papel="apoiador" onSalvo={vi.fn()} onCancelar={vi.fn()} />);

    expect(screen.getByText(/artefatos comprobatórios do adulto/i)).toHaveAttribute(
      "role",
      "status",
    );
  });
});

describe("cadastro de Admin", () => {
  it("mostra o aviso de coleta do dado do Admin, sem bloquear o envio", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const cadastrarEspiado = vi.spyOn(personasApi, "incluirAdmin").mockResolvedValue({
      id: "admin-2",
      nome: "Admin de Tal",
      email: "admin@example.org",
      whatsapp: null,
    });

    render(<FormularioDeAdmin onSalvo={vi.fn()} onCancelar={vi.fn()} />);

    expect(screen.getByText(/nome, o e-mail e o whatsapp do admin/i)).toHaveAttribute(
      "role",
      "status",
    );

    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/^nome$/i), "Admin de Tal");
    await usuario.type(screen.getByLabelText(/e-mail/i), "admin@example.org");
    await usuario.click(screen.getByRole("button", { name: /incluir/i }));

    await waitFor(() => expect(cadastrarEspiado).toHaveBeenCalled());
  });
});

describe("a tabela de Mestres e de Apoiadores", () => {
  it("lista os cadastrados, com nome, e-mail e nick", () => {
    render(<ListaDeAdultos adultos={[MESTRE_COM_ARTEFATO]} onAbrirFicha={vi.fn()} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: MESTRE_COM_ARTEFATO.nome })).toBeInTheDocument();
    expect(screen.getByText(MESTRE_COM_ARTEFATO.email)).toBeInTheDocument();
    expect(screen.getByText(MESTRE_COM_ARTEFATO.nick as string)).toBeInTheDocument();
  });

  it("sinaliza na coluna própria quem está sem nick, sem sugerir nenhum", () => {
    render(<ListaDeAdultos adultos={[ADULTO_SEM_NICK]} onAbrirFicha={vi.fn()} />);

    expect(screen.getByText(/sem nick/i)).toBeInTheDocument();
    expect(screen.queryByText(/sugest/i)).not.toBeInTheDocument();
  });
});

describe("a ficha do adulto", () => {
  it("mostra os artefatos comprobatórios com rótulo e endereço alcançável", () => {
    render(<FichaDoAdulto adulto={MESTRE_COM_ARTEFATO} onNickGravado={vi.fn()} />);

    const [artefato] = MESTRE_COM_ARTEFATO.artefatos;
    expect(screen.getByText(new RegExp(artefato.rotulo))).toBeInTheDocument();
    expect(screen.getByRole("link", { name: artefato.endereco })).toHaveAttribute(
      "href",
      artefato.endereco,
    );
  });

  it("adulto sem artefato nenhum mostra a ficha sem lista, e não uma ficha quebrada", () => {
    render(
      <FichaDoAdulto
        adulto={{ ...MESTRE_COM_ARTEFATO, artefatos: [] }}
        onNickGravado={vi.fn()}
      />,
    );

    expect(screen.queryByRole("list")).not.toBeInTheDocument();
    expect(screen.getByText(/nenhum artefato registrado/i)).toBeInTheDocument();
  });

  it("não oferece campo algum para alterar nome, e-mail, WhatsApp ou artefato", () => {
    render(<FichaDoAdulto adulto={MESTRE_COM_ARTEFATO} onNickGravado={vi.fn()} />);

    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
  });

  it("marca o artefato de cadastro editado e mostra o original ao lado do vigente", () => {
    const mestreComArtefatoEditado: AdultoDaLista = {
      ...MESTRE_COM_ARTEFATO,
      artefatos: [
        {
          rotulo: "Certificado atualizado",
          endereco: "https://exemplo.org/certificado-novo",
          rotulo_original: "Certificado de curso",
          endereco_original: "https://exemplo.org/certificado",
        },
      ],
    };

    render(<FichaDoAdulto adulto={mestreComArtefatoEditado} onNickGravado={vi.fn()} />);

    expect(screen.getByText(/certificado atualizado/i)).toBeInTheDocument();
    expect(screen.getByText(/editado pelo próprio adulto/i)).toBeInTheDocument();
    expect(screen.getByText(/certificado de curso/i)).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "https://exemplo.org/certificado" }),
    ).toHaveAttribute("href", "https://exemplo.org/certificado");
  });

  it("artefato intocado aparece sem marca e sem valor original", () => {
    render(<FichaDoAdulto adulto={MESTRE_COM_ARTEFATO} onNickGravado={vi.fn()} />);

    expect(screen.queryByText(/editado pelo próprio adulto/i)).not.toBeInTheDocument();
  });

  it("não oferece editar, restaurar ou remover o artefato editado", () => {
    const mestreComArtefatoEditado: AdultoDaLista = {
      ...MESTRE_COM_ARTEFATO,
      artefatos: [
        {
          rotulo: "Certificado atualizado",
          endereco: "https://exemplo.org/certificado-novo",
          rotulo_original: "Certificado de curso",
          endereco_original: "https://exemplo.org/certificado",
        },
      ],
    };

    render(<FichaDoAdulto adulto={mestreComArtefatoEditado} onNickGravado={vi.fn()} />);

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("oferece gravar o nick que falta, sem sugerir nenhum", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    render(<FichaDoAdulto adulto={ADULTO_SEM_NICK} onNickGravado={vi.fn()} />);
    const usuario = userEvent.setup();

    expect(screen.getByText(/sem nick/i)).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: /gravar nick/i }));

    expect(screen.getByLabelText(/nick recebido por fora/i)).toHaveValue("");
    expect(screen.queryByText(/sugest/i)).not.toBeInTheDocument();
  });
});

describe("a gestão liga a linha da tabela à ficha", () => {
  it("abre a ficha ao acionar a linha e recarrega a lista quando o nick é gravado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "listarMestres")
      .mockResolvedValueOnce({ itens: [ADULTO_SEM_NICK], proximo_cursor: null })
      .mockResolvedValueOnce({
        itens: [{ ...ADULTO_SEM_NICK, nick: "NickGravado" }],
        proximo_cursor: null,
      });
    vi.spyOn(personasApi, "gravarNickDoAdulto").mockResolvedValue({ nick: "NickGravado" });

    render(<TelaDeAdultos papel="mestre" />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: ADULTO_SEM_NICK.nome }));
    expect(screen.getByRole("dialog")).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /gravar nick/i }));
    await usuario.type(screen.getByLabelText(/nick recebido por fora/i), "NickGravado");
    await usuario.click(screen.getByRole("button", { name: /^gravar$/i }));

    await waitFor(() => expect(personasApi.listarMestres).toHaveBeenCalledTimes(2));
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });
});

describe("cadastro de responsável", () => {
  it("mostra o aviso de coleta do nome, do vínculo e do usuário de acesso", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-1",
      nome: "Dona Maria",
    });
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [GUERREIRO],
      proximo_cursor: null,
    });

    render(<FormularioDeResponsavel onConcluido={vi.fn()} onCancelar={vi.fn()} />);

    expect(screen.getByText(/nome do responsável, o vínculo/i)).toHaveAttribute(
      "role",
      "status",
    );

    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Dona Maria");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));

    expect(await screen.findByText(/nome do responsável, o vínculo/i)).toBeInTheDocument();
  });

  // O defeito que esta fatia corrige atravessou o CI porque o teste dublava
  // `cadastrarResponsavel`: a tela mandava `POST /v1/responsaveis` **sem
  // corpo** e o núcleo respondia 422 a toda tentativa. Estes dois afirmam o
  // corpo que sai da tela, com o cliente real por cima de `fetch`
  // (`RF-02-06`).
  it("o cadastro leva o nome ao núcleo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [GUERREIRO],
      proximo_cursor: null,
    });
    configurarAcessoAoNucleo({
      chaveDeAplicacao: "chave-de-teste",
      urlDoNucleo: "https://nucleo.teste",
    });
    const requisicao = vi.fn().mockResolvedValue({
      ok: true,
      status: 201,
      json: () => Promise.resolve({ id: "resp-1", nome: "Dona Maria" }),
      headers: new Headers(),
    } as Response);
    vi.stubGlobal("fetch", requisicao);

    render(<FormularioDeResponsavel onConcluido={vi.fn()} onCancelar={vi.fn()} />);
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nome do responsável/i), "  Dona Maria  ");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));

    await screen.findByText(/vincule os guerreiros/i);
    const [url, opcoes] = requisicao.mock.calls[0];
    expect(String(url)).toContain("/v1/responsaveis");
    expect(opcoes?.method).toBe("POST");
    expect(JSON.parse(String(opcoes?.body))).toEqual({ nome: "Dona Maria" });
  });

  it("sem nome, o cadastro não chega ao núcleo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const cadastrar = vi.spyOn(personasApi, "cadastrarResponsavel");

    render(<FormularioDeResponsavel onConcluido={vi.fn()} onCancelar={vi.fn()} />);
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));

    expect(await screen.findByText(/informe o nome do responsável/i)).toBeInTheDocument();
    expect(cadastrar).not.toHaveBeenCalled();
  });
});

// A lista de vínculos já criados imprimia só o grau de parentesco: dois
// vínculos de "Pai" viravam duas linhas idênticas e o Admin não sabia a quem
// cada uma se referia (`RF-02-06`).
describe("o vínculo já criado identifica o Guerreiro(a) pelo nick", () => {
  function vinculoDe(id: string, guerreiroId: string, grau: string): VinculoCriado {
    return {
      id,
      responsavel_id: "resp-1",
      guerreiro_id: guerreiroId,
      grau_de_parentesco: grau,
      inicio: "2026-09-26T10:00:00-03:00",
    };
  }

  async function abrirOPassoDeVinculo(guerreiros: GuerreiroDaLista[]) {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-1",
      nome: "Dona Maria",
    });
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: guerreiros,
      proximo_cursor: null,
    });

    render(<FormularioDeResponsavel onConcluido={vi.fn()} onCancelar={vi.fn()} />);
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Dona Maria");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/vincule os guerreiros/i);
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
    vi.spyOn(personasApi, "criarVinculo").mockResolvedValue(
      vinculoDe("v-1", GUERREIRO.id, "Pai"),
    );

    await vincular(usuario, GUERREIRO.id, "Pai");

    await screen.findByRole("list", { name: /vínculos já criados/i });
    expect(linhasDosVinculos()).toEqual([`${GUERREIRO.nick} — Pai`]);
  });

  it("dois vínculos de mesmo parentesco continuam distinguíveis", async () => {
    const usuario = await abrirOPassoDeVinculo([GUERREIRO, GUERREIRO_SEM_VINCULO]);
    vi.spyOn(personasApi, "criarVinculo")
      .mockResolvedValueOnce(vinculoDe("v-1", GUERREIRO.id, "Pai"))
      .mockResolvedValueOnce(vinculoDe("v-2", GUERREIRO_SEM_VINCULO.id, "Pai"));

    await vincular(usuario, GUERREIRO.id, "Pai");
    await screen.findByRole("list", { name: /vínculos já criados/i });
    await vincular(usuario, GUERREIRO_SEM_VINCULO.id, "Pai");
    await waitFor(() => expect(linhasDosVinculos()).toHaveLength(2));

    const linhas = linhasDosVinculos();
    expect(linhas).toEqual([`${GUERREIRO.nick} — Pai`, `${GUERREIRO_SEM_VINCULO.nick} — Pai`]);
    expect(new Set(linhas).size).toBe(2);
  });

  it("Guerreiro(a) sem nick gravado não apaga a linha", async () => {
    const semNick: GuerreiroDaLista = { ...GUERREIRO, id: "guerreiro-9", nick: "" };
    const usuario = await abrirOPassoDeVinculo([semNick]);
    vi.spyOn(personasApi, "criarVinculo").mockResolvedValue(
      vinculoDe("v-1", semNick.id, "Mãe"),
    );

    await vincular(usuario, semNick.id, "Mãe");

    await screen.findByRole("list", { name: /vínculos já criados/i });
    const [linha] = linhasDosVinculos();
    expect(linha).toMatch(/sem nick/i);
    expect(linha).toMatch(/Mãe/);
  });
});

describe("o quarto responsável é barrado", () => {
  it("explica o teto de três e o vínculo não é criado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-1",
      nome: "Dona Maria",
    });
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [GUERREIRO],
      proximo_cursor: null,
    });
    vi.spyOn(personasApi, "criarVinculo").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Este Guerreiro(a) já tem três responsáveis vigentes.",
        campo: "guerreiro_id",
      }),
    );

    render(<FormularioDeResponsavel onConcluido={vi.fn()} onCancelar={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Dona Maria");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/vincule os guerreiros/i);

    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), GUERREIRO.id);
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "tio");
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));

    expect(await screen.findByText(/três responsáveis/i)).toBeInTheDocument();
  });
});
