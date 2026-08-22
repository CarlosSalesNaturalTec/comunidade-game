import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ErroDaApi } from "../api/cliente";
import * as aportesApi from "../aportes/api";
import type { SessaoAberta } from "../autenticacao/ContextoDeSessao";
import * as comunidadesApi from "../comunidades/api";
import * as personasApi from "../personas/api";
import * as pontosDeApoioApi from "../pontos-de-apoio/api";
import * as recursosApi from "../recursos/api";
import type { SolicitacaoDeParticipacao } from "./api";
import * as filasApi from "./api";
import { TelaDeFilas } from "./TelaDeFilas";

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
};

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
};

const COMUNIDADE = {
  id: "comunidade-1",
  nome: "Comunidade de Teste",
  localizacao: "Bairro de teste",
  series_abertas: null,
  series_ativas: null,
  registros_validos: null,
  continuidade: null,
};

const PONTO_DE_APOIO = {
  id: "ponto-1",
  nome: "Sede",
  comunidade_virtual_id: COMUNIDADE.id,
  responsavel_id: null,
  ativo: true,
};

const TIPO_DE_RECURSO = {
  id: "tipo-1",
  nome: "Lanche",
  natureza: "consumivel",
  unidade: "unidade",
  exige_comprovante: false,
  valor_em_moedas: "1.50",
  vigencia_inicio: "2026-01-01",
};

function solicitacaoDeMestre(
  parcial: Partial<SolicitacaoDeParticipacao> = {},
): SolicitacaoDeParticipacao {
  return {
    id: "solicitacao-1",
    nome_ou_razao_social: "Fulano de Tal",
    email: "fulano@example.org",
    whatsapp: "11999990000",
    pretensao: "mestre",
    apresentacao: "Quero ser Mestre.",
    instituicao: null,
    links: null,
    situacao: "recebida",
    prazo: "2026-08-29T00:00:00-03:00",
    em_atraso: false,
    avaliado_por_id: null,
    parecer: null,
    decidido_em: null,
    nick: null,
    aporte_declarado: null,
    comprovante_anexado: false,
    ...parcial,
  };
}

function solicitacaoDeApoiador(
  parcial: Partial<SolicitacaoDeParticipacao> = {},
): SolicitacaoDeParticipacao {
  return solicitacaoDeMestre({
    pretensao: "apoiador",
    nick: "apoiador-pretendido",
    aporte_declarado: "R$ 100 em lanches",
    comprovante_anexado: true,
    ...parcial,
  });
}

