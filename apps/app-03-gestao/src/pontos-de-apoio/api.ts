import { chamarNucleo } from "comum/api";

export interface PontoDeApoioDaLista {
  id: string;
  nome: string;
  comunidade_virtual_id: string;
  responsavel_id: string | null;
  ativo: boolean;
}

interface ListaDePontosDeApoio {
  itens: PontoDeApoioDaLista[];
  proximo_cursor: string | null;
}

// Admin declara a comunidade, sempre; o Mestre a tem derivada do próprio
// vínculo no núcleo, e por isso não a envia (`RF-07-47`, `RF-01-18`).
export function listarPontosDeApoio(
  token: string,
  comunidadeId?: string,
): Promise<ListaDePontosDeApoio> {
  const consulta = comunidadeId ? `?comunidade=${encodeURIComponent(comunidadeId)}` : "";
  return chamarNucleo<ListaDePontosDeApoio>(`/v1/pontos-de-apoio${consulta}`, { token });
}

export interface CadastrarPontoDeApoioEntrada {
  nome: string;
  comunidade_id: string;
}

interface PontoDeApoioCriado {
  id: string;
  nome: string;
  comunidade_virtual_id: string;
  responsavel_id: string | null;
  ativo: boolean;
}

export function cadastrarPontoDeApoio(
  entrada: CadastrarPontoDeApoioEntrada,
  token: string,
): Promise<PontoDeApoioCriado> {
  return chamarNucleo<PontoDeApoioCriado>("/v1/pontos-de-apoio", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// Rota própria, de Admin, sempre com motivo — distinta do `PUT` de cadastro
// para que a mudança de estado fique legível na trilha de auditoria
// (`RF-07-47`, `RN-07-33`).
export function desativarPontoDeApoio(
  idDoPontoDeApoio: string,
  motivo: string,
  token: string,
): Promise<PontoDeApoioCriado> {
  return chamarNucleo<PontoDeApoioCriado>(
    `/v1/pontos-de-apoio/${idDoPontoDeApoio}/desativacao`,
    { metodo: "POST", corpo: { motivo }, token },
  );
}

export function reativarPontoDeApoio(
  idDoPontoDeApoio: string,
  motivo: string,
  token: string,
): Promise<PontoDeApoioCriado> {
  return chamarNucleo<PontoDeApoioCriado>(
    `/v1/pontos-de-apoio/${idDoPontoDeApoio}/reativacao`,
    { metodo: "POST", corpo: { motivo }, token },
  );
}

// Só o Admin designa ou troca o responsável pelo acervo, entre Mestres e
// Apoiadores cadastrados; a troca substitui o designado anterior
// (`RF-02-52`, `RF-07-49`, `RN-07-34`).
export function designarResponsavel(
  idDoPontoDeApoio: string,
  responsavelId: string,
  token: string,
): Promise<PontoDeApoioCriado> {
  return chamarNucleo<PontoDeApoioCriado>(
    `/v1/pontos-de-apoio/${idDoPontoDeApoio}/responsavel`,
    { metodo: "PUT", corpo: { responsavel_id: responsavelId }, token },
  );
}

export interface SaldoDoTipoDeRecurso {
  tipo_de_recurso_id: string;
  nome: string;
  saldo: string;
}

// Só o disponível na origem — a mesma apuração que `livro-razao` já expõe
// por par tipo de recurso e ponto de apoio (`RF-07-19`, design — Decisions).
export function listarSaldosDoPontoDeApoio(
  idDoPontoDeApoio: string,
  token: string,
): Promise<SaldoDoTipoDeRecurso[]> {
  return chamarNucleo<SaldoDoTipoDeRecurso[]>(
    `/v1/pontos-de-apoio/${idDoPontoDeApoio}/saldos`,
    { token },
  );
}

export interface TransferirSaldoEntrada {
  tipo_de_recurso_id: string;
  ponto_de_apoio_origem_id: string;
  ponto_de_apoio_destino_id: string;
  quantidade: string;
  motivo: string;
}

interface LancamentoDaTransferencia {
  id: string;
  ponto_de_apoio_id: string;
  quantidade: string;
}

interface TransferenciaCriada {
  debito: LancamentoDaTransferencia;
  credito: LancamentoDaTransferencia;
}

export function transferirSaldo(
  entrada: TransferirSaldoEntrada,
  token: string,
): Promise<TransferenciaCriada> {
  return chamarNucleo<TransferenciaCriada>("/v1/lancamentos/transferencia", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface LancamentoDoExtrato {
  id: string;
  natureza: string;
  tipo_de_recurso_id: string;
  ponto_de_apoio_id: string;
  quantidade: string;
  valor_em_moedas: string;
  lancamento_original_id: string | null;
  motivo_do_ajuste: string | null;
  lancamento_relacionado_id: string | null;
}

interface PaginaDeLancamentos {
  itens: LancamentoDoExtrato[];
  proximo_cursor: string | null;
}

export interface FiltroDoExtrato {
  periodoInicio?: string;
  periodoFim?: string;
  tipoDeRecursoId?: string;
  cursor?: string;
}

// O extrato de um ponto de apoio, com o filtro obrigatório que evita
// misturar o livro-razão de espaços diferentes — é por ele que o ajuste
// alcança o lançamento a corrigir (`RF-02-40`, `RF-01-18`, `RF-01-28`).
export function listarLancamentos(
  idDoPontoDeApoio: string,
  token: string,
  filtro: FiltroDoExtrato = {},
): Promise<PaginaDeLancamentos> {
  const parametros = new URLSearchParams({ ponto_de_apoio: idDoPontoDeApoio });
  if (filtro.periodoInicio) parametros.set("periodo_inicio", filtro.periodoInicio);
  if (filtro.periodoFim) parametros.set("periodo_fim", filtro.periodoFim);
  if (filtro.tipoDeRecursoId) parametros.set("tipo_de_recurso", filtro.tipoDeRecursoId);
  if (filtro.cursor) parametros.set("cursor", filtro.cursor);
  return chamarNucleo<PaginaDeLancamentos>(`/v1/lancamentos?${parametros.toString()}`, {
    token,
  });
}

export interface LancarAjusteEntrada {
  quantidade: string;
  valor_em_moedas: string;
  motivo: string;
}

// A correção se faz por lançamento novo, que referencia o original sem
// alterá-lo — não há caminho de edição nem de remoção (`RF-02-40`,
// `RN-02-12`).
export function lancarAjuste(
  idDoLancamento: string,
  entrada: LancarAjusteEntrada,
  token: string,
): Promise<LancamentoDoExtrato> {
  return chamarNucleo<LancamentoDoExtrato>(`/v1/lancamentos/${idDoLancamento}/ajuste`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}
