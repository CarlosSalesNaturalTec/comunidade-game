import { chamarNucleo } from "comum/api";

export interface AvatarENick {
  avatar: string | null;
  nick: string;
}

export interface PresencaDoPainel extends AvatarENick {
  guerreiro_id: string;
  modo: "reconhecimento" | "confirmacao";
  confirmador_id: string | null;
}

export interface GuerreiroDoPainel extends AvatarENick {
  guerreiro_id: string;
}

export interface EquipeDoPainel {
  id: string;
  integrantes: AvatarENick[];
  missao_id: string | null;
  missao_titulo: string | null;
}

export interface AtividadePrevista {
  id: string;
  titulo: string;
  missao_id: string;
  missao_titulo: string;
}

export interface RecursoProvido {
  tipo_de_recurso_id: string;
  quantidade: string;
}

export interface SaldoDoTipo {
  tipo_de_recurso_id: string;
  saldo: string;
}

export type TipoDePendencia = "lancamento_da_atividade_realizada" | "digitalizacao_do_termo";

export interface PendenciaDoPainel {
  tipo: TipoDePendencia;
  guerreiro_id: string | null;
  nick: string | null;
  consentimento_id: string | null;
}

export interface PainelDoDia {
  aula_id: string | null;
  comunidade_virtual_id: string | null;
  ponto_de_apoio_id: string | null;
  presencas: PresencaDoPainel[];
  aguardando_aparelho: GuerreiroDoPainel[];
  equipes: EquipeDoPainel[];
  atividades_previstas: AtividadePrevista[];
  recursos_providos: RecursoProvido[];
  saldo_do_ponto_de_apoio: SaldoDoTipo[];
  pendencias: PendenciaDoPainel[];
}

// O estado do encontro em andamento, numa leitura só — sondado a cada 10
// segundos pela tela (`RF-02-41` a `RF-02-47`, `RF-02-69`, documento 03 §1).
export function obterPainelDoDia(token: string): Promise<PainelDoDia> {
  return chamarNucleo<PainelDoDia>("/v1/painel-do-dia", { token });
}

export interface AnexoDoTermo {
  id: string;
  consentimento_id: string;
  registrado_em: string;
}

// Anexa a digitalização do termo de biometria assinado no encontro — PDF,
// JPG ou PNG, restrito ao Admin (`RF-02-68`).
export function anexarDigitalizacaoDoTermo(
  consentimentoId: string,
  arquivo: File,
  token: string,
): Promise<AnexoDoTermo> {
  const formulario = new FormData();
  formulario.set("digitalizacao", arquivo);

  return chamarNucleo<AnexoDoTermo>(`/v1/consentimentos/${consentimentoId}/anexo`, {
    metodo: "POST",
    formulario,
    token,
  });
}
