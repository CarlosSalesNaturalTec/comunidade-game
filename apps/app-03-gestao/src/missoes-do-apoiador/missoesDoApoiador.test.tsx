import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TelaDeRecursos } from "../recursos/TelaDeRecursos";
import type { MissaoDoApoiador } from "./api";
import * as missoesApi from "./api";
import { ListaDeMissoes } from "./ListaDeMissoes";
import { PublicacaoDeMissao } from "./PublicacaoDeMissao";

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
  persona_id: "admin-1",
};

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
};

const TIPO = {
  id: "tipo-1",
  nome: "Lanche",
  natureza: "material",
  unidade: "unidade",
  exige_comprovante: false,
  valor_em_moedas: "1",
  vigencia_inicio: "2026-01-01",
};

const NECESSIDADE = {
  aula_id: "aula-1",
  tipo_de_recurso_id: TIPO.id,
  quantidade_faltante: "5",
  valor_em_moedas: "5",
  comunidade_virtual_id: "comunidade-1",
  ponto_de_apoio_id: "ponto-1",
  inicio_em: "2026-08-21T10:00:00-03:00",
  fim_em: "2026-08-21T12:00:00-03:00",
};

const MISSAO_ABERTA: MissaoDoApoiador = {
  id: "missao-1",
  nivel_de_necessidade: "acontecer",
  titulo: "O lanche do encontro",
  o_que_se_pede: "Um lanche para vinte crianças",
  quantidade: "100.00",
  falta: "40.00",
  coberto: "60.00",
  prazo: "2026-12-01",
  selo_nome: "Lanche garantido",
  selo_familia: "frente",
  situacao: "aberta",
  vencida: false,
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

function configurarSessao(sessao: SessaoAberta | null) {
  vi.mocked(useSessao).mockReturnValue({
    sessao,
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

afterEach(() => {
  vi.restoreAllMocks();
});

describe("publicação de missão", () => {
  it("publica a partir de uma necessidade em aberto", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const publicarEspiado = vi
      .spyOn(missoesApi, "publicarMissao")
      .mockResolvedValue(MISSAO_ABERTA);

    render(
      <PublicacaoDeMissao
        necessidades={[NECESSIDADE]}
        nomeDoTipoDeRecurso={() => TIPO.nome}
        onPublicada={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();

    await usuario.selectOptions(
      screen.getByLabelText(/necessidade de origem/i),
      `${NECESSIDADE.aula_id}::${NECESSIDADE.tipo_de_recurso_id}`,
    );
    await usuario.type(screen.getByLabelText(/^título$/i), "O lanche do encontro");
    await usuario.type(
      screen.getByLabelText(/o que se pede/i),
      "Um lanche para vinte crianças",
    );
    await usuario.type(screen.getByLabelText(/valor da missão/i), "100");
    await usuario.type(screen.getByLabelText(/prazo/i), "2026-12-01");
    await usuario.type(screen.getByLabelText(/selo que rende/i), "Lanche garantido");

    await usuario.click(screen.getByRole("button", { name: /publicar missão/i }));

    await waitFor(() => expect(publicarEspiado).toHaveBeenCalledTimes(1));
    expect(publicarEspiado).toHaveBeenCalledWith(
      expect.objectContaining({
        aulaId: NECESSIDADE.aula_id,
        tipoDeRecursoId: NECESSIDADE.tipo_de_recurso_id,
        titulo: "O lanche do encontro",
      }),
      SESSAO_DE_ADMIN.token,
    );
  });

  it("a recusa por faltar necessidade por trás aparece em linguagem simples", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(missoesApi, "publicarMissao").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        campo: "aula_id",
        mensagem: "Não há necessidade de recurso publicada para esta aula e tipo de recurso.",
      }),
    );

    render(
      <PublicacaoDeMissao
        necessidades={[NECESSIDADE]}
        nomeDoTipoDeRecurso={() => TIPO.nome}
        onPublicada={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();

    await usuario.selectOptions(
      screen.getByLabelText(/necessidade de origem/i),
      `${NECESSIDADE.aula_id}::${NECESSIDADE.tipo_de_recurso_id}`,
    );
    await usuario.type(screen.getByLabelText(/^título$/i), "O lanche do encontro");
    await usuario.type(
      screen.getByLabelText(/o que se pede/i),
      "Um lanche para vinte crianças",
    );
    await usuario.type(screen.getByLabelText(/valor da missão/i), "100");
    await usuario.type(screen.getByLabelText(/prazo/i), "2026-12-01");
    await usuario.type(screen.getByLabelText(/selo que rende/i), "Lanche garantido");

    await usuario.click(screen.getByRole("button", { name: /publicar missão/i }));

    expect(
      await screen.findByText(/não há necessidade de recurso publicada/i),
    ).toBeInTheDocument();
    expect(
      screen.queryByText(/erro_de_validacao|traceback|exception/i),
    ).not.toBeInTheDocument();
  });
});

describe("lista de missões", () => {
  it("mostra o coberto, o que falta e a situação, sem nick de quem cobriu", () => {
    render(
      <ListaDeMissoes
        missoes={[MISSAO_ABERTA]}
        token="token-do-admin"
        aoDespublicada={vi.fn()}
      />,
    );

    expect(screen.getByText(/o lanche do encontro/i)).toBeInTheDocument();
    expect(screen.getByText(/situação: aberta/i)).toBeInTheDocument();
    expect(screen.getByText(/coberto: 60.00/i)).toBeInTheDocument();
    expect(screen.getByText(/falta: 40.00/i)).toBeInTheDocument();
    expect(screen.queryByText(/nick/i)).not.toBeInTheDocument();
  });

  it("a despublicação avisa que nada é estornado", () => {
    render(
      <ListaDeMissoes
        missoes={[MISSAO_ABERTA]}
        token="token-do-admin"
        aoDespublicada={vi.fn()}
      />,
    );

    expect(screen.getByText(/não estorna aporte já homologado/i)).toBeInTheDocument();
  });

  it("missão concluída não oferece despublicação", () => {
    render(
      <ListaDeMissoes
        missoes={[{ ...MISSAO_ABERTA, situacao: "concluida" }]}
        token="token-do-admin"
        aoDespublicada={vi.fn()}
      />,
    );

    expect(screen.queryByRole("button", { name: /despublicar/i })).not.toBeInTheDocument();
  });

  it("a despublicação recusada pela missão concluída mostra a recusa", async () => {
    vi.spyOn(missoesApi, "despublicarMissao").mockRejectedValue(
      new ErroDaApi(409, {
        codigo: "despublicacao_de_missao_concluida_recusada",
        mensagem: "Missão concluída não se despublica.",
      }),
    );

    render(
      <ListaDeMissoes
        missoes={[MISSAO_ABERTA]}
        token="token-do-admin"
        aoDespublicada={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /despublicar/i }));

    expect(await screen.findByText(/missão concluída não se despublica/i)).toBeInTheDocument();
  });
});

describe("área Recursos", () => {
  it("quem não é Admin não alcança a publicação de missão", () => {
    configurarSessao(SESSAO_DE_MESTRE);

    render(<TelaDeRecursos />);

    expect(screen.queryByRole("form", { name: /publicar missão/i })).not.toBeInTheDocument();
  });
});
