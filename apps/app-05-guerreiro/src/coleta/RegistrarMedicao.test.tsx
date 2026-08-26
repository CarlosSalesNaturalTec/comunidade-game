import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as coletaApi from "../api/coleta";
import { RegistrarMedicao } from "./RegistrarMedicao";

const CHAVE_DE_SESSAO = "app-05:teste-registrar-medicao";

const SERIE_NUMERICA: coletaApi.SerieDoGuerreiro = {
  id: "serie-1",
  desafio_de_coleta_id: "desafio-1",
  local_id: "local-1",
  comunidade_virtual_id: "comunidade-1",
  cadencia: "semanal",
  estado: "ativa",
  pontos: 0,
  proxima_medicao: null,
  tipo_de_coleta: { nome: "Temperatura", forma_de_registro: "numero", unidade: "°C" },
};

const SERIE_DE_FOTO: coletaApi.SerieDoGuerreiro = {
  ...SERIE_NUMERICA,
  tipo_de_coleta: { nome: "Foto do ponto", forma_de_registro: "foto", unidade: null },
};

async function renderizar(
  serie: coletaApi.SerieDoGuerreiro,
  aoConcluir: () => void = () => {},
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
        <RegistrarMedicao serie={serie} aoConcluir={aoConcluir} />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
  Object.defineProperty(window.navigator, "onLine", { value: true, configurable: true });
});

describe("registro de medição", () => {
  it("valor digitado grava origem manual", async () => {
    const registrar = vi.spyOn(coletaApi, "registrarMedicao").mockResolvedValue({
      id: "registro-1",
      serie_de_coleta_id: SERIE_NUMERICA.id,
      valor: 25,
      unidade: "°C",
      origem: "manual",
      situacao: "valida",
      a_conferir: false,
      comunidade_virtual_id: "comunidade-1",
      pontos_creditados: 5,
      pontuou: true,
      momento_do_fato: new Date().toISOString(),
      momento_do_registro: new Date().toISOString(),
    });

    await renderizar(SERIE_NUMERICA);
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/valor/i), "25");
    await usuario.click(screen.getByRole("button", { name: /gravar medição/i }));

    await vi.waitFor(() =>
      expect(registrar).toHaveBeenCalledWith(
        expect.objectContaining({ origem: "manual", valor: 25, unidade: "°C" }),
        "token-do-guerreiro",
      ),
    );
  });

  it("ditado por voz grava origem voz, e o áudio nunca é enviado", async () => {
    class ReconhecimentoFalso {
      lang = "";
      onresult: ((evento: unknown) => void) | null = null;
      onerror: (() => void) | null = null;
      onend: (() => void) | null = null;
      start() {
        this.onresult?.({ results: { 0: { 0: { transcript: "vinte e cinco 25" } } } });
      }
    }
    (window as unknown as { SpeechRecognition: unknown }).SpeechRecognition =
      ReconhecimentoFalso;

    const registrar = vi.spyOn(coletaApi, "registrarMedicao").mockResolvedValue({
      id: "registro-1",
      serie_de_coleta_id: SERIE_NUMERICA.id,
      valor: 25,
      unidade: "°C",
      origem: "voz",
      situacao: "valida",
      a_conferir: false,
      comunidade_virtual_id: "comunidade-1",
      pontos_creditados: 5,
      pontuou: true,
      momento_do_fato: new Date().toISOString(),
      momento_do_registro: new Date().toISOString(),
    });

    await renderizar(SERIE_NUMERICA);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /falar o valor/i }));
    await usuario.click(screen.getByRole("button", { name: /gravar medição/i }));

    await vi.waitFor(() =>
      expect(registrar).toHaveBeenCalledWith(
        expect.objectContaining({ origem: "voz", valor: 25 }),
        "token-do-guerreiro",
      ),
    );
    const argumentosDoEnvio = registrar.mock.calls[0][0];
    expect(argumentosDoEnvio.midia).toBeUndefined();
    expect(
      (window as unknown as { SpeechRecognition: unknown }).SpeechRecognition,
    ).toBeDefined();
    delete (window as unknown as { SpeechRecognition?: unknown }).SpeechRecognition;
  });

  it("tipo de mídia pede a foto como o próprio registro, não pede valor numérico", async () => {
    await renderizar(SERIE_DE_FOTO);

    expect(screen.queryByLabelText(/^valor/i)).not.toBeInTheDocument();
    expect(await screen.findByLabelText(/envie uma foto/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /gravar medição/i })).toBeDisabled();
  });

  it("registro fora da faixa entra a conferir, explicado sem acusação", async () => {
    vi.spyOn(coletaApi, "registrarMedicao").mockResolvedValue({
      id: "registro-1",
      serie_de_coleta_id: SERIE_NUMERICA.id,
      valor: 999,
      unidade: "°C",
      origem: "manual",
      situacao: "valida",
      a_conferir: true,
      comunidade_virtual_id: "comunidade-1",
      pontos_creditados: 0,
      pontuou: false,
      momento_do_fato: new Date().toISOString(),
      momento_do_registro: new Date().toISOString(),
    });

    await renderizar(SERIE_NUMERICA);
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/valor/i), "999");
    await usuario.click(screen.getByRole("button", { name: /gravar medição/i }));

    const devolutiva = await screen.findByRole("status");
    expect(devolutiva).toHaveTextContent(/mestre vai dar uma olhada/i);
    expect(devolutiva.textContent).not.toMatch(/erro|inválid|falh/i);
  });

  it("sem rede, o registro é recusado na hora e nada é enviado", async () => {
    Object.defineProperty(window.navigator, "onLine", { value: false, configurable: true });
    const registrar = vi.spyOn(coletaApi, "registrarMedicao");

    await renderizar(SERIE_NUMERICA);
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/valor/i), "25");
    await usuario.click(screen.getByRole("button", { name: /gravar medição/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/sem internet/i);
    expect(registrar).not.toHaveBeenCalled();
  });
});
