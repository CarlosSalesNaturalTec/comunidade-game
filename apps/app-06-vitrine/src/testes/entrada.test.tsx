import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";

// Os seis endereços de destino entram por variável de ambiente, uma por
// ambiente (design — decisão 4). Este arquivo declara os seis para exercitar o
// encaminhamento; o caso sem endereço publicado está em arquivo próprio, para
// isolar os dois.
vi.mock("../api/configuracao", async () => {
  const real =
    await vi.importActual<typeof import("../api/configuracao")>("../api/configuracao");
  return {
    ...real,
    URL_DA_APP_01_AULA: "https://aula.example.org",
    URL_DA_APP_03_GESTAO: "https://gestao.example.org",
    URL_DA_APP_05_GUERREIRO: "https://minhaarea.example.org",
    URL_DA_APP_07_RESPONSAVEL: "https://responsavel.example.org",
    URL_DA_APP_08_APOIADOR: "https://apoiador.example.org",
    URL_DA_APP_09_MESTRE: "https://mestre.example.org",
  };
});

const DESTINOS: [string, string, string][] = [
  ["Sou Guerreiro ou Guerreira", "Minha Área", "https://minhaarea.example.org"],
  [
    "Sou responsável por um Guerreiro ou Guerreira",
    "Área dos responsáveis",
    "https://responsavel.example.org",
  ],
  ["Sou Mestre", "Área do Mestre", "https://mestre.example.org"],
  ["Sou Apoiador", "Área do Apoiador", "https://apoiador.example.org"],
  ["Sou da gestão", "Gestão", "https://gestao.example.org"],
  ["Este é o aparelho da aula", "Aula presencial", "https://aula.example.org"],
];

describe("o botão Entrar pergunta e encaminha", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
  });

  it("o botão está em toda tela, em todos os recortes (RF-03-58)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    expect(screen.getByRole("button", { name: "Entrar" })).toBeVisible();
    await testeDeUsuario.click(screen.getByRole("button", { name: "Pesquisadores" }));
    expect(screen.getByRole("button", { name: "Entrar" })).toBeVisible();
    await testeDeUsuario.click(screen.getByRole("button", { name: "Gestores públicos" }));
    expect(screen.getByRole("button", { name: "Entrar" })).toBeVisible();
  });

  it("pergunta quem está entrando, sem escolha pré-marcada (RF-03-58, RF-03-60)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));

    expect(await screen.findByText(/quem está entrando/i)).toBeVisible();
    for (const [rotulo] of DESTINOS) {
      expect(screen.getByRole("button", { name: rotulo })).toBeVisible();
    }
    expect(screen.queryByRole("link")).toBeNull();
  });

  it.each(DESTINOS)(
    "%s é encaminhada à aplicação dela (RF-03-59)",
    async (rotulo, nomeDoDestino, url) => {
      render(<App />);
      const testeDeUsuario = userEvent.setup();

      await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));
      await testeDeUsuario.click(screen.getByRole("button", { name: rotulo }));

      const link = await screen.findByRole("link", {
        name: new RegExp(`Ir para a ${nomeDoDestino}`, "i"),
      });
      expect(link).toHaveAttribute("href", url);
    },
  );

  it("nenhuma tela de entrada pede credencial ou revela cadastro (RF-03-61, RN-03-27)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));
    await testeDeUsuario.click(
      screen.getByRole("button", { name: "Sou Guerreiro ou Guerreira" }),
    );

    expect(screen.queryByRole("textbox")).toBeNull();
    expect(screen.queryByLabelText(/nick|senha|usuário|e-mail/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("listbox")).toBeNull();
    expect(
      screen.getByText(/a vitrine não pede nem confere senha, nick ou imagem/i),
    ).toBeVisible();
  });

  it("a escolha não sobrevive ao fechamento do diálogo (RF-03-60)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Sou Mestre" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: /fechar/i }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));

    expect(await screen.findByText(/quem está entrando/i)).toBeVisible();
    expect(screen.getByRole("button", { name: "Sou Mestre" })).toBeVisible();
    expect(screen.queryByRole("link")).toBeNull();
  });
});

describe("a orientação de quem ainda não tem cadastro", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
  });

  it("leva o futuro Apoiador ao pré-cadastro da App 08 (RF-03-62)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Sou Apoiador" }));

    expect(screen.getByRole("heading", { name: /ainda não tenho cadastro/i })).toBeVisible();
    expect(screen.getByText(/entrar não cria cadastro/i)).toBeVisible();
    expect(
      screen.getByRole("link", { name: /pré-cadastro da Área do Apoiador/i }),
    ).toHaveAttribute("href", "https://apoiador.example.org");
  });

  it.each(["Sou Guerreiro ou Guerreira", "Sou responsável por um Guerreiro ou Guerreira"])(
    "orienta %s a procurar a gestão no encontro (RF-03-62)",
    async (rotulo) => {
      render(<App />);
      const testeDeUsuario = userEvent.setup();

      await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));
      await testeDeUsuario.click(screen.getByRole("button", { name: rotulo }));

      expect(screen.getByText(/procura a gestão no encontro/i)).toBeVisible();
    },
  );

  it("nomeia o formulário do Mestre em texto, sem link (RF-03-62)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Sou Mestre" }));

    expect(
      screen.getByText(/formulário de solicitação de participação da vitrine/i),
    ).toBeVisible();
    const links = screen.getAllByRole("link").map((no) => no.getAttribute("href"));
    expect(links).toEqual(["https://mestre.example.org"]);
  });

  it("gestão e aparelho da aula não recebem orientação, que o PRD não lhes dá", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Sou da gestão" }));

    expect(screen.queryByRole("heading", { name: /ainda não tenho cadastro/i })).toBeNull();
  });
});
