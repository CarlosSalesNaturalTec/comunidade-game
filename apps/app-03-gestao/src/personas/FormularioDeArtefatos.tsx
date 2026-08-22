import { Botao, Campo } from "comum/react";
import type { ArtefatoComprobatorio } from "./api";

interface Props {
  artefatos: ArtefatoComprobatorio[];
  aoAlterar: (artefatos: ArtefatoComprobatorio[]) => void;
  erro?: string | null;
}

// Endereço e rótulo declarados — nunca anexo de arquivo: a prova do adulto
// é link, não arquivo (`RF-02-04`, `RN-02-01`, documento 02 §1).
export function FormularioDeArtefatos({ artefatos, aoAlterar, erro }: Props) {
  function alterarUm(indice: number, campo: keyof ArtefatoComprobatorio, valor: string) {
    aoAlterar(
      artefatos.map((artefato, i) =>
        i === indice ? { ...artefato, [campo]: valor } : artefato,
      ),
    );
  }

  function remover(indice: number) {
    aoAlterar(artefatos.filter((_, i) => i !== indice));
  }

  function adicionar() {
    aoAlterar([...artefatos, { endereco: "", rotulo: "" }]);
  }

  return (
    <fieldset>
      <legend>Artefatos comprobatórios</legend>
      {artefatos.map((artefato, indice) => (
        // biome-ignore lint/suspicious/noArrayIndexKey: a lista não é reordenada
        <div key={indice} className="cg-campo-de-artefato">
          <Campo
            rotulo="Rótulo"
            valor={artefato.rotulo}
            aoAlterar={(valor) => alterarUm(indice, "rotulo", valor)}
          />
          <Campo
            rotulo="Endereço"
            valor={artefato.endereco}
            aoAlterar={(valor) => alterarUm(indice, "endereco", valor)}
          />
          <Botao variante="secundaria" onClick={() => remover(indice)}>
            Remover
          </Botao>
        </div>
      ))}
      {erro && (
        <p role="alert" className="cg-campo__erro">
          {erro}
        </p>
      )}
      <Botao variante="secundaria" onClick={adicionar}>
        Acrescentar artefato
      </Botao>
    </fieldset>
  );
}
