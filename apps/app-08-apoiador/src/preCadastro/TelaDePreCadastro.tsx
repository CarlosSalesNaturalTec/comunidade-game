import { ErroDaApi } from "comum/api";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type ChangeEvent, type FormEvent, useEffect, useState } from "react";
import { URL_DO_FORMULARIO_DA_VITRINE } from "../api/configuracao";
import {
  ESCADA_POR_PERFIL,
  formatarMoedas,
  type PerfilDeApoiador,
} from "../compartilhado/escada";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import {
  listarMissoesAbertas,
  listarNecessidadesEmAberto,
  type MissaoDoApoiador,
  type NecessidadeDeRecurso,
  registrarPreCadastroDeApoiador,
} from "./api";

const FORMATOS_ACEITOS = "PDF, JPG ou PNG";

type FormaDeAporte = "missao" | "necessidade" | "escada" | "livre" | "sem_dinheiro";

interface Props {
  /** Caminho de volta para quem já tem cadastro (design — decisão 1). */
  aoIrParaEntrada: () => void;
}

function formatarDataDaAula(isoDeInicio: string): string {
  const data = new Date(isoDeInicio);
  return Number.isNaN(data.getTime())
    ? isoDeInicio
    : data.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric" });
}

function tempoDeEsperaEmLinguagemSimples(segundos: number): string {
  if (segundos < 60) return `${segundos} segundo${segundos === 1 ? "" : "s"}`;
  const minutos = Math.ceil(segundos / 60);
  return `${minutos} minuto${minutos === 1 ? "" : "s"}`;
}

