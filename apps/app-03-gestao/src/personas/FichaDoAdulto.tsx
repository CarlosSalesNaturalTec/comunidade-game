import { Botao, EstadoDaLista } from "comum/react";
import { useState } from "react";
import type { AdultoDaLista } from "./api";
import { FormularioDeNick } from "./FormularioDeNick";

interface Props {
  adulto: AdultoDaLista;
  onNickGravado: () => void;
}

// Ficha de leitura: a prova que sustentou o cadastro de Mestre ou de
// Apoiador, conferível pelo Admin. NEVER oferece editar, restaurar ou
// remover artefato, nem nome, e-mail, WhatsApp ou papel (`RF-02-02`,
// `RF-02-03`, `RF-02-04`, `RN-02-01`, `RN-09-14`) — só o caminho de gravar
// o nick que falta (`RF-02-01`, `RN-14-10`). O artefato do cadastro que o
// próprio adulto editou aparece marcado, com o original ao lado do
// vigente — decisão do fundador, 2026-09-06.
export function FichaDoAdulto({ adulto, onNickGravado }: Props) {
  const [gravandoNick, definirGravandoNick] = useState(false);

  return (
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
      <div>
        <dt>Artefatos comprobatórios</dt>
        <dd>
          {adulto.artefatos.length === 0 ? (
            <EstadoDaLista>Nenhum artefato registrado.</EstadoDaLista>
          ) : (
            <ul>
              {adulto.artefatos.map((artefato) => (
                <li key={artefato.endereco}>
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
                    )}
                </li>
              ))}
            </ul>
          )}
        </dd>
      </div>
    </dl>
  );
}
