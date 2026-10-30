import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { ProvedorDeSessao } from "comum/autenticacao";
import { ProvedorDeNarracao } from "comum/narracao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { PendenciaDeEntrega } from "../api/entregasPendentes";
import * as entregasApi from "../api/entregasPendentes";
import { TelaInicial } from "../inicio/TelaInicial";
import { ProvedorDeEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";
import { TelaDeEntregasDoEncontro } from "./TelaDeEntregasDoEncontro";

const PENDENCIA: PendenciaDeEntrega = {
  guerreiro_id: "guerreiro-1",
  guerreiro_nick: "zeferina",
  guerreiro_avatar: "onca",
  trilha_id: "trilha-1",
  trilha_nome: "Território Vivo",
  missao_id: "missao-1",
  missao_titulo: "Mapear a praça",
  recompensa_de_marco_id: "recompensa-1",
  tipo_de_recurso_id: "tipo-1",
  tipo_de_recurso_nome: "Kit de robótica",
  tipo_de_recurso_unidade: "unidade",
  quantidade: "1.00",
  quantidade_esgotada: false,
};

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
  localStorage.clear();
});

function renderizarTela() {
  return render(
    <TelaDeEntregasDoEncontro
      tokenDeTrabalho="token-de-trabalho"
      aulaId="aula-1"
      aoVoltar={vi.fn()}
    />,
  );
}

function renderizarTelaInicial(papelDeTrabalho: string) {
  return render(
    <ProvedorDeNarracao>
      <ProvedorDeEstadoDeRede>
        <ProvedorDeSessao chaveDeArmazenamento="teste:app-01:sessao-guerreiro">
          <TelaInicial
            tokenDeTrabalho="token-de-trabalho"
            personaIdDeTrabalho="persona-de-trabalho-1"
            papelDeTrabalho={papelDeTrabalho}
            aulaId="aula-1"
            aoVoltarAoInicio={vi.fn()}
            podeAbrirMomentoDeTroca={false}
            momentoDeTrocaAberto={false}
            abrindoMomentoDeTroca={false}
            erroDeAberturaDaTroca={null}
            aoAbrirMomentoDeTroca={vi.fn()}
            aoFecharMomentoDeTroca={vi.fn()}
            aoEncerrarSessaoDeTrabalho={vi.fn()}
          />
        </ProvedorDeSessao>
      </ProvedorDeEstadoDeRede>
    </ProvedorDeNarracao>,
  );
}

// O cartão é do Mestre, no molde da chave do momento de troca: o Admin nunca
// confirma entrega (`RF-04-71`, `RF-04-49`, `RN-02-17`, design — decisão 4).
describe("o caminho das entregas na tela inicial (RF-04-71, RN-02-17)", () => {
  it("aparece ao Mestre, entre a chave da troca e o encerramento", async () => {
    renderizarTelaInicial("mestre");

    await screen.findByText(/o que você quer fazer/i);
    const grupo = screen.getByRole("group", { name: "Para quem opera o aparelho" });
    const cartao = screen.getByRole("button", { name: /entregas pendentes do encontro/i });

    expect(grupo).toContainElement(cartao);
    // No mesmo padrão dos demais, com glifo ao lado do rótulo.
    expect(cartao.querySelector("svg")).not.toBeNull();
    const cartoes = Array.from(document.querySelectorAll(".cg-caminho"));
    expect(cartoes[cartoes.length - 2]).toBe(cartao);
    expect(cartoes[cartoes.length - 1].textContent).toMatch(/encerrar a sessão de trabalho/i);
  });

  it("não aparece ao Admin, e o encerramento segue por último", async () => {
    renderizarTelaInicial("admin");

    await screen.findByText(/o que você quer fazer/i);
    expect(
      screen.queryByRole("button", { name: /entregas pendentes do encontro/i }),
    ).not.toBeInTheDocument();
    const cartoes = Array.from(document.querySelectorAll(".cg-caminho"));
    expect(cartoes[cartoes.length - 1].textContent).toMatch(/encerrar a sessão de trabalho/i);
  });

  it("o cartão leva à fila do encontro, recortada por esta aula", async () => {
    const listar = vi
      .spyOn(entregasApi, "listarEntregasPendentesDoEncontro")
      .mockResolvedValue([PENDENCIA]);
    const usuario = userEvent.setup();
    renderizarTelaInicial("mestre");

    await screen.findByText(/o que você quer fazer/i);
    await usuario.click(
      screen.getByRole("button", { name: /entregas pendentes do encontro/i }),
    );

    expect(await screen.findByText(/zeferina/i)).toBeInTheDocument();
    expect(listar).toHaveBeenCalledWith("aula-1", "token-de-trabalho");
  });
});

