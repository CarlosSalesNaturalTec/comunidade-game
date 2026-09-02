import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import * as acompanhamentoApi from "../acompanhamento/api";
import * as aportesApi from "../aportes/api";
import * as desafiosExtrasApi from "../desafiosExtras/api";
import * as documentosApi from "../documentos/api";
import * as efetividadeApi from "../efetividade/api";
import * as identidadeApi from "../identidade/api";
import * as missoesApi from "../missoes/api";
import * as preCadastroApi from "../preCadastro/api";
import * as propostasApi from "../propostas/api";
import * as sustentoApi from "../sustento/api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

// Critério de aceite da PRD-14 §12: nenhuma tela oferece campo de mensagem,
// telefone ou e-mail de Guerreiro(a), família ou Mestre. Garantia negativa
// verificada por teste — não confia na revisão de código (`RF-14-59`,
// `RN-14-20`, `RN-14-24`, design — decisão 5).
function semCanalDeContato() {
  expect(screen.queryByRole("textbox", { name: /mensagem/i })).not.toBeInTheDocument();
  expect(screen.queryByRole("textbox", { name: /resposta/i })).not.toBeInTheDocument();
  expect(
    screen.queryByText(/telefone (do|da) (guerreiro|família|mestre)/i),
  ).not.toBeInTheDocument();
  expect(
    screen.queryByText(/e-?mail (do|da) (guerreiro|família|mestre)/i),
  ).not.toBeInTheDocument();
  expect(
    screen.queryByText(/contato (com o|direto com o|do|da) (guerreiro|família|mestre)/i),
  ).not.toBeInTheDocument();
  expect(document.querySelector('a[href^="mailto:"]')).toBeNull();
  expect(document.querySelector('a[href^="tel:"]')).toBeNull();
}

describe("canal fechado — sem sessão", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(preCadastroApi, "listarNecessidadesEmAberto").mockResolvedValue([]);
    vi.spyOn(preCadastroApi, "listarMissoesAbertas").mockResolvedValue([]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("a porta pública de pré-cadastro não oferece canal", async () => {
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i });

    semCanalDeContato();
  });

  it("a área de direitos e dados sem sessão não oferece canal", async () => {
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i });
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(
      screen.getByRole("button", { name: /ver em direitos e dados/i }),
    );
    await screen.findByRole("heading", { name: /^direitos e dados$/i });

    semCanalDeContato();
  });
});

describe("canal fechado — com sessão", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(aportesApi, "listarNecessidadesEmAberto").mockResolvedValue([]);
    vi.spyOn(aportesApi, "listarMeusAportes").mockResolvedValue({
      poder_sustentador_em_moedas: "0.00",
      aportes: [],
    });
    vi.spyOn(aportesApi, "listarMinhasDeclaracoesDeAporte").mockResolvedValue([]);
    vi.spyOn(missoesApi, "listarMissoesAbertas").mockResolvedValue({
      existir: [],
      acontecer: [],
      reconhecer: [],
      permanecer: [],
    });
    vi.spyOn(efetividadeApi, "lerPainelDeEfetividade").mockResolvedValue({
      desafios: { propostos: [], publicados: [], concluidos: [] },
      moedas: { total_em_moedas: "0.00", aportes: [] },
      cobertura_de_ods: { por_comunidade: [] },
    });
    vi.spyOn(sustentoApi, "consultarMeuSustento").mockResolvedValue({
      nivel: 0,
      nome_do_nivel: "—",
      frente_que_falta: "—",
      selos: { frente: [], modalidade: [], ato: [], multiplicacao: [] },
    });
    vi.spyOn(desafiosExtrasApi, "listarMeusDesafiosExtras").mockResolvedValue([]);
    vi.spyOn(documentosApi, "listarMeusDocumentos").mockResolvedValue([]);
    vi.spyOn(identidadeApi, "lerMinhaIdentidade").mockResolvedValue({
      nick: "ApoiadoraDoTeste",
      avatar: null,
      moedas_acumuladas: "10.00",
      avatar_proprio_liberado: true,
      moedas_faltantes_para_avatar_proprio: null,
    });
    vi.spyOn(acompanhamentoApi, "listarMeusFavoritos").mockResolvedValue({
      guerreiros: [],
      mestres: [],
    });
    vi.spyOn(acompanhamentoApi, "listarGuerreirosPublicos").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(acompanhamentoApi, "listarPoderesPublicos").mockResolvedValue([]);
    vi.spyOn(acompanhamentoApi, "listarCriacoesPublicas").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(acompanhamentoApi, "listarCoberturaPublicaDeOds").mockResolvedValue([]);
    vi.spyOn(propostasApi, "listarMinhasPropostas").mockResolvedValue([]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  async function entrarComoApoiador() {
    vi.spyOn(authApi, "loginPorCredencial").mockResolvedValue({
      token: "token-do-apoiador",
      expira_em: new Date().toISOString(),
      papel: "apoiador",
    });
    vi.spyOn(authApi, "eu").mockResolvedValue({
      persona_id: "apoiador-1",
      papel: "apoiador",
      permissoes: {},
    });

    render(<App />);
    const testeDeUsuario = userEvent.setup();
    await testeDeUsuario.click(await screen.findByRole("button", { name: /^entrar$/i }));
    await testeDeUsuario.type(await screen.findByLabelText(/^usuário$/i), "apoiadora");
    await testeDeUsuario.type(screen.getByLabelText(/^senha$/i), "senha-123");
    await testeDeUsuario.click(screen.getByRole("button", { name: /^entrar$/i }));
    await screen.findByRole("button", { name: /propor desafio extra/i });
    return testeDeUsuario;
  }

  const AREAS = [
    "identidade pública",
    "documentos comprobatórios",
    "propor desafio extra",
    "meus desafios",
    "efetividade",
    "meus aportes",
    "necessidades em aberto",
    "missões",
    "sustento",
    "declarar aporte",
    "situação das declarações",
    "acompanhamento",
    "propostas",
    "direitos e dados",
  ];

  it.each(AREAS)(
    'a área "%s" não oferece canal com Guerreiro(a), família ou Mestre',
    async (rotulo) => {
      const testeDeUsuario = await entrarComoApoiador();

      await testeDeUsuario.click(
        screen.getByRole("button", { name: new RegExp(`^${rotulo}$`, "i") }),
      );

      semCanalDeContato();
    },
  );

  it("a proposta de evolução vai à fila da gestão, sem destinatário nem conversa", async () => {
    const testeDeUsuario = await entrarComoApoiador();

    await testeDeUsuario.click(screen.getByRole("button", { name: /^propostas$/i }));

    expect(screen.queryByLabelText(/destinatário/i)).not.toBeInTheDocument();
    semCanalDeContato();
  });
});
