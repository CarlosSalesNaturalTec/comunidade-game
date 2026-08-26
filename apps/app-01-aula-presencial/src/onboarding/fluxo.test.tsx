import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import * as biometriaModulo from "comum/biometria";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as consentimentosApi from "../api/consentimentos";
import * as descritorApi from "../api/descritor";
import * as guerreirosApi from "../api/guerreiros";
import * as responsaveisApi from "../api/responsaveis";
import { FluxoDeOnboarding } from "./FluxoDeOnboarding";

afterEach(() => {
  vi.restoreAllMocks();
});

function renderizar(aoConcluir = vi.fn(), aoVoltar = vi.fn()) {
  return render(
    <FluxoDeOnboarding
      tokenDeTrabalho="token-de-trabalho"
      personaIdDeTrabalho="mestre-1"
      aulaId="aula-1"
      aoConcluir={aoConcluir}
      aoVoltar={aoVoltar}
    />,
  );
}

async function preencherCadastroDoGuerreiro() {
  const usuario = userEvent.setup();
  await usuario.type(screen.getByLabelText(/^nome$/i), "Zeferina");
  await usuario.type(screen.getByLabelText(/^nick$/i), "ZeferinaGuerreira");
  await usuario.type(screen.getByLabelText(/data de nascimento/i), "2016-01-01");
  await usuario.type(screen.getByLabelText(/características do avatar/i), "trança-e-capa");
  await usuario.click(screen.getByRole("button", { name: /concluir cadastro/i }));
  return usuario;
}

describe("fluxo de onboarding — jornada 5.2", () => {
  it("aparelho sem câmera conclui o cadastro ativo e sem imagem, sem pedir responsável", async () => {
    vi.spyOn(guerreirosApi, "cadastrarGuerreiroNoEncontro").mockResolvedValue({
      id: "guerreiro-1",
      nome: "Zeferina",
      nascimento: "2016-01-01",
      nick: "ZeferinaGuerreira",
      avatar: "opaco",
    });
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(false);
    const cadastrarResponsavel = vi.spyOn(responsaveisApi, "cadastrarResponsavelNoEncontro");
    const aoConcluir = vi.fn();
    renderizar(aoConcluir);

    await preencherCadastroDoGuerreiro();

    expect(await screen.findByText(/cadastro concluído/i)).toBeInTheDocument();
    expect(screen.getByText(/exige um aparelho com câmera/i)).toBeInTheDocument();
    expect(cadastrarResponsavel).not.toHaveBeenCalled();

    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /^concluir$/i }));
    expect(aoConcluir).toHaveBeenCalled();
  });

  it("a cadeia inteira: guerreiro, responsável, termo e captura", async () => {
    vi.spyOn(guerreirosApi, "cadastrarGuerreiroNoEncontro").mockResolvedValue({
      id: "guerreiro-1",
      nome: "Zeferina",
      nascimento: "2016-01-01",
      nick: "ZeferinaGuerreira",
      avatar: "opaco",
    });
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(responsaveisApi, "cadastrarResponsavelNoEncontro").mockResolvedValue({
      id: "responsavel-1",
      nome: "Maria",
    });
    vi.spyOn(responsaveisApi, "criarVinculo").mockResolvedValue({
      id: "vinculo-1",
      responsavel_id: "responsavel-1",
      guerreiro_id: "guerreiro-1",
      grau_de_parentesco: "mãe",
      inicio: new Date().toISOString(),
    });
    const registrarConsentimento = vi
      .spyOn(consentimentosApi, "registrarConsentimento")
      .mockResolvedValue({ id: "consentimento-1", registrado_em: new Date().toISOString() });
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2]);
    const enviarDescritor = vi.spyOn(descritorApi, "enviarDescritor").mockResolvedValue({
      guerreiro_id: "guerreiro-1",
      gravado_em: new Date().toISOString(),
    });
    const aoConcluir = vi.fn();
    renderizar(aoConcluir);

    const usuario = await preencherCadastroDoGuerreiro();

    await usuario.type(await screen.findByLabelText(/nome do responsável/i), "Maria");
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "mãe");
    await usuario.click(screen.getByRole("button", { name: /continuar para o termo/i }));

    expect(await screen.findByText(/termo de consentimento/i)).toBeInTheDocument();
    // A câmera não abre enquanto a confirmação não é dada — a tela de
    // captura ainda não existe no documento.
    expect(screen.queryByRole("button", { name: /iniciar captura/i })).not.toBeInTheDocument();

    await usuario.click(
      screen.getByRole("button", { name: /confirmo: o termo impresso foi assinado/i }),
    );
    expect(registrarConsentimento).toHaveBeenCalledWith(
      expect.objectContaining({ testemunha_id: "mestre-1", origem: "impressa" }),
      "token-de-trabalho",
    );

    await usuario.click(await screen.findByRole("button", { name: /iniciar captura/i }));

    expect(enviarDescritor).toHaveBeenCalledWith(
      "guerreiro-1",
      { descritor: [0.1, 0.2] },
      "token-de-trabalho",
    );
    await vi.waitFor(() => expect(aoConcluir).toHaveBeenCalled());
  });

  it("retomada: falha no envio do descritor não volta ao termo nem recadastra o consentimento", async () => {
    vi.spyOn(guerreirosApi, "cadastrarGuerreiroNoEncontro").mockResolvedValue({
      id: "guerreiro-1",
      nome: "Zeferina",
      nascimento: "2016-01-01",
      nick: "ZeferinaGuerreira",
      avatar: "opaco",
    });
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(responsaveisApi, "cadastrarResponsavelNoEncontro").mockResolvedValue({
      id: "responsavel-1",
      nome: "Maria",
    });
    vi.spyOn(responsaveisApi, "criarVinculo").mockResolvedValue({
      id: "vinculo-1",
      responsavel_id: "responsavel-1",
      guerreiro_id: "guerreiro-1",
      grau_de_parentesco: "mãe",
      inicio: new Date().toISOString(),
    });
    const registrarConsentimento = vi
      .spyOn(consentimentosApi, "registrarConsentimento")
      .mockResolvedValue({ id: "consentimento-1", registrado_em: new Date().toISOString() });
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2]);
    vi.spyOn(descritorApi, "enviarDescritor").mockRejectedValueOnce(new Error("rede caiu"));

    renderizar();
    const usuario = await preencherCadastroDoGuerreiro();
    await usuario.type(await screen.findByLabelText(/nome do responsável/i), "Maria");
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "mãe");
    await usuario.click(screen.getByRole("button", { name: /continuar para o termo/i }));
    await usuario.click(
      await screen.findByRole("button", { name: /confirmo: o termo impresso foi assinado/i }),
    );
    await usuario.click(await screen.findByRole("button", { name: /iniciar captura/i }));
    await screen.findByRole("alert");

    expect(registrarConsentimento).toHaveBeenCalledTimes(1);
    expect(screen.queryByText(/termo de consentimento/i)).not.toBeInTheDocument();
  });
});
