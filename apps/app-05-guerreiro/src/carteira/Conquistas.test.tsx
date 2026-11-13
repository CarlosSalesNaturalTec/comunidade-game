import { act, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import * as customizacaoApi from "comum/customizacao";
import * as customizacaoRotas from "comum/customizacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as carteiraApi from "../api/carteira";
import { Conquistas } from "./Conquistas";

const CHAVE_DE_SESSAO = "app-05:teste-conquistas";

async function renderizar() {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <Conquistas />
      </ProvedorDeSessao>,
    );
  });
}

beforeEach(() => {
  vi.spyOn(customizacaoRotas, "lerMinhasCustomizacoes").mockResolvedValue({
    kits_abertos: [],
    registros: [],
  });
});

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("recompensas de marco conquistadas", () => {
  it("mostra a conquista aguardando o Mestre, sem caminho de compra", async () => {
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([
      {
        recompensa_de_marco_id: "recompensa-1",
        trilha_id: "trilha-1",
        missao_id: "missao-1",
        tipo_de_recurso_id: "recurso-1",
        tipo_de_recurso_nome: "Camisa do Comunidade Game",
        tipo_de_recurso_unidade: "unidade",
        quantidade: 1,
        entregue: false,
        entregue_em: null,
        ciente: false,
      },
    ]);

    await renderizar();

    expect(await screen.findByText(/aguardando o mestre confirmar/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /comprar/i })).not.toBeInTheDocument();
  });

  it("mostra a entrega confirmada com a data", async () => {
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([
      {
        recompensa_de_marco_id: "recompensa-1",
        trilha_id: "trilha-1",
        missao_id: "missao-1",
        tipo_de_recurso_id: "recurso-1",
        tipo_de_recurso_nome: "Camisa do Comunidade Game",
        tipo_de_recurso_unidade: "unidade",
        quantidade: 1,
        entregue: true,
        entregue_em: "2026-08-01T10:00:00Z",
        ciente: true,
      },
    ]);

    await renderizar();

    expect(await screen.findByText(/entregue em/i)).toBeInTheDocument();
  });

  it("a lista nomeia o que foi conquistado, não só a quantidade", async () => {
    // `RF-05-45`: a leitura passou a trazer o nome e a unidade do tipo, e a
    // lista imprimia "Quantidade conquistada: 1" — que não diz se é o livro,
    // a camisa ou o kit.
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([
      {
        recompensa_de_marco_id: "recompensa-1",
        trilha_id: "trilha-1",
        missao_id: "missao-1",
        tipo_de_recurso_id: "recurso-1",
        tipo_de_recurso_nome: "Livro da linha Alpha",
        tipo_de_recurso_unidade: "unidade",
        quantidade: 2,
        entregue: false,
        entregue_em: null,
        ciente: false,
      },
    ]);

    await renderizar();

    expect(await screen.findByText("2 Livro da linha Alpha")).toBeInTheDocument();
    expect(screen.queryByText(/Quantidade conquistada/i)).not.toBeInTheDocument();
  });

  it("sem conquista nenhuma, explica em vez de mostrar tela vazia", async () => {
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([]);

    await renderizar();

    expect(await screen.findByText(/ainda não conquistou/i)).toBeInTheDocument();
  });
});

const KIT_CONQUISTADO: carteiraApi.RecompensaConquistada = {
  recompensa_de_marco_id: "recompensa-kit",
  trilha_id: "trilha-1",
  missao_id: "missao-1",
  tipo_de_recurso_id: "recurso-kit",
  tipo_de_recurso_nome: "Kit de robótica",
  tipo_de_recurso_unidade: "unidade",
  quantidade: 1,
  entregue: true,
  entregue_em: "2026-10-01T10:00:00Z",
  ciente: true,
};

const CAMISA_CONQUISTADA: carteiraApi.RecompensaConquistada = {
  ...KIT_CONQUISTADO,
  recompensa_de_marco_id: "recompensa-camisa",
  tipo_de_recurso_id: "recurso-camisa",
  tipo_de_recurso_nome: "Camisa do Comunidade Game",
};

const KIT_ABERTO: customizacaoApi.KitAberto = {
  entrega_de_recompensa_id: "entrega-kit",
  recompensa_de_marco_id: "recompensa-kit",
  tipo_de_recurso_nome: "Kit de robótica",
  trilha_nome: "Robótica",
  customizacao_aberta: true,
  pendente: null,
};

