import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { limparToken } from "comum/autenticacao";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import * as preCadastroApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

function arquivoDeComprovante(nome = "comprovante.pdf", tipo = "application/pdf") {
  return new File(["conteudo do comprovante"], nome, { type: tipo });
}

async function preencherIdentificacao(testeDeUsuario: ReturnType<typeof userEvent.setup>) {
  await testeDeUsuario.type(screen.getByLabelText(/nome ou razão social/i), "Fulana de Tal");
  await testeDeUsuario.type(screen.getByLabelText(/^e-mail$/i), "fulana@example.org");
  await testeDeUsuario.type(screen.getByLabelText(/whatsapp/i), "+55 11 90000-0000");
  await testeDeUsuario.type(screen.getByLabelText(/^nick$/i), "ApoiadoraPretendida");
}

describe("porta pública de pré-cadastro", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(preCadastroApi, "listarNecessidadesEmAberto").mockResolvedValue([]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("quem não tem sessão vê a porta e o caminho de entrada", async () => {
    render(<App />);

    expect(
      await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /^entrar$/i })).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /propor desafio extra/i }),
    ).not.toBeInTheDocument();
  });

  it("a tela não oferece campo de documento", async () => {
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i });

    expect(screen.queryByLabelText(/cpf/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/cnpj/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/documento de identidade/i)).not.toBeInTheDocument();
  });

  it("a escada troca com o perfil declarado — a de pessoa física começa em 1 moeda", async () => {
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i });
    const testeDeUsuario = userEvent.setup();

    const selectDaEscada = screen.getByLabelText(/^valor sugerido$/i) as HTMLSelectElement;
    expect(selectDaEscada.options[0]?.textContent).toMatch(/1 moeda\b/);

    await testeDeUsuario.click(screen.getByLabelText(/pessoa jurídica/i));

    expect(selectDaEscada.options[0]?.textContent).toMatch(/50 moedas/);
  });

  it("o valor livre abaixo do menor degrau é aceito com o equivalente em moedas", async () => {
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i });
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByLabelText("Um valor livre"));
    await testeDeUsuario.type(screen.getByLabelText("Valor livre (R$)"), "5");

    expect(await screen.findByText(/equivalente a 0,5 moeda/i)).toBeInTheDocument();
  });

  it("o envio sem comprovante é recusado dizendo os formatos válidos", async () => {
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i });
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: /enviar pré-cadastro/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/pdf, jpg ou png/i);
  });

  it("a declaração de que nada ali cria acesso aparece antes do envio", async () => {
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i });

    expect(screen.getByText(/não cria cadastro nem acesso/i)).toBeInTheDocument();
    expect(screen.getByText(/não emite recibo/i)).toBeInTheDocument();
  });

  it("envio bem-sucedido confirma a fila da gestão sem abrir sessão", async () => {
    vi.spyOn(preCadastroApi, "registrarPreCadastroDeApoiador").mockResolvedValue({
      id: "solicitacao-1",
      prazo: "2026-09-08T00:00:00Z",
    });
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i });
    const testeDeUsuario = userEvent.setup();

    await preencherIdentificacao(testeDeUsuario);
    await testeDeUsuario.upload(
      screen.getByLabelText(/comprovante da transferência/i),
      arquivoDeComprovante(),
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /enviar pré-cadastro/i }));

    expect(
      await screen.findByText(/pedido registrado na fila da gestão/i),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /propor desafio extra/i }),
    ).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^sair$/i })).not.toBeInTheDocument();
  });

  it("429 do freio mostra o tempo de espera sem CAPTCHA e sem perder o preenchido", async () => {
    vi.spyOn(preCadastroApi, "registrarPreCadastroDeApoiador").mockRejectedValue(
      new ErroDaApi(
        429,
        { codigo: "freio_por_origem_acionado", mensagem: "Muitas tentativas em pouco tempo." },
        90,
      ),
    );
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i });
    const testeDeUsuario = userEvent.setup();

    await preencherIdentificacao(testeDeUsuario);
    await testeDeUsuario.upload(
      screen.getByLabelText(/comprovante da transferência/i),
      arquivoDeComprovante(),
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /enviar pré-cadastro/i }));

    expect(await screen.findByText(/2 minutos/i)).toBeInTheDocument();
    expect(screen.queryByText(/captcha/i)).not.toBeInTheDocument();
    expect(screen.getByLabelText(/nome ou razão social/i)).toHaveValue("Fulana de Tal");
    expect(screen.getByLabelText(/^nick$/i)).toHaveValue("ApoiadoraPretendida");
  });

  it("422 de formato mostra os formatos válidos", async () => {
    vi.spyOn(preCadastroApi, "registrarPreCadastroDeApoiador").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Comprovante aceito apenas em PDF, JPG ou PNG.",
        campo: "comprovante",
      }),
    );
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i });
    const testeDeUsuario = userEvent.setup();

    await preencherIdentificacao(testeDeUsuario);
    await testeDeUsuario.upload(
      screen.getByLabelText(/comprovante da transferência/i),
      arquivoDeComprovante("comprovante.docx", "application/msword"),
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /enviar pré-cadastro/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/pdf, jpg ou png/i);
  });

  it("sem endereço configurado, o encaminhamento à vitrine explica o caminho em texto", async () => {
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i });
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByLabelText(/sem transferir dinheiro/i));

    expect(
      await screen.findByText(/formulário de solicitação da vitrine/i),
    ).toBeInTheDocument();
    expect(screen.queryByRole("link")).not.toBeInTheDocument();
  });
});
