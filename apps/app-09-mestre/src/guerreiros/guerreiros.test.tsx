import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import * as pontuacao from "comum/pontuacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as responsaveisApi from "../responsaveis/api";
import { TelaDeGuerreiros } from "./TelaDeGuerreiros";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return { ...real, useSessao: vi.fn() };
});

vi.mock("comum/pontuacao", async () => {
  const real = await vi.importActual<typeof import("comum/pontuacao")>("comum/pontuacao");
  return { ...real, lerHistoricoDePontuacaoDoGuerreiro: vi.fn() };
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

const GUERREIRA = { id: "guerreiro-1", nick: "guerreira-teste", avatar: "avatar-1" };

afterEach(() => {
  vi.restoreAllMocks();
});

describe("TelaDeGuerreiros (RF-09-143, RF-09-144)", () => {
  it("lista por nick a comunidade do vínculo e abre a ficha com o histórico", async () => {
    configurarSessao();
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: [GUERREIRA],
      proximo_cursor: null,
    });
    vi.mocked(pontuacao.lerHistoricoDePontuacaoDoGuerreiro).mockResolvedValue({
      saldos: {
        regular: [{ trilha_id: "t1", poder_id: null, nome: "Robótica", total: 15 }],
        extra: { acumulado: 30, saldo_disponivel: 5 },
      },
      itens: [
        {
          id: "l1",
          registrado_em: "2026-11-10T13:00:00Z",
          conta: "regular",
          origem: "ocorrencia_de_conduta",
          valor: -5,
          valor_no_acumulado: null,
          trilha_id: "t1",
          poder_id: null,
          nome_da_trilha_ou_poder: "Robótica",
          detalhe: null,
          motivo: "Desrespeitou um colega.",
        },
      ],
      proximo_cursor: null,
    });
    render(<TelaDeGuerreiros />);

    await userEvent.click(
      await screen.findByRole("button", { name: "Abrir a ficha de guerreira-teste" }),
    );

    expect(await screen.findByText("Saldo disponível: 5")).toBeInTheDocument();
    expect(screen.getByText("Motivo: Desrespeitou um colega.")).toBeInTheDocument();
    expect(pontuacao.lerHistoricoDePontuacaoDoGuerreiro).toHaveBeenCalledWith(
      "token-do-mestre",
      "guerreiro-1",
      null,
    );
  });

  it("diz quando não há Guerreiro(a) na comunidade do vínculo", async () => {
    configurarSessao();
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    render(<TelaDeGuerreiros />);

    expect(
      await screen.findByText("Nenhum Guerreiro(a) ativo nas comunidades do seu vínculo."),
    ).toBeInTheDocument();
  });

  it("mostra a recusa do núcleo na ficha", async () => {
    configurarSessao();
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: [GUERREIRA],
      proximo_cursor: null,
    });
    vi.mocked(pontuacao.lerHistoricoDePontuacaoDoGuerreiro).mockRejectedValue(
      new ErroDaApi(403, {
        codigo: "permissao_negada",
        mensagem: "O Mestre lê só o histórico de Guerreiro(a) da comunidade do seu vínculo.",
      }),
    );
    render(<TelaDeGuerreiros />);

    await userEvent.click(
      await screen.findByRole("button", { name: "Abrir a ficha de guerreira-teste" }),
    );

    expect(
      await screen.findByText(
        "O Mestre lê só o histórico de Guerreiro(a) da comunidade do seu vínculo.",
      ),
    ).toBeInTheDocument();
  });
});
