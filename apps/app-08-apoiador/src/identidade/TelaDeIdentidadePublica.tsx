import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Campo, Moldura } from "comum/react";
import { type FormEvent, useCallback, useEffect, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import {
  conferirDisponibilidadeDeNick,
  gravarMinhaIdentidade,
  type IdentidadeDoApoiador,
  lerMinhaIdentidade,
} from "./api";

// Marca neutra enquanto a marca gráfica do projeto for pendência do
// documento 09 — nada além de um rótulo textual, para não inventar imagem
// (`RF-14-15`, design — Risks).
const ROTULO_DO_AVATAR_PADRAO = "Avatar padrão do projeto";

// O card na moldura comum do documento 11 §8.2: avatar centralizado, nick
// abaixo e o total de moedas em destaque — a prévia, não a página pública
// do PRD-03.
function CardDoApoiador({ identidade }: { identidade: IdentidadeDoApoiador }) {
  const avatarProprio = identidade.avatar_proprio_liberado && identidade.avatar;
  return (
    <div className="cg-card-do-apoiador">
      <div
        className="cg-card-do-apoiador__avatar"
        role="img"
        aria-label={avatarProprio ? "Avatar do Apoiador" : ROTULO_DO_AVATAR_PADRAO}
      >
        {avatarProprio ? (
          <img src={identidade.avatar ?? undefined} alt="" />
        ) : (
          <span>{ROTULO_DO_AVATAR_PADRAO}</span>
        )}
      </div>
      <p className="cg-card-do-apoiador__nick">{identidade.nick ?? "—"}</p>
      <p className="cg-card-do-apoiador__moedas">{identidade.moedas_acumuladas} moedas</p>
    </div>
  );
}

// Define ou troca nick e avatar a qualquer tempo, mostra a prévia do card e,
// abaixo do piso de 10 moedas, o avatar padrão com quanto falta — sem
// cobrar nem insistir (`RF-14-12` a `RF-14-17`, `RN-14-09` a `RN-14-11`,
// PRD-14 §§5.2, 12).
export function TelaDeIdentidadePublica() {
  const { sessao } = useSessao();
  const [identidade, definirIdentidade] = useState<IdentidadeDoApoiador | null>(null);
  const [carregando, definirCarregando] = useState(true);

  const [nick, definirNick] = useState("");
  const [erroDeNick, definirErroDeNick] = useState<string | null>(null);
  const [sugestoesDeNick, definirSugestoesDeNick] = useState<string[]>([]);
  const [gravandoNick, definirGravandoNick] = useState(false);
  const [sucessoDeNick, definirSucessoDeNick] = useState(false);

  const [avatar, definirAvatar] = useState("");
  const [erroDeAvatar, definirErroDeAvatar] = useState<string | null>(null);
  const [gravandoAvatar, definirGravandoAvatar] = useState(false);
  const [sucessoDeAvatar, definirSucessoDeAvatar] = useState(false);

  const carregarIdentidade = useCallback(async () => {
    if (!sessao) return;
    definirCarregando(true);
    try {
      const lida = await lerMinhaIdentidade(sessao.token);
      definirIdentidade(lida);
      definirNick(lida.nick ?? "");
    } finally {
      definirCarregando(false);
    }
  }, [sessao]);

  useEffect(() => {
    carregarIdentidade();
  }, [carregarIdentidade]);

  async function aoGravarNick(evento: FormEvent) {
    evento.preventDefault();
    if (!sessao) return;
    definirGravandoNick(true);
    definirErroDeNick(null);
    definirSugestoesDeNick([]);
    definirSucessoDeNick(false);
    try {
      const atualizada = await gravarMinhaIdentidade({ nick }, sessao.token);
      definirIdentidade(atualizada);
      definirSucessoDeNick(true);
    } catch (erroCapturado) {
      if (erroCapturado instanceof ErroDaApi && erroCapturado.campo === "nick") {
        definirErroDeNick(erroCapturado.message);
        // As sugestões de variação vêm da mesma conferência do pré-cadastro
        // — a recusa da gravação não as traz (`RF-14-13`).
        const disponibilidade = await conferirDisponibilidadeDeNick(nick).catch(() => null);
        definirSugestoesDeNick(disponibilidade?.sugestoes ?? []);
      } else {
        definirErroDeNick(
          erroCapturado instanceof ErroDaApi
            ? erroCapturado.message
            : "Não foi possível gravar o nick. Tente novamente.",
        );
      }
    } finally {
      definirGravandoNick(false);
    }
  }

  async function aoGravarAvatar(evento: FormEvent) {
    evento.preventDefault();
    if (!sessao) return;
    definirGravandoAvatar(true);
    definirErroDeAvatar(null);
    definirSucessoDeAvatar(false);
    try {
      const atualizada = await gravarMinhaIdentidade({ avatar }, sessao.token);
      definirIdentidade(atualizada);
      definirSucessoDeAvatar(true);
    } catch (erroCapturado) {
      // O 409 do núcleo já traz quantas moedas faltam na própria mensagem
      // (`RF-14-16`, `RN-14-11`).
      definirErroDeAvatar(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível gravar o avatar. Tente novamente.",
      );
    } finally {
      definirGravandoAvatar(false);
    }
  }

  if (carregando || !identidade) {
    return (
      <Moldura>
        <Cabecalho titulo="Identidade pública" />
      </Moldura>
    );
  }

  return (
    <Moldura>
      <Cabecalho
        titulo="Identidade pública"
        subtitulo="Como você aparece para quem visita a comunidade — sempre em moedas, nunca em reais."
      />

      <AvisoDeColeta dado="o nick e o avatar da sua identidade pública" />

      <CardDoApoiador identidade={identidade} />

      <form onSubmit={aoGravarNick}>
        <Campo rotulo="Nick" valor={nick} aoAlterar={definirNick} erro={erroDeNick} />
        {sugestoesDeNick.length > 0 && (
          <p>Sugestões disponíveis: {sugestoesDeNick.join(", ")}</p>
        )}
        <Botao tipo="submit" desabilitado={gravandoNick}>
          Gravar nick
        </Botao>
      </form>
      {sucessoDeNick && <Aviso tipo="sucesso">Nick gravado.</Aviso>}

      {identidade.avatar_proprio_liberado ? (
        <form onSubmit={aoGravarAvatar}>
          <Campo
            rotulo="Avatar (endereço da imagem)"
            valor={avatar}
            aoAlterar={definirAvatar}
            erro={erroDeAvatar}
          />
          <Botao tipo="submit" desabilitado={gravandoAvatar}>
            Gravar avatar
          </Botao>
        </form>
      ) : (
        <Aviso tipo="atencao">
          Faltam {identidade.moedas_faltantes_para_avatar_proprio} moedas para liberar o avatar
          próprio. Até lá, a página mostra o avatar padrão do projeto.
        </Aviso>
      )}
      {sucessoDeAvatar && <Aviso tipo="sucesso">Avatar gravado.</Aviso>}
    </Moldura>
  );
}
