import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { configurarAcessoAoNucleo, ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { CAMADAS_DO_AVATAR, tracoDoCatalogo } from "comum/avatar";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as agendaApi from "../agenda/api";
import type {
  AdultoDaLista,
  AportesDoProvedor,
  GuerreiroDaLista,
  ResponsavelDaLista,
  VinculoCriado,
} from "./api";
import * as personasApi from "./api";
import { FichaDoAdulto } from "./FichaDoAdulto";
import { FormularioDeAdmin } from "./FormularioDeAdmin";
import { FormularioDeAdulto } from "./FormularioDeAdulto";
import { FormularioDeGuerreiro } from "./FormularioDeGuerreiro";
import { FormularioDeResponsavel } from "./FormularioDeResponsavel";
import { ListaDeAdultos } from "./ListaDeAdultos";
import { ListaDeGuerreiros } from "./ListaDeGuerreiros";
import { TelaDeAdultos } from "./TelaDeAdultos";
import { TelaDeResponsaveis } from "./TelaDeResponsaveis";

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
  ativo: true,
  artefatos: [
    {
      id: "artefato-do-cadastro",
      rotulo: "Certificado de curso",
      endereco: "https://exemplo.org/certificado",
      publicado: true,
    },
  ],
};

const ADULTO_SEM_NICK: AdultoDaLista = {
  id: "a1",
  nome: "Apoiador de Tal",
  email: "a@example.org",
  whatsapp: null,
  nick: null,
  ativo: true,
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
    await usuario.selectOptions(screen.getByLabelText(/^comunidade$/i), COMUNIDADE.id);
    await usuario.selectOptions(
      await screen.findByLabelText(/aula em que se cadastra/i),
      AULA.id,
    );
  }

  it("Admin cadastra o Guerreiro(a) sem escolher avatar, e o avatar sai do catálogo", async () => {
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
    const [dados] = vi.mocked(personasApi.cadastrarGuerreiro).mock.calls[0];
    const enviado = JSON.parse(dados.avatar) as Record<string, string>;
    for (const camada of CAMADAS_DO_AVATAR) {
      expect(tracoDoCatalogo(camada.nome, enviado[camada.nome])).not.toBeNull();
    }
  });

  it("o formulário não tem campo de avatar, no cadastro nem na edição", () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(agendaApi, "listarAgenda").mockResolvedValue({ itens: [], proximo_cursor: null });

    const { unmount } = render(
      <FormularioDeGuerreiro
        comunidades={[COMUNIDADE]}
        onSalvo={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );
    expect(screen.queryByLabelText(/avatar/i)).not.toBeInTheDocument();
    unmount();

    render(
      <FormularioDeGuerreiro
        comunidades={[COMUNIDADE]}
        guerreiroExistente={GUERREIRO}
        onSalvo={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );
    expect(screen.queryByLabelText(/avatar/i)).not.toBeInTheDocument();
  });

  it("a edição reenvia o avatar gravado, sem sortear outro", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "editarGuerreiro").mockResolvedValue(GUERREIRO);

    render(
      <FormularioDeGuerreiro
        comunidades={[COMUNIDADE]}
        guerreiroExistente={GUERREIRO}
        onSalvo={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();
    await usuario.clear(screen.getByLabelText(/^nome$/i));
    await usuario.type(screen.getByLabelText(/^nome$/i), "Zeferina Nova");
    await usuario.click(screen.getByRole("button", { name: /^salvar$/i }));

    await waitFor(() => expect(personasApi.editarGuerreiro).toHaveBeenCalled());
    const [, dados] = vi.mocked(personasApi.editarGuerreiro).mock.calls[0];
    expect(dados.avatar).toBe(GUERREIRO.avatar);
    expect(dados.nome).toBe("Zeferina Nova");
  });

  it("Guerreiro(a) sem avatar gravado recebe um sorteado na edição", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "editarGuerreiro").mockResolvedValue(GUERREIRO);

    render(
      <FormularioDeGuerreiro
        comunidades={[COMUNIDADE]}
        guerreiroExistente={{ ...GUERREIRO, avatar: "" }}
        onSalvo={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );
    await userEvent.setup().click(screen.getByRole("button", { name: /^salvar$/i }));

    await waitFor(() => expect(personasApi.editarGuerreiro).toHaveBeenCalled());
    const [, dados] = vi.mocked(personasApi.editarGuerreiro).mock.calls[0];
    expect(dados.avatar).not.toBe("");
    expect(JSON.parse(dados.avatar).v).toBe(1);
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
      screen.getByText(/o nome, a data de nascimento e o nick do guerreiro/i),
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

  it("a gestão não vê a imagem do Guerreiro(a) — nem coluna de avatar ou início do vínculo", () => {
    render(
      <ListaDeGuerreiros
        guerreiros={[GUERREIRO]}
        comunidades={[COMUNIDADE]}
        onEditar={vi.fn()}
        onAbrirFicha={vi.fn()}
      />,
    );

    expect(screen.getByText("ZeferinaGuerreira")).toBeInTheDocument();
    expect(screen.queryByRole("img")).not.toBeInTheDocument();
    expect(screen.queryByRole("columnheader", { name: /avatar/i })).not.toBeInTheDocument();
    expect(
      screen.queryByRole("columnheader", { name: /início do vínculo/i }),
    ).not.toBeInTheDocument();
    expect(screen.queryByText(/desde/i)).not.toBeInTheDocument();
  });
});

