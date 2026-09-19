import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import * as biometriaModulo from "comum/biometria";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as medicoesApi from "../api/medicoesDoLimiar";
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

function renderizar(props: Partial<Parameters<typeof TelaDeMedicaoDoLimiar>[0]> = {}) {
  return render(
    <TelaDeMedicaoDoLimiar
      alcance="operador"
      tokenDeTrabalho="token-de-trabalho"
      aulaId="aula-1"
      aoVoltar={vi.fn()}
      {...props}
    />,
  );
}

async function clicar(rotulo: RegExp) {
  const usuario = userEvent.setup();
  await usuario.click(screen.getByRole("button", { name: rotulo }));
}

function serie(nome: RegExp) {
  return screen.getByRole("heading", { name: nome }).closest("section") as HTMLElement;
}

/** A lista de medições da série — escopo estreito de propósito: o destaque
 * do "maior piso" repete o mesmo número, e uma busca na seção inteira acharia
 * os dois. */
function listaDa(nome: RegExp) {
  return within(serie(nome).querySelector("ol") as HTMLElement);
}

/** O piso completo: 8 capturas da mesma pessoa contra a referência. Os valores
 * dão distâncias baixas, bem abaixo do teto. */
const CAPTURAS_DE_PISO = [0.11, 0.12, 0.13, 0.11, 0.12, 0.14, 0.13, 0.12];
/** O teto completo: 8 capturas de pessoas diferentes, todas distantes. */
const CAPTURAS_DE_TETO = [0.5, 0.52, 0.55, 0.51, 0.53, 0.56, 0.54, 0.52];

async function medirSerieInteira(quantas: number) {
  for (let i = 0; i < quantas; i++) {
    await clicar(/capturar e comparar/i);
  }
}

/** Uma medição completa e com folga, pronta para confirmar. */
async function medicaoConcluida() {
  prepararCapturas(0.1, ...CAPTURAS_DE_PISO, ...CAPTURAS_DE_TETO);
  renderizar();
  await clicar(/capturar a referência/i);
  await medirSerieInteira(CAPTURAS_DE_PISO.length);
  await clicar(/teto — outra pessoa/i);
  await clicar(/capturar e comparar/i);
  await clicar(/trocou a pessoa diante da câmera/i);
  await medirSerieInteira(CAPTURAS_DE_TETO.length - 1);
}

