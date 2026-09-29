import { render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import * as leituras from "../api/leituras";
import { esquecerConteudoInstitucional } from "../institucional/useConteudoInstitucional";

const QUEM_SOMOS =
  "## Nota de transparência sobre IA\n\nA plataforma usa IA e diz isso.\n\nSobre o gerado com IA, veja o bloco Licenças, logo abaixo.\n\n## Licenças\n\nCódigo aberto e conteúdo em CC BY-SA.";
const COMO_APOIAR =
  "Doações por PIX.\n\nChave PIX (CNPJ): 51.730.395/0001-19\nTitular: Robô Educa — Kits Robóticos Educacionais";

function publicar(
  parcial: Partial<Record<leituras.ChaveDeSecaoInstitucional, string | null>> = {},
  video: string | null = null,
) {
  const quem = parcial["quem-somos"] === undefined ? QUEM_SOMOS : parcial["quem-somos"];
  const contatos = parcial.contatos === undefined ? null : parcial.contatos;
  const como = parcial["como-apoiar"] === undefined ? COMO_APOIAR : parcial["como-apoiar"];
  return vi.spyOn(leituras, "lerConteudoInstitucional").mockResolvedValue([
    { secao: "quem-somos", texto: quem, video_url: video },
    { secao: "contatos", texto: contatos, video_url: null },
    { secao: "como-apoiar", texto: como, video_url: null },
  ]);
}

function titulosDeSecao(): string[] {
  return screen
    .getAllByRole("heading", { level: 2 })
    .map((titulo) => titulo.textContent ?? "");
}

describe("conteúdo institucional da vitrine", () => {
  beforeEach(() => {
    esquecerConteudoInstitucional();
    window.history.pushState(null, "", "/");
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("Quem somos traz a nota e as licenças, cada uma sob o seu título (RF-03-45, RF-03-48)", async () => {
    publicar();
    render(<App />);

    const nota = await screen.findByRole("heading", {
      name: "Nota de transparência sobre IA",
    });
    const licencas = screen.getByRole("heading", { name: "Licenças" });
    expect(nota).toHaveAttribute("id", "nota-de-transparencia-sobre-ia");
    expect(licencas).toHaveAttribute("id", "licencas");
    expect(screen.getByText(/veja o bloco Licenças/)).toBeInTheDocument();
    const quemSomos = screen.getByRole("heading", {
      name: "Quem somos",
      level: 2,
    }).parentElement;
    expect(quemSomos).toContainElement(nota);
  });

  it("o endereço da nota leva direto a ela, em foco (RF-03-48)", async () => {
    publicar();
    window.history.pushState(null, "", "/#nota-de-transparencia-sobre-ia");
    render(<App />);

    const nota = await screen.findByRole("heading", {
      name: "Nota de transparência sobre IA",
    });
    await waitFor(() => expect(nota).toHaveFocus());
  });

  it("o vídeo é um link, sem player embutido nem recurso de terceiro (RF-03-49, RF-03-51)", async () => {
    publicar({}, "https://videos.exemplo.org/apresentacao");
    const { container } = render(<App />);

    const link = await screen.findByRole("link", {
      name: "Assistir ao vídeo de apresentação",
    });
    expect(link).toHaveAttribute("href", "https://videos.exemplo.org/apresentacao");
    expect(link).toHaveAttribute("rel", expect.stringContaining("noopener"));
    expect(container.querySelector("iframe, video, embed, object, script")).toBeNull();
  });

  it("sem link de vídeo, nada aparece no lugar (RF-03-49)", async () => {
    publicar();
    render(<App />);

    await screen.findByRole("heading", { name: "Nota de transparência sobre IA" });
    expect(screen.queryByRole("link", { name: /vídeo/i })).not.toBeInTheDocument();
  });

  it("seção sem texto diz que não foi publicada e não inventa conteúdo (RF-03-45)", async () => {
    publicar();
    render(<App />);

    expect(await screen.findAllByText(/ainda não foi publicado/)).not.toHaveLength(0);
    expect(
      screen.getByText("O conteúdo de “Contatos” ainda não foi publicado."),
    ).toBeVisible();
  });

  it("Como apoiar mostra a chave PIX e o titular que o núcleo devolveu (RF-03-46)", async () => {
    publicar();
    render(<App />);

    const chave = await screen.findByText(/51\.730\.395\/0001-19/);
    expect(chave).toHaveTextContent("Titular: Robô Educa — Kits Robóticos Educacionais");
  });

  it("a chave publicada é a que o Admin editou, sem depender da versão da aplicação (RF-03-46)", async () => {
    publicar({ "como-apoiar": "Chave PIX: outra-chave-do-admin" });
    render(<App />);

    expect(await screen.findByText(/outra-chave-do-admin/)).toBeVisible();
    expect(screen.queryByText(/51\.730\.395/)).not.toBeInTheDocument();
  });

  it("uma única leitura alimenta as três seções", async () => {
    const leitura = publicar();
    render(<App />);

    await screen.findByText(/51\.730\.395/);
    expect(leitura).toHaveBeenCalledTimes(1);
  });

  it("em sociedade civil, Quem somos abre e Como apoiar e Contatos fecham (RF-03-45)", async () => {
    publicar();
    render(<App />);
    await screen.findByText(/51\.730\.395/);

    const titulos = titulosDeSecao();
    expect(titulos[0]).toBe("Quem somos");
    expect(titulos.slice(-2)).toEqual(["Como apoiar", "Contatos"]);
  });

  it.each(["/pesquisadores", "/gestores-publicos"])(
    "Contatos fecha o recorte %s (RF-03-45)",
    async (caminho) => {
      publicar({ contatos: "Escreva para contato@exemplo.org" });
      window.history.pushState(null, "", caminho);
      render(<App />);

      const secao = (await screen.findByRole("heading", { name: "Contatos", level: 2 }))
        .parentElement as HTMLElement;
      expect(await within(secao).findByText(/contato@exemplo\.org/)).toBeVisible();
      expect(titulosDeSecao().at(-1)).toBe("Contatos");
    },
  );

  it("falha na leitura avisa em linguagem simples, sem travar a tela", async () => {
    vi.spyOn(leituras, "lerConteudoInstitucional").mockRejectedValue(new Error("fora do ar"));
    render(<App />);

    expect(
      (
        await screen.findAllByText(
          "Não foi possível carregar esta seção agora. Tente de novo.",
        )
      ).length,
    ).toBeGreaterThan(0);
    expect(screen.getByRole("heading", { name: "Comunidade Game", level: 1 })).toBeVisible();
  });
});
