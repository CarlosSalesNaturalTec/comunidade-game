import { BlocoRecolhivel, Botao, EstadoDaLista, MarcaDeGravacao } from "comum/react";
import { useState } from "react";
import type { RecompensaDeMarco } from "../recompensas/api";
import type { TipoDeRecurso } from "../recursos/api";
import type {
  CadenciaDeColeta,
  EtapaDoCiclo,
  MissaoDaTrilha,
  NivelDoLocal,
  TipoDeColeta,
} from "./api";
import { Bibliografia } from "./Bibliografia";
import { CadenciaDeRetomada } from "./CadenciaDeRetomada";
import { DeclaracaoDeRecompensa } from "./DeclaracaoDeRecompensa";
import { DesafioDeDesbloqueio } from "./DesafioDeDesbloqueio";
import { EtiquetasOds } from "./EtiquetasOds";
import { FormularioDeAtividade } from "./FormularioDeAtividade";
import { FormularioDeConteudo } from "./FormularioDeConteudo";
import { FormularioDeDesafioDeColeta, ROTULO_DO_NIVEL } from "./FormularioDeDesafioDeColeta";
import { PreVisualizacaoDaMissao } from "./PreVisualizacaoDaMissao";
import { TemplateDaMissao } from "./TemplateDaMissao";

interface Props {
  idDaTrilha: string;
  missoes: MissaoDaTrilha[];
  tiposDeColeta: TipoDeColeta[];
  tiposDeRecurso: TipoDeRecurso[];
  recompensasDeMarco: RecompensaDeMarco[];
  onAtualizarMissao: (missao: MissaoDaTrilha) => void;
  onDeclararRecompensa: (recompensa: RecompensaDeMarco) => void;
}

const ROTULO_DA_ETAPA: Record<EtapaDoCiclo, string> = {
  abertura: "Abertura",
  desenvolvimento: "Desenvolvimento",
  marcos: "Marcos",
  fechamento: "Fechamento",
};

const ROTULO_DA_CADENCIA_DE_COLETA: Record<CadenciaDeColeta, string> = {
  diaria: "Diária",
  semanal: "Semanal",
  mensal: "Mensal",
};

function rotuloDoNivel(nivel: NivelDoLocal): string {
  return ROTULO_DO_NIVEL[nivel] ?? nivel;
}

function resumoDaCadencia(missao: MissaoDaTrilha): string {
  return missao.cadencia_de_retomada && missao.cadencia_de_retomada.length > 0
    ? `Retomada em ${missao.cadencia_de_retomada.join(", ")} dias`
    : "Sem retomada declarada";
}

// A sondagem se chama pelo nome: para o Mestre ela não é o desbloqueio de
// uma missão, é o que abre a trilha e mostra de onde a turma parte
// (`RF-09-81`, `RN-09-30`).
function resumoDoDesafioDeDesbloqueio(missao: MissaoDaTrilha): string {
  if (missao.tipo_do_desafio_de_desbloqueio == null) {
    return missao.e_sondagem
      ? "Sondagem ainda sem perguntas."
      : "Ainda sem desafio de desbloqueio.";
  }
  // O quiz diz quantas perguntas tem, para o Mestre saber o tamanho do que
  // escreveu sem abrir o bloco (`RF-09-118`).
  if (missao.tipo_do_desafio_de_desbloqueio === "quiz") {
    const total = (missao.perguntas_do_desbloqueio ?? []).length;
    return missao.e_sondagem
      ? `Sondagem com ${total} pergunta(s).`
      : `Quiz com ${total} pergunta(s).`;
  }
  return "Desafio prático declarado.";
}

function resumoDosDesafiosDeColeta(missao: MissaoDaTrilha): string {
  const total = (missao.desafios_de_coleta ?? []).length;
  return total > 0
    ? `${total} desafio(s) de coleta declarado(s)`
    : "Nenhum desafio de coleta declarado.";
}

function resumoDasEtiquetasDaMissao(missao: MissaoDaTrilha): string {
  return missao.etiquetas_ods.length > 0
    ? `${missao.etiquetas_ods.length} objetivo(s) etiquetado(s)`
    : "Sem ODS etiquetado nesta missão.";
}

function resumoDasAtividades(missao: MissaoDaTrilha): string {
  return missao.atividades.length > 0
    ? `${missao.atividades.length} atividade(s)`
    : "Nenhuma atividade declarada.";
}

function resumoDosConteudos(missao: MissaoDaTrilha): string {
  const total = (missao.conteudos ?? []).length;
  return total > 0 ? `${total} conteúdo(s)` : "Nenhum conteúdo declarado.";
}

function resumoDaBibliografia(missao: MissaoDaTrilha): string {
  const total = (missao.bibliografia ?? []).length;
  return total > 0 ? `${total} entrada(s) de bibliografia` : "Nenhuma bibliografia declarada.";
}

