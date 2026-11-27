import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, MidiaDoNucleo } from "comum/react";
import type { RecompensaDeMarco } from "../recompensas/api";
import type { TipoDeRecurso } from "../recursos/api";
import {
  lerImagemDaPergunta,
  type MissaoDaTrilha,
  ROTULO_DA_FORMA_DE_COMPROVACAO,
} from "./api";
import { ConteudoExibido } from "./ConteudoExibido";

interface Props {
  missao: MissaoDaTrilha;
  autorNome: string | null;
  // As recompensas de marco já filtradas por esta missão, e o catálogo que
  // dá nome ao tipo de recurso delas (`RF-09-84`).
  recompensas?: RecompensaDeMarco[];
  tiposDeRecurso?: TipoDeRecurso[];
  onFechar: () => void;
}

// A licença é fixa, a mesma que a leitura pública da trilha já declara
// (documento 03 — código aberto e CC BY-SA); não é parâmetro de operação.
const LICENCA = "CC BY-SA";

// O crédito sem nick cai no mesmo texto de reserva da App 05, para que a
// pré-visualização não invente autor nem o omita (`RF-09-25`).
const CREDITO_SEM_NICK = "Mestre autor";

// Apresenta a missão na mesma ordem e na mesma forma em que o Guerreiro(a) a
// encontrará (`app-05-guerreiro/src/trilha/Missao.tsx`), a partir do que já
// está gravado: a trilha em rascunho não sai pela leitura pública
// (`RF-09-04`), e a pré-visualização nunca grava nem publica nada
// (`RF-09-25`). Ela espelha aquela tela em vez de partilhar componente com
// ela — as duas podem divergir, e é a suíte que segura (design — decisão 4).
// Nomes distintos, na ordem em que foram declarados: a recompensa aparece só
// pelo recurso, sem a quantidade (decisão do fundador de 2026-11-27). Tipo
// fora do catálogo cai no mesmo texto de reserva do bloco de recompensa.
function nomesDasRecompensas(
  recompensas: RecompensaDeMarco[],
  tiposDeRecurso: TipoDeRecurso[],
): string[] {
  const nomeDoTipo = new Map(tiposDeRecurso.map((tipo) => [tipo.id, tipo.nome]));
  const nomes = recompensas.map((r) => nomeDoTipo.get(r.tipo_de_recurso_id) ?? "Recurso");
  return [...new Set(nomes)];
}

