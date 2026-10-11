import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { PaginaDoNucleo } from "../api/leituras";
import { ListaDeRegistros } from "../listas/ListaDeRegistros";

// A lista de registros do `RF-03-02` e do `RF-03-82`: uma linha por registro,
// dez por página, avançar e voltar percorrendo tudo, e **nada** gravado no
// aparelho (`RN-03-22`).

interface Registro {
  id: string;
  nome: string;
  avatar: string | null;
}

/** Um acervo com `quantidade` registros, servido em páginas de dez por cursor
 * — o mesmo contrato do núcleo: só para a frente, e sem total. */
function acervo(quantidade: number) {
  const registros: Registro[] = Array.from({ length: quantidade }, (_, indice) => ({
    id: `r-${indice}`,
    nome: `Registro ${indice}`,
    avatar: "avatar-de-teste",
  }));

  const ler = vi.fn(async (cursor: string | null): Promise<PaginaDoNucleo<Registro>> => {
    const inicio = cursor === null ? 0 : Number(cursor);
    const itens = registros.slice(inicio, inicio + 10);
    const fim = inicio + itens.length;
    return { itens, proximo_cursor: fim < registros.length ? String(fim) : null };
  });

  return { registros, ler };
}

function montar(quantidade: number) {
  const { registros, ler } = acervo(quantidade);
  const renderizado = render(
    <ListaDeRegistros
      ler={ler}
      chave="teste/registros"
      idDe={(registro) => registro.id}
      linhaDe={(registro) => ({
        avatar: registro.avatar,
        identificacao: registro.nome,
        destino: `/registros/${registro.id}`,
        dados: "dado principal",
      })}
      rotulo="Registros"
      carregando="Carregando os registros…"
      falha="Não foi possível carregar os registros agora. Tente de novo."
      vazio="Nenhum registro por enquanto."
    />,
  );
  return { ...renderizado, registros, ler };
}

afterEach(() => {
  vi.restoreAllMocks();
  window.localStorage.clear();
  window.sessionStorage.clear();
});

describe("a lista de registros", () => {
  it("a primeira página traz dez linhas, com a posição em texto (RF-03-82)", async () => {
    montar(23);

    expect(await screen.findByText("Registro 0")).toBeVisible();
    expect(screen.getAllByRole("listitem")).toHaveLength(10);
    expect(screen.getByText("Página 1")).toBeVisible();
    expect(screen.getByRole("button", { name: "Próxima página" })).toBeEnabled();
    // Na primeira página não há para onde voltar.
    expect(screen.getByRole("button", { name: "Página anterior" })).toBeDisabled();
  });

  it("a lista curta não oferece paginação (RF-03-82)", async () => {
    montar(3);

    expect(await screen.findByText("Registro 0")).toBeVisible();
    expect(screen.getAllByRole("listitem")).toHaveLength(3);
    expect(screen.queryByRole("button", { name: "Próxima página" })).toBeNull();
    expect(screen.queryByRole("button", { name: "Página anterior" })).toBeNull();
    expect(screen.queryByText(/^Página/)).toBeNull();
  });

  it("avançar e voltar percorrem a lista inteira sem pular nem repetir (RF-03-82)", async () => {
    const { registros } = montar(23);
    const testeDeUsuario = userEvent.setup();

    const percorridos: string[] = [];
    const recolher = () =>
      percorridos.push(
        ...screen.getAllByRole("listitem").map((linha) => linha.textContent ?? ""),
      );

    expect(await screen.findByText("Registro 0")).toBeVisible();
    recolher();
    await testeDeUsuario.click(screen.getByRole("button", { name: "Próxima página" }));
    expect(await screen.findByText("Registro 10")).toBeVisible();
    recolher();
    await testeDeUsuario.click(screen.getByRole("button", { name: "Próxima página" }));
    expect(await screen.findByText("Registro 20")).toBeVisible();
    recolher();

    // Cada registro apareceu uma vez, nenhum foi pulado e nenhum se repetiu.
    expect(percorridos).toEqual(registros.map((registro) => `${registro.nome}dado principal`));
    // A última página não oferece avançar.
    expect(screen.getByRole("button", { name: "Próxima página" })).toBeDisabled();
    expect(screen.getByText("Página 3")).toBeVisible();

    // Voltar desfaz a ida, página por página, sem pular nem repetir.
    await testeDeUsuario.click(screen.getByRole("button", { name: "Página anterior" }));
    expect(await screen.findByText("Registro 10")).toBeVisible();
    await testeDeUsuario.click(screen.getByRole("button", { name: "Página anterior" }));
    expect(await screen.findByText("Registro 0")).toBeVisible();
    expect(screen.getByText("Página 1")).toBeVisible();
    expect(screen.queryByText("Registro 10")).toBeNull();
  });

  it("a célula que identifica o registro é o acionável, em endereço próprio (RF-03-03)", async () => {
    montar(2);

    const porta = await screen.findByRole("link", { name: "Registro 0" });
    expect(porta).toHaveAttribute("href", "/registros/r-0");
  });

  it("linha sem avatar não abre buraco (RF-03-02)", async () => {
    const { container } = render(
      <ListaDeRegistros
        ler={async (): Promise<PaginaDoNucleo<Registro>> => ({
          itens: [{ id: "r-0", nome: "Sem avatar", avatar: null }],
          proximo_cursor: null,
        })}
        chave="teste/sem-avatar"
        idDe={(registro) => registro.id}
        linhaDe={(registro) => ({
          identificacao: registro.nome,
          dados: "localização · 3 vinculados",
        })}
        rotulo="Registros"
        carregando="Carregando…"
        falha="Falhou."
        vazio="Nada."
      />,
    );

    expect(await screen.findByText("Sem avatar")).toBeVisible();
    const linha = container.querySelector(".cg-lista-de-registros__linha");
    expect(linha?.querySelector(".cg-lista-de-registros__avatar")).toBeNull();
    expect(linha?.textContent).toBe("Sem avatarlocalização · 3 vinculados");
  });

  it("a lista não é tabela: sem cabeçalho de coluna e sem grade (documento 15 §6)", async () => {
    const { container } = montar(23);

    expect(await screen.findByText("Registro 0")).toBeVisible();
    expect(container.querySelector("table")).toBeNull();
    expect(container.querySelector("thead")).toBeNull();
    expect(screen.queryAllByRole("columnheader")).toHaveLength(0);
    // A lista é `<ol>`: a ordem é informação, e a linha é item de lista.
    expect(container.querySelector("ol.cg-lista-de-registros")).not.toBeNull();
  });

  it("percorrer a lista não guarda nada no aparelho (RN-03-22)", async () => {
    montar(23);
    const testeDeUsuario = userEvent.setup();

    expect(await screen.findByText("Registro 0")).toBeVisible();
    await testeDeUsuario.click(screen.getByRole("button", { name: "Próxima página" }));
    expect(await screen.findByText("Registro 10")).toBeVisible();

    expect(window.localStorage.length).toBe(0);
    expect(window.sessionStorage.length).toBe(0);
    expect(document.cookie).toBe("");
  });

  it("a lista vazia diz o que tem, e não oferece controle (RF-03-82)", async () => {
    montar(0);

    expect(await screen.findByText("Nenhum registro por enquanto.")).toBeVisible();
    expect(screen.queryByRole("button", { name: "Próxima página" })).toBeNull();
  });
});
