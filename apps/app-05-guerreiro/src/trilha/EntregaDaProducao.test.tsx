import { act, fireEvent, render, screen } from "@testing-library/react";
import { ErroDaApi } from "comum/api";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { EntregaDaProducao } from "./EntregaDaProducao";

const CHAVE_DE_SESSAO = "app-05:teste-entrega-da-producao";

const ATIVIDADES: trilhaApi.AtividadeDaMissaoPublica[] = [
  { id: "atividade-1", titulo: "Atividade Única", producao_esperada: "Um texto." },
];

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
        <EntregaDaProducao missaoId="missao-1" atividades={ATIVIDADES} />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("entrega da produção", () => {
  it("as três formas aparecem lado a lado com o caminho do encontro", async () => {
    await renderizar();

    expect(screen.getByRole("button", { name: "Escrever" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Gravar a fala" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Fotografar" })).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Entregar ao Mestre no encontro" }),
    ).toBeInTheDocument();
  });

  it("avisa o descarte antes de enviar em áudio ou foto", async () => {
    await renderizar();

    fireEvent.click(screen.getByRole("button", { name: "Gravar a fala" }));

    expect(
      screen.getByText(/é descartad[ao] na leitura|é usado só para ler/i),
    ).toBeInTheDocument();
  });

  it("quem escolhe o encontro não perde a missão e não vê formulário", async () => {
    await renderizar();

    fireEvent.click(screen.getByRole("button", { name: "Entregar ao Mestre no encontro" }));

    expect(screen.getByText(/você não perde a missão/i)).toBeInTheDocument();
    expect(screen.queryByRole("form")).not.toBeInTheDocument();
  });

  it("entrega em texto envia a atividade declarada e mostra a devolutiva sem ponto", async () => {
    const entregar = vi.spyOn(trilhaApi, "entregarProducaoIndividual").mockResolvedValue({
      id: "producao-1",
      equipe_id: null,
      guerreiro_id: "guerreiro-1",
      missao_id: "missao-1",
      atividade_id: "atividade-1",
      forma: "texto",
      transcricao: "Minha produção.",
      devolutiva: "Você foi bem em X, tente Y a seguir.",
      registrado_em: "2026-01-01T00:00:00Z",
    });

    await renderizar();

    fireEvent.change(screen.getByLabelText(/sua produção/i), {
      target: { value: "Minha produção." },
    });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Entregar" }));
    });

    expect(entregar).toHaveBeenCalledWith(
      "missao-1",
      {
        atividadeId: "atividade-1",
        forma: "texto",
        texto: "Minha produção.",
        arquivo: undefined,
      },
      "token-do-guerreiro",
    );
    expect(screen.getByText(/você foi bem em x/i)).toBeInTheDocument();
    expect(screen.getByText(/não vale ponto/i)).toBeInTheDocument();
    expect(screen.queryByText(/nível|badge/i)).not.toBeInTheDocument();
  });

  it("devolutiva que não vem confirma que a produção foi guardada", async () => {
    vi.spyOn(trilhaApi, "entregarProducaoIndividual").mockResolvedValue({
      id: "producao-1",
      equipe_id: null,
      guerreiro_id: "guerreiro-1",
      missao_id: "missao-1",
      atividade_id: "atividade-1",
      forma: "texto",
      transcricao: "Minha produção.",
      devolutiva: null,
      registrado_em: "2026-01-01T00:00:00Z",
    });

    await renderizar();

    fireEvent.change(screen.getByLabelText(/sua produção/i), {
      target: { value: "Minha produção." },
    });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Entregar" }));
    });

    expect(screen.getByText(/foi guardada/i)).toBeInTheDocument();
    expect(screen.getByText(/retorno não veio agora/i)).toBeInTheDocument();
  });

  it("leitura indisponível mostra mensagem para tentar de novo", async () => {
    vi.spyOn(trilhaApi, "entregarProducaoIndividual").mockRejectedValue(
      new ErroDaApi(503, {
        codigo: "leitura_da_producao_indisponivel",
        mensagem: "A leitura da produção não veio agora.",
      }),
    );

    await renderizar();

    fireEvent.click(screen.getByRole("button", { name: "Fotografar" }));
    const arquivo = new File(["foto"], "foto.jpg", { type: "image/jpeg" });
    fireEvent.change(screen.getByLabelText(/^foto$/i), { target: { files: [arquivo] } });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Entregar" }));
    });

    expect(screen.getByText(/tente enviar de novo/i)).toBeInTheDocument();
  });
});
