import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as cliente from "../api/cliente";
import * as fala from "../fala/fala";
import * as api from "./api";
import { AVISO_DA_CUSTOMIZACAO, RegistroDaCustomizacao } from "./RegistroDaCustomizacao";

const REGISTRO: api.RegistroDeCustomizacao = {
  id: "registro-1",
  entrega_de_recompensa_id: "entrega-1",
  descricao: "Pintei o robô de azul",
  situacao: "pendente",
  tem_midia: false,
  tipo_do_arquivo: null,
  motivo_do_julgamento: null,
  registrado_em: "2026-11-13T12:00:00Z",
};

function foto(): File {
  return new File(["x"], "kit.jpg", { type: "image/jpeg" });
}

function renderizar(props: Partial<Parameters<typeof RegistroDaCustomizacao>[0]> = {}) {
  const aoConcluir = vi.fn();
  render(
    <RegistroDaCustomizacao
      entregaDeRecompensaId="entrega-1"
      token="token"
      aoConcluir={aoConcluir}
      aoCancelar={() => {}}
      {...props}
    />,
  );
  return { aoConcluir };
}

beforeEach(() => {
  vi.spyOn(fala, "existeTranscricaoDeFala").mockReturnValue(false);
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe("registro da customização do kit (RF-05-102)", () => {
  it("traz o aviso aprovado e o Saber mais antes do seletor da foto ou do vídeo", () => {
    renderizar();
    const aviso = screen.getByText(AVISO_DA_CUSTOMIZACAO, { exact: false });
    const seletor = screen.getByLabelText("Foto ou vídeo do kit");
    expect(screen.getByRole("button", { name: "Saber mais" })).toBeInTheDocument();
    expect(
      aviso.compareDocumentPosition(seletor) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
  });

  it("o seletor oferece só imagem e vídeo, pela câmera traseira", () => {
    renderizar();
    const seletor = screen.getByLabelText("Foto ou vídeo do kit");
    expect(seletor).toHaveAttribute("accept", "image/*,video/*");
    expect(seletor).toHaveAttribute("capture", "environment");
  });

  it("deixa o registro indisponível sem descrição ou sem mídia", async () => {
    const usuario = userEvent.setup();
    renderizar();
    const botao = screen.getByRole("button", { name: "Registrar a customização" });
    expect(botao).toBeDisabled();
    await usuario.upload(screen.getByLabelText("Foto ou vídeo do kit"), foto());
    expect(botao).toBeDisabled();
    await usuario.type(screen.getByLabelText("O que você customizou no kit"), "   ");
    expect(botao).toBeDisabled();
    await usuario.type(screen.getByLabelText("O que você customizou no kit"), "Pintei");
    expect(botao).toBeEnabled();
  });

  it("a fala transcrita cai no campo, editável, e é ela que vai ao núcleo", async () => {
    vi.mocked(fala.existeTranscricaoDeFala).mockReturnValue(true);
    vi.spyOn(fala, "iniciarTranscricao").mockImplementation((retornos) => {
      retornos.aoTranscrever("Pintei o robô de azul");
      retornos.aoEncerrar?.();
      return () => {};
    });
    const registrar = vi.spyOn(api, "registrarMinhaCustomizacao").mockResolvedValue(REGISTRO);
    vi.spyOn(api, "enviarMidiaDaCustomizacao").mockResolvedValue({
      ...REGISTRO,
      tem_midia: true,
    });
    const usuario = userEvent.setup();
    const { aoConcluir } = renderizar();

    await usuario.click(screen.getByRole("button", { name: "Falar a descrição" }));
    expect(screen.getByLabelText("O que você customizou no kit")).toHaveValue(
      "Pintei o robô de azul",
    );
    await usuario.upload(screen.getByLabelText("Foto ou vídeo do kit"), foto());
    await usuario.click(screen.getByRole("button", { name: "Registrar a customização" }));

    expect(registrar).toHaveBeenCalledWith(
      { entrega_de_recompensa_id: "entrega-1", descricao: "Pintei o robô de azul" },
      "token",
    );
    expect(aoConcluir).toHaveBeenCalled();
  });

  it("sem transcrição no aparelho, segue só por texto", () => {
    renderizar();
    expect(
      screen.queryByRole("button", { name: "Falar a descrição" }),
    ).not.toBeInTheDocument();
    expect(
      screen.getByText("Este aparelho não transcreve fala. Escreva a descrição."),
    ).toBeInTheDocument();
  });

  it("caindo a rede, diz e retoma o envio ao mesmo registro, sem criar outro", async () => {
    const registrar = vi.spyOn(api, "registrarMinhaCustomizacao").mockResolvedValue(REGISTRO);
    const enviar = vi
      .spyOn(api, "enviarMidiaDaCustomizacao")
      .mockRejectedValueOnce(new TypeError("Failed to fetch"))
      .mockResolvedValueOnce({ ...REGISTRO, tem_midia: true });
    const usuario = userEvent.setup();
    const { aoConcluir } = renderizar();

    await usuario.type(screen.getByLabelText("O que você customizou no kit"), "Pintei");
    await usuario.upload(screen.getByLabelText("Foto ou vídeo do kit"), foto());
    await usuario.click(screen.getByRole("button", { name: "Registrar a customização" }));

    expect(await screen.findByText(/A conexão caiu no meio do envio/)).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Tentar novamente" }));

    expect(registrar).toHaveBeenCalledTimes(1);
    expect(enviar).toHaveBeenCalledTimes(2);
    expect(enviar.mock.calls[1][0]).toBe("registro-1");
    expect(aoConcluir).toHaveBeenCalledTimes(1);
  });

  it("o pendente sem mídia só envia, sem pedir a descrição de novo", async () => {
    const registrar = vi.spyOn(api, "registrarMinhaCustomizacao");
    const enviar = vi
      .spyOn(api, "enviarMidiaDaCustomizacao")
      .mockResolvedValue({ ...REGISTRO, tem_midia: true });
    const usuario = userEvent.setup();
    renderizar({ registroIdInicial: "registro-1" });

    expect(screen.queryByLabelText("O que você customizou no kit")).not.toBeInTheDocument();
    await usuario.upload(screen.getByLabelText("Foto ou vídeo do kit"), foto());
    await usuario.click(screen.getByRole("button", { name: "Enviar a foto ou o vídeo" }));

    expect(registrar).not.toHaveBeenCalled();
    expect(enviar.mock.calls[0][0]).toBe("registro-1");
  });

  it("a recusa do núcleo aparece como vem", async () => {
    vi.spyOn(api, "registrarMinhaCustomizacao").mockRejectedValue(
      new cliente.ErroDaApi(422, {
        codigo: "regra",
        mensagem: "Há um registro deste kit aguardando o Mestre.",
      }),
    );
    const usuario = userEvent.setup();
    renderizar();

    await usuario.type(screen.getByLabelText("O que você customizou no kit"), "Pintei");
    await usuario.upload(screen.getByLabelText("Foto ou vídeo do kit"), foto());
    await usuario.click(screen.getByRole("button", { name: "Registrar a customização" }));

    expect(
      await screen.findByText("Há um registro deste kit aguardando o Mestre."),
    ).toBeInTheDocument();
  });
});
