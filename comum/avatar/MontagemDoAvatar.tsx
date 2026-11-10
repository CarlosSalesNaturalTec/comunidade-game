import { useId } from "react";
import { Avatar } from "./Avatar";
import { CAMADAS_DO_AVATAR, type NomeDeCamada } from "./catalogo";
import { type AvatarDoGuerreiro, escreverAvatar } from "./objeto";

interface Props {
  /** O avatar de onde a montagem parte — o vigente de quem altera, ou o de
   * partida de quem cadastra. */
  avatar: AvatarDoGuerreiro;
  aoAlterar: (avatar: AvatarDoGuerreiro) => void;
  tamanho?: number;
}

// A montagem do avatar por camada, promovida da `TelaDeCadastro` da App 01
// quando a App 05 passou a deixar o Guerreiro(a) alterar o próprio avatar
// (`RF-04-07`, `RF-05-51`, documento 15 §7). Uma escolha por camada, na ordem
// do §7.1, cada traço pelo nome dizível, com o avatar composto à vista.
//
// É controlada e não grava nada: a composição acontece toda no aparelho, e
// gravar é ato de quem a consome.
export function MontagemDoAvatar({ avatar, aoAlterar, tamanho = 96 }: Props) {
  const idDaEscolha = useId();

  function escolherTraco(camada: NomeDeCamada, tracoId: string) {
    aoAlterar(escreverAvatar({ ...avatar, [camada]: tracoId }));
  }

  return (
    <fieldset className="cg-escolha-de-avatar">
      <legend>Monte o seu avatar</legend>
      <Avatar avatar={avatar} tamanho={tamanho} />
      {CAMADAS_DO_AVATAR.map((camada) => (
        <div className="cg-campo" key={camada.nome}>
          <label htmlFor={`${idDaEscolha}-${camada.nome}`}>{camada.rotulo}</label>
          <select
            id={`${idDaEscolha}-${camada.nome}`}
            value={avatar[camada.nome]}
            onChange={(evento) => escolherTraco(camada.nome, evento.target.value)}
          >
            {camada.tracos.map((traco) => (
              <option key={traco.id} value={traco.id}>
                {traco.nome}
              </option>
            ))}
          </select>
        </div>
      ))}
    </fieldset>
  );
}