function resumoDaRecompensa(quantidade: number): string {
  return quantidade > 0
    ? `${quantidade} recompensa(s) declarada(s)`
    : "Nenhuma recompensa declarada para este marco.";
}

// A trilha em rascunho existe sem sondagem — a marcação só distingue quando
// o Mestre a declara (`RF-09-81`, design — decisões).
export function ListaDeMissoes({
  idDaTrilha,
  missoes,
  tiposDeColeta,
  tiposDeRecurso,
  recompensasDeMarco,
  onAtualizarMissao,
  onDeclararRecompensa,
}: Props) {
  const [missaoComFormulario, definirMissaoComFormulario] = useState<string | null>(null);
  const [missaoComFormularioDeConteudo, definirMissaoComFormularioDeConteudo] = useState<
    string | null
  >(null);
  const [missaoComFormularioDeColeta, definirMissaoComFormularioDeColeta] = useState<
    string | null
  >(null);
  const [missaoEmPreVisualizacao, definirMissaoEmPreVisualizacao] = useState<string | null>(
    null,
  );
  // Os três blocos que fecham ao gravar (atividade, conteúdo, desafio de
  // coleta) desmontam o formulário — o bloco recolhível, que permanece,
  // guarda o instante da última gravação de cada um (documento 15 §6.2,
  // design — decisão 5).
  const [gravadoEm, definirGravadoEm] = useState<Record<string, Date>>({});
  const tipoPorId = new Map(tiposDeColeta.map((tipo) => [tipo.id, tipo]));

  if (missoes.length === 0) {
    return <EstadoDaLista>Nenhuma missão acrescentada ainda.</EstadoDaLista>;
  }

  const missoesNaOrdem = [...missoes].sort((a, b) => a.posicao - b.posicao);

  function marcarGravado(chave: string) {
    definirGravadoEm((atual) => ({ ...atual, [chave]: new Date() }));
  }

  return (
    <ul className="lista-de-missoes" aria-label="Missões da trilha">
      {missoesNaOrdem.map((missao) => (
        <li key={missao.id} className="lista-de-missoes__item">
          <div className="lista-de-missoes__linha">
            <span className="lista-de-missoes__posicao">{missao.posicao}.</span>
            <span className="lista-de-missoes__titulo">{missao.titulo}</span>
            {missao.e_sondagem && <span className="lista-de-missoes__sondagem">Sondagem</span>}
            <span className="lista-de-missoes__etapa">
              {ROTULO_DA_ETAPA[missao.etapa_do_ciclo] ?? missao.etapa_do_ciclo}
            </span>
            <span className="lista-de-missoes__obrigatoriedade">
              {missao.obrigatoria ? "Obrigatória" : "Opcional"}
            </span>
          </div>

          <BlocoRecolhivel
            titulo="Template da missão"
            resumo="Sugestão de estrutura por IA para esta missão."
          >
            <TemplateDaMissao missao={missao} onAtualizada={onAtualizarMissao} />
          </BlocoRecolhivel>

          <BlocoRecolhivel titulo="Conteúdo" resumo={resumoDosConteudos(missao)}>
            <section aria-label={`Conteúdo de ${missao.titulo}`}>
              <ul>
                {(missao.conteudos ?? []).map((conteudo) => (
                  <li key={conteudo.id}>
                    {conteudo.tipo}
                    {conteudo.autoria === "terceiro" && conteudo.fonte && (
                      <> — fonte: {conteudo.fonte}</>
                    )}
                  </li>
                ))}
              </ul>

              {missaoComFormularioDeConteudo === missao.id ? (
                <FormularioDeConteudo
                  idDaMissao={missao.id}
                  onSalvo={(conteudo) => {
                    definirMissaoComFormularioDeConteudo(null);
                    marcarGravado(`${missao.id}:conteudo`);
                    onAtualizarMissao({
                      ...missao,
                      conteudos: [...(missao.conteudos ?? []), conteudo],
                    });
                  }}
                  onCancelar={() => definirMissaoComFormularioDeConteudo(null)}
                />
              ) : (
                <Botao
                  variante="secundaria"
                  onClick={() => definirMissaoComFormularioDeConteudo(missao.id)}
                >
                  Novo conteúdo
                </Botao>
              )}
              <MarcaDeGravacao instante={gravadoEm[`${missao.id}:conteudo`] ?? null} />
            </section>
          </BlocoRecolhivel>

          <BlocoRecolhivel titulo="Bibliografia" resumo={resumoDaBibliografia(missao)}>
            <Bibliografia
              idDaMissao={missao.id}
              entradas={missao.bibliografia ?? []}
              onSalva={(bibliografia) =>
                onAtualizarMissao({
                  ...missao,
                  bibliografia: [...(missao.bibliografia ?? []), bibliografia],
                })
              }
            />
          </BlocoRecolhivel>

          <BlocoRecolhivel titulo="Cadência de retomada" resumo={resumoDaCadencia(missao)}>
            <CadenciaDeRetomada missao={missao} onAtualizada={onAtualizarMissao} />
          </BlocoRecolhivel>

          <BlocoRecolhivel titulo="Atividades" resumo={resumoDasAtividades(missao)}>
            <ul aria-label={`Atividades de ${missao.titulo}`}>
              {missao.atividades.map((atividade) => (
                <li key={atividade.id}>
                  {atividade.titulo} — {atividade.modalidade} / {atividade.formato}
                </li>
              ))}
            </ul>

            {missaoComFormulario === missao.id ? (
              <FormularioDeAtividade
                idDaMissao={missao.id}
                onSalvo={(atividade) => {
                  definirMissaoComFormulario(null);
                  marcarGravado(`${missao.id}:atividades`);
                  onAtualizarMissao({
                    ...missao,
                    atividades: [...missao.atividades, atividade],
                  });
                }}
                onCancelar={() => definirMissaoComFormulario(null)}
              />
            ) : (
              <Botao
                variante="secundaria"
                onClick={() => definirMissaoComFormulario(missao.id)}
              >
                Nova atividade
              </Botao>
            )}
            <MarcaDeGravacao instante={gravadoEm[`${missao.id}:atividades`] ?? null} />
          </BlocoRecolhivel>

          <BlocoRecolhivel
            titulo={missao.e_sondagem ? "Sondagem" : "Desafio de desbloqueio"}
            resumo={resumoDoDesafioDeDesbloqueio(missao)}
          >
            <DesafioDeDesbloqueio missao={missao} onAtualizada={onAtualizarMissao} />
          </BlocoRecolhivel>

          <BlocoRecolhivel
            titulo="Recompensa pelo desbloqueio"
            resumo={resumoDaRecompensa(
              recompensasDeMarco.filter((r) => r.missao_id === missao.id).length,
            )}
          >
            <DeclaracaoDeRecompensa
              idDaTrilha={idDaTrilha}
              missao={missao}
              tiposDeRecurso={tiposDeRecurso}
              recompensas={recompensasDeMarco.filter((r) => r.missao_id === missao.id)}
              onDeclarada={onDeclararRecompensa}
            />
          </BlocoRecolhivel>

          <BlocoRecolhivel
            titulo="Desafios de coleta"
            resumo={resumoDosDesafiosDeColeta(missao)}
          >
            <section aria-label={`Desafios de coleta de ${missao.titulo}`}>
              {(missao.desafios_de_coleta ?? []).length === 0 ? (
                <p>Esta missão ainda não tem desafio de coleta declarado.</p>
              ) : (
                <ul>
                  {(missao.desafios_de_coleta ?? []).map((desafio) => {
                    const tipo = tipoPorId.get(desafio.tipo_de_coleta_id);
                    return (
                      <li key={desafio.id}>
                        {tipo ? tipo.nome : "Tipo de coleta"} ·{" "}
                        {ROTULO_DA_CADENCIA_DE_COLETA[desafio.cadencia]} ·{" "}
                        {rotuloDoNivel(desafio.granularidade_exigida)} ·{" "}
                        {desafio.registros_que_pontuam_por_periodo} registro(s) por período
                      </li>
                    );
                  })}
                </ul>
              )}

              {missaoComFormularioDeColeta === missao.id ? (
                <FormularioDeDesafioDeColeta
                  idDaMissao={missao.id}
                  tiposDeColeta={tiposDeColeta}
                  onSalvo={(desafio) => {
                    definirMissaoComFormularioDeColeta(null);
                    marcarGravado(`${missao.id}:coleta`);
                    onAtualizarMissao({
                      ...missao,
                      desafios_de_coleta: [...(missao.desafios_de_coleta ?? []), desafio],
                    });
                  }}
                  onCancelar={() => definirMissaoComFormularioDeColeta(null)}
                />
              ) : (
                <Botao
                  variante="secundaria"
                  onClick={() => definirMissaoComFormularioDeColeta(missao.id)}
                >
                  Novo desafio de coleta
                </Botao>
              )}
              <MarcaDeGravacao instante={gravadoEm[`${missao.id}:coleta`] ?? null} />
            </section>
          </BlocoRecolhivel>

          <BlocoRecolhivel titulo="ODS da missão" resumo={resumoDasEtiquetasDaMissao(missao)}>
            <EtiquetasOds
              alvo="missao"
              id={missao.id}
              etiquetas={missao.etiquetas_ods}
              onSalvo={(etiquetas) =>
                onAtualizarMissao({ ...missao, etiquetas_ods: etiquetas })
              }
            />
          </BlocoRecolhivel>

          {missaoEmPreVisualizacao === missao.id ? (
            <PreVisualizacaoDaMissao
              missao={missao}
              autorNome={null}
              onFechar={() => definirMissaoEmPreVisualizacao(null)}
            />
          ) : (
            <Botao
              variante="secundaria"
              onClick={() => definirMissaoEmPreVisualizacao(missao.id)}
            >
              Pré-visualizar missão
            </Botao>
          )}
        </li>
      ))}
    </ul>
  );
}
