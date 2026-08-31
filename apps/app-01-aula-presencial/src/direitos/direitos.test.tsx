import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TelaInicial } from "../inicio/TelaInicial";
import { TelaDeCaptura } from "../onboarding/TelaDeCaptura";
import { ProvedorDeEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";
import { AreaDetalhadaDeDireitos } from "./AreaDetalhadaDeDireitos";

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("área detalhada de direitos (RF-04-26, RN-04-06, RN-04-08, RN-04-09, RN-04-14)", () => {
  it("detalha, para cada dado coletado, a finalidade, o prazo e quem acessa", () => {
    render(<AreaDetalhadaDeDireitos aoVoltar={vi.fn()} />);

    expect(screen.getByText("Fotografia captada")).toBeInTheDocument();
    expect(
      screen.getByText(/apagada assim que o descritor é gerado — nunca sai do aparelho/i),
    ).toBeInTheDocument();
    expect(screen.getByText(/ninguém: ela não viaja pela rede/i)).toBeInTheDocument();

    expect(screen.getByText("Presença nos encontros")).toBeInTheDocument();
    expect(screen.getAllByText(/a gestão e seu responsável/i).length).toBeGreaterThan(0);
  });

  it("diz que a imagem é apagada e nunca é mostrada a ninguém", () => {
    render(<AreaDetalhadaDeDireitos aoVoltar={vi.fn()} />);

    expect(screen.getByText(/nunca sai deste aparelho/i)).toBeInTheDocument();
    expect(screen.getByText(/não vira seu avatar/i)).toBeInTheDocument();
  });

  it("diz que recusar a biometria não exclui ninguém", () => {
    render(<AreaDetalhadaDeDireitos aoVoltar={vi.fn()} />);

    expect(screen.getByText(/recusar a biometria não te tira de nada/i)).toBeInTheDocument();
  });

  it("diz o canal e o prazo do pedido de acesso, correção ou exclusão", () => {
    render(<AreaDetalhadaDeDireitos aoVoltar={vi.fn()} />);

    expect(screen.getByText(/pelo seu responsável, na app 07/i)).toBeInTheDocument();
    expect(screen.getByText(/em até 7 dias/i)).toBeInTheDocument();
  });

  it("não atende pedido de direitos ali mesmo", () => {
    render(<AreaDetalhadaDeDireitos aoVoltar={vi.fn()} />);

    expect(
      screen.getByText(/esta aplicação aqui não recebe nem responde esse tipo de pedido/i),
    ).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /pedir exclus/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /pedir acesso/i })).not.toBeInTheDocument();
  });

  it("volta para quem chamou", async () => {
    const aoVoltar = vi.fn();
    render(<AreaDetalhadaDeDireitos aoVoltar={aoVoltar} />);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /voltar/i }));

    expect(aoVoltar).toHaveBeenCalled();
  });
});

describe("aviso discreto de coleta (RF-04-26)", () => {
  it("a tela inicial traz o aviso, com caminho para a área detalhada", async () => {
    render(
      <ProvedorDeEstadoDeRede>
        <ProvedorDeSessao chaveDeArmazenamento="teste:direitos:inicio">
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

    const caminho = await screen.findByRole("button", { name: /veja o que a gente coleta/i });
    const usuario = userEvent.setup();
    await usuario.click(caminho);

    expect(await screen.findByText(/o que a gente guarda sobre você/i)).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /^voltar$/i }));
    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
  });

  it("a tela de captura traz o aviso do que está sendo coletado ali", async () => {
    render(
      <TelaDeCaptura
        tokenDeTrabalho="token-de-trabalho"
        guerreiroId="guerreiro-1"
        aoConcluir={vi.fn()}
        aoVoltar={vi.fn()}
      />,
    );

    const caminho = screen.getByRole("button", { name: /veja o que a gente coleta/i });
    const usuario = userEvent.setup();
    await usuario.click(caminho);

    expect(await screen.findByText(/o que a gente guarda sobre você/i)).toBeInTheDocument();
  });
});
