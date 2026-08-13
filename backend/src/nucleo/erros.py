from pydantic import BaseModel


class CorpoDeErro(BaseModel):
    codigo: str
    mensagem: str
    campo: str | None = None


class ErroDeAplicacao(Exception):
    """Erro que os manipuladores convertem no corpo único de `CorpoDeErro`."""

    status_code: int
    codigo: str
    mensagem: str

    def __init__(self, mensagem: str | None = None, *, campo: str | None = None) -> None:
        self.mensagem = mensagem or self.mensagem
        self.campo = campo
        super().__init__(self.mensagem)


class ChaveInvalida(ErroDeAplicacao):
    status_code = 401
    codigo = "chave_invalida"
    mensagem = "Chave de aplicação ausente, inválida ou revogada."


class SessaoAusente(ErroDeAplicacao):
    status_code = 401
    codigo = "sessao_ausente"
    mensagem = "Esta rota exige uma sessão de persona autenticada."


class SessaoInvalida(ErroDeAplicacao):
    status_code = 401
    codigo = "sessao_invalida"
    mensagem = "Sessão inexistente, encerrada ou expirada."


class TrocaDeSenhaPendente(ErroDeAplicacao):
    status_code = 403
    codigo = "troca_de_senha_pendente"
    mensagem = "Troque a senha provisória antes de continuar."


class PermissaoNegada(ErroDeAplicacao):
    status_code = 403
    codigo = "permissao_negada"
    mensagem = "O papel desta persona não autoriza esta operação."


class LoginSemCadastro(ErroDeAplicacao):
    status_code = 403
    codigo = "login_sem_cadastro"
    mensagem = (
        "Esta conta não corresponde a nenhum cadastro. Quem quer ser Mestre ou "
        "Apoiador pode solicitar participação pelo formulário da vitrine."
    )


class CredencialInvalida(ErroDeAplicacao):
    status_code = 401
    codigo = "credencial_invalida"
    mensagem = "Usuário ou senha inválidos."


class ServicoIndisponivel(ErroDeAplicacao):
    status_code = 503
    codigo = "servico_indisponivel"
    mensagem = "Serviço de verificação de identidade indisponível. Tente novamente em instantes."


class NaoEncontrado(ErroDeAplicacao):
    status_code = 404
    codigo = "nao_encontrado"
    mensagem = "Recurso não encontrado."


class ParametroInvalido(ErroDeAplicacao):
    status_code = 422
    codigo = "parametro_invalido"
    mensagem = "Parâmetro inválido."


class ParametroDesconhecido(ErroDeAplicacao):
    status_code = 422
    codigo = "parametro_desconhecido"
    mensagem = "Parâmetro não reconhecido por esta rota."


class TamanhoDePaginaAcimaDoTeto(ErroDeAplicacao):
    status_code = 422
    codigo = "tamanho_de_pagina_acima_do_teto"
    mensagem = "Tamanho de página acima do teto permitido."


class ErroDeValidacao(ErroDeAplicacao):
    status_code = 422
    codigo = "erro_de_validacao"
    mensagem = "Campo inválido ou em falta."


class ErroInterno(ErroDeAplicacao):
    status_code = 500
    codigo = "erro_interno"
    mensagem = "Ocorreu um erro inesperado. Tente novamente em instantes."


class ConsentimentoImutavel(ErroDeAplicacao):
    status_code = 409
    codigo = "consentimento_imutavel"
    mensagem = "Consentimento é somente inserção; revogar grava um registro novo."


class AcessoAoTemplateImutavel(ErroDeAplicacao):
    status_code = 409
    codigo = "acesso_ao_template_imutavel"
    mensagem = "Registro de acesso ao template biométrico é somente inserção."


class AuditoriaImutavel(ErroDeAplicacao):
    status_code = 409
    codigo = "auditoria_imutavel"
    mensagem = "Registro de auditoria é somente inserção."


class DebitoDePontoRegularRecusado(ErroDeAplicacao):
    status_code = 409
    codigo = "debito_de_ponto_regular_recusado"
    mensagem = "Ponto regular nunca é debitado, em nenhuma operação."


class DebitoDePontoExtraRecusado(ErroDeAplicacao):
    status_code = 409
    codigo = "debito_de_ponto_extra_recusado"
    mensagem = "O acumulado de ponto extra só cresce, em nenhuma operação decresce."


class AutenticacaoBiometricaInvalida(ErroDeAplicacao):
    status_code = 401
    codigo = "autenticacao_biometrica_invalida"
    mensagem = "Nick ou imagem não reconhecidos. Peça a um Mestre para confirmar sua entrada."


class CotaDeLeituraExcedida(ErroDeAplicacao):
    status_code = 429
    codigo = "cota_de_leitura_excedida"
    mensagem = "Cota de leitura desta chave excedida. Tente novamente mais tarde."


class DocumentoPessoalRecusado(ErroDeAplicacao):
    status_code = 422
    codigo = "documento_pessoal_recusado"
    mensagem = "A plataforma não coleta CPF, CNPJ nem documento de identidade."


class ConjuntoDeDadosNaoLiberado(ErroDeAplicacao):
    status_code = 409
    codigo = "conjunto_de_dados_nao_liberado"
    mensagem = "O conjunto de dados só é liberado depois da aprovação de um Admin."


class SolicitacaoDeChaveNaoDisponivelParaEmissao(ErroDeAplicacao):
    status_code = 409
    codigo = "solicitacao_de_chave_nao_disponivel_para_emissao"
    mensagem = "A chave só pode ser emitida sobre solicitação aprovada e sem chave emitida."


class PrazoDeApresentacaoVencido(ErroDeAplicacao):
    status_code = 422
    codigo = "prazo_de_apresentacao_vencido"
    mensagem = "O prazo para apresentar a URL venceu. Solicite uma nova chave."


class UrlJaApresentada(ErroDeAplicacao):
    status_code = 409
    codigo = "url_ja_apresentada"
    mensagem = "Esta chave já tem uma URL apresentada."


class FreioPorOrigemAcionado(ErroDeAplicacao):
    """`RF-01-65`: leva o tempo de espera calculado pelo freio, que o
    manipulador de `principal.py` também expõe no cabeçalho `Retry-After`
    (design — Decisions)."""

    status_code = 429
    codigo = "freio_por_origem_acionado"
    mensagem = "Muitas tentativas em pouco tempo. Tente novamente mais tarde."

    def __init__(self, mensagem: str | None = None, *, tempo_de_espera_em_segundos: int) -> None:
        super().__init__(mensagem)
        self.tempo_de_espera_em_segundos = tempo_de_espera_em_segundos