describe("a fila do encontro na App 01 (RF-09-75, RF-09-76)", () => {
  it("quem chegou e conquistou aparece com nick, avatar, trilha, marco e recurso", async () => {
    vi.spyOn(entregasApi, "listarEntregasPendentesDoEncontro").mockResolvedValue([PENDENCIA]);
    renderizarTela();

    const item = await screen.findByText(/zeferina/i);
    const linha = item.closest("li") as HTMLElement;
    expect(linha.textContent).toContain("onca");
    expect(linha.textContent).toContain("Território Vivo");
    expect(linha.textContent).toContain("Mapear a praça");
    expect(linha.textContent).toContain("Kit de robótica");
    expect(linha.textContent).toContain("1.00");
  });

  it("não apresenta valor em moedas nem em reais", async () => {
    vi.spyOn(entregasApi, "listarEntregasPendentesDoEncontro").mockResolvedValue([PENDENCIA]);
    renderizarTela();

    await screen.findByText(/zeferina/i);
    expect(document.body.textContent).not.toMatch(/moeda|R\$/i);
  });

  it("o encontro sem pendência alguma diz que não há, sem erro", async () => {
    vi.spyOn(entregasApi, "listarEntregasPendentesDoEncontro").mockResolvedValue([]);
    renderizarTela();

    expect(
      await screen.findByText(/nenhuma entrega pendente neste encontro/i),
    ).toBeInTheDocument();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  // A aula já declara o ponto de apoio obrigatoriamente (`RF-01-71`): no
  // encontro não há o que escolher (`RF-09-76`, documento 02 §8.1).
  it("nenhum seletor de ponto de apoio é oferecido", async () => {
    vi.spyOn(entregasApi, "listarEntregasPendentesDoEncontro").mockResolvedValue([PENDENCIA]);
    renderizarTela();

    await screen.findByText(/zeferina/i);
    expect(screen.queryByRole("combobox")).not.toBeInTheDocument();
    expect(document.body.textContent).not.toMatch(/ponto de apoio.*selecione/i);
  });

  it("a confirmação declara a aula, e a fila é relida depois dela", async () => {
    const listar = vi
      .spyOn(entregasApi, "listarEntregasPendentesDoEncontro")
      .mockResolvedValueOnce([PENDENCIA])
      .mockResolvedValueOnce([]);
    const confirmar = vi.spyOn(entregasApi, "confirmarEntregaNoEncontro").mockResolvedValue({
      id: "entrega-1",
      recompensa_de_marco_id: "recompensa-1",
      guerreiro_id: "guerreiro-1",
      ponto_de_apoio_id: "ponto-da-aula-1",
      lancamento_id: "lancamento-1",
      registrado_em: new Date().toISOString(),
    });
    const usuario = userEvent.setup();
    renderizarTela();

    await screen.findByText(/zeferina/i);
    await usuario.click(screen.getByRole("button", { name: /confirmar entrega/i }));

    await waitFor(() =>
      expect(screen.getByText(/nenhuma entrega pendente neste encontro/i)).toBeInTheDocument(),
    );
    expect(confirmar).toHaveBeenCalledWith(
      "recompensa-1",
      { guerreiro_id: "guerreiro-1", aula_id: "aula-1" },
      "token-de-trabalho",
    );
    expect(listar).toHaveBeenCalledTimes(2);
  });

  it("a recusa do núcleo é apresentada como ela vem", async () => {
    vi.spyOn(entregasApi, "listarEntregasPendentesDoEncontro").mockResolvedValue([PENDENCIA]);
    vi.spyOn(entregasApi, "confirmarEntregaNoEncontro").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Lastro insuficiente no ponto de apoio informado para esta entrega.",
      }),
    );
    const usuario = userEvent.setup();
    renderizarTela();

    await screen.findByText(/zeferina/i);
    await usuario.click(screen.getByRole("button", { name: /confirmar entrega/i }));

    expect(
      await screen.findByText(/lastro insuficiente no ponto de apoio/i),
    ).toBeInTheDocument();
  });
});
