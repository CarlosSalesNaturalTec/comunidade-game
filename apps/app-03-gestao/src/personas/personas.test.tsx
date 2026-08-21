import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as agendaApi from "../agenda/api";
import { ErroDaApi } from "../api/cliente";
import type { SessaoAberta } from "../autenticacao/ContextoDeSessao";
import type { GuerreiroDaLista } from "./api";
import * as personasApi from "./api";
import { FormularioDeAdulto } from "./FormularioDeAdulto";
import { FormularioDeGuerreiro } from "./FormularioDeGuerreiro";
import { FormularioDeResponsavel } from "./FormularioDeResponsavel";
import { ListaDeAdultos } from "./ListaDeAdultos";
import { ListaDeGuerreiros } from "./ListaDeGuerreiros";

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
};

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
};

vi.mock("../autenticacao/ContextoDeSessao", async () => {
  const real = await vi.importActual<typeof import("../autenticacao/ContextoDeSessao")>(
    "../autenticacao/ContextoDeSessao",
  );
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

import { useSessao } from "../autenticacao/ContextoDeSessao";

function configurarSessao(sessao: SessaoAberta | null) {
  vi.mocked(useSessao).mockReturnValue({
    sessao,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
  });
}

const GUERREIRO: GuerreiroDaLista = {
  id: "guerreiro-1",
  nome: "Zeferina",
  nascimento: "2015-03-20",
  nick: "ZeferinaGuerreira",
  avatar: "avatar-opaco",
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
    render(<ListaDeGuerreiros guerreiros={[GUERREIRO]} onEditar={vi.fn()} />);

    expect(screen.getByText("ZeferinaGuerreira")).toBeInTheDocument();
    expect(screen.queryByRole("img")).not.toBeInTheDocument();
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
});

describe("gravar o nick do adulto na colisão", () => {
  it("sinaliza na lista quem está sem nick", () => {
    render(
      <ListaDeAdultos
        adultos={[
          {
            id: "a1",
            nome: "Apoiador de Tal",
            email: "a@example.org",
            whatsapp: null,
            nick: null,
            artefatos: [],
          },
        ]}
        onNickGravado={vi.fn()}
      />,
    );

    expect(screen.getByText(/sem nick/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /gravar nick/i })).toBeInTheDocument();
  });

  it("a aplicação não sugere nick ao Admin", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    render(
      <ListaDeAdultos
        adultos={[
          {
            id: "a1",
            nome: "Apoiador de Tal",
            email: "a@example.org",
            whatsapp: null,
            nick: null,
            artefatos: [],
          },
        ]}
        onNickGravado={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /gravar nick/i }));

    expect(screen.getByLabelText(/nick recebido por fora/i)).toHaveValue("");
    expect(screen.queryByText(/sugest/i)).not.toBeInTheDocument();
  });
});

describe("o quarto responsável é barrado", () => {
  it("explica o teto de três e o vínculo não é criado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "cadastrarResponsavel").mockResolvedValue({ id: "resp-1" });
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

    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/vincule os guerreiros/i);

    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), GUERREIRO.id);
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "tio");
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));

    expect(await screen.findByText(/três responsáveis/i)).toBeInTheDocument();
  });
});
