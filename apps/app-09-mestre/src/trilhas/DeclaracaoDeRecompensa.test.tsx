import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { RecompensaDeMarco } from "../recompensas/api";
import * as recompensasApi from "../recompensas/api";
import type { TipoDeRecurso } from "../recursos/api";
import type { MissaoDaTrilha } from "./api";
import { DeclaracaoDeRecompensa } from "./DeclaracaoDeRecompensa";

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
};

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

import { useSessao } from "comum/autenticacao";

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

function missao(): MissaoDaTrilha {
  return {
    id: "missao-1",
    trilha_id: "trilha-1",
    titulo: "Missão marco",
    posicao: 1,
    nivel_de_dificuldade: 1,
    obrigatoria: true,
    e_sondagem: false,
    etapa_do_ciclo: "marcos",
    cadencia_de_retomada: null,
    atividades: [],
    etiquetas_ods: [],
  };
}

function tipoDeRecurso(): TipoDeRecurso {
  return {
    id: "tipo-1",
    nome: "Camisa",
    natureza: "duravel",
    unidade: "unidade",
    exige_comprovante: false,
    valor_em_moedas: "10.00",
    vigencia_inicio: "2026-01-01",
  };
}

function recompensa(sobrescreve: Partial<RecompensaDeMarco> = {}): RecompensaDeMarco {
  return {
    id: "recompensa-1",
    trilha_id: "trilha-1",
    missao_id: "missao-1",
    tipo_de_recurso_id: "tipo-1",
    quantidade: "30",
    autor_id: "mestre-1",
    registrado_em: "2026-08-29T10:00:00-03:00",
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("Declaração da recompensa de marco", () => {
  it("declara a recompensa do desbloqueio com tipo e quantidade", async () => {
    configurarSessao();
    vi.spyOn(recompensasApi, "declararRecompensaDeMarco").mockResolvedValue(recompensa());
    const aoDeclarar = vi.fn();

    render(
      <DeclaracaoDeRecompensa
        idDaTrilha="trilha-1"
        missao={missao()}
        tiposDeRecurso={[tipoDeRecurso()]}
        recompensas={[]}
        onDeclarada={aoDeclarar}
      />,
    );
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /^declarar recompensa$/i }));
    await usuario.selectOptions(screen.getByLabelText(/tipo de recurso/i), "tipo-1");
    await usuario.type(screen.getByLabelText(/quantidade/i), "30");
    await usuario.click(screen.getByRole("button", { name: /^declarar recompensa$/i }));

    await waitFor(() =>
      expect(recompensasApi.declararRecompensaDeMarco).toHaveBeenCalledWith(
        "trilha-1",
        { missao_id: "missao-1", tipo_de_recurso_id: "tipo-1", quantidade: "30" },
        "token-do-mestre",
      ),
    );
    expect(aoDeclarar).toHaveBeenCalledWith(recompensa());
  });

  it("a tela não oferece campo de preço, pontos nem contrapartida", () => {
    configurarSessao();

    render(
      <DeclaracaoDeRecompensa
        idDaTrilha="trilha-1"
        missao={missao()}
        tiposDeRecurso={[tipoDeRecurso()]}
        recompensas={[]}
        onDeclarada={vi.fn()}
      />,
    );

    expect(screen.queryByLabelText(/preço/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/pontos/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/lastro/i)).not.toBeInTheDocument();
  });

  it("apresenta a recompensa já declarada junto da missão", () => {
    configurarSessao();

    render(
      <DeclaracaoDeRecompensa
        idDaTrilha="trilha-1"
        missao={missao()}
        tiposDeRecurso={[tipoDeRecurso()]}
        recompensas={[recompensa()]}
        onDeclarada={vi.fn()}
      />,
    );

    expect(screen.getByText(/30 camisa/i)).toBeInTheDocument();
  });
});
