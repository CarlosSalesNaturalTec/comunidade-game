import { chamarNucleo } from "comum/api";

// A recompensa de marco é sempre uma missão da própria trilha — o marco
// alcançado é o desbloqueio dela, nunca preço nem contrapartida do
// Guerreiro(a) (`RF-09-71`, `RF-09-84`, `RN-09-26`, `RN-09-39`).
export interface RecompensaDeMarco {
  id: string;
  trilha_id: string;
  missao_id: string;
  tipo_de_recurso_id: string;
  quantidade: string;
  autor_id: string;
  registrado_em: string;
}

export interface DeclararRecompensaDeMarcoEntrada {
  missao_id: string;
  tipo_de_recurso_id: string;
  quantidade: string;
}

export function declararRecompensaDeMarco(
  idDaTrilha: string,
  entrada: DeclararRecompensaDeMarcoEntrada,
  token: string,
): Promise<RecompensaDeMarco> {
  return chamarNucleo<RecompensaDeMarco>(`/v1/trilhas/${idDaTrilha}/recompensas-de-marco`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export function listarRecompensasDeMarco(
  idDaTrilha: string,
  token: string,
): Promise<RecompensaDeMarco[]> {
  return chamarNucleo<RecompensaDeMarco[]>(`/v1/trilhas/${idDaTrilha}/recompensas-de-marco`, {
    token,
  });
}

// A fila é da comunidade do Mestre, não da autoria da trilha: quem entrega
// é quem está no encontro (`RF-09-75`, `RN-09-18`).
export interface PendenciaDeEntrega {
  guerreiro_id: string;
  guerreiro_nick: string;
  guerreiro_avatar: string;
  trilha_id: string;
  trilha_nome: string;
  missao_id: string;
  missao_titulo: string;
  recompensa_de_marco_id: string;
  tipo_de_recurso_id: string;
  quantidade: string;
  quantidade_esgotada: boolean;
}

export function listarEntregasPendentes(token: string): Promise<PendenciaDeEntrega[]> {
  return chamarNucleo<PendenciaDeEntrega[]>("/v1/recompensas-de-marco/pendentes", { token });
}

export interface RegistrarEntregaEntrada {
  guerreiro_id: string;
  ponto_de_apoio_id: string;
}

export interface EntregaDeRecompensa {
  id: string;
  recompensa_de_marco_id: string;
  missao_id: string;
  trilha_id: string;
  tipo_de_recurso_id: string;
  quantidade: string;
  guerreiro_id: string;
  ponto_de_apoio_id: string;
  lancamento_id: string;
  autor_id: string;
  registrado_em: string;
}

// A confirmação exige o Mestre vinculado à comunidade do Guerreiro(a) e o
// lastro no ponto de apoio escolhido — as cinco recusas já são do núcleo
// (`RF-07-13`, `RN-09-26`, `RN-09-27`).
export function registrarEntrega(
  idDaRecompensa: string,
  entrada: RegistrarEntregaEntrada,
  token: string,
): Promise<EntregaDeRecompensa> {
  return chamarNucleo<EntregaDeRecompensa>(
    `/v1/recompensas-de-marco/${idDaRecompensa}/entregas`,
    {
      metodo: "POST",
      corpo: entrada,
      token,
    },
  );
}
