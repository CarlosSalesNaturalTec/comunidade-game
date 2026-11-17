import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo, EstadoDaLista } from "comum/react";
import { useState } from "react";
import {
  type AdultoDaLista,
  type ArtefatoComprobatorio,
  corrigirArtefatoDoAdulto,
  incluirArtefatoDoAdulto,
  type PapelDoAdulto,
  removerArtefatoDoAdulto,
} from "./api";

interface Props {
  papel: PapelDoAdulto;
  adulto: AdultoDaLista;
  aoAlterar: (adulto: AdultoDaLista) => void;
}

type Edicao = { artefatoId: string | null; rotulo: string; endereco: string };

// Os artefatos comprobatórios do adulto: incluir, corrigir e remover pela
// gestão, sempre link declarado. O último não sai — o núcleo recusa, e a
// recusa aparece aqui (`RF-02-117`, `RF-02-04`, `RN-02-01`). O artefato que o
// próprio adulto editou segue marcado, com o original ao lado do vigente, e
// a correção do Admin não apaga esse original (`RN-09-14`).
export function ArtefatosDoAdulto({ papel, adulto, aoAlterar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [edicao, definirEdicao] = useState<Edicao | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function executar(ato: (token: string) => Promise<AdultoDaLista>) {
    if (!sessao) return;
    definirErro(null);
    definirEnviando(true);
    try {
      const atualizado = await ato(sessao.token);
      definirEdicao(null);
      aoAlterar(atualizado);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.status === 422) {
        definirErro(erroCapturado.message);
        return;
      }
      definirErro("Não foi possível alterar o artefato. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  function salvar(atual: Edicao) {
    const artefato = { rotulo: atual.rotulo, endereco: atual.endereco };
    if (!artefato.rotulo.trim() || !artefato.endereco.trim()) {
      definirErro("Informe o rótulo e o endereço.");
      return;
    }
    executar((token) =>
      atual.artefatoId === null
        ? incluirArtefatoDoAdulto(papel, adulto.id, artefato, token)
        : corrigirArtefatoDoAdulto(papel, adulto.id, atual.artefatoId, artefato, token),
    );
  }

  function remover(artefato: ArtefatoComprobatorio) {
    executar((token) => removerArtefatoDoAdulto(papel, adulto.id, artefato.id, token));
  }

  const formulario = edicao && (
    <div className="cg-campo-de-artefato">
      <Campo
        rotulo="Rótulo"
        valor={edicao.rotulo}
        aoAlterar={(rotulo) => definirEdicao({ ...edicao, rotulo })}
        focoInicial
      />
      <Campo
        rotulo="Endereço"
        valor={edicao.endereco}
        aoAlterar={(endereco) => definirEdicao({ ...edicao, endereco })}
      />
      <Botao onClick={() => salvar(edicao)} desabilitado={enviando}>
        Salvar artefato
      </Botao>
      <Botao variante="secundaria" onClick={() => definirEdicao(null)}>
        Cancelar
      </Botao>
    </div>
  );

  return (
    <div>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {adulto.artefatos.length === 0 ? (
        <EstadoDaLista>Nenhum artefato registrado.</EstadoDaLista>
      ) : (
        <ul>
          {adulto.artefatos.map((artefato) => (
            <li key={artefato.id}>
              {edicao?.artefatoId === artefato.id ? (
                formulario
              ) : (
                <>
                  {artefato.rotulo}:{" "}
                  <a href={artefato.endereco} target="_blank" rel="noreferrer">
                    {artefato.endereco}
                  </a>
                  {artefato.rotulo_original !== null &&
                    artefato.rotulo_original !== undefined && (
                      <>
                        {" "}
                        <span>
                          — editado pelo próprio adulto. Declarado no cadastro como "
                          {artefato.rotulo_original}":{" "}
                        </span>
                        <a
                          href={artefato.endereco_original ?? undefined}
                          target="_blank"
                          rel="noreferrer"
                        >
                          {artefato.endereco_original}
                        </a>
                      </>
                    )}{" "}
                  <Botao
                    variante="secundaria"
                    onClick={() =>
                      definirEdicao({
                        artefatoId: artefato.id,
                        rotulo: artefato.rotulo,
                        endereco: artefato.endereco,
                      })
                    }
                  >
                    Corrigir
                  </Botao>
                  <Botao
                    variante="secundaria"
                    desabilitado={enviando}
                    onClick={() => remover(artefato)}
                  >
                    Remover
                  </Botao>
                </>
              )}
            </li>
          ))}
        </ul>
      )}
      {edicao?.artefatoId === null
        ? formulario
        : edicao === null && (
            <Botao
              variante="secundaria"
              onClick={() => definirEdicao({ artefatoId: null, rotulo: "", endereco: "" })}
            >
              Acrescentar artefato
            </Botao>
          )}
    </div>
  );
}
