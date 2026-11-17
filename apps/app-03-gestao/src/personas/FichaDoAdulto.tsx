import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useState } from "react";
import { AcoesDoAdulto } from "./AcoesDoAdulto";
import { AportesDoAdulto } from "./AportesDoAdulto";
import { ArtefatosDoAdulto } from "./ArtefatosDoAdulto";
import type { AdultoDaLista, PapelDoAdulto } from "./api";
import { EdicaoDoAdulto } from "./EdicaoDoAdulto";
import { FormularioDeNick } from "./FormularioDeNick";

interface Props {
  papel: PapelDoAdulto;
  adulto: AdultoDaLista;
  // Só o Admin mantém o cadastro; os outros papéis veem a ficha de leitura.
  podeManter: boolean;
  onNickGravado: () => void;
  onAlterado: (adulto: AdultoDaLista) => void;
  onExcluido: () => void;
}

// A ficha de Mestre ou de Apoiador: a prova que sustentou o cadastro,
// conferível pelo Admin, que também corrige nome, e-mail, WhatsApp e
// artefatos e exclui, desativa ou reativa (`RF-02-117` a `RF-02-119`,
// `RN-02-34`, `RN-02-35`). Nick já gravado, papel e termos de doação não se
// alteram aqui — trocar nick é ato do próprio adulto (documento 02 §1); o
// nick que falta se grava pela ficha (`RF-02-01`, `RN-14-10`).
export function FichaDoAdulto({
  papel,
  adulto,
  podeManter,
  onNickGravado,
  onAlterado,
  onExcluido,
}: Props) {
  const [gravandoNick, definirGravandoNick] = useState(false);
  const [editando, definirEditando] = useState(false);

  return (
    <div>
      {!adulto.ativo && (
        <Aviso tipo="atencao">Cadastro desativado — sem acesso e fora da vitrine.</Aviso>
      )}
      {editando ? (
        <EdicaoDoAdulto
          papel={papel}
          adulto={adulto}
          aoSalvar={(salvo) => {
            definirEditando(false);
            onAlterado(salvo);
          }}
          aoCancelar={() => definirEditando(false)}
        />
      ) : (
        <dl>
          <div>
            <dt>Nome</dt>
            <dd>{adulto.nome}</dd>
          </div>
          <div>
            <dt>E-mail</dt>
            <dd>{adulto.email}</dd>
          </div>
          <div>
            <dt>WhatsApp</dt>
            <dd>{adulto.whatsapp ?? "Não informado"}</dd>
          </div>
          <div>
            <dt>Nick</dt>
            <dd>
              {adulto.nick !== null ? (
                adulto.nick
              ) : gravandoNick ? (
                <FormularioDeNick
                  personaId={adulto.id}
                  onGravado={onNickGravado}
                  onCancelar={() => definirGravandoNick(false)}
                />
              ) : (
                <>
                  <EstadoDaLista>Sem nick — não aparece em superfície pública.</EstadoDaLista>
                  <Botao variante="secundaria" onClick={() => definirGravandoNick(true)}>
                    Gravar nick
                  </Botao>
                </>
              )}
            </dd>
          </div>
        </dl>
      )}
      {podeManter && !editando && (
        <Botao variante="secundaria" onClick={() => definirEditando(true)}>
          Editar dados
        </Botao>
      )}

      <h4>Artefatos comprobatórios</h4>
      {podeManter ? (
        <ArtefatosDoAdulto papel={papel} adulto={adulto} aoAlterar={onAlterado} />
      ) : adulto.artefatos.length === 0 ? (
        <EstadoDaLista>Nenhum artefato registrado.</EstadoDaLista>
      ) : (
        <ul>
          {adulto.artefatos.map((artefato) => (
            <li key={artefato.id}>
              {artefato.rotulo}:{" "}
              <a href={artefato.endereco} target="_blank" rel="noreferrer">
                {artefato.endereco}
              </a>
            </li>
          ))}
        </ul>
      )}

      <h4>Aportes</h4>
      <AportesDoAdulto provedorId={adulto.id} />

      {podeManter && (
        <AcoesDoAdulto
          papel={papel}
          adulto={adulto}
          aoAlterar={onAlterado}
          aoExcluir={onExcluido}
        />
      )}
    </div>
  );
}
