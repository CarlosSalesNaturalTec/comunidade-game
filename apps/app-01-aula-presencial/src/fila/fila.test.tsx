import { render, renderHook, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import type { ReactNode } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as presencasApi from "../api/presencas";
import * as sessoesDeGuerreiroApi from "../api/sessoesDeGuerreiro";
import { TelaDeEntradaDoGuerreiro } from "../entrada/TelaDeEntradaDoGuerreiro";
import { TelaInicial } from "../inicio/TelaInicial";
import { guardarVerificadorDeTeste } from "../pin/paraTestes";
import { pinBloqueadoNoAparelho } from "../pin/pinDeConfirmacao";
import { ProvedorDeEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";
import {
  enfileirarPresenca,
  lerFilaDePresenca,
  removerDaFilaDePresenca,
} from "./filaDePresenca";
import { useSincronizacaoDaFilaDePresenca } from "./sincronizacao";

function envolver({ children }: { children: ReactNode }) {
  return <ProvedorDeEstadoDeRede>{children}</ProvedorDeEstadoDeRede>;
}

afterEach(() => {
  vi.restoreAllMocks();
  localStorage.clear();
  sessionStorage.clear();
});

describe("fila local de presença — armazenamento (RF-04-23, RN-04-12, RN-04-13)", () => {
  it("enfileira, lê e remove só os três campos de presença", () => {
    enfileirarPresenca({
      aula_id: "aula-1",
      nick: "zeferina",
      momento_do_fato: "2026-08-30T14:00:00Z",
    });

    const itens = lerFilaDePresenca("aula-1");
    expect(itens).toHaveLength(1);
    expect(Object.keys(itens[0]).sort()).toEqual(["aula_id", "momento_do_fato", "nick"]);

    const bruto = localStorage.getItem("app-01:fila-de-presenca:aula-1");
    expect(bruto).not.toBeNull();
    expect(JSON.parse(bruto as string)).toEqual([
      { aula_id: "aula-1", nick: "zeferina", momento_do_fato: "2026-08-30T14:00:00Z" },
    ]);

    removerDaFilaDePresenca(itens[0]);
    expect(lerFilaDePresenca("aula-1")).toHaveLength(0);
  });

  it("cada aula tem sua própria fila", () => {
    enfileirarPresenca({ aula_id: "aula-1", nick: "zeferina", momento_do_fato: "t1" });
    enfileirarPresenca({ aula_id: "aula-2", nick: "joao", momento_do_fato: "t2" });

    expect(lerFilaDePresenca("aula-1")).toEqual([
      { aula_id: "aula-1", nick: "zeferina", momento_do_fato: "t1" },
    ]);
    expect(lerFilaDePresenca("aula-2")).toEqual([
      { aula_id: "aula-2", nick: "joao", momento_do_fato: "t2" },
    ]);
  });
});

describe("entrada do Guerreiro(a) sem rede — enfileira em vez de perder (RF-04-23)", () => {
  it("a criança que chega sem rede entra na fila, sem abrir sessão", async () => {
    await guardarVerificadorDeTeste();
    const confirmar = vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro");

    render(
      <ProvedorDeEstadoDeRede>
        <ProvedorDeSessao chaveDeArmazenamento="teste:fila:guerreiro">
          <TelaDeEntradaDoGuerreiro
            tokenDeTrabalho="token-de-trabalho"
            aulaId="aula-1"
            caminho="presenca"
            aoVoltar={vi.fn()}
          />
        </ProvedorDeSessao>
      </ProvedorDeEstadoDeRede>,
    );
    window.dispatchEvent(new Event("offline"));
    await screen.findByText(/entrada por reconhecimento facial não funciona/i);

    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.type(screen.getByLabelText(/pin de quem confirma/i), "4821");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    expect(await screen.findByText(/presença de zeferina foi guardada/i)).toBeInTheDocument();
    expect(confirmar).not.toHaveBeenCalled();

    const itens = lerFilaDePresenca("aula-1");
    expect(itens).toHaveLength(1);
    expect(itens[0].nick).toBe("zeferina");
  });

  it("sem rede a entrada por reconhecimento não é oferecida", async () => {
    render(
      <ProvedorDeEstadoDeRede>
        <ProvedorDeSessao chaveDeArmazenamento="teste:fila:guerreiro2">
          <TelaDeEntradaDoGuerreiro
            tokenDeTrabalho="token-de-trabalho"
            aulaId="aula-1"
            caminho="presenca"
            aoVoltar={vi.fn()}
          />
        </ProvedorDeSessao>
      </ProvedorDeEstadoDeRede>,
    );
    window.dispatchEvent(new Event("offline"));

    expect(
      await screen.findByText(/entrada por reconhecimento facial não funciona/i),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /confirmar identidade/i })).toBeInTheDocument();
  });
});