// A porta pública inteira: apresentação, pré-cadastro sem documento, as três
// formas de declarar o aporte em dinheiro — cada uma com o equivalente em
// moedas —, o comprovante obrigatório e o encaminhamento de quem apoia sem
// dinheiro (`RF-14-01` a `RF-14-07`, PRD-14 §5.1).
export function TelaDePreCadastro({ aoIrParaEntrada }: Props) {
  const [nomeOuRazaoSocial, definirNomeOuRazaoSocial] = useState("");
  const [email, definirEmail] = useState("");
  const [whatsapp, definirWhatsapp] = useState("");
  const [nick, definirNick] = useState("");
  const [perfil, definirPerfil] = useState<PerfilDeApoiador>("pessoa_fisica");

  const [formaDeAporte, definirFormaDeAporte] = useState<FormaDeAporte>("escada");
  const [missoes, definirMissoes] = useState<MissaoDoApoiador[]>([]);
  const [missaoSelecionadaId, definirMissaoSelecionadaId] = useState("");
  const [necessidades, definirNecessidades] = useState<NecessidadeDeRecurso[]>([]);
  const [necessidadeSelecionadaId, definirNecessidadeSelecionadaId] = useState("");
  const [degrauSelecionado, definirDegrauSelecionado] = useState(0);
  const [valorLivreTexto, definirValorLivreTexto] = useState("");
  const [comprovante, definirComprovante] = useState<File | null>(null);

  const [enviando, definirEnviando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [tempoDeEspera, definirTempoDeEspera] = useState<string | null>(null);
  const [sucesso, definirSucesso] = useState(false);

  useEffect(() => {
    listarNecessidadesEmAberto()
      .then(definirNecessidades)
      .catch(() => definirNecessidades([]));
    listarMissoesAbertas()
      .then(definirMissoes)
      .catch(() => definirMissoes([]));
  }, []);

  const escada = ESCADA_POR_PERFIL[perfil];
  const missaoSelecionada = missoes.find((m) => m.id === missaoSelecionadaId);
  const necessidadeSelecionada = necessidades.find(
    (n) => n.aula_id === necessidadeSelecionadaId,
  );
  const valorLivreEmReais = Number(valorLivreTexto.replace(",", "."));
  const valorLivreValido = valorLivreTexto.trim() !== "" && !Number.isNaN(valorLivreEmReais);

  function compoeAporteDeclarado(): string | null {
    if (formaDeAporte === "missao") {
      if (!missaoSelecionada) return null;
      return (
        `Missão "${missaoSelecionada.titulo}" — falta ${missaoSelecionada.falta} moedas, ` +
        `prazo ${formatarDataDaAula(missaoSelecionada.prazo)}.`
      );
    }
    if (formaDeAporte === "necessidade") {
      if (!necessidadeSelecionada) return null;
      const moedas =
        necessidadeSelecionada.valor_em_moedas ??
        String(necessidadeSelecionada.quantidade_faltante);
      return (
        `Necessidade da aula de ${formatarDataDaAula(necessidadeSelecionada.inicio_em)}, ` +
        `${necessidadeSelecionada.quantidade_faltante} unidades — equivalente a ${moedas} moedas.`
      );
    }
    if (formaDeAporte === "escada") {
      const valor = escada[degrauSelecionado];
      return `Valor sugerido de R$ ${valor.toFixed(2)} — equivalente a ${formatarMoedas(valor)}.`;
    }
    if (formaDeAporte === "livre") {
      if (!valorLivreValido) return null;
      return `Valor livre de R$ ${valorLivreEmReais.toFixed(2)} — equivalente a ${formatarMoedas(valorLivreEmReais)}.`;
    }
    return null;
  }

  function aoEscolherComprovante(evento: ChangeEvent<HTMLInputElement>) {
    definirComprovante(evento.target.files?.[0] ?? null);
  }

  async function aoEnviar(evento: FormEvent) {
    evento.preventDefault();
    definirErro(null);
    definirTempoDeEspera(null);
    definirSucesso(false);

    const aporteDeclarado = compoeAporteDeclarado();
    if (!aporteDeclarado) {
      definirErro("Escolha uma forma de aporte válida.");
      return;
    }
    if (!comprovante) {
      definirErro(`Anexe o comprovante em ${FORMATOS_ACEITOS} para enviar o pré-cadastro.`);
      return;
    }

    definirEnviando(true);
    try {
      await registrarPreCadastroDeApoiador({
        nome_ou_razao_social: nomeOuRazaoSocial,
        email,
        whatsapp,
        perfil,
        nick,
        aporte_declarado: aporteDeclarado,
        comprovante,
      });
      definirSucesso(true);
      definirComprovante(null);
    } catch (erroCapturado) {
      if (
        erroCapturado instanceof ErroDaApi &&
        erroCapturado.tempoDeEsperaEmSegundos != null
      ) {
        definirTempoDeEspera(
          tempoDeEsperaEmLinguagemSimples(erroCapturado.tempoDeEsperaEmSegundos),
        );
      } else if (erroCapturado instanceof ErroDaApi) {
        definirErro(erroCapturado.message);
      } else {
        definirErro("Não foi possível enviar o pré-cadastro. Tente novamente.");
      }
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Comunidade Game — Área do Apoiador"
        subtitulo="Quem sustenta o projeto começa aqui. O pré-cadastro não cria acesso: um Admin confere o comprovante antes de qualquer coisa."
      />

      <AvisoDeColeta dado="o nome ou razão social, e-mail, WhatsApp, nick e perfil do pré-cadastro" />

      <p>
        Já tem cadastro?{" "}
        <Botao variante="secundaria" onClick={aoIrParaEntrada}>
          Entrar
        </Botao>
      </p>

      <form onSubmit={aoEnviar}>
        <Campo
          rotulo="Nome ou razão social"
          valor={nomeOuRazaoSocial}
          aoAlterar={definirNomeOuRazaoSocial}
        />
        <Campo rotulo="E-mail" tipo="email" valor={email} aoAlterar={definirEmail} />
        <Campo rotulo="WhatsApp" valor={whatsapp} aoAlterar={definirWhatsapp} />
        <Campo rotulo="Nick" valor={nick} aoAlterar={definirNick} />

        <fieldset>
          <legend>Perfil</legend>
          <label>
            <input
              type="radio"
              name="perfil"
              value="pessoa_fisica"
              checked={perfil === "pessoa_fisica"}
              onChange={() => definirPerfil("pessoa_fisica")}
            />
            Pessoa física
          </label>
          <label>
            <input
              type="radio"
              name="perfil"
              value="pessoa_juridica"
              checked={perfil === "pessoa_juridica"}
              onChange={() => definirPerfil("pessoa_juridica")}
            />
            Pessoa jurídica
          </label>
        </fieldset>

        <fieldset>
          <legend>Como você quer apoiar</legend>
          <label>
            <input
              type="radio"
              name="forma-de-aporte"
              value="missao"
              checked={formaDeAporte === "missao"}
              onChange={() => definirFormaDeAporte("missao")}
            />
            Uma missão aberta
          </label>
          <label>
            <input
              type="radio"
              name="forma-de-aporte"
              value="necessidade"
              checked={formaDeAporte === "necessidade"}
              onChange={() => definirFormaDeAporte("necessidade")}
            />
            Uma necessidade publicada
          </label>
          <label>
            <input
              type="radio"
              name="forma-de-aporte"
              value="escada"
              checked={formaDeAporte === "escada"}
              onChange={() => definirFormaDeAporte("escada")}
            />
            Um valor sugerido
          </label>
          <label>
            <input
              type="radio"
              name="forma-de-aporte"
              value="livre"
              checked={formaDeAporte === "livre"}
              onChange={() => definirFormaDeAporte("livre")}
            />
            Um valor livre
          </label>
          <label>
            <input
              type="radio"
              name="forma-de-aporte"
              value="sem_dinheiro"
              checked={formaDeAporte === "sem_dinheiro"}
              onChange={() => definirFormaDeAporte("sem_dinheiro")}
            />
            Quero apoiar sem transferir dinheiro — material, serviço ou divulgação
          </label>
        </fieldset>

        {formaDeAporte === "missao" && (
          <div className="cg-campo">
            <label htmlFor="missao-selecionada">Missão aberta</label>
            <select
              id="missao-selecionada"
              value={missaoSelecionadaId}
              onChange={(evento) => definirMissaoSelecionadaId(evento.target.value)}
            >
              <option value="">Selecione…</option>
              {missoes.map((missao) => (
                <option key={missao.id} value={missao.id}>
                  {missao.titulo} — falta {missao.falta} moedas
                </option>
              ))}
            </select>
          </div>
        )}

        {formaDeAporte === "necessidade" && (
          <div className="cg-campo">
            <label htmlFor="necessidade-selecionada">Necessidade</label>
            <select
              id="necessidade-selecionada"
              value={necessidadeSelecionadaId}
              onChange={(evento) => definirNecessidadeSelecionadaId(evento.target.value)}
            >
              <option value="">Selecione…</option>
              {necessidades.map((necessidade) => (
                <option key={necessidade.aula_id} value={necessidade.aula_id}>
                  Aula de {formatarDataDaAula(necessidade.inicio_em)} —{" "}
                  {necessidade.quantidade_faltante} unidades
                  {necessidade.valor_em_moedas
                    ? ` — ${necessidade.valor_em_moedas} moedas`
                    : ""}
                </option>
              ))}
            </select>
          </div>
        )}

        {formaDeAporte === "escada" && (
          <div className="cg-campo">
            <label htmlFor="degrau-da-escada">Valor sugerido</label>
            <select
              id="degrau-da-escada"
              value={degrauSelecionado}
              onChange={(evento) => definirDegrauSelecionado(Number(evento.target.value))}
            >
              {escada.map((valor, indice) => (
                <option key={valor} value={indice}>
                  R$ {valor.toFixed(2)} — {formatarMoedas(valor)}
                </option>
              ))}
            </select>
          </div>
        )}

        {formaDeAporte === "livre" && (
          <div className="cg-campo">
            <Campo
              rotulo="Valor livre (R$)"
              tipo="number"
              valor={valorLivreTexto}
              aoAlterar={definirValorLivreTexto}
            />
            {valorLivreValido && <p>Equivalente a {formatarMoedas(valorLivreEmReais)}.</p>}
          </div>
        )}

        {formaDeAporte === "sem_dinheiro" &&
          (URL_DO_FORMULARIO_DA_VITRINE ? (
            <p>
              Apoio em material, serviço ou divulgação entra pelo{" "}
              <a href={URL_DO_FORMULARIO_DA_VITRINE}>formulário de solicitação da vitrine</a>.
            </p>
          ) : (
            <p>
              Apoio em material, serviço ou divulgação entra pelo formulário de solicitação da
              vitrine, na página inicial do Comunidade Game.
            </p>
          ))}

        {formaDeAporte !== "sem_dinheiro" && (
          <>
            <div className="cg-campo">
              <label htmlFor="comprovante-do-aporte">
                Comprovante da transferência ({FORMATOS_ACEITOS})
              </label>
              <input id="comprovante-do-aporte" type="file" onChange={aoEscolherComprovante} />
            </div>

            <p>
              O pré-cadastro não cria cadastro nem acesso. Um Admin vai conferir o comprovante,
              e a plataforma não emite recibo — quem precisar de um pede à pessoa jurídica
              vinculada, fora da plataforma.
            </p>

            <Botao tipo="submit" desabilitado={enviando}>
              Enviar pré-cadastro
            </Botao>
          </>
        )}
      </form>

      {enviando && <Aviso tipo="andamento">Enviando…</Aviso>}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {tempoDeEspera && (
        <Aviso tipo="erro">
          Muitas tentativas em pouco tempo. Espere {tempoDeEspera} e tente de novo.
        </Aviso>
      )}
      {sucesso && (
        <Aviso tipo="sucesso">
          Pedido registrado na fila da gestão. Nenhum cadastro nem acesso foi criado — aguarde
          o contato depois da conferência do Admin.
        </Aviso>
      )}
    </Moldura>
  );
}