describe("bancada de medição do limiar", () => {
  it("apresenta a distância na unidade do núcleo", async () => {
    prepararCapturas(0.1, 0.2);
    renderizar();

    await clicar(/capturar a referência/i);
    await clicar(/capturar e comparar/i);

    // 1024 posições com diferença de 0,1 dão 3,2 — o mesmo número que
    // `_distancia_euclidiana` calcularia no núcleo.
    expect(await listaDa(/^piso/i).findByText("3.200")).toBeInTheDocument();
  });

  it("guarda um só descritor de referência ao longo de três capturas", async () => {
    prepararCapturas(0.1, 0.2, 0.3);
    renderizar();

    await clicar(/capturar a referência/i);
    await clicar(/capturar e comparar/i);
    await clicar(/capturar e comparar/i);

    // A terceira captura é comparada com a MESMA referência (0,1), não com a
    // segunda: se a comparada tivesse virado referência, a distância seria
    // 3,2 de novo em vez de 6,4 (`RN-04-32`).
    const piso = listaDa(/^piso/i);
    expect(await piso.findByText("3.200")).toBeInTheDocument();
    expect(await piso.findByText("6.400")).toBeInTheDocument();
  });

  // `RF-04-66`: as duas séries aparecem separadas, e é a folga entre elas que
  // diz se existe limiar viável.
  it("separa as capturas na série que quem opera declarou", async () => {
    prepararCapturas(0.1, 0.2, 0.5);
    renderizar();

    await clicar(/capturar a referência/i);
    await clicar(/capturar e comparar/i);
    await clicar(/teto — outra pessoa/i);
    await clicar(/capturar e comparar/i);

    expect(await listaDa(/^piso/i).findByText("3.200")).toBeInTheDocument();
    expect(listaDa(/^piso/i).queryByText("12.800")).not.toBeInTheDocument();
    expect(await listaDa(/^teto/i).findByText("12.800")).toBeInTheDocument();
  });

  it("mostra o maior piso e o menor teto em destaque", async () => {
    prepararCapturas(0.1, 0.2, 0.3, 0.5, 0.6);
    renderizar();

    await clicar(/capturar a referência/i);
    await clicar(/capturar e comparar/i);
    await clicar(/capturar e comparar/i);
    await clicar(/teto — outra pessoa/i);
    await clicar(/capturar e comparar/i);
    await clicar(/capturar e comparar/i);

    expect(await screen.findByText(/maior piso/i)).toHaveTextContent("6.400");
    expect(screen.getByText(/menor teto/i)).toHaveTextContent("12.800");
  });

  // `RN-04-35`: o critério de conclusão.
  it("não oferece a gravação enquanto as séries não fecham o mínimo", async () => {
    prepararCapturas(0.1, 0.2);
    renderizar();

    await clicar(/capturar a referência/i);
    await clicar(/capturar e comparar/i);

    expect(await screen.findByText(/faltam capturas/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /confirmar e gravar/i }),
    ).not.toBeInTheDocument();
  });

  it("teto de uma pessoa só não conclui a medição", async () => {
    prepararCapturas(0.1, ...CAPTURAS_DE_PISO, ...CAPTURAS_DE_TETO);
    renderizar();

    await clicar(/capturar a referência/i);
    await medirSerieInteira(CAPTURAS_DE_PISO.length);
    await clicar(/teto — outra pessoa/i);
    await medirSerieInteira(CAPTURAS_DE_TETO.length);

    // Oito capturas de teto, mas ninguém declarou troca de pessoa.
    expect(await screen.findByText(/ao menos 2 pessoas/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /confirmar e gravar/i }),
    ).not.toBeInTheDocument();
  });

  it("séries que se sobrepõem não geram limiar", async () => {
    // O teto cai dentro da faixa do piso: não existe número que acerte os
    // dois lados (`RN-04-35`).
    const tetoSobreposto = [0.12, 0.13, 0.11, 0.12, 0.14, 0.13, 0.12, 0.11];
    prepararCapturas(0.1, ...CAPTURAS_DE_PISO, ...tetoSobreposto);
    renderizar();

    await clicar(/capturar a referência/i);
    await medirSerieInteira(CAPTURAS_DE_PISO.length);
    await clicar(/teto — outra pessoa/i);
    await clicar(/capturar e comparar/i);
    await clicar(/trocou a pessoa diante da câmera/i);
    await medirSerieInteira(tetoSobreposto.length - 1);

    expect(await screen.findByText(/séries se sobrepõem/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /confirmar e gravar/i }),
    ).not.toBeInTheDocument();
  });

  it("propõe o ponto médio entre o maior piso e o menor teto", async () => {
    await medicaoConcluida();

    // maior piso: |0.14 - 0.1| * 32 = 1.28 · menor teto: |0.5 - 0.1| * 32 = 12.8
    // ponto médio: (1.28 + 12.8) / 2 = 7.04
    expect(await screen.findByText(/limiar proposto/i)).toHaveTextContent("7.040");
  });

  it("só grava depois da confirmação, e manda distâncias, nunca descritor", async () => {
    const gravar = vi.spyOn(medicoesApi, "gravarMedicaoDoLimiar").mockResolvedValue({
      id: "medicao-1",
      ponto_de_apoio_id: "ponto-1",
      limiar: 7.04,
      distancias_do_piso: [],
      distancias_do_teto: [],
      pessoas_no_teto: 2,
      medido_por: "mestre-1",
      registrado_em: new Date().toISOString(),
    });

    await medicaoConcluida();
    expect(gravar).not.toHaveBeenCalled();

    await clicar(/confirmar e gravar/i);

    expect(gravar).toHaveBeenCalledTimes(1);
    const [entrada, token] = gravar.mock.calls[0];
    expect(token).toBe("token-de-trabalho");
    expect(entrada.aula_id).toBe("aula-1");
    expect(entrada.distancias_do_piso).toHaveLength(8);
    expect(entrada.distancias_do_teto).toHaveLength(8);
    expect(entrada.pessoas_no_teto).toBe(2);
    // O limiar não vai no corpo: o núcleo o calcula das mesmas séries.
    expect(entrada).not.toHaveProperty("limiar");
    expect(entrada).not.toHaveProperty("descritor");
    expect(JSON.stringify(entrada)).not.toContain("0.1,0.1,0.1");

    expect(await screen.findByText(/gravado para o ponto de apoio/i)).toBeInTheDocument();
  });

  it("não fala com o núcleo durante a medição, só na gravação", async () => {
    const buscar = vi.spyOn(globalThis, "fetch");
    prepararCapturas(0.1, 0.2);
    renderizar();

    await clicar(/capturar a referência/i);
    await clicar(/capturar e comparar/i);

    await listaDa(/^piso/i).findByText("3.200");
    expect(buscar).not.toHaveBeenCalled();
  });

  it("fora do onboarding, mede apenas quem opera", () => {
    renderizar();

    expect(screen.getByRole("heading", { name: /medição do limiar/i })).toBeInTheDocument();
    expect(screen.getByText(/só mede quem opera/i)).toBeInTheDocument();
    expect(screen.queryByText(/guerreiro\(a\) do cadastro/i)).not.toBeInTheDocument();
  });

  it("dentro do onboarding, mede o Guerreiro(a) daquele cadastro", () => {
    renderizar({ alcance: "guerreiro", nickDoGuerreiro: "Zefa" });

    expect(screen.getByText(/capturas de Zefa/i)).toBeInTheDocument();
    expect(screen.queryByText(/só mede quem opera/i)).not.toBeInTheDocument();
  });

  it("a referência se troca por ato de quem opera, nunca sozinha", async () => {
    prepararCapturas(0.1, 0.2, 0.5);
    renderizar();

    await clicar(/capturar a referência/i);
    await clicar(/capturar e comparar/i);
    await listaDa(/^piso/i).findByText("3.200");

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
    const { container } = renderizar();

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
    renderizar();

    await clicar(/capturar a referência/i);

    expect(await screen.findByText(/câmera não pôde ser preparada/i)).toBeInTheDocument();
    expect(screen.queryByText(/pessoa diante da câmera/i)).not.toBeInTheDocument();
    expect(provar).not.toHaveBeenCalled();
  });

  it("encerra a câmera ao sair da tela", () => {
    const encerrar = vi.spyOn(biometriaModulo, "encerrarCaptura").mockImplementation(() => {});
    const { unmount } = renderizar();

    unmount();

    expect(encerrar).toHaveBeenCalled();
  });
});
