import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as api from "./api";
import { CHAVE_DE_ARMAZENAMENTO_PADRAO, lerToken } from "./armazenamentoDeSessao";
import { ProvedorDeSessao, useSessao } from "./ContextoDeSessao";

function Conteudo({ rotulo, idToken = "id-token-de-teste" }: { rotulo: string; idToken?: string }) {
  const { sessao, restaurando, entrarComGoogle, sair } = useSessao();
  if (restaurando) return <p>Restaurando {rotulo}…</p>;
  if (!sessao) {
    return (
      <button type="button" onClick={() => entrarComGoogle(idToken)}>
        Entrar {rotulo}
      </button>
    );
  }
  return (
    <div>
      <p>
        {rotulo} aberta como {sessao.papel}
      </p>
      <button type="button" onClick={sair}>
        Sair {rotulo}
      </button>
    </div>
  );
}

function mockarAberturaDeSessao(papel: "guerreiro" | "mestre" = "mestre") {
  vi.spyOn(api, "loginSocial").mockResolvedValue({
    token: `token-de-${papel}`,
    expira_em: new Date().toISOString(),
    papel,
  });
  vi.spyOn(api, "eu").mockResolvedValue({
    persona_id: "algum-id",
    papel,
    permissoes: {},
  });
}

describe("a chave de armazenamento da sessão é parametrizável", () => {
  beforeEach(() => {
    sessionStorage.clear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("sem propriedade, o token vai para a chave padrão de sempre", async () => {
    mockarAberturaDeSessao();
    render(
      <ProvedorDeSessao>
        <Conteudo rotulo="padrão" />
      </ProvedorDeSessao>,
    );
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /entrar padrão/i }));

    await screen.findByText(/padrão aberta como mestre/i);
    expect(lerToken(CHAVE_DE_ARMAZENAMENTO_PADRAO)).toBe("token-de-mestre");
  });

  it("com chave explícita, o token vai para ela, não para a padrão", async () => {
    mockarAberturaDeSessao("guerreiro");
    render(
      <ProvedorDeSessao chaveDeArmazenamento="app-01:sessao-guerreiro">
        <Conteudo rotulo="guerreiro" />
      </ProvedorDeSessao>,
    );
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /entrar guerreiro/i }));

    await screen.findByText(/guerreiro aberta como guerreiro/i);
    expect(lerToken("app-01:sessao-guerreiro")).toBe("token-de-guerreiro");
    expect(lerToken(CHAVE_DE_ARMAZENAMENTO_PADRAO)).toBeNull();
  });

  it("dois provedores aninhados, com chaves distintas, convivem sem que um derrube o outro", async () => {
    vi.spyOn(api, "loginSocial").mockImplementation((idToken: string) =>
      Promise.resolve({
        token: idToken === "id-trabalho" ? "token-de-trabalho" : "token-de-guerreiro",
        expira_em: new Date().toISOString(),
        papel: idToken === "id-trabalho" ? "mestre" : "guerreiro",
      }),
    );
    vi.spyOn(api, "eu").mockImplementation((token: string) =>
      Promise.resolve({
        persona_id: "algum-id",
        papel: token === "token-de-trabalho" ? "mestre" : "guerreiro",
        permissoes: {},
      }),
    );

    function Aninhado() {
      return (
        <ProvedorDeSessao chaveDeArmazenamento="app-01:sessao-trabalho">
          <Conteudo rotulo="trabalho" idToken="id-trabalho" />
          <ProvedorDeSessao chaveDeArmazenamento="app-01:sessao-guerreiro">
            <Conteudo rotulo="guerreiro" idToken="id-guerreiro" />
          </ProvedorDeSessao>
        </ProvedorDeSessao>
      );
    }

    render(<Aninhado />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^entrar trabalho$/i }));
    await screen.findByText(/trabalho aberta como mestre/i);

    // A sessão do Guerreiro(a) segue pedindo entrada — a de trabalho não a abriu.
    expect(screen.getByRole("button", { name: /^entrar guerreiro$/i })).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /^entrar guerreiro$/i }));
    await screen.findByText(/guerreiro aberta como guerreiro/i);

    // As duas convivem: a de trabalho não foi derrubada pela do Guerreiro(a).
    expect(screen.getByText(/trabalho aberta como mestre/i)).toBeInTheDocument();
    expect(lerToken("app-01:sessao-trabalho")).toBe("token-de-trabalho");
    expect(lerToken("app-01:sessao-guerreiro")).toBe("token-de-guerreiro");

    await usuario.click(screen.getByRole("button", { name: /^sair guerreiro$/i }));
    await waitFor(() =>
      expect(screen.getByRole("button", { name: /^entrar guerreiro$/i })).toBeInTheDocument(),
    );

    // Sair do Guerreiro(a) não encerra a sessão de trabalho.
    expect(screen.getByText(/trabalho aberta como mestre/i)).toBeInTheDocument();
    expect(lerToken("app-01:sessao-trabalho")).toBe("token-de-trabalho");
  });
});