function registro(
  parcial: Partial<customizacaoApi.RegistroDeCustomizacao>,
): customizacaoApi.RegistroDeCustomizacao {
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

function cartaoDe(nome: RegExp): HTMLElement {
  const item = screen.getByText(nome).closest("li");
  if (!item) throw new Error("cartão não encontrado");
  return item;
}

describe("customização do kit na lista de conquistas (RF-05-102, RF-05-103)", () => {
  it("o kit aberto oferece o registro; a recompensa sem customização não muda", async () => {
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([
      KIT_CONQUISTADO,
      CAMISA_CONQUISTADA,
    ]);
    vi.mocked(customizacaoRotas.lerMinhasCustomizacoes).mockResolvedValue({
      kits_abertos: [KIT_ABERTO],
      registros: [],
    });

    await renderizar();

    const kit = cartaoDe(/Kit de robótica/);
    expect(
      await within(kit).findByRole("button", { name: "Registrar a customização" }),
    ).toBeInTheDocument();
    const camisa = cartaoDe(/Camisa do Comunidade Game/);
    expect(within(camisa).queryByRole("button")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /comprar/i })).not.toBeInTheDocument();
  });

  it("o registro abre no cartão, com o aviso antes do envio", async () => {
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([KIT_CONQUISTADO]);
    vi.mocked(customizacaoRotas.lerMinhasCustomizacoes).mockResolvedValue({
      kits_abertos: [KIT_ABERTO],
      registros: [],
    });
    const usuario = userEvent.setup();

    await renderizar();
    await usuario.click(
      await screen.findByRole("button", { name: "Registrar a customização" }),
    );

    expect(
      screen.getByText(customizacaoApi.AVISO_DA_CUSTOMIZACAO, { exact: false }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Foto ou vídeo do kit")).toBeInTheDocument();
  });

  it("o pendente aguarda a aula, diz que expira e, cancelado, volta a oferecer o registro", async () => {
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([KIT_CONQUISTADO]);
    const pendente = registro({});
    vi.mocked(customizacaoRotas.lerMinhasCustomizacoes)
      .mockResolvedValueOnce({
        kits_abertos: [{ ...KIT_ABERTO, pendente }],
        registros: [pendente],
      })
      .mockResolvedValueOnce({
        kits_abertos: [KIT_ABERTO],
        registros: [{ ...pendente, situacao: "cancelado" }],
      });
    const cancelar = vi
      .spyOn(customizacaoRotas, "cancelarCustomizacao")
      .mockResolvedValue({ ...pendente, situacao: "cancelado" });
    const usuario = userEvent.setup();

    await renderizar();

    expect(await screen.findByText(/Aguardando a aula/)).toBeInTheDocument();
    expect(screen.getByText(/até o fim do ciclo, este registro expira/)).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Cancelar" }));

    expect(cancelar).toHaveBeenCalledWith("registro-1", "token-do-guerreiro");
    expect(
      await screen.findByRole("button", { name: "Registrar a customização" }),
    ).toBeInTheDocument();
  });

  it("o pendente sem mídia oferece retomar o envio do mesmo registro", async () => {
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([KIT_CONQUISTADO]);
    const pendente = registro({ tem_midia: false, tipo_do_arquivo: null });
    vi.mocked(customizacaoRotas.lerMinhasCustomizacoes).mockResolvedValue({
      kits_abertos: [{ ...KIT_ABERTO, pendente }],
      registros: [pendente],
    });
    const usuario = userEvent.setup();

    await renderizar();
    await usuario.click(
      await screen.findByRole("button", { name: "Enviar a foto ou o vídeo" }),
    );

    expect(screen.queryByLabelText("O que você customizou no kit")).not.toBeInTheDocument();
    expect(screen.getByLabelText("Foto ou vídeo do kit")).toBeInTheDocument();
  });

  it("o reprovado mostra o motivo e Enviar de novo abre um registro novo", async () => {
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([KIT_CONQUISTADO]);
    vi.mocked(customizacaoRotas.lerMinhasCustomizacoes).mockResolvedValue({
      kits_abertos: [KIT_ABERTO],
      registros: [
        registro({
          id: "antigo",
          situacao: "aprovado",
          registrado_em: "2026-10-01T10:00:00Z",
        }),
        registro({
          situacao: "reprovado",
          motivo_do_julgamento: "A foto mostra o seu rosto.",
        }),
      ],
    });
    const usuario = userEvent.setup();

    await renderizar();

    expect(
      await screen.findByText("O Mestre pediu um ajuste: A foto mostra o seu rosto."),
    ).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Enviar de novo" }));
    expect(screen.getByLabelText("O que você customizou no kit")).toBeInTheDocument();
  });

  it("a falha só das customizações não esconde as conquistas", async () => {
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([KIT_CONQUISTADO]);
    vi.mocked(customizacaoRotas.lerMinhasCustomizacoes).mockRejectedValue(
      new TypeError("rede"),
    );

    await renderizar();

    expect(
      await screen.findByText(/Não foi possível carregar a customização dos seus kits/),
    ).toBeInTheDocument();
    expect(screen.getByText(/Kit de robótica/)).toBeInTheDocument();
  });
});