describe("o vínculo de comunidade na lista de Guerreiros e Guerreiras", () => {
  it("apresenta nick, nome e a comunidade herdada da aula", () => {
    render(
      <ListaDeGuerreiros
        guerreiros={[GUERREIRO]}
        comunidades={[COMUNIDADE]}
        onEditar={vi.fn()}
        onAbrirFicha={vi.fn()}
      />,
    );

    const linha = screen.getByRole("row", { name: /ZeferinaGuerreira/ });
    expect(within(linha).getByRole("rowheader")).toHaveTextContent("ZeferinaGuerreira");
    expect(within(linha).getByRole("cell", { name: "Zeferina" })).toBeInTheDocument();
    expect(within(linha).getByRole("cell", { name: /comunidade/i })).toBeInTheDocument();
  });

  it("Guerreiro(a) sem vínculo vigente é informado, não acusado", () => {
    render(
      <ListaDeGuerreiros
        guerreiros={[GUERREIRO_SEM_VINCULO]}
        comunidades={[COMUNIDADE]}
        onEditar={vi.fn()}
        onAbrirFicha={vi.fn()}
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

const SEM_APORTES: AportesDoProvedor = {
  provedor_id: "mestre-1",
  poder_sustentador_em_moedas: "0.00",
  aportes: [],
  declaracoes_pendentes: [],
};

function renderizarFicha(
  adulto: AdultoDaLista,
  opcoes: { podeManter?: boolean; onAlterado?: () => void; onExcluido?: () => void } = {},
) {
  return render(
    <FichaDoAdulto
      papel="mestre"
      adulto={adulto}
      podeManter={opcoes.podeManter ?? false}
      onNickGravado={vi.fn()}
      onAlterado={opcoes.onAlterado ?? vi.fn()}
      onExcluido={opcoes.onExcluido ?? vi.fn()}
    />,
  );
}

const ARTEFATO_EDITADO_PELO_MESTRE: AdultoDaLista = {
  ...MESTRE_COM_ARTEFATO,
  artefatos: [
    {
      id: "artefato-do-cadastro",
      rotulo: "Certificado atualizado",
      endereco: "https://exemplo.org/certificado-novo",
      publicado: true,
      rotulo_original: "Certificado de curso",
      endereco_original: "https://exemplo.org/certificado",
    },
  ],
};

describe("a ficha do adulto", () => {
  beforeEach(() => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "lerAportesDoProvedor").mockResolvedValue(SEM_APORTES);
  });

  it("mostra os artefatos comprobatórios com rótulo e endereço alcançável", () => {
    renderizarFicha(MESTRE_COM_ARTEFATO);

    const [artefato] = MESTRE_COM_ARTEFATO.artefatos;
    expect(screen.getByText(new RegExp(artefato.rotulo))).toBeInTheDocument();
    expect(screen.getByRole("link", { name: artefato.endereco })).toHaveAttribute(
      "href",
      artefato.endereco,
    );
  });

  it("adulto sem artefato nenhum mostra a ficha sem lista, e não uma ficha quebrada", () => {
    renderizarFicha({ ...MESTRE_COM_ARTEFATO, artefatos: [] });

    expect(screen.queryByRole("list")).not.toBeInTheDocument();
    expect(screen.getByText(/nenhum artefato registrado/i)).toBeInTheDocument();
  });

  it("quem não é Admin vê a ficha de leitura, sem campo nem ação de manutenção", () => {
    configurarSessao(SESSAO_DE_ADMIN);
    renderizarFicha(MESTRE_COM_ARTEFATO, { podeManter: false });

    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /editar dados|excluir/i })).toBeNull();
  });

  it("marca o artefato de cadastro editado e mostra o original ao lado do vigente", () => {
    configurarSessao(SESSAO_DE_ADMIN);
    renderizarFicha(ARTEFATO_EDITADO_PELO_MESTRE, { podeManter: true });

    expect(screen.getByText(/certificado atualizado/i)).toBeInTheDocument();
    expect(screen.getByText(/editado pelo próprio adulto/i)).toBeInTheDocument();
    expect(screen.getByText(/certificado de curso/i)).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "https://exemplo.org/certificado" }),
    ).toHaveAttribute("href", "https://exemplo.org/certificado");
  });

  it("artefato intocado aparece sem marca e sem valor original", () => {
    configurarSessao(SESSAO_DE_ADMIN);
    renderizarFicha(MESTRE_COM_ARTEFATO, { podeManter: true });

    expect(screen.queryByText(/editado pelo próprio adulto/i)).not.toBeInTheDocument();
  });

  it("o Admin corrige o WhatsApp e a ficha recebe o valor novo (RF-02-117)", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const salvo = { ...MESTRE_COM_ARTEFATO, whatsapp: "71988887777" };
    const alterar = vi.spyOn(personasApi, "alterarAdulto").mockResolvedValue(salvo);
    const onAlterado = vi.fn();
    renderizarFicha(MESTRE_COM_ARTEFATO, { podeManter: true, onAlterado });
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /editar dados/i }));
    const campo = screen.getByLabelText(/whatsapp/i);
    await usuario.clear(campo);
    await usuario.type(campo, "71988887777");
    await usuario.click(screen.getByRole("button", { name: /^salvar$/i }));

    expect(alterar).toHaveBeenCalledWith(
      "mestre",
      MESTRE_COM_ARTEFATO.id,
      expect.objectContaining({ whatsapp: "71988887777" }),
      expect.any(String),
    );
    await waitFor(() => expect(onAlterado).toHaveBeenCalledWith(salvo));
  });

  it("a edição não oferece campo de nick, de papel nem de termos", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    renderizarFicha(MESTRE_COM_ARTEFATO, { podeManter: true });
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /editar dados/i }));

    expect(screen.queryByLabelText(/nick/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/papel/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/termo/i)).not.toBeInTheDocument();
  });

  it("a recusa do último artefato aparece na ficha e o artefato segue listado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "removerArtefatoDoAdulto").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "O cadastro precisa manter ao menos um artefato comprobatório.",
        campo: "artefato_id",
      }),
    );
    renderizarFicha(MESTRE_COM_ARTEFATO, { podeManter: true });
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /^remover$/i }));

    expect(await screen.findByText(/ao menos um artefato/i)).toBeInTheDocument();
    const [artefato] = MESTRE_COM_ARTEFATO.artefatos;
    expect(screen.getByRole("link", { name: artefato.endereco })).toBeInTheDocument();
  });

  it("exclusão recusada por uso aponta a desativação (RN-02-34)", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "excluirAdulto").mockRejectedValue(
      new ErroDaApi(422, { codigo: "adulto_em_uso", mensagem: "Em uso.", campo: "id" }),
    );
    const onExcluido = vi.fn();
    renderizarFicha(MESTRE_COM_ARTEFATO, { podeManter: true, onExcluido });
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /^excluir$/i }));
    await usuario.click(screen.getByRole("button", { name: /confirmar exclusão/i }));

    expect(await screen.findByText(/pode desativá-lo/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /^desativar$/i })).toBeInTheDocument();
    expect(onExcluido).not.toHaveBeenCalled();
  });

  it("exclusão confirmada fecha a ficha (RF-02-118)", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "excluirAdulto").mockResolvedValue(undefined);
    const onExcluido = vi.fn();
    renderizarFicha(MESTRE_COM_ARTEFATO, { podeManter: true, onExcluido });
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /^excluir$/i }));
    await usuario.click(screen.getByRole("button", { name: /confirmar exclusão/i }));

    await waitFor(() => expect(onExcluido).toHaveBeenCalled());
  });

  it("desativa com confirmação e, desativado, oferece reativar (RF-02-119)", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const desativado = { ...MESTRE_COM_ARTEFATO, ativo: false };
    vi.spyOn(personasApi, "desativarAdulto").mockResolvedValue(desativado);
    const onAlterado = vi.fn();
    const { rerender } = renderizarFicha(MESTRE_COM_ARTEFATO, {
      podeManter: true,
      onAlterado,
    });
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /^desativar$/i }));
    await usuario.click(screen.getByRole("button", { name: /confirmar desativação/i }));
    await waitFor(() => expect(onAlterado).toHaveBeenCalledWith(desativado));

    rerender(
      <FichaDoAdulto
        papel="mestre"
        adulto={desativado}
        podeManter
        onNickGravado={vi.fn()}
        onAlterado={onAlterado}
        onExcluido={vi.fn()}
      />,
    );
    expect(screen.getByText(/cadastro desativado/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /^reativar$/i })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^desativar$/i })).not.toBeInTheDocument();
  });

  it("oferece gravar o nick que falta, sem sugerir nenhum", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    renderizarFicha(ADULTO_SEM_NICK);
    const usuario = userEvent.setup();

    expect(screen.getByText(/sem nick/i)).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: /gravar nick/i }));

    expect(screen.getByLabelText(/nick recebido por fora/i)).toHaveValue("");
    expect(screen.queryByText(/sugest/i)).not.toBeInTheDocument();
  });
});

