import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { ProvedorDeSessao } from "comum/autenticacao";
import { ProvedorDeNarracao } from "comum/narracao";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { BemRecebido, PresenteNaFila, RegistroDeCustomizacao } from "../api/cuidadoDoBem";
import * as cuidadoApi from "../api/cuidadoDoBem";
import { TelaInicial } from "../inicio/TelaInicial";
import { ProvedorDeEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";
import { TelaDoCuidadoNoEncontro } from "./TelaDoCuidadoNoEncontro";

const REGISTRO_PENDENTE: RegistroDeCustomizacao = {
  id: "registro-1",
  entrega_de_recompensa_id: "entrega-kit",
  descricao: "Pintei o robô de azul e pus asas de EVA.",
  situacao: "pendente",
  tem_midia: true,
  tipo_do_arquivo: "image/png",
  motivo_do_julgamento: null,
};

const KIT_COM_PENDENTE: BemRecebido = {
  entrega_de_recompensa_id: "entrega-kit",
  tipo_de_recurso_nome: "Kit MDF do robô",
  trilha_nome: "Território Vivo",
  customizacao_aberta: true,
  ultimo_aprovado: {
    fonte: "comprovacao_do_pratico",
    id: "desbloqueio-1",
    descricao: null,
    tipo_do_arquivo: "image/png",
  },
  pendente: REGISTRO_PENDENTE,
  pontuado_na_aula: null,
};

const LIVRO: BemRecebido = {
  entrega_de_recompensa_id: "entrega-livro",
  tipo_de_recurso_nome: "Livro de apoio",
  trilha_nome: "Território Vivo",
  customizacao_aberta: false,
  ultimo_aprovado: null,
  pendente: null,
  pontuado_na_aula: null,
};

function presente(...bens: BemRecebido[]): PresenteNaFila {
  return { guerreiro_id: "guerreiro-1", guerreiro: { avatar: null, nick: "zeferina" }, bens };
}

beforeEach(() => {
  vi.spyOn(cuidadoApi, "lerMidiaDoRegistro").mockResolvedValue(new Blob(["agora"]));
  vi.spyOn(cuidadoApi, "lerMidiaDoUltimoAprovado").mockResolvedValue(new Blob(["antes"]));
  globalThis.URL.createObjectURL = vi.fn(() => "blob:local");
  globalThis.URL.revokeObjectURL = vi.fn();
});

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
  localStorage.clear();
});

function renderizarTela() {
  return render(
    <TelaDoCuidadoNoEncontro
      tokenDeTrabalho="token-de-trabalho"
      aulaId="aula-1"
      aoVoltar={vi.fn()}
    />,
  );
}

function renderizarTelaInicial(papelDeTrabalho: string) {
  return render(
    <ProvedorDeNarracao>
      <ProvedorDeEstadoDeRede>
        <ProvedorDeSessao chaveDeArmazenamento="teste:app-01:sessao-guerreiro">
          <TelaInicial
            tokenDeTrabalho="token-de-trabalho"
            personaIdDeTrabalho="persona-de-trabalho-1"
            papelDeTrabalho={papelDeTrabalho}
            aulaId="aula-1"
            aoVoltarAoInicio={vi.fn()}
            podeAbrirMomentoDeTroca={false}
            momentoDeTrocaAberto={false}
            abrindoMomentoDeTroca={false}
            erroDeAberturaDaTroca={null}
            aoAbrirMomentoDeTroca={vi.fn()}
            aoFecharMomentoDeTroca={vi.fn()}
            aoEncerrarSessaoDeTrabalho={vi.fn()}
          />
        </ProvedorDeSessao>
      </ProvedorDeEstadoDeRede>
    </ProvedorDeNarracao>,
  );
}

