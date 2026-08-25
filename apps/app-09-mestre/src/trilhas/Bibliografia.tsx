import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useEffect, useId, useState } from "react";
import {
  type BibliografiaDaMissao,
  criarBibliografia,
  type ExemplarDoAcervo,
  listarAcervo,
} from "./api";

interface Props {
  idDaMissao: string;
  entradas: BibliografiaDaMissao[];
  onSalva: (bibliografia: BibliografiaDaMissao) => void;
}

// Título e capítulo em texto, com o exemplar do acervo opcional — escolhido
// de uma lista, nunca digitado como identificador, e sem nenhum campo para
// digitar disponibilidade ou Apoiador: os dois só existem na leitura
// pública (`RF-09-21` a `RF-09-23`).
export function Bibliografia({ idDaMissao, entradas, onSalva }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoExemplar = useId();
  const [titulo, definirTitulo] = useState("");
  const [capitulo, definirCapitulo] = useState("");
  const [exemplarId, definirExemplarId] = useState("");
  const [acervo, definirAcervo] = useState<ExemplarDoAcervo[]>([]);
  const [erroDeCampo, definirErroDeCampo] = useState<string | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);

  useEffect(() => {
    if (!sessao) return;
    listarAcervo(sessao.token)
      .then(definirAcervo)
      .catch(() => definirAcervo([]));
  }, [sessao]);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!titulo.trim()) {
      definirErroDeCampo("Informe o título.");
      return;
    }
    if (!capitulo.trim()) {
      definirErroDeCampo("Informe o capítulo recomendado.");
      return;
    }

    if (!sessao) return;
    definirEnviando(true);
    try {
      const bibliografia = await criarBibliografia(
        idDaMissao,
        {
          titulo,
          capitulo,
          item_patrimonial_id: exemplarId || undefined,
        },
        sessao.token,
      );
      definirTitulo("");
      definirCapitulo("");
      definirExemplarId("");
      definirMostrarFormulario(false);
      onSalva(bibliografia);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi) {
        definirErroDeRecusa(erro.message);
        return;
      }
      definirErroDeRecusa("Não foi possível salvar a bibliografia. Tente novamente.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <section aria-label="Bibliografia da missão">
      <h3>Bibliografia</h3>

      <ul>
        {entradas.map((entrada) => (
          <li key={entrada.id}>
            {entrada.titulo} — {entrada.capitulo}
            {entrada.item_patrimonial_id && (
              <>
                {" "}
                ·{" "}
                {entrada.disponivel
                  ? "Exemplar disponível no ponto de apoio"
                  : "Exemplar não disponível neste ponto de apoio"}
                {entrada.apoiador_nome && <> · Doado por {entrada.apoiador_nome}</>}
              </>
            )}
          </li>
        ))}
      </ul>

      {mostrarFormulario ? (
        <form onSubmit={aoSubmeter} aria-label="Nova entrada de bibliografia">
          <Campo
            rotulo="Título"
            valor={titulo}
            aoAlterar={definirTitulo}
            erro={erroDeCampo === "Informe o título." ? erroDeCampo : null}
          />
          <Campo
            rotulo="Capítulo recomendado"
            valor={capitulo}
            aoAlterar={definirCapitulo}
            erro={erroDeCampo === "Informe o capítulo recomendado." ? erroDeCampo : null}
          />

          <div className="cg-campo">
            <label htmlFor={idDoExemplar}>Exemplar do acervo (opcional)</label>
            <select
              id={idDoExemplar}
              value={exemplarId}
              onChange={(evento) => definirExemplarId(evento.target.value)}
            >
              <option value="">Nenhum exemplar</option>
              {acervo.map((exemplar) => (
                <option key={exemplar.id} value={exemplar.id}>
                  {exemplar.titulo} — tombo {exemplar.numero_de_tombo}
                </option>
              ))}
            </select>
          </div>

          {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

          <Botao tipo="submit" desabilitado={enviando}>
            Acrescentar bibliografia
          </Botao>
          <Botao variante="secundaria" onClick={() => definirMostrarFormulario(false)}>
            Cancelar
          </Botao>
        </form>
      ) : (
        <Botao variante="secundaria" onClick={() => definirMostrarFormulario(true)}>
          Nova bibliografia
        </Botao>
      )}
    </section>
  );
}