describe("a tabela marca o adulto desativado", () => {
  it("a linha do desativado declara a desativação (RF-02-119)", () => {
    render(
      <ListaDeAdultos
        adultos={[{ ...MESTRE_COM_ARTEFATO, ativo: false }]}
        onAbrirFicha={vi.fn()}
      />,
    );

    expect(screen.getByText(/desativado/i)).toBeInTheDocument();
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

// A sub-área Responsáveis tinha só o botão de cadastrar: responsável
// cadastrado ficava inalcançável, e o cadastro interrompido antes do vínculo
// não aparecia em lugar nenhum (`RF-02-111`).
describe("lista de responsáveis na gestão", () => {
  const COM_VINCULO: ResponsavelDaLista = {
    id: "resp-1",
    nome: "Dona Maria",
    vinculados: [
      {
        guerreiro_id: GUERREIRO.id,
        nick: GUERREIRO.nick,
        grau_de_parentesco: "mãe",
      },
    ],
  };

  const SEM_VINCULO: ResponsavelDaLista = {
    id: "resp-2",
    nome: "Seu João",
    vinculados: [],
  };

  function configurarLista(itens: ResponsavelDaLista[]) {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [GUERREIRO],
      proximo_cursor: null,
    });
    return vi.spyOn(personasApi, "listarResponsaveis").mockResolvedValue({
      itens,
      proximo_cursor: null,
    });
  }

  it("apresenta os responsáveis cadastrados, com os vinculados", async () => {
    configurarLista([COM_VINCULO]);

    render(<TelaDeResponsaveis />);

    expect(await screen.findByText("Dona Maria")).toBeInTheDocument();
    const tabela = screen.getByRole("table", { name: /responsáveis cadastrados/i });
    expect(within(tabela).getByText(/ZeferinaGuerreira \(mãe\)/)).toBeInTheDocument();
  });

  it("sinaliza o cadastro interrompido, sem Guerreiro(a) vinculado", async () => {
    configurarLista([SEM_VINCULO]);

    render(<TelaDeResponsaveis />);

    expect(await screen.findByText("Seu João")).toBeInTheDocument();
    expect(screen.getByText(/cadastro por concluir/i)).toBeInTheDocument();
  });

  it("lista vazia é dita, e o cadastro continua oferecido", async () => {
    configurarLista([]);

    render(<TelaDeResponsaveis />);

    expect(await screen.findByText(/nenhum responsável cadastrado/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /cadastrar responsável/i })).toBeInTheDocument();
  });

  it("exibe o aviso de coleta da tela", async () => {
    configurarLista([COM_VINCULO]);

    render(<TelaDeResponsaveis />);

    expect(await screen.findByText(/nome do responsável e o vínculo/i)).toHaveAttribute(
      "role",
      "status",
    );
  });

  it("não expõe credencial nem dado civil da criança", async () => {
    // Nick escolhido para não conter o nome civil: o do fixture padrão é
    // "ZeferinaGuerreira", que traz "Zeferina" dentro, e a asserção passaria
    // por acidente.
    configurarLista([
      {
        id: "resp-3",
        nome: "Dona Maria",
        vinculados: [
          {
            guerreiro_id: GUERREIRO.id,
            nick: "NickSemNomeCivil",
            grau_de_parentesco: "mãe",
          },
        ],
      },
    ]);

    render(<TelaDeResponsaveis />);
    await screen.findByText("Dona Maria");

    const tabela = screen.getByRole("table", { name: /responsáveis cadastrados/i });
    expect(tabela.textContent).not.toMatch(/senha|usuário|credencial/i);
    expect(tabela.textContent).not.toContain(GUERREIRO.nome);
    expect(tabela.textContent).not.toContain(GUERREIRO.nascimento);
  });

  it("retoma um responsável e vincula outro Guerreiro(a), sem cadastrar ninguém", async () => {
    configurarLista([SEM_VINCULO]);
    const cadastrar = vi.spyOn(personasApi, "cadastrarResponsavel");
    const criarVinculo = vi.spyOn(personasApi, "criarVinculo").mockResolvedValue({
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
    configurarLista([SEM_VINCULO]);
    vi.spyOn(personasApi, "criarVinculo").mockRejectedValue(
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

    expect(await screen.findByText(/três responsáveis/i)).toBeInTheDocument();
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

describe("os aportes na ficha do adulto", () => {
  const APORTES: AportesDoProvedor = {
    provedor_id: "apoiador-1",
    poder_sustentador_em_moedas: "20.00",
    aportes: [
      {
        id: "aporte-1",
        data_do_aporte: "2026-11-10",
        tipo_de_recurso_nome: "Doação em dinheiro",
        tipo_de_recurso_unidade: "R$",
        quantidade: "150.00",
        valor_em_moedas: "15.00",
        valor_de_origem: "150.00",
        ponto_de_apoio_nome: "Quilombo",
        forma: "financeira",
        destinacao: "lastro",
        tem_comprovante: true,
      },
      {
        id: "aporte-2",
        data_do_aporte: "2026-03-01",
        tipo_de_recurso_nome: "Lanche",
        tipo_de_recurso_unidade: "unidade",
        quantidade: "10.00",
        valor_em_moedas: "5.00",
        valor_de_origem: null,
        ponto_de_apoio_nome: "Quilombo",
        forma: "material",
        destinacao: "lastro",
        tem_comprovante: false,
      },
    ],
    declaracoes_pendentes: [
      {
        id: "declaracao-1",
        registrado_em: "2026-11-15T09:00:00-03:00",
        valor_declarado: "30.00",
        origem_da_escolha: "valor_livre",
      },
    ],
  };

  beforeEach(() => {
    configurarSessao(SESSAO_DE_ADMIN);
  });

  it("mostra o Poder Sustentador e o aporte com moedas e comprovante", async () => {
    const leitura = vi.spyOn(personasApi, "lerAportesDoProvedor").mockResolvedValue(APORTES);
    renderizarFicha(MESTRE_COM_ARTEFATO);

    const tabela = await screen.findByRole("table", { name: /aportes homologados/i });
    expect(leitura).toHaveBeenCalledWith(MESTRE_COM_ARTEFATO.id, SESSAO_DE_ADMIN.token);
    expect(screen.getByText("20 moedas")).toBeInTheDocument();
    const linhas = within(tabela).getAllByRole("row");
    expect(within(linhas[1]).getByText("10/11/2026")).toBeInTheDocument();
    expect(within(linhas[1]).getByText("150 R$")).toBeInTheDocument();
    expect(within(linhas[1]).getByText("Com comprovante")).toBeInTheDocument();
    expect(within(linhas[2]).getByText("Sem comprovante")).toBeInTheDocument();
  });

  it("mostra os reais sempre ao lado das moedas, e só quando houver", async () => {
    vi.spyOn(personasApi, "lerAportesDoProvedor").mockResolvedValue(APORTES);
    renderizarFicha(MESTRE_COM_ARTEFATO);

    const tabela = await screen.findByRole("table", { name: /aportes homologados/i });
    const [, comReais, semReais] = within(tabela).getAllByRole("row");
    expect(within(comReais).getByText(/^15 moedas \(R\$\s150,00\)$/)).toBeInTheDocument();
    expect(within(semReais).getByText("5 moedas")).toBeInTheDocument();
  });

  it("mostra a declaração pendente à parte, sem ação de homologar ou recusar", async () => {
    vi.spyOn(personasApi, "lerAportesDoProvedor").mockResolvedValue(APORTES);
    renderizarFicha(MESTRE_COM_ARTEFATO);

    const lista = await screen.findByRole("list", { name: /declarações pendentes/i });
    expect(within(lista).getByText(/R\$\s30,00 declarados/)).toBeInTheDocument();
    expect(within(lista).getByText(/valor livre/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /homolog|recus/i })).not.toBeInTheDocument();
  });

  it("ficha sem aporte mostra o Poder Sustentador em zero e o aviso", async () => {
    vi.spyOn(personasApi, "lerAportesDoProvedor").mockResolvedValue(SEM_APORTES);
    renderizarFicha(MESTRE_COM_ARTEFATO);

    expect(await screen.findByText(/ainda não há aporte/i)).toBeInTheDocument();
    expect(screen.getByText("0 moedas")).toBeInTheDocument();
    expect(
      screen.queryByRole("list", { name: /declarações pendentes/i }),
    ).not.toBeInTheDocument();
  });

  it("a seção não oferece baixar, editar, estornar, homologar nem recusar", async () => {
    vi.spyOn(personasApi, "lerAportesDoProvedor").mockResolvedValue(APORTES);
    renderizarFicha({ ...MESTRE_COM_ARTEFATO, nick: "Mestre" });

    const secao = await screen.findByRole("region", { name: "Aportes" });
    await within(secao).findByRole("table");
    expect(within(secao).queryByRole("button")).not.toBeInTheDocument();
    expect(within(secao).queryByRole("link")).not.toBeInTheDocument();
    expect(within(secao).queryByRole("textbox")).not.toBeInTheDocument();
  });

  it("avisa quando a leitura falha", async () => {
    vi.spyOn(personasApi, "lerAportesDoProvedor").mockRejectedValue(new Error("rede"));
    renderizarFicha(MESTRE_COM_ARTEFATO);

    expect(
      await screen.findByText(/não foi possível carregar os aportes/i),
    ).toBeInTheDocument();
  });
});
