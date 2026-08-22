import { chamarNucleo } from "../api/cliente";

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