describe("o caminho do cuidado na tela inicial (RF-04-81)", () => {
  it("aparece ao Mestre, no grupo de quem opera, e leva à fila desta aula", async () => {
    const ler = vi.spyOn(cuidadoApi, "lerFilaDoCuidado").mockResolvedValue([presente(LIVRO)]);
    const usuario = userEvent.setup();
    renderizarTelaInicial("mestre");

    await screen.findByText(/o que você quer fazer/i);
    const grupo = screen.getByRole("group", { name: "Para quem opera o aparelho" });
    const cartao = screen.getByRole("button", { name: /customizações a julgar/i });
    expect(grupo).toContainElement(cartao);
    expect(cartao.querySelector("svg")).not.toBeNull();

    await usuario.click(cartao);
    expect(await screen.findByText(/zeferina/i)).toBeInTheDocument();
    expect(ler).toHaveBeenCalledWith("aula-1", "token-de-trabalho");
  });

  it("não aparece ao Admin", async () => {
    renderizarTelaInicial("admin");

    await screen.findByText(/o que você quer fazer/i);
    expect(
      screen.queryByRole("button", { name: /customizações a julgar/i }),
    ).not.toBeInTheDocument();
  });
});

describe("a fila do cuidado do encontro (RF-04-81 a RF-04-84)", () => {
  it("traz quem chegou, com os bens recebidos, a trilha e o tipo de recurso", async () => {
    vi.spyOn(cuidadoApi, "lerFilaDoCuidado").mockResolvedValue([
      presente(KIT_COM_PENDENTE, LIVRO),
    ]);
    renderizarTela();

    const bens = await screen.findByRole("list", { name: /bens recebidos por zeferina/i });
    expect(bens.textContent).toContain("Kit MDF do robô — Território Vivo");
    expect(bens.textContent).toContain("Livro de apoio — Território Vivo");
  });

  it("encontro sem ninguém na fila diz que não há, sem erro", async () => {
    vi.spyOn(cuidadoApi, "lerFilaDoCuidado").mockResolvedValue([]);
    renderizarTela();

    expect(await screen.findByText(/nada a julgar neste encontro/i)).toBeInTheDocument();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("mostra o registro novo e a descrição ao lado do último aprovado, pela rota do bem", async () => {
    vi.spyOn(cuidadoApi, "lerFilaDoCuidado").mockResolvedValue([presente(KIT_COM_PENDENTE)]);
    renderizarTela();

    const novo = await screen.findByRole("region", { name: "Registro novo" });
    const antes = screen.getByRole("region", { name: "Último registro aprovado" });
    expect(novo.textContent).toContain("Pintei o robô de azul");
    await waitFor(() => {
      expect(
        within(novo).getByRole("img", { name: /registro novo do kit/i }),
      ).toBeInTheDocument();
      expect(
        within(antes).getByRole("img", { name: /último registro aprovado do kit/i }),
      ).toBeInTheDocument();
    });
    expect(cuidadoApi.lerMidiaDoRegistro).toHaveBeenCalledWith(
      "registro-1",
      "token-de-trabalho",
    );
    expect(cuidadoApi.lerMidiaDoUltimoAprovado).toHaveBeenCalledWith(
      "entrega-kit",
      "token-de-trabalho",
    );
  });

  it("aprovar confirma o ponto extra e o acervo, e relê a fila", async () => {
    const ler = vi
      .spyOn(cuidadoApi, "lerFilaDoCuidado")
      .mockResolvedValueOnce([presente(KIT_COM_PENDENTE)])
      .mockResolvedValue([
        presente({ ...KIT_COM_PENDENTE, pontuado_na_aula: "customizacao" }),
      ]);
    const julgar = vi
      .spyOn(cuidadoApi, "julgarCustomizacao")
      .mockResolvedValue({ ...REGISTRO_PENDENTE, situacao: "aprovado" });
    const usuario = userEvent.setup();
    renderizarTela();

    await usuario.click(
      await screen.findByRole("button", { name: /aprovar a customização/i }),
    );

    expect(julgar).toHaveBeenCalledWith(
      "registro-1",
      { aula_id: "aula-1", aprovado: true },
      "token-de-trabalho",
    );
    expect(await screen.findByText(/1 ponto extra para zeferina/i)).toBeInTheDocument();
    expect(screen.getByText(/entrou no acervo/i)).toBeInTheDocument();
    expect(ler).toHaveBeenCalledTimes(2);
    expect(
      await screen.findByText(/já pontuou neste encontro pela customização/i),
    ).toBeInTheDocument();
  });

  it("reprovar sem motivo não envia, e com motivo envia", async () => {
    vi.spyOn(cuidadoApi, "lerFilaDoCuidado").mockResolvedValue([presente(KIT_COM_PENDENTE)]);
    const julgar = vi
      .spyOn(cuidadoApi, "julgarCustomizacao")
      .mockResolvedValue({ ...REGISTRO_PENDENTE, situacao: "reprovado" });
    const usuario = userEvent.setup();
    renderizarTela();

    await usuario.click(
      await screen.findByRole("button", { name: /reprovar a customização/i }),
    );
    await usuario.click(screen.getByRole("button", { name: /confirmar a reprovação/i }));
    expect(julgar).not.toHaveBeenCalled();
    expect(screen.getByLabelText(/motivo da reprovação/i)).toHaveAttribute(
      "aria-invalid",
      "true",
    );

    await usuario.type(
      screen.getByLabelText(/motivo da reprovação/i),
      "A foto mostra o rosto.",
    );
    await usuario.click(screen.getByRole("button", { name: /confirmar a reprovação/i }));
    expect(julgar).toHaveBeenCalledWith(
      "registro-1",
      { aula_id: "aula-1", aprovado: false, motivo: "A foto mostra o rosto." },
      "token-de-trabalho",
    );
  });

  it("a recusa do núcleo aparece como vem", async () => {
    vi.spyOn(cuidadoApi, "lerFilaDoCuidado").mockResolvedValue([presente(KIT_COM_PENDENTE)]);
    vi.spyOn(cuidadoApi, "julgarCustomizacao").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Este bem já pontuou neste encontro pela conservação.",
      }),
    );
    const usuario = userEvent.setup();
    renderizarTela();

    await usuario.click(
      await screen.findByRole("button", { name: /aprovar a customização/i }),
    );

    expect(
      await screen.findByText("Este bem já pontuou neste encontro pela conservação."),
    ).toBeInTheDocument();
  });

  it("a conservação validada confirma o ponto extra", async () => {
    vi.spyOn(cuidadoApi, "lerFilaDoCuidado").mockResolvedValue([presente(LIVRO)]);
    const validar = vi.spyOn(cuidadoApi, "validarConservacao").mockResolvedValue({});
    const usuario = userEvent.setup();
    renderizarTela();

    await usuario.click(await screen.findByRole("button", { name: /validar a conservação/i }));

    expect(validar).toHaveBeenCalledWith(
      "aula-1",
      { guerreiro_id: "guerreiro-1", entrega_de_recompensa_id: "entrega-livro" },
      "token-de-trabalho",
    );
    expect(
      await screen.findByText(/conservação validada: 1 ponto extra para zeferina/i),
    ).toBeInTheDocument();
  });

  it("o bem que já pontuou diz por qual caminho e não oferece nada", async () => {
    vi.spyOn(cuidadoApi, "lerFilaDoCuidado").mockResolvedValue([
      presente({ ...KIT_COM_PENDENTE, pontuado_na_aula: "conservacao" }),
    ]);
    renderizarTela();

    expect(
      await screen.findByText(/já pontuou neste encontro pela conservação/i),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /validar|aprovar|reprovar|registrar/i }),
    ).toBeNull();
  });

  it("no kit com pendente, oferece conservação ou customização", async () => {
    vi.spyOn(cuidadoApi, "lerFilaDoCuidado").mockResolvedValue([presente(KIT_COM_PENDENTE)]);
    renderizarTela();

    expect(
      await screen.findByRole("button", { name: /validar a conservação/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /aprovar a customização/i }),
    ).toBeInTheDocument();
  });

  it("bem com customização fechada não oferece captura nem julgamento", async () => {
    vi.spyOn(cuidadoApi, "lerFilaDoCuidado").mockResolvedValue([presente(LIVRO)]);
    renderizarTela();

    await screen.findByRole("button", { name: /validar a conservação/i });
    expect(screen.queryByRole("button", { name: /registrar a customização/i })).toBeNull();
    expect(screen.queryByRole("button", { name: /aprovar a customização/i })).toBeNull();
  });
});

