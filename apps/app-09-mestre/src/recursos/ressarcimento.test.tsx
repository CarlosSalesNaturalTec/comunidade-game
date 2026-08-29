import { render, screen } from "@testing-library/react";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { AbsorcaoDoMestre, PontoDeApoioDaLista, TipoDeRecurso } from "./api";
import * as recursosApi from "./api";
import { TelaDeRecursos } from "./TelaDeRecursos";

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

const PONTO_DE_APOIO: PontoDeApoioDaLista = {
  id: "ponto-1",
  nome: "Ponto Central",
  comunidade_virtual_id: "comunidade-1",
};

const TIPO_LANCHE: TipoDeRecurso = {
  id: "tipo-lanche",
  nome: "Lanche",
  natureza: "consumivel",
  unidade: "unidade",
  exige_comprovante: false,
  valor_em_moedas: "2.00",
  vigencia_inicio: "2026-01-01",
};

const TIPO_OFICINA: TipoDeRecurso = {
  id: "tipo-oficina",
  nome: "Oficina",
  natureza: "servico",
  unidade: "hora",
  exige_comprovante: false,
  valor_em_moedas: "5.00",
  vigencia_inicio: "2026-01-01",
};

function absorcao(sobrescreve: Partial<AbsorcaoDoMestre> = {}): AbsorcaoDoMestre {
  return {
    id: "aporte-1",
    tipo_de_recurso_id: TIPO_LANCHE.id,
    quantidade: "10",
    ponto_de_apoio_id: PONTO_DE_APOIO.id,
    valor_em_moedas: "20.00",
    situacao_de_ressarcimento: "em_aberto",
    data_do_aporte: "2026-08-29",
    ...sobrescreve,
  };
}

function configurarLeituraBase() {
  vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([TIPO_LANCHE, TIPO_OFICINA]);
  vi.spyOn(recursosApi, "listarMeusPontosDeApoio").mockResolvedValue([PONTO_DE_APOIO]);
  vi.spyOn(recursosApi, "listarMinhasNecessidades").mockResolvedValue([]);
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("O Mestre acompanha a situação do ressarcimento do que absorveu (RF-09-59)", () => {
  it("apresenta cada aporte com tipo, quantidade, ponto de apoio, moedas, data e situação", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasAbsorcoes").mockResolvedValue([absorcao()]);

    render(<TelaDeRecursos />);

    const item = await screen.findByText("Lanche", {
      selector: ".minhas-absorcoes__tipo",
    });
    const linha = item.closest("li");
    expect(linha).not.toBeNull();
    expect(linha).toHaveTextContent("10");
    expect(linha).toHaveTextContent("Ponto Central");
    expect(linha).toHaveTextContent("20.00 moedas");
    expect(linha).toHaveTextContent(/ressarcimento em aberto/i);
  });

  it("não oferece ação de exigir, apressar, reordenar ou cancelar", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasAbsorcoes").mockResolvedValue([absorcao()]);

    render(<TelaDeRecursos />);

    await screen.findByText("Lanche", { selector: ".minhas-absorcoes__tipo" });
    expect(
      screen.queryByRole("button", { name: /exigir|apressar|reordenar|cancelar/i }),
    ).not.toBeInTheDocument();
  });

  it("a absorção de outra persona não é apresentada — o núcleo já recorta pela sessão", async () => {
    configurarSessao();
    configurarLeituraBase();
    // A rota `/v1/meus-aportes/ressarciveis` já é recortada pelo operador em
    // sessão; a aplicação apenas apresenta o que ela devolve, sem mesclar
    // nada de outra persona.
    vi.spyOn(recursosApi, "listarMinhasAbsorcoes").mockResolvedValue([absorcao()]);

    render(<TelaDeRecursos />);

    await screen.findByText("Lanche", { selector: ".minhas-absorcoes__tipo" });
    expect(screen.getAllByRole("listitem")).toHaveLength(1);
  });

  it("a absorção de serviço aparece como não se aplica, e não como pendência", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasAbsorcoes").mockResolvedValue([
      absorcao({
        tipo_de_recurso_id: TIPO_OFICINA.id,
        situacao_de_ressarcimento: "nao_se_aplica",
      }),
    ]);

    render(<TelaDeRecursos />);

    const item = await screen.findByText("Oficina", {
      selector: ".minhas-absorcoes__tipo",
    });
    const linha = item.closest("li");
    expect(linha).toHaveTextContent(/não se aplica/i);
    expect(linha).not.toHaveTextContent(/ressarcimento em aberto/i);
  });
});

describe("A App 09 não coleta nem exibe dado bancário (RF-09-60)", () => {
  it("nenhum campo de chave PIX, banco ou conta é apresentado em toda a área", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasAbsorcoes").mockResolvedValue([absorcao()]);

    render(<TelaDeRecursos />);

    await screen.findByText("Lanche", { selector: ".minhas-absorcoes__tipo" });
    expect(screen.queryByLabelText(/chave pix/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/banco/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/^conta$/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/pix:/i)).not.toBeInTheDocument();
  });

  it("declara que a plataforma não guarda dado bancário e que a chave PIX vai por e-mail ao Admin", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasAbsorcoes").mockResolvedValue([absorcao()]);

    render(<TelaDeRecursos />);

    expect(await screen.findByText(/não guarda dado bancário/i)).toBeInTheDocument();
    expect(screen.getByText(/chave pix é enviada por e-mail ao admin/i)).toBeInTheDocument();
    expect(screen.queryByText(/mailto:/i)).not.toBeInTheDocument();
  });

  it("a situação é lida da aplicação, sem que nenhum e-mail seja enviado por ela", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasAbsorcoes").mockResolvedValue([
      absorcao({ situacao_de_ressarcimento: "ressarcido" }),
    ]);

    render(<TelaDeRecursos />);

    const item = await screen.findByText("Lanche", {
      selector: ".minhas-absorcoes__tipo",
    });
    expect(item.closest("li")).toHaveTextContent(/ressarcido/i);
  });
});