export function PreVisualizacaoDaMissao({
  missao,
  autorNome,
  recompensas = [],
  tiposDeRecurso = [],
  onFechar,
}: Props) {
  const { sessao } = useSessao();
  const token = sessao?.token ?? null;
  const conteudos = [...(missao.conteudos ?? [])].sort((a, b) => a.ordem - b.ordem);
  const bibliografia = missao.bibliografia ?? [];
  const perguntas = missao.perguntas_do_desbloqueio ?? [];
  const nomesDaRecompensa = nomesDasRecompensas(recompensas, tiposDeRecurso);
  const pratico = missao.tipo_do_desafio_de_desbloqueio === "pratico";

  return (
    <section aria-label={`Pré-visualização de ${missao.titulo}`} className="cg-moldura">
      <h2>Pré-visualização — {missao.titulo}</h2>

      {!missao.obrigatoria && (
        <Aviso tipo="andamento">
          Essa missão é opcional — ela não conta no que falta para o próximo nível.
        </Aviso>
      )}

      {conteudos.length === 0 && <p>Nenhum conteúdo escrito ainda.</p>}
      <ul aria-label="Conteúdo da missão">
        {conteudos.map((conteudo) => (
          <li key={conteudo.id}>
            <ConteudoExibido conteudo={conteudo} tituloDaMissao={missao.titulo} />
            {conteudo.autoria === "terceiro" && conteudo.fonte && (
              <p>Fonte: {conteudo.fonte}</p>
            )}
          </li>
        ))}
      </ul>

      <p>
        Crédito: {autorNome ?? CREDITO_SEM_NICK} — licença {LICENCA}
      </p>

      <h3>Bibliografia</h3>
      {bibliografia.length === 0 && <p>Nenhuma bibliografia declarada ainda.</p>}
      <ul aria-label="Bibliografia da missão">
        {bibliografia.map((entrada) => (
          <li key={entrada.id}>
            {entrada.titulo} — {entrada.capitulo}
          </li>
        ))}
      </ul>

      {/* As atividades são como o Guerreiro(a) entrega a produção: sem elas,
          a pré-visualização mostra menos do que ele verá (`RF-09-25`). */}
      <h3>Atividades</h3>
      {missao.atividades.length === 0 && <p>Nenhuma atividade declarada ainda.</p>}
      <ul aria-label="Atividades da missão">
        {missao.atividades.map((atividade) => (
          <li key={atividade.id}>
            {atividade.titulo} — {atividade.producao_esperada}
          </li>
        ))}
      </ul>

      <h3>{missao.e_sondagem ? "Sondagem" : "Desafio de desbloqueio"}</h3>
      {missao.tipo_do_desafio_de_desbloqueio == null && (
        <p>
          {missao.e_sondagem
            ? "Sondagem ainda sem perguntas."
            : "Ainda sem desafio de desbloqueio."}
        </p>
      )}
      {missao.tipo_do_desafio_de_desbloqueio === "pratico" && (
        <>
          <p>{missao.desafio_de_desbloqueio_enunciado}</p>
          {/* A forma aceita e o critério são o que o Guerreiro(a) lê na hora
              de entregar: sem eles a pré-visualização não é "como ele a
              verá" (`RF-09-25`, `RF-09-129`, `RF-09-130`). */}
          {missao.desafio_pratico_forma_de_comprovacao && (
            <p>
              Comprovação em{" "}
              {ROTULO_DA_FORMA_DE_COMPROVACAO[missao.desafio_pratico_forma_de_comprovacao]}.
            </p>
          )}
          {missao.desafio_pratico_criterio_de_aceite && (
            <p>{missao.desafio_pratico_criterio_de_aceite}</p>
          )}
        </>
      )}
      {missao.tipo_do_desafio_de_desbloqueio === "quiz" && (
        // Em leitura: o enunciado e as alternativas como o Guerreiro(a) as
        // lerá, sem a indicação de qual é a correta, que é do autor.
        <ol aria-label="Perguntas do desbloqueio">
          {perguntas.map((pergunta) => (
            <li key={pergunta.id}>
              {pergunta.enunciado}
              {pergunta.imagem_referencia && (
                <MidiaDoNucleo
                  id={pergunta.id}
                  buscar={lerImagemDaPergunta}
                  token={token}
                  tipo="imagem"
                  alt={`Imagem da pergunta: ${pergunta.enunciado}`}
                  textoDeErro="Essa imagem não abriu agora, mas segue anexada."
                  ampliavel
                />
              )}
              <ul>
                {pergunta.alternativas.map((alternativa) => (
                  <li key={alternativa}>{alternativa}</li>
                ))}
              </ul>
            </li>
          ))}
        </ol>
      )}

      {/* O que o autor declarou para o desbloqueio e o Guerreiro(a) não lê na
          missão: fica à parte para a ficha seguir fiel à App 05 (`RF-09-25`,
          design — decisão 1). */}
      <section aria-label="O que só você vê" className="cg-moldura">
        <h3>O que só você vê</h3>
        <p>O Guerreiro(a) não vê isto na missão.</p>

        <h4>Recompensa pelo desbloqueio</h4>
        {nomesDaRecompensa.length === 0 ? (
          <p>Nenhuma recompensa pelo desbloqueio declarada ainda.</p>
        ) : (
          <ul aria-label="Recompensa pelo desbloqueio">
            {nomesDaRecompensa.map((nome) => (
              <li key={nome}>{nome}</li>
            ))}
          </ul>
        )}

        {/* Prático declarado antes de 2026-11-04 vem sem os dois e segue
            valendo (`RN-09-50`). */}
        {pratico && missao.desafio_pratico_titulo_curto && (
          <p>Título na vitrine: {missao.desafio_pratico_titulo_curto}</p>
        )}
        {pratico && missao.desafio_pratico_kit_apresentado && (
          <p>Kit apresentado: {missao.desafio_pratico_kit_apresentado.tipo_de_recurso_nome}</p>
        )}

        {missao.tipo_do_desafio_de_desbloqueio === "quiz" && (
          <p>
            {missao.e_sondagem
              ? "Aqui não tem passar nem reprovar: a trilha abre assim que o Guerreiro(a) responde."
              : "Passa quem acerta ao menos 60% das perguntas."}
          </p>
        )}
      </section>

      <Botao onClick={onFechar}>Fechar pré-visualização</Botao>
    </section>
  );
}
