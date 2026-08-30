import { Botao, EstadoDaLista } from "comum/react";
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
  const tipoPorId = new Map(tiposDeColeta.map((tipo) => [tipo.id, tipo]));

  if (missoes.length === 0) {
    return <EstadoDaLista>Nenhuma missão acrescentada ainda.</EstadoDaLista>;
  }

  const missoesNaOrdem = [...missoes].sort((a, b) => a.posicao - b.posicao);

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

          <p className="lista-de-missoes__retomada">
            {missao.cadencia_de_retomada && missao.cadencia_de_retomada.length > 0
              ? `Retomada em ${missao.cadencia_de_retomada.join(", ")} dias`
              : "Sem retomada declarada"}
          </p>
          <CadenciaDeRetomada missao={missao} onAtualizada={onAtualizarMissao} />

          <TemplateDaMissao missao={missao} onAtualizada={onAtualizarMissao} />

          <DeclaracaoDeRecompensa
            idDaTrilha={idDaTrilha}
            missao={missao}
            tiposDeRecurso={tiposDeRecurso}
            recompensas={recompensasDeMarco.filter((r) => r.missao_id === missao.id)}
            onDeclarada={onDeclararRecompensa}
          />

          <DesafioDeDesbloqueio missao={missao} onAtualizada={onAtualizarMissao} />

          <section aria-label={`Desafios de coleta de ${missao.titulo}`}>
            <h4>Desafios de coleta</h4>
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
          </section>

          <EtiquetasOds
            alvo="missao"
            id={missao.id}
            etiquetas={missao.etiquetas_ods}
            onSalvo={(etiquetas) => onAtualizarMissao({ ...missao, etiquetas_ods: etiquetas })}
          />

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
                onAtualizarMissao({
                  ...missao,
                  atividades: [...missao.atividades, atividade],
                });
              }}
              onCancelar={() => definirMissaoComFormulario(null)}
            />
          ) : (
            <Botao variante="secundaria" onClick={() => definirMissaoComFormulario(missao.id)}>
              Nova atividade
            </Botao>
          )}

          <section aria-label={`Conteúdo de ${missao.titulo}`}>
            <h3>Conteúdo</h3>
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
          </section>

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
