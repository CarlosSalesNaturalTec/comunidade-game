import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { useState } from "react";

interface Props {
  ativo: boolean;
  aoEditar: () => void;
  desativar: (token: string) => Promise<unknown>;
  reativar: (token: string) => Promise<unknown>;
  excluir: (token: string) => Promise<unknown>;
  // Chamada depois de toda escrita bem-sucedida, para a lista recarregar.
  aoAlterar: () => void;
}

type Confirmacao = "desativar" | "excluir" | null;

const RECUSA_POR_PAPEL = "Só o Admin mantém os catálogos.";

// Editar, Desativar/Reativar e Excluir de um tipo de qualquer dos dois
// catálogos. Desativar e Excluir pedem confirmação em dois passos, no molde
// de `DesativarPoder`; Reativar não, porque só devolve o tipo à escolha
// (`RF-02-115`, `RF-07-52`, `RN-07-40`, `RN-08-30`, design — decisão 8).
export function AcoesDoTipo({
  ativo,
  aoEditar,
  desativar,
  reativar,
  excluir,
  aoAlterar,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [confirmando, definirConfirmando] = useState<Confirmacao>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function executar(ato: (token: string) => Promise<unknown>, falha: string) {
    if (!sessao) return;
    definirErro(null);
    definirEnviando(true);
    try {
      await ato(sessao.token);
      definirConfirmando(null);
      aoAlterar();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "permissao_negada") {
        definirErro(RECUSA_POR_PAPEL);
        return;
      }
      // Tipo já usado não se exclui: o caminho é a desativação
      // (`RN-07-40`, `RN-08-30`).
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "tipo_em_uso") {
        definirConfirmando(null);
        definirErro(
          "Este tipo já está em uso e não pode ser excluído. Você pode desativá-lo: ele deixa " +
            "de ser oferecido, e o que já foi registrado com ele continua como está.",
        );
        return;
      }
      definirErro(falha);
    } finally {
      definirEnviando(false);
    }
  }

  if (confirmando === "desativar") {
    return (
      <div>
        <Aviso tipo="atencao">
          O tipo deixa de ser oferecido em escolha nova. Nada do que já existe com ele muda.
        </Aviso>
        {erro && <Aviso tipo="erro">{erro}</Aviso>}
        <Botao
          onClick={() =>
            executar(
              desativar,
              "Não foi possível desativar o tipo. Tente novamente em instantes.",
            )
          }
          desabilitado={enviando}
        >
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
          Só se exclui tipo que nunca foi usado. A exclusão não se desfaz.
        </Aviso>
        {erro && <Aviso tipo="erro">{erro}</Aviso>}
        <Botao
          onClick={() =>
            executar(excluir, "Não foi possível excluir o tipo. Tente novamente em instantes.")
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
    <div className="catalogo__acoes">
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Botao variante="secundaria" onClick={aoEditar}>
        Editar
      </Botao>
      {ativo ? (
        <Botao variante="secundaria" onClick={() => definirConfirmando("desativar")}>
          Desativar
        </Botao>
      ) : (
        <Botao
          variante="secundaria"
          desabilitado={enviando}
          onClick={() =>
            executar(
              reativar,
              "Não foi possível reativar o tipo. Tente novamente em instantes.",
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
