import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import * as leituras from "../api/leituras";
import { esquecerConteudoInstitucional } from "../institucional/useConteudoInstitucional";
import { esquecerNecessidades } from "../necessidades/useNecessidades";

// O garfo da entrada (`RF-03-42`, documentos 02 §1 e 14 §§10, 11): a porta
// pergunta o que a pessoa traz e encaminha aos dois destinos que já existem —
// dinheiro ao pré-cadastro da App 08, o resto ao formulário da vitrine. Só
// encaminha: nenhum campo novo no formulário, nenhum atributo novo no núcleo.

function comLeituras() {
  vi.spyOn(leituras, "listarNecessidades").mockResolvedValue([]);
  vi.spyOn(leituras, "lerConteudoInstitucional").mockResolvedValue([
    { secao: "quem-somos", texto: "Somos o projeto.", video_url: null },
    { secao: "contatos", texto: null, video_url: null },
    { secao: "como-apoiar", texto: "Chave PIX: uma-chave", video_url: null },
  ]);
}

async function abrirAPorta() {
  window.history.pushState(null, "", "/quero-participar");
  const tela = render(<App />);
  await screen.findByRole("heading", { name: "O que você traz?" });
  return { testeDeUsuario: userEvent.setup(), tela };
}

describe("o garfo do que a pessoa traz", () => {
  beforeEach(() => {
    esquecerConteudoInstitucional();
    esquecerNecessidades();
    localStorage.clear();
    sessionStorage.clear();
    window.history.pushState(null, "", "/");
    comLeituras();
  });
  afterEach(() => vi.restoreAllMocks());

  it("as sete modalidades do documento 14 §10 aparecem na pergunta (RF-03-42)", async () => {
    await abrirAPorta();

    for (const rotulo of [
      "Dinheiro",
      "Insumo, equipamento ou alimento",
      "Serviço",
      "Conteúdo educacional",
      "Código",
      "Divulgação",
      "Quero ensinar",
    ]) {
      expect(screen.getByRole("button", { name: rotulo })).toBeVisible();
    }
  });

  it("dinheiro vai ao pré-cadastro da App 08, com o comprovante nomeado (RF-03-42)", async () => {
    const { testeDeUsuario } = await abrirAPorta();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Dinheiro" }));

    expect(screen.getByText(/Comprovante da transferência/)).toBeVisible();
    expect(screen.getByText(/pré-cadastro na Área do Apoiador/)).toBeVisible();
    // Sem endereço publicado da App 08, o destino é nomeado em texto e nenhum
    // link quebrado aparece.
    expect(
      screen.getByText("O endereço da Área do Apoiador ainda não foi publicado."),
    ).toBeVisible();
    expect(
      screen.queryByRole("button", { name: "Abrir o formulário de participação" }),
    ).not.toBeInTheDocument();
  });

  it.each([
    ["Insumo, equipamento ou alimento", "Descrição e foto do bem"],
    ["Serviço", "O que faz e quando pode"],
    ["Conteúdo educacional", "Amostra do material"],
    ["Código", "Repositório e portfólio"],
    ["Divulgação", "Alcance e mídia própria"],
    ["Quero ensinar", "Artefatos da habilidade"],
  ])(
    "%s vai ao formulário da vitrine, com o comprobatório dela (RF-03-42)",
    async (rotulo, comprobatorio) => {
      const { testeDeUsuario } = await abrirAPorta();

      await testeDeUsuario.click(screen.getByRole("button", { name: rotulo }));
      expect(screen.getByText(new RegExp(comprobatorio))).toBeVisible();

      await testeDeUsuario.click(
        screen.getByRole("button", { name: "Abrir o formulário de participação" }),
      );
      expect(window.location.pathname).toBe("/participar");
      expect(
        await screen.findByRole("heading", { name: "Quero ser Mestre ou Apoiador" }),
      ).toBeVisible();
    },
  );

  it("o formulário segue com os campos que já tinha: o garfo não acrescenta nenhum (RF-03-42)", async () => {
    const { testeDeUsuario } = await abrirAPorta();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Código" }));
    await testeDeUsuario.click(
      screen.getByRole("button", { name: "Abrir o formulário de participação" }),
    );

    await screen.findByRole("heading", { name: "Quero ser Mestre ou Apoiador" });
    expect(screen.queryByLabelText(/modalidade/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/o que você traz/i)).not.toBeInTheDocument();
  });

  it("trocar de resposta volta à pergunta (RF-03-42)", async () => {
    const { testeDeUsuario } = await abrirAPorta();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Serviço" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Trago outra coisa" }));

    expect(screen.getByRole("button", { name: "Dinheiro" })).toBeVisible();
  });

  it("a escolha não sobrevive à recarga, e nada dela vai ao aparelho (RF-03-42, RF-03-38)", async () => {
    const { testeDeUsuario, tela } = await abrirAPorta();
    await testeDeUsuario.click(screen.getByRole("button", { name: "Divulgação" }));
    expect(screen.getByText(/Alcance e mídia própria/)).toBeVisible();
    expect(localStorage.length).toBe(0);
    expect(sessionStorage.length).toBe(0);
    expect(document.cookie).toBe("");

    // Recarregar é desmontar e montar a aplicação de novo no mesmo endereço.
    tela.unmount();
    esquecerConteudoInstitucional();
    esquecerNecessidades();
    render(<App />);

    expect(await screen.findByRole("button", { name: "Dinheiro" })).toBeVisible();
  });
});
