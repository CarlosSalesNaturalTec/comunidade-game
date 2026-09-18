import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import * as biometriaModulo from "comum/biometria";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as descritorApi from "../api/descritor";
import { TelaDeCaptura } from "./TelaDeCaptura";

afterEach(() => {
  vi.restoreAllMocks();
});

function renderizar(aoConcluir = vi.fn(), aoVoltar = vi.fn()) {
  return render(
    <TelaDeCaptura
      tokenDeTrabalho="token-de-trabalho"
      guerreiroId="guerreiro-1"
      aoConcluir={aoConcluir}
      aoVoltar={aoVoltar}
    />,
  );
}

describe("captura da imagem", () => {
  it("vivacidade aprovada gera o descritor e envia só ele, sem imagem", async () => {
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    const enviar = vi.spyOn(descritorApi, "enviarDescritor").mockResolvedValue({
      guerreiro_id: "guerreiro-1",
      gravado_em: new Date().toISOString(),
    });
    const aoConcluir = vi.fn();
    renderizar(aoConcluir);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    expect(enviar).toHaveBeenCalledWith(
      "guerreiro-1",
      { descritor: [0.1, 0.2, 0.3] },
      "token-de-trabalho",
    );
    const corpoEnviado = enviar.mock.calls[0][1];
    expect(Object.keys(corpoEnviado)).toEqual(["descritor"]);
    await vi.waitFor(() => expect(aoConcluir).toHaveBeenCalled());
  });

  it("vivacidade reprovada não envia nada e oferece nova tentativa", async () => {
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(false);
    const gerarDescritor = vi.spyOn(biometriaModulo, "gerarDescritor");
    const enviar = vi.spyOn(descritorApi, "enviarDescritor");
    const aoConcluir = vi.fn();
    renderizar(aoConcluir);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/não foi possível confirmar/i);
    expect(gerarDescritor).not.toHaveBeenCalled();
    expect(enviar).not.toHaveBeenCalled();
    expect(aoConcluir).not.toHaveBeenCalled();
    expect(screen.getByRole("button", { name: /iniciar captura/i })).toBeEnabled();
  });

  it("recusa por falta de consentimento traz a mensagem do núcleo", async () => {
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(descritorApi, "enviarDescritor").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Cadastro biométrico exige consentimento vigente do responsável.",
      }),
    );
    renderizar();
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      /exige consentimento vigente do responsável/i,
    );
  });

  // O defeito que esta change conserta: qualquer 422 virava a frase do
  // consentimento, e o erro de dimensão do descritor chegou ao Mestre
  // disfarçado dela por semanas (`RF-04-20`, `RF-01-02`).
  it("recusa de outra causa não vira recusa de consentimento", async () => {
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(descritorApi, "enviarDescritor").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Descritor fora da dimensão esperada.",
        campo: "descritor",
      }),
    );
    renderizar();
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(/fora da dimensão esperada/i);
    expect(alerta).not.toHaveTextContent(/consentimento/i);
  });

  it("falha sem resposta do núcleo tem frase própria", async () => {
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(descritorApi, "enviarDescritor").mockRejectedValue(
      new TypeError("Failed to fetch"),
    );
    renderizar();
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(/não foi possível concluir a captura/i);
    expect(alerta).not.toHaveTextContent(/consentimento/i);
  });

  it("nenhuma imagem aparece em registro de erro", async () => {
    vi.spyOn(biometriaModulo, "provarVivacidade").mockRejectedValue(
      new Error("falha ao abrir a câmera"),
    );
    renderizar();
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta.textContent).not.toMatch(/data:image|base64/i);
  });

  // `RF-04-64`: a tela empresta um lugar ao módulo, que anexa o visor ali
  // dentro — ela nunca recebe fluxo, quadro nem pixel.
  it("empresta ao módulo o lugar do visor, e ele está na tela", async () => {
    const acoplar = vi.spyOn(biometriaModulo, "acoplarEspelho");
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2]);
    vi.spyOn(descritorApi, "enviarDescritor").mockResolvedValue({
      guerreiro_id: "guerreiro-1",
      gravado_em: new Date().toISOString(),
    });
    renderizar();
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    expect(acoplar).toHaveBeenCalled();
    expect(document.body.contains(acoplar.mock.calls[0][0])).toBe(true);
  });

  // `RN-04-34`: o quadro capturado não volta à tela, antes nem depois de o
  // descritor ser gerado.
  it("o quadro capturado não volta à tela", async () => {
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2]);
    vi.spyOn(descritorApi, "enviarDescritor").mockResolvedValue({
      guerreiro_id: "guerreiro-1",
      gravado_em: new Date().toISOString(),
    });
    const { container } = renderizar();
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    expect(container.querySelector("img")).toBeNull();
    expect(container.querySelector("canvas")).toBeNull();
  });

  // `RF-04-65`: o defeito que esta change conserta — preparo que falhou
  // anunciava ausência de pessoa diante da câmera.
  it("falha de preparo tem frase própria, distinta da vivacidade reprovada", async () => {
    vi.spyOn(biometriaModulo, "prepararCaptura").mockRejectedValue(
      new biometriaModulo.ErroDePreparoDaCaptura("modelos não carregaram"),
    );
    const provar = vi.spyOn(biometriaModulo, "provarVivacidade");
    renderizar();
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(/câmera não pôde ser preparada/i);
    expect(alerta).not.toHaveTextContent(/pessoa diante da câmera/i);
    expect(provar).not.toHaveBeenCalled();
  });
});