describe("PIN conferido no aparelho sem rede (RF-04-23, RN-04-38)", () => {
  function renderizarSemRede() {
    render(
      <ProvedorDeEstadoDeRede>
        <ProvedorDeSessao chaveDeArmazenamento="teste:fila:pin">
          <TelaDeEntradaDoGuerreiro
            tokenDeTrabalho="token-de-trabalho"
            aulaId="aula-1"
            caminho="presenca"
            aoVoltar={vi.fn()}
          />
        </ProvedorDeSessao>
      </ProvedorDeEstadoDeRede>,
    );
    window.dispatchEvent(new Event("offline"));
  }

  async function tentar(usuario: ReturnType<typeof userEvent.setup>, pin: string) {
    await usuario.type(screen.getByLabelText(/pin de quem confirma/i), pin);
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));
  }

  it("PIN errado sem rede não enfileira", async () => {
    await guardarVerificadorDeTeste();
    renderizarSemRede();
    await screen.findByText(/entrada por reconhecimento facial não funciona/i);
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");

    await tentar(usuario, "0000");

    expect(await screen.findByText(/pin errado/i)).toBeInTheDocument();
    expect(lerFilaDePresenca("aula-1")).toHaveLength(0);
  });

  it("o quinto erro seguido sem rede bloqueia o aparelho", async () => {
    await guardarVerificadorDeTeste();
    renderizarSemRede();
    await screen.findByText(/entrada por reconhecimento facial não funciona/i);
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");

    for (let tentativa = 0; tentativa < 5; tentativa += 1) {
      await tentar(usuario, "0000");
      await waitFor(() =>
        expect(screen.getByLabelText(/pin de quem confirma/i)).toHaveValue(""),
      );
    }

    expect(await screen.findByText(/entre outra vez pelo google/i)).toBeInTheDocument();
    expect(pinBloqueadoNoAparelho()).toBe(true);
    await usuario.type(screen.getByLabelText(/pin de quem confirma/i), "4821");
    expect(screen.getByRole("button", { name: /confirmar identidade/i })).toBeDisabled();
    expect(lerFilaDePresenca("aula-1")).toHaveLength(0);
  });

  it("sem verificador, a confirmação sem rede fica indisponível e diz por quê", async () => {
    renderizarSemRede();
    await screen.findByText(/entrada por reconhecimento facial não funciona/i);
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");

    await tentar(usuario, "4821");

    expect(await screen.findByText(/aberto sem pin cadastrado/i)).toBeInTheDocument();
    expect(lerFilaDePresenca("aula-1")).toHaveLength(0);
  });
});

describe("sincronização automática da fila (RF-04-25, RN-04-13)", () => {
  function mockarPresencaSemRede(momentoDoFato: string) {
    return vi.spyOn(presencasApi, "registrarPresencaSemRede").mockImplementation((aulaId) =>
      Promise.resolve({
        id: "presenca-1",
        aula_id: aulaId,
        guerreiro_id: "guerreiro-1",
        modo: "confirmacao",
        confirmador_id: "mestre-1",
        momento_do_fato: momentoDoFato,
      }),
    );
  }

  it("sincroniza sozinha ao montar, preservando a hora do fato original", async () => {
    enfileirarPresenca({
      aula_id: "aula-1",
      nick: "zeferina",
      momento_do_fato: "2026-08-30T14:00:00Z",
    });
    const registrar = mockarPresencaSemRede("2026-08-30T14:00:00Z");

    renderHook(() => useSincronizacaoDaFilaDePresenca("aula-1", "token-de-trabalho"), {
      wrapper: envolver,
    });

    await waitFor(() => expect(registrar).toHaveBeenCalled());
    expect(registrar).toHaveBeenCalledWith(
      "aula-1",
      { nick: "zeferina", momento_do_fato: "2026-08-30T14:00:00Z" },
      "token-de-trabalho",
    );
    await waitFor(() => expect(lerFilaDePresenca("aula-1")).toHaveLength(0));
  });

  it("a sincronização não abre sessão de Guerreiro(a)", async () => {
    enfileirarPresenca({ aula_id: "aula-1", nick: "zeferina", momento_do_fato: "t1" });
    const registrar = mockarPresencaSemRede("t1");
    const confirmar = vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro");
    const eu = vi.spyOn(autenticacaoApi, "eu");

    renderHook(() => useSincronizacaoDaFilaDePresenca("aula-1", "token-de-trabalho"), {
      wrapper: envolver,
    });

    await waitFor(() => expect(registrar).toHaveBeenCalled());
    expect(confirmar).not.toHaveBeenCalled();
    expect(eu).not.toHaveBeenCalled();
  });

  it("o reenvio que devolve o registro já existente é sucesso — some da fila sem erro", async () => {
    enfileirarPresenca({
      aula_id: "aula-1",
      nick: "zeferina",
      momento_do_fato: "2026-08-30T14:00:00Z",
    });
    // O núcleo devolve o registro já existente, com o momento original —
    // sucesso, não duplicação (`RF-04-25`).
    mockarPresencaSemRede("2026-08-30T14:00:00Z");

    const { result } = renderHook(
      () => useSincronizacaoDaFilaDePresenca("aula-1", "token-de-trabalho"),
      { wrapper: envolver },
    );

    await waitFor(() => expect(result.current.itens).toHaveLength(0));
  });

  it("falha de dado (nick errado) marca o item como falho, sem derrubar a rede", async () => {
    enfileirarPresenca({ aula_id: "aula-1", nick: "nick-errado", momento_do_fato: "t1" });
    vi.spyOn(presencasApi, "registrarPresencaSemRede").mockRejectedValue(
      new ErroDaApi(401, {
        codigo: "confirmacao_de_guerreiro_recusada",
        mensagem: "Não foi possível confirmar esse nick.",
      }),
    );

    const { result } = renderHook(
      () => useSincronizacaoDaFilaDePresenca("aula-1", "token-de-trabalho"),
      { wrapper: envolver },
    );

    await waitFor(() => expect(result.current.itens[0]?.falhou).toBe(true));
    // O item continua na fila do aparelho — só marcado como falho, para o
    // Mestre tentar de novo (design — Risks).
    expect(lerFilaDePresenca("aula-1")).toHaveLength(1);
  });

  it("o Mestre tenta de novo um item que falhou", async () => {
    enfileirarPresenca({ aula_id: "aula-1", nick: "zeferina", momento_do_fato: "t1" });
    vi.spyOn(presencasApi, "registrarPresencaSemRede")
      .mockRejectedValueOnce(new Error("rede caiu"))
      .mockResolvedValueOnce({
        id: "presenca-1",
        aula_id: "aula-1",
        guerreiro_id: "guerreiro-1",
        modo: "confirmacao",
        confirmador_id: "mestre-1",
        momento_do_fato: "t1",
      });

    const { result } = renderHook(
      () => useSincronizacaoDaFilaDePresenca("aula-1", "token-de-trabalho"),
      { wrapper: envolver },
    );
    await waitFor(() => expect(result.current.itens[0]?.falhou).toBe(true));

    await result.current.tentarDeNovo(result.current.itens[0]);

    await waitFor(() => expect(result.current.itens).toHaveLength(0));
  });
});

