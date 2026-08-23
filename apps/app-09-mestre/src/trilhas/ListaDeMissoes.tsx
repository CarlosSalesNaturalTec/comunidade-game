import { Botao, EstadoDaLista } from "comum/react";
import { useState } from "react";
import type { EtapaDoCiclo, MissaoDaTrilha } from "./api";
import { CadenciaDeRetomada } from "./CadenciaDeRetomada";
import { EtiquetasOds } from "./EtiquetasOds";
import { FormularioDeAtividade } from "./FormularioDeAtividade";

interface Props {
  missoes: MissaoDaTrilha[];
  onAtualizarMissao: (missao: MissaoDaTrilha) => void;
}

const ROTULO_DA_ETAPA: Record<EtapaDoCiclo, string> = {
  abertura: "Abertura",
  desenvolvimento: "Desenvolvimento",
  marcos: "Marcos",
  fechamento: "Fechamento",
};

// A trilha em rascunho existe sem sondagem — a marcação só distingue quando
// o Mestre a declara (`RF-09-81`, design — decisões).
export function ListaDeMissoes({ missoes, onAtualizarMissao }: Props) {
  const [missaoComFormulario, definirMissaoComFormulario] = useState<string | null>(null);

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
        </li>
      ))}
    </ul>
  );
}
