import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { MidiaDoNucleo } from "./MidiaDoNucleo";

describe("MidiaDoNucleo", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("busca a imagem e a exibe dentro da moldura de tamanho fixo", async () => {
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(() => "blob:midia-1"),
      revokeObjectURL: vi.fn(),
    });
    const buscar = vi.fn().mockResolvedValue(new Blob(["bytes"], { type: "image/png" }));

    const { container } = render(
      <MidiaDoNucleo
        id="midia-1"
        buscar={buscar}
        token="token-1"
        tipo="imagem"
        alt="Imagem de teste"
        textoDeErro="Essa imagem não abriu agora."
      />,
    );

    const imagem = (await screen.findByRole("img")) as HTMLImageElement;
    expect(imagem.src).toBe("blob:midia-1");
    expect(buscar).toHaveBeenCalledWith("midia-1", "token-1");
    expect(container.querySelector(".cg-midia-do-nucleo")).toContainElement(imagem);
  });

  it("busca o vídeo e o exibe na mesma moldura da imagem", async () => {
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(() => "blob:video-1"),
      revokeObjectURL: vi.fn(),
    });
    const buscar = vi.fn().mockResolvedValue(new Blob(["bytes"], { type: "video/mp4" }));

    const { container } = render(
      <MidiaDoNucleo
        id="video-1"
        buscar={buscar}
        token="token-1"
        tipo="video"
        alt="Vídeo de teste"
        textoDeErro="Esse vídeo não abriu agora."
      />,
    );

    const video = await screen.findByLabelText("Vídeo de teste");
    expect(video.tagName).toBe("VIDEO");
    expect(container.querySelector(".cg-midia-do-nucleo")).toContainElement(video);
  });

  it("mostra o aviso de erro sem travar quando a busca falha", async () => {
    const buscar = vi.fn().mockRejectedValue(new Error("falhou"));

    render(
      <MidiaDoNucleo
        id="midia-1"
        buscar={buscar}
        token="token-1"
        tipo="imagem"
        alt="Imagem de teste"
        textoDeErro="Essa imagem não abriu agora, mas segue anexada."
      />,
    );

    expect(
      await screen.findByText("Essa imagem não abriu agora, mas segue anexada."),
    ).toBeInTheDocument();
    expect(screen.queryByRole("img")).not.toBeInTheDocument();
  });

  it("revoga a URL de objeto ao desmontar", async () => {
    const revogar = vi.fn();
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(() => "blob:midia-1"),
      revokeObjectURL: revogar,
    });
    const buscar = vi.fn().mockResolvedValue(new Blob(["bytes"], { type: "image/png" }));

    const { unmount } = render(
      <MidiaDoNucleo
        id="midia-1"
        buscar={buscar}
        token="token-1"
        tipo="imagem"
        alt="Imagem de teste"
        textoDeErro="Essa imagem não abriu agora."
      />,
    );
    await screen.findByRole("img");

    unmount();

    expect(revogar).toHaveBeenCalledWith("blob:midia-1");
  });

  it("sem token, não busca nada", () => {
    const buscar = vi.fn();

    render(
      <MidiaDoNucleo
        id="midia-1"
        buscar={buscar}
        token={null}
        tipo="imagem"
        alt="Imagem de teste"
        textoDeErro="Essa imagem não abriu agora."
      />,
    );

    expect(buscar).not.toHaveBeenCalled();
  });
});
