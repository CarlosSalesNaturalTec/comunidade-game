import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, MarcaDeGravacao } from "comum/react";
import { useState } from "react";
import {
  type AtividadeDaMissao,
  type FatosDaAtividade,
  fatosDaAtividade,
  type MissaoDaTrilha,
  removerAtividade,
} from "./api";
import {
  FormularioDeAtividade,
  ROTULO_DA_MODALIDADE,
  ROTULO_DO_FORMATO,
} from "./FormularioDeAtividade";

interface Props {
  missao: MissaoDaTrilha;
  onAtualizada: (missao: MissaoDaTrilha) => void;
}

// A linha imprimia o valor cru do enum — `em_equipe_com_familiar /
// on_line_assincrona` — enquanto o formulário logo abaixo já tinha os dois
// dicionários de rótulo (`RF-09-127`).
function rotuloDosEixos(atividade: AtividadeDaMissao): string {
  const modalidade = ROTULO_DA_MODALIDADE[atividade.modalidade] ?? atividade.modalidade;
  const formato = ROTULO_DO_FORMATO[atividade.formato] ?? atividade.formato;
  return `${modalidade} / ${formato}`;
}

// A frase que a confirmação diz antes de o Mestre remover: quantos fatos já
// apontam para a atividade. Nenhum fato sai com ela — o Resultado gravado não
// se edita nem se remove (`RF-09-47`, `RN-09-47`).
export function fraseDosFatos(fatos: FatosDaAtividade): string {
  const partes = [
    [fatos.resultados, "Resultado lançado", "Resultados lançados"],
    [fatos.producoes, "produção entregue", "produções entregues"],
    [fatos.partidas_de_quiz, "partida de quiz", "partidas de quiz"],
    [fatos.ocorrencias_de_conduta, "ocorrência de conduta", "ocorrências de conduta"],
    [fatos.equipes_com_ela_corrente, "equipe a trabalha agora", "equipes a trabalham agora"],
  ] as const;
  const declaradas = partes
    .filter(([quantidade]) => quantidade > 0)
    .map(
      ([quantidade, singular, plural]) =>
        `${quantidade} ${quantidade === 1 ? singular : plural}`,
    );
  if (declaradas.length === 0) {
    return "Nenhum fato aponta para esta atividade. Remover?";
  }
  return `${declaradas.join(", ")} seguem apontando para esta atividade, e permanecem gravados. Remover?`;
}

// O bloco Atividades do cadastro: lista, nomeia os eixos em português,
// corrige e remove. A contagem dos fatos é buscada **no clique de remover** —
// contar cinco tabelas por atividade ao abrir a tela da trilha seria pagar
// pela remoção que quase nunca acontece (`RF-09-127`, `RF-09-128`,
// `RN-09-46`, design — decisão 10).
export function BlocoDeAtividades({ missao, onAtualizada }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [criando, definirCriando] = useState(false);
  const [emCorrecao, definirEmCorrecao] = useState<string | null>(null);
  const [confirmando, definirConfirmando] = useState<Record<string, string>>({});
  const [erro, definirErro] = useState<Record<string, string>>({});
  const [gravadoEm, definirGravadoEm] = useState<Date | null>(null);

  const atividades = missao.atividades;

  function recusaDoNucleo(erroCapturado: unknown, alternativa: string): string | null {
    if (ehRecusaDeSessao(erroCapturado)) {
      tratarRecusaDeSessao();
      return null;
    }
    return erroCapturado instanceof ErroDaApi ? erroCapturado.message : alternativa;
  }

  function semAAtividade<T>(mapa: Record<string, T>, id: string): Record<string, T> {
    const { [id]: _removido, ...resto } = mapa;
    return resto;
  }

  async function pedirRemocao(atividade: AtividadeDaMissao) {
    if (!sessao) return;
    definirErro((atual) => semAAtividade(atual, atividade.id));
    let frase: string;
    try {
      frase = fraseDosFatos(await fatosDaAtividade(atividade.id, sessao.token));
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      // Falha ao conferir os fatos não tranca a remoção: a decisão é do
      // Mestre, e a tela diz que não conseguiu conferir (design — decisão 10).
      frase = "Não foi possível conferir quantos fatos apontam para esta atividade. Remover?";
    }
    definirConfirmando((atual) => ({ ...atual, [atividade.id]: frase }));
  }

  async function remover(atividade: AtividadeDaMissao) {
    if (!sessao) return;
    definirConfirmando((atual) => semAAtividade(atual, atividade.id));
    try {
      await removerAtividade(atividade.id, sessao.token);
    } catch (erroCapturado) {
      const recusa = recusaDoNucleo(
        erroCapturado,
        "Não foi possível remover esta atividade. Tente novamente em instantes.",
      );
      if (recusa) definirErro((atual) => ({ ...atual, [atividade.id]: recusa }));
      return;
    }
    definirGravadoEm(new Date());
    onAtualizada({
      ...missao,
      atividades: atividades.filter((outra) => outra.id !== atividade.id),
    });
  }

  function aoCorrigida(corrigida: AtividadeDaMissao) {
    definirEmCorrecao(null);
    definirGravadoEm(new Date());
    onAtualizada({
      ...missao,
      atividades: atividades.map((outra) => (outra.id === corrigida.id ? corrigida : outra)),
    });
  }

  return (
    <section aria-label={`Atividades de ${missao.titulo}`}>
      <ul>
        {atividades.map((atividade) => (
          <li key={atividade.id}>
            {emCorrecao === atividade.id ? (
              <FormularioDeAtividade
                idDaMissao={missao.id}
                atividade={atividade}
                onSalvo={aoCorrigida}
                onCancelar={() => definirEmCorrecao(null)}
              />
            ) : (
              <>
                <p>
                  {atividade.titulo} — {rotuloDosEixos(atividade)}
                </p>

                <Botao variante="secundaria" onClick={() => definirEmCorrecao(atividade.id)}>
                  Corrigir
                </Botao>

                {confirmando[atividade.id] ? (
                  <>
                    <p role="alert">{confirmando[atividade.id]}</p>
                    <Botao variante="secundaria" onClick={() => remover(atividade)}>
                      Confirmar remoção
                    </Botao>
                    <Botao
                      variante="secundaria"
                      onClick={() =>
                        definirConfirmando((atual) => semAAtividade(atual, atividade.id))
                      }
                    >
                      Manter atividade
                    </Botao>
                  </>
                ) : (
                  <Botao variante="secundaria" onClick={() => pedirRemocao(atividade)}>
                    Remover
                  </Botao>
                )}

                {erro[atividade.id] && <Aviso tipo="erro">{erro[atividade.id]}</Aviso>}
              </>
            )}
          </li>
        ))}
      </ul>

      {criando ? (
        <FormularioDeAtividade
          idDaMissao={missao.id}
          onSalvo={(atividade) => {
            definirCriando(false);
            definirGravadoEm(new Date());
            onAtualizada({ ...missao, atividades: [...atividades, atividade] });
          }}
          onCancelar={() => definirCriando(false)}
        />
      ) : (
        <Botao variante="secundaria" onClick={() => definirCriando(true)}>
          Nova atividade
        </Botao>
      )}
      <MarcaDeGravacao instante={gravadoEm} />
    </section>
  );
}
