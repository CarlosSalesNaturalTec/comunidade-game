import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import * as pontuacao from "comum/pontuacao";
import { describe, expect, it, vi } from "vitest";
import type { GuerreiroDaLista } from "./api";
import { FichaDoGuerreiro } from "./FichaDoGuerreiro";
import { ListaDeGuerreiros } from "./ListaDeGuerreiros";

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

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
  persona_id: "admin-1",
};

const GUERREIRO: GuerreiroDaLista = {
  id: "guerreiro-1",
  nome: "Zeferina",
  nascimento: "2015-03-20",
  nick: "ZeferinaGuerreira",
  avatar: "avatar-opaco",
  comunidade_virtual_id: null,
  vinculo_iniciado_em: null,
};

describe("ficha do Guerreiro(a) na gestão (RF-02-116)", () => {
  it("a lista oferece a ficha de cada Guerreiro(a)", async () => {
    const onAbrirFicha = vi.fn();
    render(
      <ListaDeGuerreiros
        guerreiros={[GUERREIRO]}
        comunidades={[]}
        onEditar={vi.fn()}
        onAbrirFicha={onAbrirFicha}
      />,
    );

    await userEvent.click(screen.getByRole("button", { name: "Ficha" }));
    expect(onAbrirFicha).toHaveBeenCalledWith(GUERREIRO);
  });

  it("a ficha mostra troca e estorno com valor negativo na conta que se moveu", async () => {
    vi.mocked(useSessao).mockReturnValue({
      sessao: SESSAO_DE_ADMIN,
      tratarRecusaDeSessao: vi.fn(),
    } as unknown as ReturnType<typeof useSessao>);
    vi.mocked(pontuacao.lerHistoricoDePontuacaoDoGuerreiro).mockResolvedValue({
      saldos: { regular: [], extra: { acumulado: 25, saldo_disponivel: 0 } },
      itens: [
        {
          id: "l2",
          registrado_em: "2026-11-11T13:00:00Z",
          conta: "extra",
          origem: "estorno_de_presenca",
          valor: -2,
          valor_no_acumulado: -5,
          trilha_id: null,
          poder_id: null,
          nome_da_trilha_ou_poder: null,
          detalhe: null,
          motivo: null,
        },
        {
          id: "l1",
          registrado_em: "2026-11-10T13:00:00Z",
          conta: "extra",
          origem: "troca",
          valor: -25,
          valor_no_acumulado: 0,
          trilha_id: null,
          poder_id: null,
          nome_da_trilha_ou_poder: null,
          detalhe: "Camiseta",
          motivo: null,
        },
      ],
      proximo_cursor: null,
    });

    render(<FichaDoGuerreiro guerreiro={GUERREIRO} onVoltar={vi.fn()} />);

    expect(await screen.findByText("Presença anulada")).toBeInTheDocument();
    expect(screen.getByText(/-5 no acumulado, -2 no saldo disponível/)).toBeInTheDocument();
    expect(screen.getByText(/-25 no saldo disponível/)).toBeInTheDocument();
    expect(pontuacao.lerHistoricoDePontuacaoDoGuerreiro).toHaveBeenCalledWith(
      "token-do-admin",
      "guerreiro-1",
      null,
    );
  });
});
