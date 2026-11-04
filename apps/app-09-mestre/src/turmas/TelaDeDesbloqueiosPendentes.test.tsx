import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { ComprovacaoEntregue, DesbloqueioPendente } from "../trilhas/api";
import * as trilhasApi from "../trilhas/api";
import { TelaDeDesbloqueiosPendentes } from "./TelaDeDesbloqueiosPendentes";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

import { useSessao } from "comum/autenticacao";

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
};

function configurarSessao() {
  vi.mocked(useSessao).mockReturnValue({
    sessao: SESSAO_DE_MESTRE,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    entrarComToken: vi.fn(),
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
    entrarComCredencial: vi.fn(),
    trocaDeSenhaPendente: false,
    trocandoSenha: false,
    erroDeTrocaDeSenha: null,
    trocarSenhaProvisoria: vi.fn(),
  });
}

function entregue(sobrescreve: Partial<ComprovacaoEntregue> = {}): ComprovacaoEntregue {
  return {
    forma: "texto",
    comprovacao: "Montei com sucata do pátio.",
    entrega_presencial: false,
    tem_arquivo: false,
    tipo_do_arquivo: null,
    ...sobrescreve,
  };
}

function pendente(sobrescreve: Partial<DesbloqueioPendente> = {}): DesbloqueioPendente {
  return {
    id: "desbloqueio-1",
    guerreiro_id: "guerreiro-1",
    guerreiro_nome: "Guerreira Ana",
    missao_id: "missao-1",
    missao_titulo: "Montar o robô",
    momento: "2026-08-27T10:00:00-03:00",
    criterio_de_aceite: "Não deve aparecer o rosto da criança, só a produção.",
    comprovacao_entregue: entregue(),
    ...sobrescreve,
  };
}

const JULGADO = {
  cumpriu: true,
  publicavel: true,
  motivo: null,
  julgado_em: "2026-11-04T10:00:00-03:00",
};

afterEach(() => {
  vi.restoreAllMocks();
});

describe("bancada dos desafios práticos a julgar (RF-09-26, RF-09-117)", () => {
  it("a lista traz o que espera julgamento", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);

    render(<TelaDeDesbloqueiosPendentes />);

    expect(await screen.findByText("Guerreira Ana")).toBeInTheDocument();
    expect(screen.getByText(/montar o robô/i)).toBeInTheDocument();
  });

  it("sem nenhuma declaração pendente, avisa sem erro", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([]);

    render(<TelaDeDesbloqueiosPendentes />);

    expect(await screen.findByText(/nenhum desafio prático/i)).toBeInTheDocument();
  });
});

describe("a produção entregue aparece na bancada (RF-09-132)", () => {
  it("a comprovação escrita aparece como texto, com o critério ao lado", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);

    render(<TelaDeDesbloqueiosPendentes />);

    expect(await screen.findByText(/montei com sucata do pátio/i)).toBeInTheDocument();
    expect(screen.getByText(/não deve aparecer o rosto da criança/i)).toBeInTheDocument();
  });

  it("a comprovação em imagem é exibida na própria bancada", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([
      pendente({
        comprovacao_entregue: entregue({
          forma: "imagem",
          comprovacao: null,
          tem_arquivo: true,
          tipo_do_arquivo: "image/png",
        }),
      }),
    ]);
    vi.spyOn(trilhasApi, "lerComprovacaoDoPratico").mockResolvedValue(
      new Blob(["bytes"], { type: "image/png" }),
    );

    render(<TelaDeDesbloqueiosPendentes />);

    expect(
      await screen.findByRole("img", { name: /produção entregue por Guerreira Ana/i }),
    ).toBeInTheDocument();
  });

  it("a entrega no encontro é dita como tal, nunca como entrega faltando", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([
      pendente({
        comprovacao_entregue: entregue({
          forma: "video",
          comprovacao: null,
          entrega_presencial: true,
        }),
      }),
    ]);

    render(<TelaDeDesbloqueiosPendentes />);

    expect(await screen.findByText(/vai mostrar a produção no encontro/i)).toBeInTheDocument();
    expect(screen.queryByText(/faltou|não entregou/i)).not.toBeInTheDocument();
  });

  it("a mídia que não carrega não impede julgar", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([
      pendente({
        comprovacao_entregue: entregue({
          forma: "imagem",
          comprovacao: null,
          tem_arquivo: true,
          tipo_do_arquivo: "image/png",
        }),
      }),
    ]);
    vi.spyOn(trilhasApi, "lerComprovacaoDoPratico").mockRejectedValue(new Error("caiu"));

    render(<TelaDeDesbloqueiosPendentes />);
    const usuario = userEvent.setup();

    expect(await screen.findByText(/não abriu. você ainda pode julgar/i)).toBeInTheDocument();
    // Os controles seguem disponíveis: a mídia que não abre não trava o
    // julgamento, e marcar publicável basta para enviá-lo.
    expect(screen.getByLabelText(/cumpriu o desafio/i)).toBeEnabled();
    expect(screen.getByLabelText(/pode ir à vitrine/i)).toBeEnabled();
    await usuario.click(screen.getByLabelText(/pode ir à vitrine/i));
    expect(screen.getByRole("button", { name: /^julgar$/i })).toBeEnabled();
  });
});

