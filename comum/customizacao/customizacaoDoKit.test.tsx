import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as cliente from "../api/cliente";
import * as api from "./api";
import { CustomizacaoDoKit, ultimoRegistroDoKit } from "./CustomizacaoDoKit";

const KIT: api.KitAberto = {
  entrega_de_recompensa_id: "entrega-kit",
  recompensa_de_marco_id: "recompensa-kit",
  tipo_de_recurso_nome: "Kit de robótica",
  trilha_nome: "Robótica",
  customizacao_aberta: true,
  pendente: null,
};

function registro(parcial: Partial<api.RegistroDeCustomizacao>): api.RegistroDeCustomizacao {
  return {
    id: "registro-1",
    entrega_de_recompensa_id: "entrega-kit",
    descricao: "Pintei o robô de azul",
    situacao: "pendente",
    tem_midia: true,
    tipo_do_arquivo: "image/jpeg",
    motivo_do_julgamento: null,
    registrado_em: "2026-11-10T10:00:00Z",
    ...parcial,
  };
}

function renderizar(ultimo: api.RegistroDeCustomizacao | null) {
  const aoMudar = vi.fn().mockResolvedValue(undefined);
  const abrirFormulario = vi.fn();
  render(
    <CustomizacaoDoKit
      kit={KIT}
      ultimo={ultimo}
      token="token-do-guerreiro"
      formularioAberto={null}
      abrirFormulario={abrirFormulario}
      fecharFormulario={() => {}}
      aoMudar={aoMudar}
    />,
  );
  return { aoMudar, abrirFormulario };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("situação e ação da customização do kit (RF-05-103, RF-04-80)", () => {
  it.each([
    ["sem registro", null],
    ["cancelado", registro({ situacao: "cancelado" })],
    ["expirado", registro({ situacao: "expirado" })],
  ])("%s: oferece Registrar a customização, sem Cancelar", (_rotulo, ultimo) => {
    renderizar(ultimo);
    expect(
      screen.getByRole("button", { name: "Registrar a customização" }),
    ).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Cancelar" })).not.toBeInTheDocument();
  });

  it("pendente sem mídia: diz que falta a mídia e retoma o envio do mesmo registro", async () => {
    const { abrirFormulario } = renderizar(registro({ tem_midia: false }));
    const usuario = userEvent.setup();

    expect(screen.getByText(/Falta enviar a foto ou o vídeo/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Cancelar" })).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Enviar a foto ou o vídeo" }));
    expect(abrirFormulario).toHaveBeenCalledWith({
      entregaId: "entrega-kit",
      registroId: "registro-1",
    });
  });

  it("pendente com mídia: aguarda a aula, expira no fim do ciclo e se cancela", async () => {
    const cancelar = vi
      .spyOn(api, "cancelarCustomizacao")
      .mockResolvedValue(registro({ situacao: "cancelado" }));
    const { aoMudar } = renderizar(registro({}));
    const usuario = userEvent.setup();

    expect(screen.getByText(/Aguardando a aula/)).toBeInTheDocument();
    expect(screen.getByText(/até o fim do ciclo, este registro expira/)).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Cancelar" }));
    expect(cancelar).toHaveBeenCalledWith("registro-1", "token-do-guerreiro");
    expect(aoMudar).toHaveBeenCalled();
  });

  it("reprovado: mostra o motivo e oferece Enviar de novo, que abre registro novo", async () => {
    const { abrirFormulario } = renderizar(
      registro({ situacao: "reprovado", motivo_do_julgamento: "Falta a foto do braço" }),
    );
    const usuario = userEvent.setup();

    expect(
      screen.getByText(/O Mestre pediu um ajuste: Falta a foto do braço/),
    ).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Enviar de novo" }));
    expect(abrirFormulario).toHaveBeenCalledWith({
      entregaId: "entrega-kit",
      registroId: null,
    });
  });

  it("aprovado: diz que foi aprovado e permite registrar uma nova", () => {
    renderizar(registro({ situacao: "aprovado" }));
    expect(screen.getByText("Aprovado pelo Mestre.")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Registrar a customização" }),
    ).toBeInTheDocument();
  });

  it("o último registro decide: pendente depois de um reprovado aguarda a aula", () => {
    const reprovado = registro({
      id: "registro-0",
      situacao: "reprovado",
      motivo_do_julgamento: "Ajuste",
      registrado_em: "2026-11-01T10:00:00Z",
    });
    const pendente = registro({ registrado_em: "2026-11-12T10:00:00Z" });
    const outroKit = registro({
      id: "registro-9",
      entrega_de_recompensa_id: "outra-entrega",
      registrado_em: "2026-11-13T10:00:00Z",
    });

    const ultimo = ultimoRegistroDoKit(KIT, [pendente, reprovado, outroKit]);
    expect(ultimo?.id).toBe("registro-1");

    renderizar(ultimo);
    expect(screen.getByText(/Aguardando a aula/)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Enviar de novo" })).not.toBeInTheDocument();
  });

  it("sem registro na lista, o último é o pendente que a leitura traz no kit", () => {
    const pendente = registro({});
    expect(ultimoRegistroDoKit({ ...KIT, pendente }, [])).toBe(pendente);
  });

  it("a recusa do núcleo ao cancelar aparece como vem, e a situação é lida de novo", async () => {
    vi.spyOn(api, "cancelarCustomizacao").mockRejectedValue(
      new cliente.ErroDaApi(422, {
        codigo: "regra",
        mensagem: "Este registro já foi julgado.",
      }),
    );
    const { aoMudar } = renderizar(registro({}));
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: "Cancelar" }));
    expect(await screen.findByText("Este registro já foi julgado.")).toBeInTheDocument();
    expect(aoMudar).toHaveBeenCalled();
  });
});
