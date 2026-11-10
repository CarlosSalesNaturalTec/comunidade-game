import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { eu as lerSessao } from "comum/autenticacao/api";
import {
  type AvatarDoGuerreiro,
  lerAvatar,
  MontagemDoAvatar,
  regravarAvatar,
} from "comum/avatar";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import { alterarMeuAvatar } from "../api/carteira";

interface Props {
  aoSalvar: () => void;
  aoVoltar: () => void;
}

const FALHA_AO_SALVAR = "Não deu para salvar o seu avatar agora. Tente de novo em instantes.";
const FALHA_AO_CARREGAR = "Não deu para abrir o seu avatar agora. Tente de novo em instantes.";

// O Guerreiro(a) muda o próprio avatar: todas as nove camadas, a qualquer
// tempo e sem limite de vezes (`RF-05-51`, decisão do fundador de 2026-11-10).
// A montagem abre no avatar vigente — o que `GET /v1/eu` devolve, ou o padrão
// do projeto quando falta (documento 15 §7.3) —, e trocar traço não grava
// nada: só "Salvar o meu avatar" chama o núcleo.
//
// O texto gravado é refeito a partir do vigente por `regravarAvatar`, para a
// forma de tratamento que viaja ao lado do objeto do §7.2 nunca se perder na
// troca (design — decisão 2). Nenhuma câmera nem imagem real entra aqui: o
// avatar é o único retrato da criança (`RN-05-15`).
export function AlterarMeuAvatar({ aoSalvar, aoVoltar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [textoVigente, definirTextoVigente] = useState<string | null | undefined>(undefined);
  const [avatar, definirAvatar] = useState<AvatarDoGuerreiro | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [salvando, definirSalvando] = useState(false);

  useEffect(() => {
    if (!sessao) return;
    const token = sessao.token;
    let cancelado = false;

    lerSessao(token)
      .then((quemSou) => {
        if (cancelado) return;
        definirTextoVigente(quemSou.avatar ?? null);
        definirAvatar(lerAvatar(quemSou.avatar));
      })
      .catch((erroCapturado: unknown) => {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro(FALHA_AO_CARREGAR);
      });

    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  async function salvar() {
    if (!sessao || !avatar) return;
    definirErro(null);
    definirSalvando(true);
    try {
      await alterarMeuAvatar(sessao.token, regravarAvatar(textoVigente, avatar));
      aoSalvar();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      // A montagem segue aberta com o que foi escolhido, para tentar de novo
      // (`RN-05-48`, PRD-05 §10).
      definirErro(FALHA_AO_SALVAR);
    } finally {
      definirSalvando(false);
    }
  }

  return (
    <section className="cg-meu-avatar" aria-label="Meu avatar">
      <h2>Meu avatar</h2>
      {avatar === null && !erro && <EstadoDaLista>Abrindo o seu avatar…</EstadoDaLista>}
      {avatar !== null && <MontagemDoAvatar avatar={avatar} aoAlterar={definirAvatar} />}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <div className="cg-meu-avatar__acoes">
        {avatar !== null && (
          <Botao onClick={salvar} desabilitado={salvando}>
            {salvando ? "Salvando…" : "Salvar o meu avatar"}
          </Botao>
        )}
        <Botao variante="secundaria" onClick={aoVoltar} desabilitado={salvando}>
          Voltar sem salvar
        </Botao>
      </div>
    </section>
  );
}
