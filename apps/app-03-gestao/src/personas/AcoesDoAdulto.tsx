import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { useState } from "react";
import {
  type AdultoDaLista,
  desativarAdulto,
  excluirAdulto,
  type PapelDoAdulto,
  reativarAdulto,
} from "./api";

interface Props {
  papel: PapelDoAdulto;
  adulto: AdultoDaLista;
  aoAlterar: (adulto: AdultoDaLista) => void;
  aoExcluir: () => void;
}

type Confirmacao = "desativar" | "excluir" | null;

// Excluir, Desativar e Reativar o adulto, no molde de `AcoesDoTipo`:
// Desativar e Excluir pedem confirmação; Reativar não, porque só devolve o
// acesso. Exclusão recusada por uso aponta a desativação (`RF-02-118`,
// `RF-02-119`, `RN-02-34`, `RN-02-35`).
export function AcoesDoAdulto({ papel, adulto, aoAlterar, aoExcluir }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [confirmando, definirConfirmando] = useState<Confirmacao>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function executar(ato: (token: string) => Promise<void>, falha: string) {
    if (!sessao) return;
    definirErro(null);
    definirEnviando(true);
    try {
      await ato(sessao.token);
      definirConfirmando(null);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "permissao_negada") {
        definirErro("Só o Admin mantém o cadastro.");
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "adulto_em_uso") {
        definirConfirmando(null);
        definirErro(
          "Este cadastro já foi usado e não pode ser excluído. Você pode desativá-lo: a " +
            "pessoa perde o acesso e sai da vitrine, e o que ela já fez continua como está.",
        );
        return;
      }
      definirErro(falha);
    } finally {
      definirEnviando(false);
    }
  }

  const desativar = () =>
    executar(
      async (token) => aoAlterar(await desativarAdulto(papel, adulto.id, token)),
      "Não foi possível desativar. Tente novamente em instantes.",
    );

  if (confirmando === "desativar") {
    return (
      <div>
        <Aviso tipo="atencao">
          A pessoa perde o acesso e sai da vitrine. Nada do que ela já fez muda, e o cadastro
          pode ser reativado depois.
        </Aviso>
        {erro && <Aviso tipo="erro">{erro}</Aviso>}
        <Botao onClick={desativar} desabilitado={enviando}>
          Confirmar desativação
        </Botao>
        <Botao variante="secundaria" onClick={() => definirConfirmando(null)}>
          Voltar
        </Botao>
      </div>
    );
  }

  if (confirmando === "excluir") {
    return (
      <div>
        <Aviso tipo="atencao">
          Só se exclui cadastro que nunca foi usado. A exclusão não se desfaz.
        </Aviso>
        {erro && <Aviso tipo="erro">{erro}</Aviso>}
        <Botao
          onClick={() =>
            executar(async (token) => {
              await excluirAdulto(papel, adulto.id, token);
              aoExcluir();
            }, "Não foi possível excluir. Tente novamente em instantes.")
          }
          desabilitado={enviando}
        >
          Confirmar exclusão
        </Botao>
        <Botao variante="secundaria" onClick={() => definirConfirmando(null)}>
          Voltar
        </Botao>
      </div>
    );
  }

  return (
    <div>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {adulto.ativo ? (
        <Botao variante="secundaria" onClick={() => definirConfirmando("desativar")}>
          Desativar
        </Botao>
      ) : (
        <Botao
          variante="secundaria"
          desabilitado={enviando}
          onClick={() =>
            executar(
              async (token) => aoAlterar(await reativarAdulto(papel, adulto.id, token)),
              "Não foi possível reativar. Tente novamente em instantes.",
            )
          }
        >
          Reativar
        </Botao>
      )}
      <Botao variante="secundaria" onClick={() => definirConfirmando("excluir")}>
        Excluir
      </Botao>
    </div>
  );
}
