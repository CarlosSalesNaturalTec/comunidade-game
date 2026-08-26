import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as coletaApi from "../api/coleta";
import { AbrirSerie } from "./AbrirSerie";

const CHAVE_DE_SESSAO = "app-05:teste-abrir-serie";

async function renderizar(aoAbrir: () => void = () => {}) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <AbrirSerie aoAbrir={aoAbrir} aoSolicitarLocalFaltante={() => {}} />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

const DESAFIO_DISPONIVEL: coletaApi.DesafioDisponivel = {
  id: "desafio-disponivel",
  tipo_de_coleta: { nome: "Temperatura da rua", forma_de_registro: "numero", unidade: "°C" },
  cadencia: "semanal",
  vigencia_inicio: "2026-01-01T00:00:00Z",
  vigencia_fim: "2026-12-31T00:00:00Z",
  granularidade_exigida: "rua",
  missao_id: "missao-1",
  trilha_id: "trilha-1",
  ja_assumido: false,
  comunidade_virtual_id: "comunidade-1",
};

const DESAFIO_JA_ASSUMIDO: coletaApi.DesafioDisponivel = {
  ...DESAFIO_DISPONIVEL,
  id: "desafio-ja-assumido",
  tipo_de_coleta: { nome: "Já tenho série nesse", forma_de_registro: "numero", unidade: null },
  ja_assumido: true,
};

const LOCAL_DA_RUA: coletaApi.Local = {
  id: "local-1",
  comunidade_virtual_id: "comunidade-1",
  nivel: "rua",
  rotulo: "Rua das Flores",
  local_pai_id: null,
};

describe("abertura de série de coleta", () => {
  it("não oferece um desafio que o núcleo já recusaria por já ter sido assumido", async () => {
    vi.spyOn(coletaApi, "listarDesafiosDisponiveis").mockResolvedValue({
      itens: [DESAFIO_DISPONIVEL, DESAFIO_JA_ASSUMIDO],
      proximo_cursor: null,
    });
    vi.spyOn(coletaApi, "listarLocaisDaComunidade").mockResolvedValue({
      itens: [LOCAL_DA_RUA],
      proximo_cursor: null,
    });

    await renderizar();

    expect(await screen.findByText(/temperatura da rua/i)).toBeInTheDocument();
    expect(screen.queryByText(/já tenho série nesse/i)).not.toBeInTheDocument();
  });

  it("abre a série sobre o desafio e o local escolhidos", async () => {
    const aoAbrir = vi.fn();
    vi.spyOn(coletaApi, "listarDesafiosDisponiveis").mockResolvedValue({
      itens: [DESAFIO_DISPONIVEL],
      proximo_cursor: null,
    });
    vi.spyOn(coletaApi, "listarLocaisDaComunidade").mockResolvedValue({
      itens: [LOCAL_DA_RUA],
      proximo_cursor: null,
    });
    const abrirSerie = vi.spyOn(coletaApi, "abrirSerie").mockResolvedValue({
      id: "serie-nova",
      desafio_de_coleta_id: DESAFIO_DISPONIVEL.id,
      coletor_id: "guerreiro-1",
      local_id: LOCAL_DA_RUA.id,
      cadencia: "semanal",
      estado: "ativa",
      aberta_em: new Date().toISOString(),
      ultima_medicao_valida_em: null,
    });

    await renderizar(aoAbrir);
    const usuario = userEvent.setup();
    await usuario.selectOptions(
      await screen.findByLabelText(/qual desafio/i),
      DESAFIO_DISPONIVEL.id,
    );
    await usuario.selectOptions(
      await screen.findByLabelText(/em qual local/i),
      LOCAL_DA_RUA.id,
    );
    await usuario.click(screen.getByRole("button", { name: /abrir série/i }));

    await vi.waitFor(() =>
      expect(abrirSerie).toHaveBeenCalledWith(
        { desafioDeColetaId: DESAFIO_DISPONIVEL.id, localId: LOCAL_DA_RUA.id },
        "token-do-guerreiro",
      ),
    );
    expect(aoAbrir).toHaveBeenCalled();
  });

  it("a recusa da abertura é explicada em linguagem simples, sem termo técnico", async () => {
    vi.spyOn(coletaApi, "listarDesafiosDisponiveis").mockResolvedValue({
      itens: [DESAFIO_DISPONIVEL],
      proximo_cursor: null,
    });
    vi.spyOn(coletaApi, "listarLocaisDaComunidade").mockResolvedValue({
      itens: [LOCAL_DA_RUA],
      proximo_cursor: null,
    });
    vi.spyOn(coletaApi, "abrirSerie").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem:
          "A granularidade exigida pelo desafio é mais fina que o teto da sua Comunidade Virtual.",
        campo: "desafio_de_coleta_id",
      }),
    );

    await renderizar();
    const usuario = userEvent.setup();
    await usuario.selectOptions(
      await screen.findByLabelText(/qual desafio/i),
      DESAFIO_DISPONIVEL.id,
    );
    await usuario.selectOptions(
      await screen.findByLabelText(/em qual local/i),
      LOCAL_DA_RUA.id,
    );
    await usuario.click(screen.getByRole("button", { name: /abrir série/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa.textContent).not.toMatch(
      /granularidade|comunidade virtual|erro_de_validacao/i,
    );
    expect(recusa).toHaveTextContent(/não foi possível abrir/i);
  });
});
