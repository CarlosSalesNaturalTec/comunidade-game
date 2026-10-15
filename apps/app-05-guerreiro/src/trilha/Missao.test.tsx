import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { Missao } from "comum/trilha";
import * as trilhaApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";

const CHAVE_DE_SESSAO = "app-05:teste-missao";

// A `Missao` não busca mais nada: o dado público chega por `prop`, do
// `GuiaDaTrilha`, que é quem passou a buscar a trilha publicada. A
// bibliografia e o crédito deixaram de ser dela — são testados no guia, em
// `comum/trilha/trilha.test.tsx` (fatia 27 do PRD-04).
async function renderizar(
  missao: trilhaApi.MissaoNoPercurso,
  missaoPublica?: trilhaApi.MissaoPublica,
  aoDesbloquear = vi.fn(),
) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <Missao
          missao={missao}
          missaoPublica={missaoPublica}
          aoDesbloquear={aoDesbloquear}
          submissaoDoDesbloqueioLigada
        />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("missão no percurso", () => {
  it("bloqueada mostra o motivo, nunca cadeado mudo", async () => {
    await renderizar({
      id: "missao-2",
      titulo: "Segunda Missão",
      posicao: 2,
      obrigatoria: true,
      e_sondagem: false,
      desbloqueada: false,
      e_proxima: false,
      aguardando_mestre: false,
      motivo_do_bloqueio: 'Desbloqueie "Primeira Missão" primeiro.',
      desafio_de_desbloqueio: null,
    });

    expect(screen.getByText(/Desbloqueie "Primeira Missão" primeiro\./)).toBeInTheDocument();
  });

  it("mostra o conteúdo um por vez, na ordem do autor, com o ato junto dele", async () => {
    const missaoPublica: trilhaApi.MissaoPublica = {
      id: "missao-1",
      titulo: "Primeira Missão",
      posicao: 1,
      obrigatoria: true,
      e_sondagem: false,
      atividades: [],
      conteudos: [
        {
          id: "conteudo-2",
          ordem: 2,
          tipo: "texto",
          corpo: "Segundo parágrafo.",
          endereco: null,
          referencia: null,
          autoria: "propria",
          fonte: null,
        },
        {
          id: "conteudo-1",
          ordem: 1,
          tipo: "texto",
          corpo: "Primeiro parágrafo.",
          endereco: null,
          referencia: null,
          autoria: "propria",
          fonte: null,
        },
      ],
      bibliografia: [
        {
          id: "bib-1",
          titulo: "Livro X",
          capitulo: "Capítulo 1",
          disponivel: null,
          apoiador_nome: null,
        },
      ],
    };

    await renderizar(
      {
        id: "missao-1",
        titulo: "Primeira Missão",
        posicao: 1,
        obrigatoria: true,
        e_sondagem: false,
        desbloqueada: false,
        e_proxima: true,
        aguardando_mestre: false,
        motivo_do_bloqueio: null,
        desafio_de_desbloqueio: {
          tipo: "quiz",
          enunciado: null,
          perguntas: [
            {
              id: "pergunta-1",
              ordem: 1,
              enunciado: "Pergunta da missão.",
              alternativas: ["a", "b", "c", "d"],
              imagem_referencia: null,
            },
          ],
        },
      },
      missaoPublica,
    );

    const usuario = userEvent.setup();

    // A ordem é a do autor, e sai um conteúdo por vez (documento 15 §6.4).
    expect(await screen.findByText("Primeiro parágrafo.")).toBeInTheDocument();
    expect(screen.queryByText("Segundo parágrafo.")).not.toBeInTheDocument();
    expect(screen.getByText("Conteúdo 1 de 2")).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: "Próximo conteúdo" }));
    expect(screen.getByText("Segundo parágrafo.")).toBeInTheDocument();

    // O ato da missão fica no mesmo grupo do conteúdo, acima da primeira
    // linha separadora (`RF-04-73`, decisão do fundador de 2026-10-15).
    expect(screen.getByText(/Pergunta da missão\./)).toBeInTheDocument();

    // A bibliografia e o crédito saíram da missão: são do guia, e nem
    // recolhidos aparecem aqui.
    expect(screen.queryByText("Bibliografia")).not.toBeInTheDocument();
    expect(screen.queryByText("Crédito e licença")).not.toBeInTheDocument();
    expect(screen.queryByText(/Livro X/)).not.toBeInTheDocument();
  });

  it("opcional aparece marcada e fora da conta", async () => {
    await renderizar(
      {
        id: "missao-1",
        titulo: "Missão Opcional",
        posicao: 1,
        obrigatoria: false,
        e_sondagem: false,
        desbloqueada: false,
        e_proxima: true,
        aguardando_mestre: false,
        motivo_do_bloqueio: null,
        desafio_de_desbloqueio: null,
      },
      {
        id: "missao-1",
        titulo: "Missão Opcional",
        posicao: 1,
        obrigatoria: false,
        e_sondagem: false,
        atividades: [],
        conteudos: [],
        bibliografia: [],
      },
    );

    expect(await screen.findByText(/não conta no que falta/i)).toBeInTheDocument();
  });
});