vi.mock("../autenticacao/ContextoDeSessao", async () => {
  const real = await vi.importActual<typeof import("../autenticacao/ContextoDeSessao")>(
    "../autenticacao/ContextoDeSessao",
  );
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

import { useSessao } from "../autenticacao/ContextoDeSessao";

function configurarSessao(sessao: SessaoAberta | null) {
  vi.mocked(useSessao).mockReturnValue({
    sessao,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("área Filas", () => {
  it("abre com o filtro por natureza e a lista de participação", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [solicitacaoDeMestre()],
      proximo_cursor: null,
    });

    render(<TelaDeFilas />);

    expect(await screen.findByText("Fulano de Tal")).toBeInTheDocument();
    expect(screen.getByLabelText(/natureza/i)).toHaveValue("participacao");
  });

  it("o atraso aparece por rótulo legível, sem depender de cor", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [solicitacaoDeMestre({ em_atraso: true })],
      proximo_cursor: null,
    });

    render(<TelaDeFilas />);

    const rotulo = await screen.findByText("Em atraso");
    expect(rotulo.tagName).toBe("SPAN");
  });

  it("Mestre lê a recusa em linguagem simples, não um erro cru", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    const listarEspiado = vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao");

    render(<TelaDeFilas />);

    expect(await screen.findByText(/esta área é do admin/i)).toBeInTheDocument();
    expect(listarEspiado).not.toHaveBeenCalled();
  });

  it("aceitar com parecer mostra o desfecho registrado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [solicitacaoDeMestre()],
      proximo_cursor: null,
    });
    vi.spyOn(filasApi, "avaliarSolicitacaoDeParticipacao").mockResolvedValue(
      solicitacaoDeMestre({
        situacao: "aceita",
        parecer: "Perfil compatível.",
        avaliado_por_id: "admin-1",
        decidido_em: "2026-08-22T10:00:00-03:00",
      }),
    );

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));
    await usuario.type(screen.getByLabelText(/^parecer$/i), "Perfil compatível.");
    await usuario.click(screen.getByRole("button", { name: /^aceitar$/i }));

    await waitFor(() =>
      expect(filasApi.avaliarSolicitacaoDeParticipacao).toHaveBeenCalledWith(
        "solicitacao-1",
        { situacao: "aceita", parecer: "Perfil compatível." },
        "token-do-admin",
      ),
    );
    expect(await screen.findByText("Aceita")).toBeInTheDocument();
  });

  it("recusar com parecer vazio aponta o campo sem chamar o núcleo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [solicitacaoDeMestre()],
      proximo_cursor: null,
    });
    const avaliarEspiado = vi.spyOn(filasApi, "avaliarSolicitacaoDeParticipacao");

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));
    await usuario.click(screen.getByRole("button", { name: /^recusar$/i }));

    expect(await screen.findByText(/informe o motivo da recusa/i)).toBeInTheDocument();
    expect(avaliarEspiado).not.toHaveBeenCalled();
  });

  it("solicitação já avaliada não oferece desfecho", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [
        solicitacaoDeMestre({
          situacao: "recusada",
          parecer: "Sem vaga.",
          avaliado_por_id: "admin-1",
          decidido_em: "2026-08-20T10:00:00-03:00",
        }),
      ],
      proximo_cursor: null,
    });

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));

    expect(screen.getByText("Recusada")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^aceitar$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^recusar$/i })).not.toBeInTheDocument();
  });

  it("aceitar não cadastra ninguém, e o formulário de Apoiador abre pré-preenchido", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [
        solicitacaoDeApoiador({ situacao: "aceita", decidido_em: "2026-08-21T10:00:00" }),
      ],
      proximo_cursor: null,
    });
    const cadastrarEspiado = vi.spyOn(personasApi, "cadastrarApoiador");

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));

    const formulario = await screen.findByRole("form", { name: /novo apoiador/i });
    expect(within(formulario).getByLabelText(/^nome$/i)).toHaveValue("Fulano de Tal");
    expect(within(formulario).getByLabelText(/^e-mail$/i)).toHaveValue("fulano@example.org");
    expect(within(formulario).getByLabelText(/nick pretendido/i)).toHaveValue(
      "apoiador-pretendido",
    );
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });

  it("cadastro pré-preenchido sem artefato comprobatório é apontado e não é criado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [
        solicitacaoDeApoiador({ situacao: "aceita", decidido_em: "2026-08-21T10:00:00" }),
      ],
      proximo_cursor: null,
    });
    const cadastrarEspiado = vi.spyOn(personasApi, "cadastrarApoiador");

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));
    await usuario.click(await screen.findByRole("button", { name: /^cadastrar$/i }));

    expect(
      await screen.findByText(/ao menos um artefato comprobatório é obrigatório/i),
    ).toBeInTheDocument();
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });

  it("a homologação mostra o valor em moedas, e nenhum valor em reais", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [
        solicitacaoDeApoiador({ situacao: "aceita", decidido_em: "2026-08-21T10:00:00" }),
      ],
      proximo_cursor: null,
    });
    vi.spyOn(personasApi, "cadastrarApoiador").mockResolvedValue({
      id: "apoiador-1",
      nome: "Fulano de Tal",
      email: "fulano@example.org",
      whatsapp: "11999990000",
      nick: "apoiador-pretendido",
      artefatos: [{ endereco: "https://exemplo.org", rotulo: "Perfil" }],
    });
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_DE_APOIO],
      proximo_cursor: null,
    });
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([TIPO_DE_RECURSO]);
    vi.spyOn(aportesApi, "homologarAporte").mockResolvedValue({
      id: "aporte-1",
      provedor_id: "apoiador-1",
      tipo_de_recurso_id: TIPO_DE_RECURSO.id,
      quantidade: "10",
      ponto_de_apoio_id: PONTO_DE_APOIO.id,
      valor_em_moedas: "15.00",
      forma: "material",
      data_do_aporte: "2026-08-22",
    });

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));
    await usuario.click(await screen.findByRole("button", { name: /acrescentar artefato/i }));
    await usuario.type(screen.getByLabelText(/^rótulo$/i), "Perfil");
    await usuario.type(screen.getByLabelText(/^endereço$/i), "https://exemplo.org");
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    await usuario.selectOptions(
      await screen.findByLabelText(/tipo de recurso/i),
      TIPO_DE_RECURSO.id,
    );
    await usuario.type(screen.getByLabelText(/quantidade/i), "10");
    await usuario.type(screen.getByLabelText(/data do aporte/i), "2026-08-22");
    await usuario.click(screen.getByRole("button", { name: /homologar aporte/i }));

    const aviso = await screen.findByText(/aporte homologado: 15\.00 moedas/i);
    expect(aviso).toBeInTheDocument();
    // O valor oficial creditado nunca aparece em reais (`RN-02-19`) — o
    // "R$" que existe na tela é só o texto livre que o próprio pré-cadastro
    // declarou, mostrado como referência ao Admin (`RF-02-83`).
    expect(aviso.textContent).not.toMatch(/r\$/i);
  });

  it("solicitação já homologada não oferece homologar de novo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [
        solicitacaoDeApoiador({ situacao: "aceita", decidido_em: "2026-08-21T10:00:00" }),
      ],
      proximo_cursor: null,
    });
    vi.spyOn(personasApi, "cadastrarApoiador").mockResolvedValue({
      id: "apoiador-1",
      nome: "Fulano de Tal",
      email: "fulano@example.org",
      whatsapp: "11999990000",
      nick: "apoiador-pretendido",
      artefatos: [{ endereco: "https://exemplo.org", rotulo: "Perfil" }],
    });
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_DE_APOIO],
      proximo_cursor: null,
    });
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([TIPO_DE_RECURSO]);
    vi.spyOn(aportesApi, "homologarAporte").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Esta solicitação de participação já foi homologada.",
        campo: "solicitacao_de_participacao_id",
      }),
    );

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));
    await usuario.click(await screen.findByRole("button", { name: /acrescentar artefato/i }));
    await usuario.type(screen.getByLabelText(/^rótulo$/i), "Perfil");
    await usuario.type(screen.getByLabelText(/^endereço$/i), "https://exemplo.org");
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    await usuario.selectOptions(
      await screen.findByLabelText(/tipo de recurso/i),
      TIPO_DE_RECURSO.id,
    );
    await usuario.type(screen.getByLabelText(/quantidade/i), "10");
    await usuario.type(screen.getByLabelText(/data do aporte/i), "2026-08-22");
    await usuario.click(screen.getByRole("button", { name: /homologar aporte/i }));

    expect(
      await screen.findByText(/o aporte desta solicitação já foi homologado/i),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /homologar aporte/i }),
    ).not.toBeInTheDocument();
  });
});
