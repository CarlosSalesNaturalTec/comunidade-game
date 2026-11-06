import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { urlDaDocumentacaoDaApi } from "../desenvolvedor/enderecos";
import App from "./TelaDaVitrine";

// O endereço do núcleo entra por variável de ambiente; aqui é declarado para
// exercitar o link da documentação da API (`RF-03-67`).
vi.mock("../api/configuracao", async () => {
  const real =
    await vi.importActual<typeof import("../api/configuracao")>("../api/configuracao");
  return { ...real, URL_DO_NUCLEO: "https://nucleo.example.org" };
});

function abrirAArea() {
  window.history.pushState(null, "", "/desenvolvedor");
}

describe("Área do Apoiador Desenvolvedor", () => {
  beforeEach(() => {
    abrirAArea();
  });
  afterEach(() => {
    vi.restoreAllMocks();
    window.localStorage.clear();
  });

  it("abre com as quatro coisas do RF-03-67, sem pedir login", () => {
    render(<App />);

    expect(
      screen.getByRole("heading", { name: /Área do Apoiador Desenvolvedor/ }),
    ).toBeVisible();
    expect(screen.getByRole("link", { name: /Documentação da plataforma/ })).toBeVisible();
    expect(
      screen.getByRole("link", { name: /Documentação da API \(Swagger\)/ }),
    ).toBeVisible();
    expect(screen.getByRole("link", { name: /Repositório no GitHub/ })).toBeVisible();
    expect(screen.getByRole("heading", { name: /Peça a sua chave/ })).toBeVisible();
    expect(screen.queryByLabelText(/senha/i)).toBeNull();
  });

  it("o link da documentação da API abre o Swagger do núcleo em nova aba (RF-03-67)", () => {
    render(<App />);

    const link = screen.getByRole("link", { name: /Documentação da API \(Swagger\)/ });
    expect(link).toHaveAttribute("href", "https://nucleo.example.org/docs");
    expect(link).toHaveAttribute("target", "_blank");
  });

  it("sem endereço do núcleo declarado não há link da documentação da API", () => {
    expect(urlDaDocumentacaoDaApi("")).toBeNull();
    expect(urlDaDocumentacaoDaApi("https://nucleo.example.org/")).toBe(
      "https://nucleo.example.org/docs",
    );
  });

  it("a área não oferece assistente nem consulta o núcleo ao abrir (decisão de 2026-11-06)", () => {
    const busca = vi.spyOn(globalThis, "fetch");

    render(<App />);

    expect(screen.queryByText(/assistente/i)).toBeNull();
    expect(screen.queryByLabelText(/pergunte/i)).toBeNull();
    expect(busca).not.toHaveBeenCalled();
  });

  it("a área é alcançada pela vitrine, como seção (RN-03-29)", async () => {
    window.history.pushState(null, "", "/");
    render(<App />);

    await userEvent.click(
      screen.getByRole("button", { name: /Abrir a Área do Apoiador Desenvolvedor/ }),
    );

    expect(
      screen.getByRole("heading", { name: /Área do Apoiador Desenvolvedor/ }),
    ).toBeVisible();
  });
});
