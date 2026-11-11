import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
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

  // Numa sequência paginada o React reaproveita a instância entre itens. O
  // estado tem de acompanhar o `id`, senão a mídia do item anterior fica na
  // tela sob o item novo (spec `area-do-guerreiro`, design — decisão 6).
  it("trocando de item, não deixa a mídia do anterior na tela e diz que carrega", async () => {
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(
        (bytes: Blob) => `blob:${(bytes as Blob & { nome?: string }).nome}`,
      ),
      revokeObjectURL: vi.fn(),
    });
    const primeira = new Blob(["a"], { type: "image/png" }) as Blob & { nome?: string };
    primeira.nome = "midia-1";
    const segunda = new Blob(["b"], { type: "image/png" }) as Blob & { nome?: string };
    segunda.nome = "midia-2";
    let liberarSegunda: (bytes: Blob) => void = () => {};
    const buscar = vi.fn((idBuscado: string) =>
      idBuscado === "midia-1"
        ? Promise.resolve(primeira as Blob)
        : new Promise<Blob>((resolver) => {
            liberarSegunda = resolver;
          }),
    );

    const propriedades = {
      buscar,
      token: "token-1",
      tipo: "imagem" as const,
      alt: "Imagem de teste",
      textoDeErro: "Essa imagem não abriu agora.",
    };
    const { rerender } = render(<MidiaDoNucleo id="midia-1" {...propriedades} />);
    expect((await screen.findByRole("img")).getAttribute("src")).toBe("blob:midia-1");

    rerender(<MidiaDoNucleo id="midia-2" {...propriedades} />);

    // A imagem do item anterior sai na hora, e a moldura declara a carga.
    expect(screen.queryByRole("img")).not.toBeInTheDocument();
    expect(screen.getByText("Carregando…")).toBeInTheDocument();

    liberarSegunda(segunda as Blob);
    expect((await screen.findByRole("img")).getAttribute("src")).toBe("blob:midia-2");
  });

  it("a falha de um item não acompanha o item seguinte", async () => {
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(() => "blob:midia-2"),
      revokeObjectURL: vi.fn(),
    });
    const buscar = vi.fn((idBuscado: string) =>
      idBuscado === "midia-1"
        ? Promise.reject(new Error("falhou"))
        : Promise.resolve(new Blob(["b"], { type: "image/png" })),
    );

    const propriedades = {
      buscar,
      token: "token-1",
      tipo: "imagem" as const,
      alt: "Imagem de teste",
      textoDeErro: "Essa imagem não abriu agora.",
    };
    const { rerender } = render(<MidiaDoNucleo id="midia-1" {...propriedades} />);
    expect(await screen.findByText("Essa imagem não abriu agora.")).toBeInTheDocument();

    rerender(<MidiaDoNucleo id="midia-2" {...propriedades} />);

    expect(screen.queryByText("Essa imagem não abriu agora.")).not.toBeInTheDocument();
    expect(await screen.findByRole("img")).toBeInTheDocument();
  });

  // As duas quedas da trava de navegação: sem elas, mídia que não abre — ou
  // item seguinte sem mídia — prende quem percorre a sequência.
  it("reporta o fim da carga quando a busca falha", async () => {
    const aoMudarCarregamento = vi.fn();
    const buscar = vi.fn().mockRejectedValue(new Error("falhou"));

    render(
      <MidiaDoNucleo
        id="midia-1"
        buscar={buscar}
        token="token-1"
        tipo="imagem"
        alt="Imagem de teste"
        textoDeErro="Essa imagem não abriu agora."
        aoMudarCarregamento={aoMudarCarregamento}
      />,
    );
    await screen.findByText("Essa imagem não abriu agora.");

    expect(aoMudarCarregamento).toHaveBeenNthCalledWith(1, true);
    expect(aoMudarCarregamento).toHaveBeenLastCalledWith(false);
  });

  it("reporta o fim da carga ao desmontar com a busca em curso", async () => {
    const aoMudarCarregamento = vi.fn();
    const buscar = vi.fn(() => new Promise<Blob>(() => {}));

    const { unmount } = render(
      <MidiaDoNucleo
        id="midia-1"
        buscar={buscar}
        token="token-1"
        tipo="imagem"
        alt="Imagem de teste"
        textoDeErro="Essa imagem não abriu agora."
        aoMudarCarregamento={aoMudarCarregamento}
      />,
    );
    expect(aoMudarCarregamento).toHaveBeenLastCalledWith(true);

    unmount();

    expect(aoMudarCarregamento).toHaveBeenLastCalledWith(false);
  });

  describe("ampliação da imagem", () => {
    function montar(props: Partial<Parameters<typeof MidiaDoNucleo>[0]> = {}) {
      vi.stubGlobal("URL", {
        ...URL,
        createObjectURL: vi.fn(() => "blob:midia-1"),
        revokeObjectURL: vi.fn(),
      });
      const buscar = vi.fn().mockResolvedValue(new Blob(["bytes"], { type: "image/png" }));
      render(
        <MidiaDoNucleo
          id="midia-1"
          buscar={buscar}
          token="token-1"
          tipo="imagem"
          alt="Mapa do bairro"
          textoDeErro="Essa imagem não abriu agora."
          ampliavel
          {...props}
        />,
      );
      return buscar;
    }

    it("tocar na imagem a abre em tela cheia, sem nova busca", async () => {
      const usuario = userEvent.setup();
      const buscar = montar();

      await usuario.click(
        await screen.findByRole("button", { name: "Ampliar imagem: Mapa do bairro" }),
      );

      const dialogo = screen.getByRole("dialog", { name: "Mapa do bairro" });
      expect(dialogo).toHaveClass("cg-dialogo--tela-cheia");
      const ampliada = within(dialogo).getByRole("img", {
        name: "Mapa do bairro",
      }) as HTMLImageElement;
      expect(ampliada.src).toBe("blob:midia-1");
      expect(buscar).toHaveBeenCalledTimes(1);
    });

    it("fechar pelo botão ou pelo Esc devolve o foco à imagem da moldura", async () => {
      const usuario = userEvent.setup();
      montar();
      const controle = await screen.findByRole("button", {
        name: "Ampliar imagem: Mapa do bairro",
      });

      await usuario.click(controle);
      await usuario.click(screen.getByRole("button", { name: "Fechar" }));
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
      expect(controle).toHaveFocus();

      await usuario.keyboard("{Enter}");
      expect(screen.getByRole("dialog")).toBeInTheDocument();
      await usuario.keyboard("{Escape}");
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
      expect(controle).toHaveFocus();
    });

    it("sem ampliavel, a imagem não é controle", async () => {
      montar({ ampliavel: false });
      await screen.findByRole("img", { name: "Mapa do bairro" });
      expect(screen.queryByRole("button")).not.toBeInTheDocument();
    });

    it("vídeo e áudio nunca ganham o controle de ampliar", async () => {
      montar({ tipo: "video" });
      await screen.findByLabelText("Mapa do bairro");
      expect(screen.queryByRole("button")).not.toBeInTheDocument();
    });

    it("carregando e falha não oferecem ampliação", async () => {
      vi.stubGlobal("URL", { ...URL, createObjectURL: vi.fn(), revokeObjectURL: vi.fn() });
      render(
        <MidiaDoNucleo
          id="midia-1"
          buscar={vi.fn().mockRejectedValue(new Error("rede"))}
          token="token-1"
          tipo="imagem"
          alt="Mapa do bairro"
          textoDeErro="Essa imagem não abriu agora."
          ampliavel
        />,
      );
      expect(screen.queryByRole("button")).not.toBeInTheDocument();
      await screen.findByText("Essa imagem não abriu agora.");
      expect(screen.queryByRole("button")).not.toBeInTheDocument();
    });
  });
});
