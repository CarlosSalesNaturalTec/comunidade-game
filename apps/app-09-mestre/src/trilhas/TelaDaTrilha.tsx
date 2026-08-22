import { Botao, Cabecalho, Moldura } from "comum/react";
import { useState } from "react";
import type { MissaoDaTrilha, TrilhaDoMestre } from "./api";
import { FormularioDeMissao } from "./FormularioDeMissao";
import { ListaDeMissoes } from "./ListaDeMissoes";

interface Props {
  trilha: TrilhaDoMestre;
  aoVoltar: () => void;
  onAtualizarTrilha: (trilha: TrilhaDoMestre) => void;
}

export function TelaDaTrilha({ trilha, aoVoltar, onAtualizarTrilha }: Props) {
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);

  function aoAcrescentarMissao(missao: MissaoDaTrilha) {
    definirMostrarFormulario(false);
    onAtualizarTrilha({ ...trilha, missoes: [...trilha.missoes, missao] });
  }

  function aoAtualizarMissao(missaoAtualizada: MissaoDaTrilha) {
    onAtualizarTrilha({
      ...trilha,
      missoes: trilha.missoes.map((missao) =>
        missao.id === missaoAtualizada.id ? missaoAtualizada : missao,
      ),
    });
  }

  return (
    <Moldura>
      <Cabecalho
        titulo={trilha.nome}
        subtitulo={trilha.objetivo}
        acao={{ rotulo: "Voltar", aoAcionar: aoVoltar }}
      />

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

      <ListaDeMissoes missoes={trilha.missoes} onAtualizarMissao={aoAtualizarMissao} />
    </Moldura>
  );
}
