import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { Equipe } from "../api/equipes";
import * as equipesApi from "../api/equipes";
import { TelaDeEquipes } from "./TelaDeEquipes";

function equipe(sobrescreve: Partial<Equipe> = {}): Equipe {
  return {
    id: "equipe-1",
    aula_id: "aula-1",
    integrantes: [{ avatar: "avatar-1", nick: "zeferina", papel: null }],
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("equipes da aula", () => {
  it("carrega e mostra a lista das equipes da aula, só avatar e nick", async () => {
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [equipe()],
      proximo_cursor: null,
    });

    render(<TelaDeEquipes aulaId="aula-1" token="token-guerreiro" aoVoltar={vi.fn()} />);

    expect(await screen.findByText("zeferina")).toBeInTheDocument();
    expect(equipesApi.listarEquipesDaAula).toHaveBeenCalledWith("aula-1", "token-guerreiro");
  });

  it("aula sem equipe mostra o estado vazio", async () => {
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeEquipes aulaId="aula-1" token="token-guerreiro" aoVoltar={vi.fn()} />);

    expect(await screen.findByText(/nenhuma equipe formada/i)).toBeInTheDocument();
  });

  it("cria a equipe e ela aparece na lista, com o próprio criador dentro", async () => {
    vi.spyOn(equipesApi, "listarEquipesDaAula")
      .mockResolvedValueOnce({ itens: [], proximo_cursor: null })
      .mockResolvedValueOnce({ itens: [equipe()], proximo_cursor: null });
    vi.spyOn(equipesApi, "criarEquipe").mockResolvedValue(equipe());

    render(<TelaDeEquipes aulaId="aula-1" token="token-guerreiro" aoVoltar={vi.fn()} />);
    await screen.findByText(/nenhuma equipe formada/i);

    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /criar equipe/i }));

    expect(await screen.findByText("zeferina")).toBeInTheDocument();
    expect(equipesApi.criarEquipe).toHaveBeenCalledWith("aula-1", null, "token-guerreiro");
  });

  it("o papel declarado é enviado ao criar e ao entrar", async () => {
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(equipesApi, "criarEquipe").mockResolvedValue(equipe());

    render(<TelaDeEquipes aulaId="aula-1" token="token-guerreiro" aoVoltar={vi.fn()} />);
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/seu papel/i), "quem constrói");
    await usuario.click(screen.getByRole("button", { name: /criar equipe/i }));

    await waitFor(() =>
      expect(equipesApi.criarEquipe).toHaveBeenCalledWith(
        "aula-1",
        "quem constrói",
        "token-guerreiro",
      ),
    );
  });

  it("entra numa equipe existente, e o botão vira sair", async () => {
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [equipe()],
      proximo_cursor: null,
    });
    vi.spyOn(equipesApi, "entrarNaEquipe").mockResolvedValue(
      equipe({
        integrantes: [
          { avatar: "avatar-1", nick: "zeferina", papel: null },
          { avatar: "avatar-2", nick: "quem-entrou", papel: null },
        ],
      }),
    );

    render(<TelaDeEquipes aulaId="aula-1" token="token-guerreiro" aoVoltar={vi.fn()} />);
    await screen.findByText("zeferina");

    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /entrar nesta equipe/i }));

    expect(
      await screen.findByRole("button", { name: /sair desta equipe/i }),
    ).toBeInTheDocument();
    expect(equipesApi.entrarNaEquipe).toHaveBeenCalledWith(
      "equipe-1",
      null,
      "token-guerreiro",
    );
  });

  it("sai da equipe por conta própria", async () => {
    vi.spyOn(equipesApi, "listarEquipesDaAula")
      .mockResolvedValueOnce({ itens: [equipe()], proximo_cursor: null })
      .mockResolvedValueOnce({ itens: [equipe()], proximo_cursor: null });
    vi.spyOn(equipesApi, "entrarNaEquipe").mockResolvedValue(equipe());
    vi.spyOn(equipesApi, "sairDaEquipe").mockResolvedValue(undefined);

    render(<TelaDeEquipes aulaId="aula-1" token="token-guerreiro" aoVoltar={vi.fn()} />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /entrar nesta equipe/i }));
    await usuario.click(await screen.findByRole("button", { name: /sair desta equipe/i }));

    await waitFor(() =>
      expect(equipesApi.sairDaEquipe).toHaveBeenCalledWith("equipe-1", "token-guerreiro"),
    );
    expect(
      await screen.findByRole("button", { name: /entrar nesta equipe/i }),
    ).toBeInTheDocument();
  });

  it("a recusa do sexto integrante aparece em linguagem simples", async () => {
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [equipe()],
      proximo_cursor: null,
    });
    vi.spyOn(equipesApi, "entrarNaEquipe").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Esta equipe já tem os cinco integrantes permitidos.",
      }),
    );

    render(<TelaDeEquipes aulaId="aula-1" token="token-guerreiro" aoVoltar={vi.fn()} />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /entrar nesta equipe/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/cinco integrantes/i);
  });

  it("nenhum dado além de avatar e nick aparece por integrante", async () => {
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [equipe()],
      proximo_cursor: null,
    });

    render(<TelaDeEquipes aulaId="aula-1" token="token-guerreiro" aoVoltar={vi.fn()} />);

    const item = await screen.findByText("zeferina");
    const linha = item.closest("li");
    expect(linha).not.toBeNull();
    // biome-ignore lint/style/noNonNullAssertion: verificado na linha acima
    expect(within(linha!).queryByText(/198|nascimento/i)).not.toBeInTheDocument();
  });

  it("voltar ao início aciona aoVoltar", async () => {
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const aoVoltar = vi.fn();

    render(<TelaDeEquipes aulaId="aula-1" token="token-guerreiro" aoVoltar={aoVoltar} />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /voltar ao início/i }));

    expect(aoVoltar).toHaveBeenCalled();
  });
});
