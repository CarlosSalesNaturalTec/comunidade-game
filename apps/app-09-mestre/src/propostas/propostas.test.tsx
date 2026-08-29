import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { PropostaDoAutor } from "./api";
import * as propostasApi from "./api";
import { TelaDePropostas } from "./TelaDePropostas";

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
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

function proposta(sobrescreve: Partial<PropostaDoAutor> = {}): PropostaDoAutor {
  return {
    id: "proposta-1",
    alvo_tipo: "plataforma",
    alvo_id: null,
    texto: "Podíamos ter um mural entre trilhas.",
    situacao: "recebida",
    prazo: "2026-09-01T00:00:00-03:00",
    em_atraso: false,
    motivo_do_retorno: null,
    decidido_em: null,
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("O Mestre registra a proposta de evolução e acompanha o status (RF-09-55)", () => {
  it("registra a proposta em texto", async () => {
    configurarSessao();
    vi.spyOn(propostasApi, "listarMinhasPropostas")
      .mockResolvedValueOnce([])
      .mockResolvedValueOnce([proposta()]);
    const registrarEspiado = vi
      .spyOn(propostasApi, "registrarProposta")
      .mockResolvedValue({ id: "proposta-1", prazo: "2026-09-01T00:00:00-03:00" });

    render(<TelaDePropostas />);
    const usuario = userEvent.setup();

    await usuario.type(
      screen.getByLabelText(/^proposta$/i),
      "Podíamos ter um mural entre trilhas.",
    );
    await usuario.click(screen.getByRole("button", { name: /enviar proposta/i }));

    await waitFor(() =>
      expect(registrarEspiado).toHaveBeenCalledWith(
        "Podíamos ter um mural entre trilhas.",
        "token-do-mestre",
      ),
    );
    expect(
      await screen.findByText(/podíamos ter um mural entre trilhas/i),
    ).toBeInTheDocument();
    expect(screen.getByText(/^recebida$/i)).toBeInTheDocument();
  });

  it("não oferece nenhum campo ou botão de gravação de áudio", async () => {
    configurarSessao();
    vi.spyOn(propostasApi, "listarMinhasPropostas").mockResolvedValue([]);

    render(<TelaDePropostas />);

    await screen.findByText(/nenhuma proposta registrada ainda/i);
    expect(screen.queryByRole("button", { name: /gravar|áudio/i })).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/áudio/i)).not.toBeInTheDocument();
    expect(document.querySelector("audio")).not.toBeInTheDocument();
  });

  it("o desfecho não adotado mostra o motivo em linguagem simples, sem e-mail", async () => {
    configurarSessao();
    vi.spyOn(propostasApi, "listarMinhasPropostas").mockResolvedValue([
      proposta({
        situacao: "nao_adotada",
        motivo_do_retorno: "Já está no roteiro de outra fatia.",
        decidido_em: "2026-08-25T00:00:00-03:00",
      }),
    ]);

    render(<TelaDePropostas />);

    expect(await screen.findByText(/não adotada/i)).toBeInTheDocument();
    expect(
      screen.getByText(/motivo do retorno: já está no roteiro de outra fatia/i),
    ).toBeInTheDocument();
    expect(screen.queryByText(/e-mail/i)).not.toBeInTheDocument();
  });

  it("a lista não mostra proposta de outra persona", async () => {
    configurarSessao();
    // `/v1/sugestoes/minhas` já recorta pelo autor em sessão — o mock
    // simula exatamente essa leitura, só com a proposta do Mestre.
    vi.spyOn(propostasApi, "listarMinhasPropostas").mockResolvedValue([
      proposta({ id: "proposta-do-mestre", texto: "Proposta do Mestre." }),
    ]);

    render(<TelaDePropostas />);

    expect(await screen.findByText("Proposta do Mestre.")).toBeInTheDocument();
    expect(screen.getAllByRole("listitem")).toHaveLength(1);
  });

  it("nenhuma ação de adotar ou não adotar é apresentada", async () => {
    configurarSessao();
    vi.spyOn(propostasApi, "listarMinhasPropostas").mockResolvedValue([proposta()]);

    render(<TelaDePropostas />);

    await screen.findByText(/podíamos ter um mural entre trilhas/i);
    expect(
      screen.queryByRole("button", { name: /adotar|não adotar|avaliar/i }),
    ).not.toBeInTheDocument();
  });

  it("a proposta vazia não é enviada", async () => {
    configurarSessao();
    vi.spyOn(propostasApi, "listarMinhasPropostas").mockResolvedValue([]);
    const registrarEspiado = vi.spyOn(propostasApi, "registrarProposta");

    render(<TelaDePropostas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /enviar proposta/i }));

    expect(await screen.findByText(/escreva a proposta antes de enviar/i)).toBeInTheDocument();
    expect(registrarEspiado).not.toHaveBeenCalled();
  });

  it("a recusa do núcleo vira mensagem simples", async () => {
    configurarSessao();
    vi.spyOn(propostasApi, "listarMinhasPropostas").mockResolvedValue([]);
    vi.spyOn(propostasApi, "registrarProposta").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Alvo de atividade ou trilha exige o identificador.",
        campo: "alvo_id",
      }),
    );

    render(<TelaDePropostas />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/^proposta$/i), "Uma proposta qualquer.");
    await usuario.click(screen.getByRole("button", { name: /enviar proposta/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa).toHaveTextContent(/exige o identificador/i);
    expect(recusa.textContent).not.toMatch(/erro_de_validacao/i);
  });
});