describe("os dois vereditos e o motivo (RF-09-133, RF-09-134, RN-09-52, RN-09-53)", () => {
  it("a tela diz o que cada veredito faz", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);

    render(<TelaDeDesbloqueiosPendentes />);

    expect(await screen.findByText(/credita 5\s*pontos/i)).toBeInTheDocument();
    expect(screen.getByText(/portfólio público/i)).toBeInTheDocument();
  });

  it("os dois vereditos vão num ato só e a pendência sai da lista", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);
    const julgarEspiado = vi
      .spyOn(trilhasApi, "julgarDesafioPratico")
      .mockResolvedValue(JULGADO);

    render(<TelaDeDesbloqueiosPendentes />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByLabelText(/pode ir à vitrine/i));
    await usuario.click(screen.getByRole("button", { name: /^julgar$/i }));

    await waitFor(() =>
      expect(julgarEspiado).toHaveBeenCalledWith(
        "missao-1",
        "guerreiro-1",
        { cumpriu: true, publicavel: true, motivo: null },
        "token-do-mestre",
      ),
    );
    expect(screen.queryByText("Guerreira Ana")).not.toBeInTheDocument();
  });

  it("publicável fica indisponível no que o Mestre marca como não cumprido", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);

    render(<TelaDeDesbloqueiosPendentes />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByLabelText(/cumpriu o desafio/i));

    expect(screen.getByLabelText(/pode ir à vitrine/i)).toBeDisabled();
    expect(screen.getByText(/só a entrega que você julgar cumprida/i)).toBeInTheDocument();
  });

  it("publicável fica indisponível na entrega presencial, que não tem o que publicar", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([
      pendente({
        comprovacao_entregue: entregue({
          forma: "video",
          comprovacao: null,
          entrega_presencial: true,
        }),
      }),
    ]);

    render(<TelaDeDesbloqueiosPendentes />);

    expect(await screen.findByLabelText(/pode ir à vitrine/i)).toBeDisabled();
    expect(screen.getByText(/não há comprovação a publicar/i)).toBeInTheDocument();
  });

  it("o motivo é exigido antes do toque quando o Mestre recusa", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);

    render(<TelaDeDesbloqueiosPendentes />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByLabelText(/cumpriu o desafio/i));

    expect(screen.getByRole("button", { name: /^julgar$/i })).toBeDisabled();
    expect(screen.getByText(/escreva o motivo/i)).toBeInTheDocument();

    await usuario.type(
      screen.getByLabelText(/motivo, em linguagem simples/i),
      "Faltou mostrar a peça montada.",
    );

    expect(screen.getByRole("button", { name: /^julgar$/i })).toBeEnabled();
  });

  it("o motivo é exigido para cumprir sem publicar, que também é um não", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);

    render(<TelaDeDesbloqueiosPendentes />);

    // Nasce com cumpriu marcado e publicável desmarcado, e há comprovação a
    // publicar: é veredito negativo, e o motivo falta.
    expect(await screen.findByRole("button", { name: /^julgar$/i })).toBeDisabled();
    expect(screen.getByText(/escreva o motivo/i)).toBeInTheDocument();
  });

  it("cumpriu e publicável dispensa o motivo", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);

    render(<TelaDeDesbloqueiosPendentes />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByLabelText(/pode ir à vitrine/i));

    expect(screen.getByRole("button", { name: /^julgar$/i })).toBeEnabled();
    expect(screen.queryByText(/escreva o motivo/i)).not.toBeInTheDocument();
  });

  it("a entrega presencial cumprida dispensa o motivo", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([
      pendente({
        comprovacao_entregue: entregue({
          forma: "video",
          comprovacao: null,
          entrega_presencial: true,
        }),
      }),
    ]);

    render(<TelaDeDesbloqueiosPendentes />);

    expect(await screen.findByRole("button", { name: /^julgar$/i })).toBeEnabled();
  });

  it("a tela diz que não passar não elimina", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);

    render(<TelaDeDesbloqueiosPendentes />);

    expect(await screen.findByText(/não passar não o elimina/i)).toBeInTheDocument();
  });

  it("a recusa do núcleo chega com o motivo, sem limpar o que o Mestre escreveu", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);
    vi.spyOn(trilhasApi, "julgarDesafioPratico").mockRejectedValue(
      new Error("Esta declaração já foi julgada."),
    );

    render(<TelaDeDesbloqueiosPendentes />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByLabelText(/cumpriu o desafio/i));
    await usuario.type(
      screen.getByLabelText(/motivo, em linguagem simples/i),
      "Faltou a peça montada.",
    );
    await usuario.click(screen.getByRole("button", { name: /^julgar$/i }));

    expect(await screen.findByText(/esta declaração já foi julgada/i)).toBeInTheDocument();
    // O veredito marcado e o texto escrito permanecem.
    expect(screen.getByLabelText(/cumpriu o desafio/i)).not.toBeChecked();
    expect(screen.getByLabelText(/motivo, em linguagem simples/i)).toHaveValue(
      "Faltou a peça montada.",
    );
    expect(screen.getByText("Guerreira Ana")).toBeInTheDocument();
  });
});
