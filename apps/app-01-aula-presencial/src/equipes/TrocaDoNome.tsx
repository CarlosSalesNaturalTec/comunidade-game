import { ErroDaApi } from "comum/api";
import { Aviso, Botao, Campo } from "comum/react";
import { useState } from "react";
import { type Equipe, renomearEquipe, TETO_DO_NOME_DA_EQUIPE } from "../api/equipes";

interface Props {
  equipe: Equipe;
  token: string;
  aoRenomear: (equipe: Equipe) => void;
}

// Troca do nome da equipe por quem a integra (`RF-04-70`, `RN-04-39`). Quem
// chama decide quando oferecê-la — só a integrante, e nunca à equipe da
// trilha já homologada. Recusada a troca, o nome anterior segue na tela e a
// frase do núcleo aparece como é (`RN-04-36`).
export function TrocaDoNome({ equipe, token, aoRenomear }: Props) {
  const [aberta, definirAberta] = useState(false);
  const [nome, definirNome] = useState(equipe.nome);
  const [erro, definirErro] = useState<string | null>(null);
  const [emAndamento, definirEmAndamento] = useState(false);

  if (!aberta) {
    return (
      <Botao
        variante="secundaria"
        onClick={() => {
          definirNome(equipe.nome);
          definirErro(null);
          definirAberta(true);
        }}
      >
        Trocar o nome
      </Botao>
    );
  }

  async function salvar() {
    definirErro(null);
    definirEmAndamento(true);
    try {
      const renomeada = await renomearEquipe(equipe.id, nome.trim(), token);
      definirAberta(false);
      aoRenomear(renomeada);
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível trocar o nome. Tente novamente.",
      );
    } finally {
      definirEmAndamento(false);
    }
  }

  return (
    <div className="cg-troca-do-nome">
      <Campo
        rotulo="Novo nome da equipe"
        valor={nome}
        aoAlterar={definirNome}
        maxLength={TETO_DO_NOME_DA_EQUIPE}
      />
      <Botao onClick={salvar} desabilitado={emAndamento || nome.trim().length === 0}>
        Salvar o nome
      </Botao>
      <Botao
        variante="secundaria"
        onClick={() => definirAberta(false)}
        desabilitado={emAndamento}
      >
        Cancelar
      </Botao>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
    </div>
  );
}
