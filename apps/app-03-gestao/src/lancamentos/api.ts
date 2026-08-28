import { chamarNucleo } from "comum/api";

export const DESFECHOS = [
  { valor: "realizada", rotulo: "Realizada" },
  { valor: "realizada_com_merito", rotulo: "Realizada com mérito" },
  { valor: "merito_extra_por_auxilio", rotulo: "Mérito extra por auxílio aos colegas" },
] as const;

export type Desfecho = (typeof DESFECHOS)[number]["valor"];

export interface ParticipanteDoLancamento {
  guerreiro_id: string;
  atividade_id: string;
  momento_do_fato: string;
  producao: string;
  desfecho: Desfecho;
}

interface AulaAposLancamento {
  id: string;
  situacao: string;
}

// O lançamento é um único ato por aula, que converte as reservas em baixa
// e passa a aula a realizada — não há operação de baixa separada
// (`RF-02-34`, `RF-02-39`, `RF-07-09`).
export function lancarAtividadeRealizada(
  idDaAula: string,
  participantes: ParticipanteDoLancamento[],
  token: string,
): Promise<AulaAposLancamento> {
  return chamarNucleo<AulaAposLancamento>(`/v1/aulas/${idDaAula}/lancamentos`, {
    metodo: "POST",
    corpo: { resultados: participantes },
    token,
  });
}

export interface ConfirmarPresencaEntrada {
  guerreiro_id: string;
  modo: "confirmacao";
  momento_do_fato: string;
}

interface PresencaCriada {
  id: string;
  aula_id: string;
  guerreiro_id: string;
  modo: string;
  confirmador_id: string | null;
  momento_do_fato: string;
  anulada_em: string | null;
  anulada_por_id: string | null;
  motivo_da_anulacao: string | null;
}

// A área só oferece o modo confirmação: o reconhecimento é exclusivo da
// App 01, sob a sessão de trabalho do aparelho (`RF-02-36`, `RF-04-18`).
export function confirmarPresenca(
  idDaAula: string,
  entrada: ConfirmarPresencaEntrada,
  token: string,
): Promise<PresencaCriada> {
  return chamarNucleo<PresencaCriada>(`/v1/aulas/${idDaAula}/presencas`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// Desfaz a presença registrada por engano sem apagá-la, liberando o par
// (aula, guerreiro) para o registro correto (`RF-02-36`, `RN-02-12`).
export function anularPresenca(
  idDaAula: string,
  idDaPresenca: string,
  motivo: string,
  token: string,
): Promise<PresencaCriada> {
  return chamarNucleo<PresencaCriada>(
    `/v1/aulas/${idDaAula}/presencas/${idDaPresenca}/anulacao`,
    { metodo: "POST", corpo: { motivo }, token },
  );
}

export interface RegistrarOcorrenciaEntrada {
  guerreiro_id: string;
  aula_id: string;
  atividade_id: string;
  motivo: string;
  momento_do_fato: string;
}

interface OcorrenciaCriada {
  id: string;
  guerreiro_id: string;
  aula_id: string;
  atividade_id: string;
  valor: number;
  motivo: string | null;
  momento_do_fato: string;
}

// Vale no ato, sem fila de revisão — o valor vem da tabela do documento 11
// §5, e a tela nunca o declara (`RF-02-37`, `RN-02-13`).
export function registrarOcorrenciaDeConduta(
  entrada: RegistrarOcorrenciaEntrada,
  token: string,
): Promise<OcorrenciaCriada> {
  return chamarNucleo<OcorrenciaCriada>("/v1/ocorrencias-de-conduta", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}
