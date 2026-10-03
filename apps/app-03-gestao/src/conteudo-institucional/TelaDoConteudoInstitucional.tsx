import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import {
  lerConteudoInstitucional,
  SECOES,
  type SecaoInstitucional,
  type SecaoPublicada,
} from "./api";
import { FormularioDaSecao } from "./FormularioDaSecao";

function formatarPublicacao(publicada: SecaoPublicada): string {
  if (!publicada.publicado_em) return "Nunca publicada.";
  const data = new Date(publicada.publicado_em);
  const quando = Number.isNaN(data.getTime())
    ? publicada.publicado_em
    : data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
  // Sem autor é a semeadura da implantação, que não tem persona por trás — a
  // tela diz o que sabe, e NUNCA inventa um nome.
  return publicada.autor_id
    ? `Publicado por ${publicada.autor_id} em ${quando}.`
    : `Publicado na implantação, em ${quando}.`;
}

// Área própria, não fila nem cadastro: as três seções que a vitrine
// apresenta, editadas uma por vez. A leitura é a de Admin, que traz autor e
// data — a pública, sob `/vitrine`, os omite de propósito (`RF-02-80`,
// `RF-03-45`, design — decisão 1).
export function TelaDoConteudoInstitucional() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [secoes, definirSecoes] = useState<SecaoPublicada[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [publicada, definirPublicada] = useState<SecaoInstitucional | null>(null);

  const ehAdmin = sessao?.papel === "admin";

  const carregar = useCallback(async () => {
    if (!sessao || !ehAdmin) return;
    try {
      definirSecoes(await lerConteudoInstitucional(sessao.token));
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro(
        "Não foi possível carregar o conteúdo institucional. Tente novamente em instantes.",
      );
    }
  }, [sessao, ehAdmin, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  return (
    <Moldura>
      <Cabecalho titulo="Conteúdo institucional" />

      {!ehAdmin && (
        <Aviso tipo="atencao">
          Esta área é do Admin. Fale com um Admin da comunidade se precisar publicar o conteúdo
          institucional da vitrine.
        </Aviso>
      )}

      {ehAdmin && (
        <>
          {erro && <Aviso tipo="erro">{erro}</Aviso>}

          {secoes === null && !erro && (
            <EstadoDaLista>Carregando o conteúdo institucional…</EstadoDaLista>
          )}

          {secoes !== null &&
            SECOES.map(({ chave, rotulo }) => {
              const atual = secoes.find((item) => item.secao === chave);
              if (!atual) return null;
              return (
                <section key={chave} aria-labelledby={`secao-${chave}`}>
                  <h3 id={`secao-${chave}`}>{rotulo}</h3>
                  <p>{formatarPublicacao(atual)}</p>

                  {publicada === chave && (
                    <Aviso tipo="sucesso">{rotulo} passou a valer com o texto novo.</Aviso>
                  )}

                  <FormularioDaSecao
                    secao={chave}
                    rotulo={rotulo}
                    publicada={atual}
                    onPublicada={(atualizada) => {
                      definirSecoes((anteriores) =>
                        (anteriores ?? []).map((item) =>
                          item.secao === chave ? atualizada : item,
                        ),
                      );
                      definirPublicada(chave);
                    }}
                  />
                </section>
              );
            })}
        </>
      )}
    </Moldura>
  );
}
