import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import * as biometriaModulo from "comum/biometria";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TelaDeMedicaoDoLimiar } from "./TelaDeMedicaoDoLimiar";

afterEach(() => {
  vi.restoreAllMocks();
});

function descritor(valor: number): number[] {
  return new Array(1024).fill(valor);
}

function prepararCapturas(...valores: number[]) {
  vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
  const gerar = vi.spyOn(biometriaModulo, "gerarDescritor");
  for (const valor of valores) {
    gerar.mockResolvedValueOnce(descritor(valor));
  }
  return gerar;
}

async function clicar(rotulo: RegExp) {
  const usuario = userEvent.setup();
  await usuario.click(screen.getByRole("button", { name: rotulo }));
}

describe("bancada de medição do limiar", () => {
  it("apresenta a distância na unidade do núcleo", async () => {
    prepararCapturas(0.1, 0.2);
    render(<TelaDeMedicaoDoLimiar alcance="operador" aoVoltar={vi.fn()} />);

    await clicar(/capturar a referência/i);
    await clicar(/capturar e comparar/i);

    // 1024 posições com diferença de 0,1 dão 3,2 — o mesmo número que
    // `_distancia_euclidiana` calcularia no núcleo.
    expect(await screen.findByText("3.200")).toBeInTheDocument();
  });

  it("guarda um só descritor de referência ao longo de três capturas", async () => {
    prepararCapturas(0.1, 0.2, 0.3);
    render(<TelaDeMedicaoDoLimiar alcance="operador" aoVoltar={vi.fn()} />);

    await clicar(/capturar a referência/i);
    await clicar(/capturar e comparar/i);
    await clicar(/capturar e comparar/i);

    // A terceira captura é comparada com a MESMA referência (0,1), não com a
    // segunda: se a comparada tivesse virado referência, a distância seria
    // 3,2 de novo em vez de 6,4 (`RN-04-32`).
    expect(await screen.findByText("3.200")).toBeInTheDocument();
    expect(await screen.findByText("6.400")).toBeInTheDocument();
  });

  it("não fala com o núcleo durante a medição inteira", async () => {
    const buscar = vi.spyOn(globalThis, "fetch");
    prepararCapturas(0.1, 0.2);
    render(<TelaDeMedicaoDoLimiar alcance="operador" aoVoltar={vi.fn()} />);

    await clicar(/capturar a referência/i);
    await clicar(/capturar e comparar/i);

    await screen.findByText("3.200");
    expect(buscar).not.toHaveBeenCalled();
  });

  it("fora do onboarding, mede apenas quem opera", () => {
    render(<TelaDeMedicaoDoLimiar alcance="operador" aoVoltar={vi.fn()} />);

    expect(screen.getByRole("heading", { name: /medição do limiar/i })).toBeInTheDocument();
    expect(screen.getByText(/só mede quem opera/i)).toBeInTheDocument();
    expect(screen.queryByText(/guerreiro\(a\) do cadastro/i)).not.toBeInTheDocument();
  });

  it("dentro do onboarding, mede o Guerreiro(a) daquele cadastro", () => {
    render(
      <TelaDeMedicaoDoLimiar alcance="guerreiro" nickDoGuerreiro="Zefa" aoVoltar={vi.fn()} />,
    );

    expect(screen.getByText(/capturas de Zefa/i)).toBeInTheDocument();
    expect(screen.queryByText(/só mede quem opera/i)).not.toBeInTheDocument();
  });

  it("a referência se troca por ato de quem opera, nunca sozinha", async () => {
    prepararCapturas(0.1, 0.2, 0.5);
    render(<TelaDeMedicaoDoLimiar alcance="operador" aoVoltar={vi.fn()} />);

    await clicar(/capturar a referência/i);
    await clicar(/capturar e comparar/i);
    await screen.findByText("3.200");

    await clicar(/trocar a referência/i);

    // A troca zera o que foi medido contra a referência anterior: os números
    // não se misturam entre referências diferentes.
    expect(screen.queryByText("3.200")).not.toBeInTheDocument();
  });

  // `RF-04-64`, `RN-04-34`: a bancada mede com o visor aberto, nas duas
  // capturas, e o quadro capturado não volta à tela.
  it("mede com o visor aberto nas duas capturas, sem devolver o quadro", async () => {
    const acoplar = vi.spyOn(biometriaModulo, "acoplarEspelho");
    prepararCapturas(0.1, 0.2);
    const { container } = render(
      <TelaDeMedicaoDoLimiar alcance="operador" aoVoltar={vi.fn()} />,
    );

    await clicar(/capturar a referência/i);
    await clicar(/capturar e comparar/i);

    expect(acoplar).toHaveBeenCalledTimes(2);
    expect(document.body.contains(acoplar.mock.calls[0][0])).toBe(true);
    expect(container.querySelector("img")).toBeNull();
    expect(container.querySelector("canvas")).toBeNull();
  });

  // `RF-04-65`: preparo que falhou não se disfarça de ausência de pessoa.
  it("falha de preparo tem frase própria e não chega a medir", async () => {
    vi.spyOn(biometriaModulo, "prepararCaptura").mockRejectedValue(
      new biometriaModulo.ErroDePreparoDaCaptura("modelos não carregaram"),
    );
    const provar = vi.spyOn(biometriaModulo, "provarVivacidade");
    render(<TelaDeMedicaoDoLimiar alcance="operador" aoVoltar={vi.fn()} />);

    await clicar(/capturar a referência/i);

    expect(await screen.findByText(/câmera não pôde ser preparada/i)).toBeInTheDocument();
    expect(screen.queryByText(/pessoa diante da câmera/i)).not.toBeInTheDocument();
    expect(provar).not.toHaveBeenCalled();
  });

  it("encerra a câmera ao sair da tela", () => {
    const encerrar = vi.spyOn(biometriaModulo, "encerrarCaptura").mockImplementation(() => {});
    const { unmount } = render(
      <TelaDeMedicaoDoLimiar alcance="operador" aoVoltar={vi.fn()} />,
    );

    unmount();

    expect(encerrar).toHaveBeenCalled();
  });
});
