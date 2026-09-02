import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type ChangeEvent, type FormEvent, useEffect, useState } from "react";
import {
  ESCADA_POR_PERFIL,
  formatarMoedas,
  type PerfilDeApoiador,
} from "../compartilhado/escada";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import { declararAporte, listarNecessidadesEmAberto, type NecessidadeDeRecurso } from "./api";

const FORMATOS_ACEITOS = "PDF, JPG ou PNG";

type FormaDeAporte = "necessidade" | "sugerido" | "livre" | "sem_dinheiro";

function formatarDataDaAula(isoDeInicio: string): string {
  const data = new Date(isoDeInicio);
  return Number.isNaN(data.getTime())
    ? isoDeInicio
    : data.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric" });
}

// A declaração do aporte pelo Apoiador em sessão: os três caminhos —
// necessidade, valor sugerido da escada do perfil escolhido nesta tela e
// valor livre —, o equivalente em moedas, o comprovante obrigatório, o
// aviso de que o aporte entra pendente e o encaminhamento de quem quer
// aportar material, serviço ou divulgação (`RF-14-23`, `RF-14-25`,
// `RF-14-26`, `RF-14-28`, `RN-14-05` a `RN-14-07`, `RN-14-09`).
export function TelaDeDeclaracaoDeAporte() {
  const { sessao } = useSessao();
  const [perfil, definirPerfil] = useState<PerfilDeApoiador>("pessoa_fisica");
  const [formaDeAporte, definirFormaDeAporte] = useState<FormaDeAporte>("sugerido");
  const [necessidades, definirNecessidades] = useState<NecessidadeDeRecurso[]>([]);
  const [necessidadeSelecionadaId, definirNecessidadeSelecionadaId] = useState("");
  const [degrauSelecionado, definirDegrauSelecionado] = useState(0);
  const [valorLivreTexto, definirValorLivreTexto] = useState("");
  const [comprovante, definirComprovante] = useState<File | null>(null);

  const [enviando, definirEnviando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [sucesso, definirSucesso] = useState(false);

  useEffect(() => {
    listarNecessidadesEmAberto()
      .then(definirNecessidades)
      .catch(() => definirNecessidades([]));
  }, []);

  const escada = ESCADA_POR_PERFIL[perfil];
  const necessidadeSelecionada = necessidades.find(
    (n) => n.aula_id === necessidadeSelecionadaId,
  );
  const valorLivreEmReais = Number(valorLivreTexto.replace(",", "."));
  const valorLivreValido = valorLivreTexto.trim() !== "" && !Number.isNaN(valorLivreEmReais);

  function aoEscolherComprovante(evento: ChangeEvent<HTMLInputElement>) {
    definirComprovante(evento.target.files?.[0] ?? null);
  }

  async function aoEnviar(evento: FormEvent) {
    evento.preventDefault();
    definirErro(null);
    definirSucesso(false);

    if (!sessao) return;
    if (!comprovante) {
      definirErro(`Anexe o comprovante em ${FORMATOS_ACEITOS} para enviar a declaração.`);
      return;
    }

    let valorDeclarado: number;
    let aulaId: string | undefined;
    let tipoDeRecursoId: string | undefined;
    if (formaDeAporte === "necessidade") {
      if (!necessidadeSelecionada) {
        definirErro("Escolha uma necessidade.");
        return;
      }
      valorDeclarado = Number(
        necessidadeSelecionada.valor_em_moedas ?? necessidadeSelecionada.quantidade_faltante,
      );
      aulaId = necessidadeSelecionada.aula_id;
      tipoDeRecursoId = necessidadeSelecionada.tipo_de_recurso_id;
    } else if (formaDeAporte === "sugerido") {
      valorDeclarado = escada[degrauSelecionado];
    } else {
      if (!valorLivreValido) {
        definirErro("Informe um valor livre válido.");
        return;
      }
      valorDeclarado = valorLivreEmReais;
    }

    definirEnviando(true);
    try {
      await declararAporte(
        {
          valor_declarado: valorDeclarado,
          origem_da_escolha:
            formaDeAporte === "necessidade"
              ? "necessidade"
              : formaDeAporte === "sugerido"
                ? "valor_sugerido"
                : "valor_livre",
          aula_id: aulaId,
          tipo_de_recurso_id: tipoDeRecursoId,
          comprovante,
        },
        sessao.token,
      );
      definirSucesso(true);
      definirComprovante(null);
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível enviar a declaração. Tente novamente.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Declarar aporte"
        subtitulo="O aporte pela aplicação é sempre em dinheiro. Material, serviço e divulgação entram pelo cadastro da gestão — procure a equipe do projeto."
      />

      <AvisoDeColeta dado="o valor declarado e o comprovante do aporte" />

      <form onSubmit={aoEnviar}>
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
          <legend>Como você quer aportar</legend>
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
              value="sugerido"
              checked={formaDeAporte === "sugerido"}
              onChange={() => definirFormaDeAporte("sugerido")}
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
                <option
                  key={`${necessidade.aula_id}-${necessidade.tipo_de_recurso_id}`}
                  value={necessidade.aula_id}
                >
                  {necessidade.tipo_de_recurso_nome} — aula de{" "}
                  {formatarDataDaAula(necessidade.inicio_em)}
                  {necessidade.valor_em_moedas
                    ? ` — ${necessidade.valor_em_moedas} moedas`
                    : ""}
                </option>
              ))}
            </select>
          </div>
        )}

        {formaDeAporte === "sugerido" && (
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

        {formaDeAporte === "sem_dinheiro" && (
          <p>
            Material, serviço e divulgação entram pelo cadastro do Admin, com termo de doação
            ou registro do material — procure a equipe do projeto.
          </p>
        )}

        {formaDeAporte !== "sem_dinheiro" && (
          <>
            <div className="cg-campo">
              <label htmlFor="comprovante-do-aporte">
                Comprovante da transferência ({FORMATOS_ACEITOS})
              </label>
              <input id="comprovante-do-aporte" type="file" onChange={aoEscolherComprovante} />
            </div>

            <p>
              O aporte entra <strong>pendente de homologação</strong>. Um Admin vai conferir o
              comprovante, e até lá ele não vira moeda, não compõe o Poder Sustentador e não
              abate o que falta a necessidade alguma.
            </p>

            <Botao tipo="submit" desabilitado={enviando}>
              Enviar declaração
            </Botao>
          </>
        )}
      </form>

      {enviando && <Aviso tipo="andamento">Enviando…</Aviso>}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {sucesso && (
        <Aviso tipo="sucesso">
          Declaração registrada na fila da gestão. A necessidade escolhida continua com a mesma
          quantidade faltante até a homologação.
        </Aviso>
      )}
    </Moldura>
  );
}