describe("a captura na hora (RF-04-82)", () => {
  const KIT_SEM_PENDENTE: BemRecebido = { ...KIT_COM_PENDENTE, pendente: null };

  it("registra em nome da criança, envia a mídia e relê a fila", async () => {
    const ler = vi
      .spyOn(cuidadoApi, "lerFilaDoCuidado")
      .mockResolvedValue([presente(KIT_SEM_PENDENTE)]);
    const capturar = vi.spyOn(cuidadoApi, "capturarCustomizacao").mockResolvedValue({
      ...REGISTRO_PENDENTE,
      id: "registro-novo",
      tem_midia: false,
    });
    const enviar = vi
      .spyOn(cuidadoApi, "enviarMidiaDaCustomizacao")
      .mockResolvedValue({ ...REGISTRO_PENDENTE, id: "registro-novo" });
    const usuario = userEvent.setup();
    renderizarTela();

    await usuario.click(
      await screen.findByRole("button", { name: /registrar a customização agora/i }),
    );
    await usuario.click(screen.getByRole("button", { name: /^registrar a customização$/i }));
    expect(capturar).not.toHaveBeenCalled();
    expect(screen.getByText(/escreva ou fale a descrição/i)).toBeInTheDocument();

    await usuario.type(
      screen.getByLabelText(/descrição da customização/i),
      "Pus rodas novas.",
    );
    const foto = new File(["png"], "kit.png", { type: "image/png" });
    await usuario.upload(screen.getByLabelText(/foto ou vídeo do kit/i), foto);
    await usuario.click(screen.getByRole("button", { name: /^registrar a customização$/i }));

    await waitFor(() => expect(ler).toHaveBeenCalledTimes(2));
    expect(capturar).toHaveBeenCalledWith(
      "aula-1",
      {
        guerreiro_id: "guerreiro-1",
        entrega_de_recompensa_id: "entrega-kit",
        descricao: "Pus rodas novas.",
      },
      "token-de-trabalho",
    );
    expect(enviar).toHaveBeenCalledWith(
      "registro-novo",
      foto,
      "token-de-trabalho",
      expect.any(Function),
    );
  });

  it("envio interrompido retoma o mesmo registro, sem criar outro", async () => {
    vi.spyOn(cuidadoApi, "lerFilaDoCuidado").mockResolvedValue([presente(KIT_SEM_PENDENTE)]);
    const capturar = vi.spyOn(cuidadoApi, "capturarCustomizacao").mockResolvedValue({
      ...REGISTRO_PENDENTE,
      id: "registro-novo",
      tem_midia: false,
    });
    const enviar = vi
      .spyOn(cuidadoApi, "enviarMidiaDaCustomizacao")
      .mockRejectedValueOnce(new Error("rede"))
      .mockResolvedValue({ ...REGISTRO_PENDENTE, id: "registro-novo" });
    const usuario = userEvent.setup();
    renderizarTela();

    await usuario.click(
      await screen.findByRole("button", { name: /registrar a customização agora/i }),
    );
    await usuario.type(
      screen.getByLabelText(/descrição da customização/i),
      "Pus rodas novas.",
    );
    await usuario.upload(
      screen.getByLabelText(/foto ou vídeo do kit/i),
      new File(["png"], "kit.png", { type: "image/png" }),
    );
    await usuario.click(screen.getByRole("button", { name: /^registrar a customização$/i }));
    await usuario.click(
      await screen.findByRole("button", { name: /enviar a foto ou o vídeo/i }),
    );

    await waitFor(() => expect(enviar).toHaveBeenCalledTimes(2));
    expect(capturar).toHaveBeenCalledTimes(1);
    expect(enviar.mock.calls[1][0]).toBe("registro-novo");
  });
});