describe("painel do Mestre — visibilidade da fila (RF-04-23, RN-04-14)", () => {
  it("o Mestre vê a lista de pendências na tela inicial, com nick e hora", async () => {
    enfileirarPresenca({
      aula_id: "aula-1",
      nick: "zeferina",
      momento_do_fato: "2026-08-30T14:00:00Z",
    });

    render(
      <ProvedorDeEstadoDeRede>
        <ProvedorDeSessao chaveDeArmazenamento="teste:fila:hub">
          <TelaInicial
            tokenDeTrabalho="token-de-trabalho"
            personaIdDeTrabalho="mestre-1"
            papelDeTrabalho="mestre"
            aulaId="aula-1"
            aoVoltarAoInicio={vi.fn()}
            podeAbrirMomentoDeTroca={false}
            momentoDeTrocaAberto={false}
            abrindoMomentoDeTroca={false}
            erroDeAberturaDaTroca={null}
            aoAbrirMomentoDeTroca={vi.fn()}
            aoFecharMomentoDeTroca={vi.fn()}
          />
        </ProvedorDeSessao>
      </ProvedorDeEstadoDeRede>,
    );

    expect(await screen.findByText("zeferina")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /tentar de novo/i })).toBeInTheDocument();
  });

  it("a lista some ao entrar num caminho de atendimento do Guerreiro(a)", async () => {
    enfileirarPresenca({ aula_id: "aula-1", nick: "zeferina", momento_do_fato: "t1" });

    render(
      <ProvedorDeEstadoDeRede>
        <ProvedorDeSessao chaveDeArmazenamento="teste:fila:hub2">
          <TelaInicial
            tokenDeTrabalho="token-de-trabalho"
            personaIdDeTrabalho="mestre-1"
            papelDeTrabalho="mestre"
            aulaId="aula-1"
            aoVoltarAoInicio={vi.fn()}
            podeAbrirMomentoDeTroca={false}
            momentoDeTrocaAberto={false}
            abrindoMomentoDeTroca={false}
            erroDeAberturaDaTroca={null}
            aoAbrirMomentoDeTroca={vi.fn()}
            aoFecharMomentoDeTroca={vi.fn()}
          />
        </ProvedorDeSessao>
      </ProvedorDeEstadoDeRede>,
    );
    await screen.findByText("zeferina");

    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /presença — entrar/i }));

    expect(await screen.findByText(/quem está chegando/i)).toBeInTheDocument();
    expect(screen.queryByText("zeferina")).not.toBeInTheDocument();
    expect(screen.queryByText(/fila de presença/i)).not.toBeInTheDocument();
  });
});
