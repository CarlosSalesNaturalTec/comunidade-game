import { ErroDaApi } from "comum/api";
import { Aviso, Botao, Campo } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import {
  criarEquipeDaTrilha,
  type Equipe,
  homologarEquipeDaTrilha,
  obterMinhaEquipeDaTrilha,
  sairDaEquipe,
} from "../api/equipes";

interface Props {
  trilhaId: string;
  trilhaTitulo: string;
  tokenDoGuerreiro: string;
  /** Presente só quando quem está na sessão de trabalho do aparelho é o
   * Mestre — só ele homologa, nunca o Guerreiro(a) nem o Admin
   * (`RF-04-62`, `RN-04-18`). */
  podeHomologar: boolean;
  tokenDeTrabalho: string | null;
}

function papelOuNulo(papel: string): string | null {
  const aparado = papel.trim();
  return aparado.length === 0 ? null : aparado;
}

// A equipe da trilha — sujeito da criação original que encerra a trilha
// (`RF-04-61`, `RN-01-44`, documento 02 §5). O Guerreiro(a) cria a sua;
// voltar a um encontro depois retoma a mesma equipe, sem duplicar — não há
// listagem das equipes de terceiros para "entrar" numa alheia (design —
// decisão 7). Depois de homologada pelo Mestre a composição fica fixa, e a
// aplicação para de oferecer formar ou homologar (`RN-04-18`).
export function EquipeDaTrilha({
  trilhaId,
  trilhaTitulo,
  tokenDoGuerreiro,
  podeHomologar,
  tokenDeTrabalho,
}: Props) {
  const [equipe, definirEquipe] = useState<Equipe | null | undefined>(undefined);
  const [papel, definirPapel] = useState("");
  const [erro, definirErro] = useState<string | null>(null);
  const [emAndamento, definirEmAndamento] = useState(false);

  const carregar = useCallback(async () => {
    try {
      const encontrada = await obterMinhaEquipeDaTrilha(trilhaId, tokenDoGuerreiro);
      definirEquipe(encontrada);
    } catch {
      definirEquipe(null);
    }
  }, [trilhaId, tokenDoGuerreiro]);

  useEffect(() => {
    definirEquipe(undefined);
    carregar();
  }, [carregar]);

  async function criar() {
    definirErro(null);
    definirEmAndamento(true);
    try {
      const criada = await criarEquipeDaTrilha(trilhaId, papelOuNulo(papel), tokenDoGuerreiro);
      definirEquipe(criada);
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível formar a equipe. Tente novamente.",
      );
    } finally {
      definirEmAndamento(false);
    }
  }

  async function sair() {
    if (!equipe) return;
    definirErro(null);
    definirEmAndamento(true);
    try {
      await sairDaEquipe(equipe.id, tokenDoGuerreiro);
      definirEquipe(null);
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível sair da equipe. Tente novamente.",
      );
    } finally {
      definirEmAndamento(false);
    }
  }

  async function homologar() {
    if (!equipe || !tokenDeTrabalho) return;
    definirErro(null);
    definirEmAndamento(true);
    try {
      await homologarEquipeDaTrilha(equipe.id, tokenDeTrabalho);
      await carregar();
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível homologar a equipe. Tente novamente.",
      );
    } finally {
      definirEmAndamento(false);
    }
  }

  if (equipe === undefined) {
    return <p>Consultando a equipe da trilha…</p>;
  }

  return (
    <section aria-label="Equipe da trilha" className="cg-equipe-da-trilha">
      <h3>Equipe da trilha — {trilhaTitulo}</h3>

      {equipe === null && !podeHomologar && (
        <>
          <Campo
            rotulo="Seu papel na equipe (opcional)"
            valor={papel}
            aoAlterar={definirPapel}
          />
          <Botao onClick={criar} desabilitado={emAndamento}>
            Formar a equipe desta trilha
          </Botao>
        </>
      )}

      {equipe === null && podeHomologar && (
        <Aviso tipo="atencao">Ainda não há equipe formada desta trilha para homologar.</Aviso>
      )}

      {equipe && (
        <>
          <ul aria-label="Integrantes da equipe da trilha">
            {equipe.integrantes.map((integrante) => (
              <li key={integrante.nick}>
                {integrante.nick}
                {integrante.papel && ` — ${integrante.papel}`}
              </li>
            ))}
          </ul>

          {equipe.homologado_em ? (
            <Aviso tipo="sucesso">
              Composição fixa — esta equipe já foi homologada pelo Mestre.
            </Aviso>
          ) : podeHomologar ? (
            <>
              <p>A composição fica fixa depois de homologada.</p>
              <Botao onClick={homologar} desabilitado={emAndamento}>
                Homologar esta equipe
              </Botao>
            </>
          ) : (
            <>
              <Aviso tipo="atencao">
                Ainda não homologada — peça ao Mestre para confirmar a equipe.
              </Aviso>
              <Botao variante="secundaria" onClick={sair} desabilitado={emAndamento}>
                Sair desta equipe
              </Botao>
            </>
          )}
        </>
      )}

      {erro && <Aviso tipo="erro">{erro}</Aviso>}
    </section>
  );
}
