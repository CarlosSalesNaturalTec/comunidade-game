import { render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { NecessidadePublica } from "../api/leituras";
import * as leituras from "../api/leituras";
import { esquecerConteudoInstitucional } from "../institucional/useConteudoInstitucional";
import { esquecerNecessidades } from "../necessidades/useNecessidades";

// As necessidades de recurso em aberto (`RF-03-47`): aparecem na porta do
// convite e em "Como apoiar", com tipo, quantidade que falta, valor em moedas,
// comunidade, ponto de apoio e o horário da aula. Nenhum campo em reais e
// nenhuma pessoa (`RF-03-10`, `RN-03-18`).

// O horário é comparado pelo mesmo formatador da tela: o fuso da máquina que
// roda o teste não muda o que se está verificando — que a aula sai com data e
// hora, em pt-BR.
const FORMATADOR_DE_HORARIO = new Intl.DateTimeFormat("pt-BR", {
  dateStyle: "short",
  timeStyle: "short",
});
const INICIO_DA_AULA = "2026-10-05T13:00:00Z";
const FIM_DA_AULA = "2026-10-05T15:00:00Z";
const HORARIO_ESPERADO = `Aula de ${FORMATADOR_DE_HORARIO.format(
  new Date(INICIO_DA_AULA),
)} a ${FORMATADOR_DE_HORARIO.format(new Date(FIM_DA_AULA))}`;

function necessidade(parcial: Partial<NecessidadePublica> = {}): NecessidadePublica {
  return {
    aula_id: "aula-1",
    tipo_de_recurso_id: "tipo-1",
    tipo_de_recurso_nome: "Lanche",
    quantidade_faltante: "10",
    valor_em_moedas: "20.00",
    comunidade_virtual_id: "comunidade-1",
    comunidade_virtual_nome: "Guerreira Zeferina",
    ponto_de_apoio_id: "ponto-1",
    ponto_de_apoio_nome: "Escola Municipal Zeferina",
    inicio_em: INICIO_DA_AULA,
    fim_em: FIM_DA_AULA,
    ...parcial,
  };
}

function comLeituras(necessidades: NecessidadePublica[]) {
  const lista = vi.spyOn(leituras, "listarNecessidades").mockResolvedValue(necessidades);
  vi.spyOn(leituras, "lerConteudoInstitucional").mockResolvedValue([
    { secao: "quem-somos", texto: "Somos o projeto.", video_url: null },
    { secao: "contatos", texto: null, video_url: null },
    { secao: "como-apoiar", texto: "Chave PIX: uma-chave", video_url: null },
  ]);
  vi.spyOn(leituras, "listarGuerreiros").mockResolvedValue({
    itens: [],
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "listarCriacoes").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarRanking").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarPoderes").mockResolvedValue([]);
  vi.spyOn(leituras, "listarComunidades").mockResolvedValue({
    itens: [],
    proximo_cursor: null,
    ciclo_rotulo: "Ciclo 01",
  });
  vi.spyOn(leituras, "lerCoberturaDeOds").mockResolvedValue([]);
  return lista;
}

async function lista(): Promise<HTMLElement> {
  return await screen.findByRole("list", { name: "Necessidades de recurso em aberto" });
}

describe("as necessidades de recurso em aberto", () => {
  beforeEach(() => {
    esquecerConteudoInstitucional();
    esquecerNecessidades();
    window.history.pushState(null, "", "/");
  });
  afterEach(() => vi.restoreAllMocks());

  it.each(["/quero-participar", "/"])(
    "a necessidade sai com tudo o que o PRD pede em %s (RF-03-47)",
    async (caminho) => {
      comLeituras([necessidade()]);
      window.history.pushState(null, "", caminho);
      render(<App />);

      const item = within(await lista()).getByRole("listitem");
      expect(within(item).getByRole("heading", { name: "Lanche" })).toBeVisible();
      expect(within(item).getByText("Falta: 10")).toBeVisible();
      expect(within(item).getByText("20.00 moedas")).toBeVisible();
      expect(within(item).getByText("Guerreira Zeferina")).toBeVisible();
      expect(within(item).getByText("Escola Municipal Zeferina")).toBeVisible();
      expect(within(item).getByText(HORARIO_ESPERADO)).toBeVisible();
    },
  );

  it("nenhuma linha traz reais, e nada além dos campos do PRD aparece (RF-03-10, RN-03-18)", async () => {
    comLeituras([
      necessidade(),
      necessidade({ aula_id: "aula-2", tipo_de_recurso_nome: "Tinta" }),
    ]);
    window.history.pushState(null, "", "/quero-participar");
    render(<App />);

    const itens = within(await lista()).getAllByRole("listitem");
    expect(itens).toHaveLength(2);
    expect((await lista()).textContent ?? "").not.toMatch(/R\$|reais/i);
    // A linha mostra só os campos que o `RF-03-47` lista: nada de nick, nome de
    // responsável ou de provedor entra, porque a rota pública não os serve e a
    // tela não acrescenta campo nenhum.
    for (const item of itens) {
      const linhas = Array.from(item.querySelectorAll("p")).map((linha) => linha.textContent);
      expect(linhas).toEqual([
        "Falta: 10",
        "20.00 moedas",
        "Guerreira Zeferina",
        "Escola Municipal Zeferina",
        HORARIO_ESPERADO,
      ]);
    }
  });

  it("tipo sem vigência aparece sem valor em moedas, e a vitrine não arbitra nenhum (RN-03-18)", async () => {
    comLeituras([necessidade({ valor_em_moedas: null })]);
    window.history.pushState(null, "", "/quero-participar");
    render(<App />);

    const item = within(await lista()).getByRole("listitem");
    expect(within(item).getByText("Sem valor de referência vigente")).toBeVisible();
    expect(within(item).queryByText(/moedas/)).not.toBeInTheDocument();
  });

  it("sem necessidade em aberto, a tela diz isso (RF-03-47)", async () => {
    comLeituras([]);
    window.history.pushState(null, "", "/quero-participar");
    render(<App />);

    expect(
      await screen.findByText("Nenhuma necessidade de recurso em aberto por enquanto."),
    ).toBeVisible();
  });

  it("a porta e Como apoiar compartilham uma única leitura por carga (RF-03-47)", async () => {
    const leitura = comLeituras([necessidade()]);
    render(<App />);
    await lista();

    expect(leitura).toHaveBeenCalledTimes(1);
  });

  it("falha na leitura avisa em linguagem simples, sem travar a tela", async () => {
    comLeituras([]);
    vi.spyOn(leituras, "listarNecessidades").mockRejectedValue(new Error("fora do ar"));
    esquecerNecessidades();
    window.history.pushState(null, "", "/quero-participar");
    render(<App />);

    expect(
      await screen.findByText(
        "Não foi possível carregar as necessidades em aberto agora. Tente de novo.",
      ),
    ).toBeVisible();
    expect(screen.getByRole("heading", { name: "Quero participar", level: 2 })).toBeVisible();
  });
});
