import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useState } from "react";
import {
  type MissaoDaTrilha,
  publicarTrilha,
  type TipoDeColeta,
  type TrilhaDoMestre,
} from "./api";
import { EtiquetasOds } from "./EtiquetasOds";
import { FormularioDeCulminancia } from "./FormularioDeCulminancia";
import { FormularioDeMissao } from "./FormularioDeMissao";
import { ListaDeMissoes } from "./ListaDeMissoes";

interface Props {
  trilha: TrilhaDoMestre;
  tiposDeColeta: TipoDeColeta[];
  aoVoltar: () => void;
  onAtualizarTrilha: (trilha: TrilhaDoMestre) => void;
}

const ROTULO_DA_MODALIDADE_DA_CULMINANCIA: Record<string, string> = {
  individual: "Individual",
  em_equipe: "Em equipe",
};

// A trilha em rascunho ou despublicada é a única que se publica — trilha já
// publicada não oferece a ação de novo (`RF-09-05`, `RF-09-11`).
const SITUACOES_QUE_PODEM_PUBLICAR = new Set(["rascunho", "despublicada"]);

// A cobertura é a união dos objetivos da trilha e das missões dela, sempre
// agregada por trilha e nunca por Guerreiro(a) — refeita a cada confirmação
// para a tela acompanhar o que o Mestre acabou de declarar (`RF-09-94`,
// `RN-01-24`).
function coberturaDaTrilha(trilha: TrilhaDoMestre): number[] {
  const objetivos = new Set<number>();
  for (const etiqueta of trilha.etiquetas_ods) objetivos.add(etiqueta.objetivo);
  for (const missao of trilha.missoes) {
    for (const etiqueta of missao.etiquetas_ods) objetivos.add(etiqueta.objetivo);
  }
  return [...objetivos].sort((a, b) => a - b);
}

function comCoberturaRefeita(trilha: TrilhaDoMestre): TrilhaDoMestre {
  return {
    ...trilha,
    cobertura_ods: { ...trilha.cobertura_ods, objetivos: coberturaDaTrilha(trilha) },
  };
}

export function TelaDaTrilha({ trilha, tiposDeColeta, aoVoltar, onAtualizarTrilha }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);
  const [mostrarFormularioDeCulminancia, definirMostrarFormularioDeCulminancia] =
    useState(false);
  const [recusaDaPublicacao, definirRecusaDaPublicacao] = useState<string | null>(null);
  const [publicando, definirPublicando] = useState(false);

  function aoAcrescentarMissao(missao: MissaoDaTrilha) {
    definirMostrarFormulario(false);
    onAtualizarTrilha(
      comCoberturaRefeita({ ...trilha, missoes: [...trilha.missoes, missao] }),
    );
  }

  function aoAtualizarMissao(missaoAtualizada: MissaoDaTrilha) {
    onAtualizarTrilha(
      comCoberturaRefeita({
        ...trilha,
        missoes: trilha.missoes.map((missao) =>
          missao.id === missaoAtualizada.id ? missaoAtualizada : missao,
        ),
      }),
    );
  }

  async function aoPublicar() {
    if (!sessao) return;
    definirRecusaDaPublicacao(null);
    definirPublicando(true);
    try {
      const trilhaAtualizada = await publicarTrilha(trilha.id, sessao.token);
      onAtualizarTrilha({ ...trilha, ...trilhaAtualizada });
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      // O núcleo já devolve, em linguagem simples, todas as travas que
      // faltam de uma vez — a tela só repassa a mensagem (`RF-09-08`,
      // `RF-09-12`).
      if (erro instanceof ErroDaApi) {
        definirRecusaDaPublicacao(erro.message);
        return;
      }
      definirRecusaDaPublicacao(
        "Não foi possível publicar a trilha. Tente novamente em instantes.",
      );
    } finally {
      definirPublicando(false);
    }
  }

  const podePublicar = SITUACOES_QUE_PODEM_PUBLICAR.has(trilha.situacao);

  return (
    <Moldura>
      <Cabecalho
        titulo={trilha.nome}
        subtitulo={trilha.objetivo}
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />

      {trilha.motivo_da_situacao && <Aviso tipo="atencao">{trilha.motivo_da_situacao}</Aviso>}

      <EtiquetasOds
        alvo="trilha"
        id={trilha.id}
        etiquetas={trilha.etiquetas_ods}
        onSalvo={(etiquetas) =>
          onAtualizarTrilha(comCoberturaRefeita({ ...trilha, etiquetas_ods: etiquetas }))
        }
      />

      <section aria-label="Cobertura de ODS da trilha">
        <h3>Cobertura de ODS da trilha</h3>
        <p>
          {trilha.cobertura_ods.objetivos.length > 0
            ? `${trilha.cobertura_ods.objetivos.map((objetivo) => `ODS ${objetivo}`).join(", ")} · ${trilha.cobertura_ods.ciclo}`
            : "Nenhum ODS coberto por esta trilha ainda."}
        </p>
      </section>

      <section aria-label="Culminância">
        <h2>Culminância</h2>
        {trilha.culminancia && !mostrarFormularioDeCulminancia && (
          <p>
            {trilha.culminancia.descricao} ·{" "}
            {ROTULO_DA_MODALIDADE_DA_CULMINANCIA[trilha.culminancia.modalidade] ??
              trilha.culminancia.modalidade}
          </p>
        )}
        {!trilha.culminancia && !mostrarFormularioDeCulminancia && (
          <p>Esta trilha ainda não tem a culminância declarada.</p>
        )}

        {mostrarFormularioDeCulminancia ? (
          <FormularioDeCulminancia
            idDaTrilha={trilha.id}
            culminancia={trilha.culminancia ?? null}
            onSalvo={(culminancia) => {
              definirMostrarFormularioDeCulminancia(false);
              onAtualizarTrilha({ ...trilha, culminancia });
            }}
            onCancelar={() => definirMostrarFormularioDeCulminancia(false)}
          />
        ) : (
          <Botao
            variante="secundaria"
            onClick={() => definirMostrarFormularioDeCulminancia(true)}
          >
            {trilha.culminancia ? "Alterar culminância" : "Declarar culminância"}
          </Botao>
        )}
      </section>

      {podePublicar && (
        <Botao onClick={aoPublicar} desabilitado={publicando}>
          Publicar trilha
        </Botao>
      )}
      {recusaDaPublicacao && <Aviso tipo="erro">{recusaDaPublicacao}</Aviso>}

      {!mostrarFormulario && (
        <Botao onClick={() => definirMostrarFormulario(true)}>Nova missão</Botao>
      )}

      {mostrarFormulario && (
        <FormularioDeMissao
          idDaTrilha={trilha.id}
          proximaPosicao={trilha.missoes.length + 1}
          onSalvo={aoAcrescentarMissao}
          onCancelar={() => definirMostrarFormulario(false)}
        />
      )}

      <ListaDeMissoes
        missoes={trilha.missoes}
        tiposDeColeta={tiposDeColeta}
        onAtualizarMissao={aoAtualizarMissao}
      />
    </Moldura>
  );
}
