import { chamarNucleo } from "comum/api";

// O que é só desta aplicação: progresso, entrega individual da produção e
// retomadas. O que as duas aplicações do percurso usam foi promovido a
// `comum/trilha/api`, e é de lá que cada tela o importa (design — decisão 2).

export interface ProgressoDaTrilha {
  trilha_id: string;
  trilha_nome: string;
  nivel_atual: number | null;
  obrigatorias_desbloqueadas: number;
  obrigatorias_totais: number;
  pontos_regulares: number;
  badges: string[];
}

// Nível e quanto falta para o próximo, pontos e badges, por trilha
// inscrita — nível é percurso, nunca saldo de pontos (`RF-05-15`,
// `RF-05-16`, `RN-05-03`, `RN-05-04`).
export function obterProgresso(token: string): Promise<ProgressoDaTrilha[]> {
  return chamarNucleo<ProgressoDaTrilha[]>("/v1/eu/progresso", { token });
}

export type FormaDeEntregaDaProducao = "texto" | "audio" | "foto";

export interface ProducaoDaMissao {
  id: string;
  equipe_id: string | null;
  guerreiro_id: string | null;
  missao_id: string;
  atividade_id: string;
  forma: FormaDeEntregaDaProducao;
  transcricao: string;
  devolutiva: string | null;
  registrado_em: string;
}

interface EntregarProducaoIndividualEntrada {
  atividadeId: string;
  forma: FormaDeEntregaDaProducao;
  texto?: string;
  arquivo?: Blob;
}

// `RF-05-74` a `RF-05-77`: a entrega individual, sobre uma missão do
// próprio percurso — a mesma superfície `multipart/form-data` da porta de
// equipe do App 01, que a foto mantém. A devolutiva volta construtiva e
// nunca credita ponto; a foto não fica no aparelho depois do envio, e a
// fala vai transcrita em `texto` — o áudio não é enviado (`RF-05-76`,
// `RN-05-32`).
export function entregarProducaoIndividual(
  missaoId: string,
  entrada: EntregarProducaoIndividualEntrada,
  token: string,
): Promise<ProducaoDaMissao> {
  const formulario = new FormData();
  formulario.set("forma", entrada.forma);
  formulario.set("atividade_id", entrada.atividadeId);
  if (entrada.texto !== undefined) formulario.set("texto", entrada.texto);
  if (entrada.arquivo !== undefined) formulario.set("arquivo", entrada.arquivo);

  return chamarNucleo<ProducaoDaMissao>(`/v1/eu/missoes/${missaoId}/producao`, {
    metodo: "POST",
    formulario,
    token,
  });
}

export interface RetomadaEmAberto {
  missao_id: string;
  missao_titulo: string;
  trilha_id: string;
  trilha_titulo: string;
  prazo: string;
}

// As retomadas em aberto do Guerreiro(a) em sessão — missão, trilha e
// prazo de cada agendamento vencido sem produção, sem lista vazia
// distinguir de erro (`RF-05-79`, `RF-05-80`).
export function listarMinhasRetomadas(token: string): Promise<RetomadaEmAberto[]> {
  return chamarNucleo<RetomadaEmAberto[]>("/v1/eu/retomadas", { token });
}
