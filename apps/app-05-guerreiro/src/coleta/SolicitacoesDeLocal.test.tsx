import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as coletaApi from "../api/coleta";
import { SolicitacoesDeLocal } from "./SolicitacoesDeLocal";

const CHAVE_DE_SESSAO = "app-05:teste-solicitacoes-de-local";

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
        <SolicitacoesDeLocal contexto={null} />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("minhas solicitações de local", () => {
  it("mostra a situação e o motivo da recusa", async () => {
    vi.spyOn(coletaApi, "listarMinhasSolicitacoes").mockResolvedValue({
      itens: [
        {
          id: "solicitacao-1",
          solicitante_id: "guerreiro-1",
          comunidade_virtual_id: "comunidade-1",
          desafio_de_coleta_id: "desafio-1",
          nivel_pretendido: "bairro",
          rotulo: "Bairro Novo",
          justificativa: "Falta um local aqui.",
          situacao: "recusada",
          avaliador_id: "mestre-1",
          motivo_da_recusa: "Já existe local equivalente na hierarquia.",
          local_criado_id: null,
          avaliado_em: "2026-08-10T12:00:00Z",
          registrado_em: "2026-08-01T12:00:00Z",
        },
      ],
      proximo_cursor: null,
    });

    await renderizar();

    expect(await screen.findByText(/bairro novo/i)).toBeInTheDocument();
    expect(screen.getByText(/^recusada/i)).toBeInTheDocument();
    expect(screen.getByText(/já existe local equivalente na hierarquia/i)).toBeInTheDocument();
  });
});
