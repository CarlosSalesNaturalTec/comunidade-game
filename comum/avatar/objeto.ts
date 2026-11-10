import { CAMADAS_DO_AVATAR, type NomeDeCamada, tracoDoCatalogo } from "./catalogo";

// O objeto pequeno e versionado do documento 15 §7.2 — o que o núcleo guarda
// no campo `avatar`, opaco a ele. Duas regras governam a leitura:
//
// - **Traço desconhecido cai no padrão da camada** e nunca quebra a
//   renderização. É o que permite crescer o catálogo sem migrar avatar de
//   ninguém, e o que faz o avatar gravado antes deste contrato continuar
//   desenhando (design — decisão 2).
// - **Avatar que falta usa o avatar padrão do projeto** (documento 15 §7.3).
//   Ele não é composição à parte: é a composição dos padrões das nove camadas,
//   em cores da marca. Assim um avatar sem nenhum traço conhecido — o texto
//   livre gravado no onboarding antigo, por exemplo — chega por si ao mesmo
//   desenho, sem caso especial.

export const VERSAO_DO_AVATAR = 1;

export type EscolhasDoAvatar = Record<NomeDeCamada, string>;

export interface AvatarDoGuerreiro extends EscolhasDoAvatar {
  v: number;
}

function composicaoPadrao(): EscolhasDoAvatar {
  return Object.fromEntries(
    CAMADAS_DO_AVATAR.map((camada) => [camada.nome, camada.padrao]),
  ) as EscolhasDoAvatar;
}

/** O avatar padrão do projeto (documento 15 §7.3): mesmo sistema, composição
 * fixa e neutra, em cores da marca. Ocupa o lugar de qualquer avatar que
 * falte, na mesma moldura dos demais. */
export const AVATAR_PADRAO_DO_PROJETO: AvatarDoGuerreiro = {
  v: VERSAO_DO_AVATAR,
  ...composicaoPadrao(),
};

function objetoOuNulo(valor: unknown): Record<string, unknown> | null {
  return typeof valor === "object" && valor !== null && !Array.isArray(valor)
    ? (valor as Record<string, unknown>)
    : null;
}

/** Resolve qualquer valor bruto no objeto do §7.2, camada por camada. */
export function resolverAvatar(bruto: unknown): AvatarDoGuerreiro {
  let objeto = objetoOuNulo(bruto);
  // A App 01 grava o objeto **aninhado**, ao lado da forma de tratamento, que
  // o documento 15 §7 exige como campo próprio e que o núcleo não tem coluna
  // para guardar (design — decisão 3). Quem lê aceita as duas formas: o
  // objeto sozinho ou dentro do envelope.
  if (objeto && objetoOuNulo(objeto.avatar)) objeto = objetoOuNulo(objeto.avatar);
  if (!objeto) return AVATAR_PADRAO_DO_PROJETO;

  const escolhas = CAMADAS_DO_AVATAR.map((camada) => {
    const escolhido = objeto?.[camada.nome];
    const conhecido =
      typeof escolhido === "string" && tracoDoCatalogo(camada.nome, escolhido) !== null;
    return [camada.nome, conhecido ? (escolhido as string) : camada.padrao];
  });

  return { v: VERSAO_DO_AVATAR, ...Object.fromEntries(escolhas) } as AvatarDoGuerreiro;
}

/** Lê o texto que o núcleo guardou no campo `avatar`. Texto ausente, vazio ou
 * que não é JSON nenhum não é erro: é avatar que falta, e desenha o padrão do
 * projeto (documento 15 §7.3). */
export function lerAvatar(texto: string | null | undefined): AvatarDoGuerreiro {
  if (!texto) return AVATAR_PADRAO_DO_PROJETO;
  try {
    return resolverAvatar(JSON.parse(texto));
  } catch {
    return AVATAR_PADRAO_DO_PROJETO;
  }
}

/** Monta o objeto versionado a gravar, a partir do que foi escolhido. Camada
 * não escolhida fica no padrão dela, e quem chama grava o objeto como texto —
 * sozinho ou aninhado ao lado da forma de tratamento. */
export function escreverAvatar(escolhas: Partial<EscolhasDoAvatar>): AvatarDoGuerreiro {
  return resolverAvatar({ v: VERSAO_DO_AVATAR, ...escolhas });
}

/** Monta o texto a gravar quando o avatar é **alterado**, a partir do texto
 * vigente. Se o vigente é o envelope da App 01 — o objeto do §7.2 em `avatar`,
 * ao lado da forma de tratamento —, troca só o objeto e preserva as demais
 * chaves: alterar o avatar nunca apaga a forma de tratamento (`RF-05-51`,
 * documento 15 §7). Objeto sozinho, texto livre antigo ou nada não têm o que
 * preservar, e o objeto novo é gravado sozinho. */
export function regravarAvatar(
  textoVigente: string | null | undefined,
  avatarNovo: AvatarDoGuerreiro,
): string {
  if (textoVigente) {
    try {
      const vigente = objetoOuNulo(JSON.parse(textoVigente));
      if (vigente && objetoOuNulo(vigente.avatar)) {
        return JSON.stringify({ ...vigente, avatar: avatarNovo });
      }
    } catch {
      // Texto que não é JSON: não há envelope a preservar.
    }
  }
  return JSON.stringify(avatarNovo);
}