// --- Conserto: a imagem e o vídeo aparecem, a referência não (`RF-05-11`)

describe("arquivo do conteúdo da missão", () => {
  function missaoComConteudo(
    conteudo: trilhaApi.ConteudoDaMissaoPublico,
  ): trilhaApi.MissaoPublica {
    return {
      id: "missao-1",
      titulo: "Primeira Missão",
      posicao: 1,
      obrigatoria: true,
      e_sondagem: false,
      atividades: [],
      conteudos: [conteudo],
      bibliografia: [],
    };
  }

  const MISSAO_ABERTA: trilhaApi.MissaoNoPercurso = {
    id: "missao-1",
    titulo: "Primeira Missão",
    posicao: 1,
    obrigatoria: true,
    e_sondagem: false,
    desbloqueada: true,
    e_proxima: false,
    aguardando_mestre: false,
    motivo_do_bloqueio: null,
    desafio_de_desbloqueio: null,
  };

  it("a imagem enviada aparece como imagem, e a referência não chega à tela", async () => {
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(() => "blob:conteudo-1"),
      revokeObjectURL: vi.fn(),
    });
    const ler = vi
      .spyOn(trilhaApi, "lerArquivoDoConteudo")
      .mockResolvedValue(new Blob(["bytes"], { type: "image/png" }));

    await renderizar(
      MISSAO_ABERTA,
      missaoComConteudo({
        id: "conteudo-1",
        ordem: 1,
        tipo: "imagem",
        corpo: null,
        endereco: null,
        referencia: "conteudos/conteudo-1/arquivo",
        autoria: "propria",
        fonte: null,
      }),
    );

    const imagem = (await screen.findByRole("img")) as HTMLImageElement;
    expect(imagem.src).toBe("blob:conteudo-1");
    expect(ler).toHaveBeenCalledWith("conteudo-1", "token-do-guerreiro");
    // A string do armazenamento nunca é o conteúdo: era ela que aparecia
    // impressa no lugar da imagem.
    expect(screen.queryByText(/conteudos\/conteudo-1\/arquivo/)).not.toBeInTheDocument();
    // A moldura de tamanho fixo é a mesma para toda mídia do núcleo
    // (`RF-05-11`, `RF-09-119`, decisão do fundador de 2026-09-17).
    expect(imagem.closest(".cg-midia-do-nucleo")).not.toBeNull();
  });

  it("o vídeo enviado aparece na mesma moldura de tamanho fixo da imagem", async () => {
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(() => "blob:conteudo-1"),
      revokeObjectURL: vi.fn(),
    });
    vi.spyOn(trilhaApi, "lerArquivoDoConteudo").mockResolvedValue(
      new Blob(["bytes"], { type: "video/mp4" }),
    );

    await renderizar(
      MISSAO_ABERTA,
      missaoComConteudo({
        id: "conteudo-1",
        ordem: 1,
        tipo: "video",
        corpo: null,
        endereco: null,
        referencia: "conteudos/conteudo-1/arquivo",
        autoria: "propria",
        fonte: null,
      }),
    );

    const video = (await screen.findByLabelText(
      /vídeo de primeira missão/i,
    )) as HTMLVideoElement;
    expect(video.tagName).toBe("VIDEO");
    expect(video.closest(".cg-midia-do-nucleo")).not.toBeNull();
  });

  it("envio não concluído não aparece quebrado nem pede bytes", async () => {
    const ler = vi.spyOn(trilhaApi, "lerArquivoDoConteudo");

    await renderizar(
      MISSAO_ABERTA,
      missaoComConteudo({
        id: "conteudo-1",
        ordem: 1,
        tipo: "video",
        corpo: null,
        endereco: null,
        referencia: null,
        autoria: "propria",
        fonte: null,
      }),
    );

    expect(screen.queryByRole("img")).not.toBeInTheDocument();
    expect(ler).not.toHaveBeenCalled();
  });

  it("o texto segue saindo do próprio conteúdo, sem pedir bytes", async () => {
    const ler = vi.spyOn(trilhaApi, "lerArquivoDoConteudo");

    await renderizar(
      MISSAO_ABERTA,
      missaoComConteudo({
        id: "conteudo-1",
        ordem: 1,
        tipo: "texto",
        corpo: "Parágrafo da missão.",
        endereco: null,
        referencia: null,
        autoria: "propria",
        fonte: null,
      }),
    );

    expect(await screen.findByText("Parágrafo da missão.")).toBeInTheDocument();
    expect(ler).not.toHaveBeenCalled();
  });
});
