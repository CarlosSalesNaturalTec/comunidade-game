from pydantic import BaseModel


class CorpoDeErro(BaseModel):
    codigo: str
    mensagem: str
    campo: str | None = None
    sugestoes: list[str] | None = None


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


class NickDeGuerreiroEmUsoNoEncontro(ErroDeValidacao):
    """Mesma recusa 422 no campo `nick` de `ErroDeValidacao`, com as
    variações de alcance total que só o caminho do encontro devolve — o
    caminho da gestão segue recusando sem elas (`RF-04-08`, design —
    decisão 4)."""

    def __init__(self, sugestoes: list[str]) -> None:
        super().__init__(mensagem="Este nick já está em uso.", campo="nick")
        self.sugestoes = sugestoes


class ErroInterno(ErroDeAplicacao):
    status_code = 500
    codigo = "erro_interno"
    mensagem = "Ocorreu um erro inesperado. Tente novamente em instantes."


class ConsentimentoImutavel(ErroDeAplicacao):
    status_code = 409
    codigo = "consentimento_imutavel"
    mensagem = "Consentimento é somente inserção; revogar grava um registro novo."


class LancamentoImutavel(ErroDeAplicacao):
    status_code = 409
    codigo = "lancamento_imutavel"
    mensagem = "Lançamento é somente inserção; a correção se faz por lançamento de ajuste."


class OcorrenciaDeCondutaImutavel(ErroDeAplicacao):
    status_code = 409
    codigo = "ocorrencia_de_conduta_imutavel"
    mensagem = "Ocorrência de conduta é somente inserção; a correção se faz por ocorrência nova."


class AcessoAoTemplateImutavel(ErroDeAplicacao):
    status_code = 409
    codigo = "acesso_ao_template_imutavel"
    mensagem = "Registro de acesso ao template biométrico é somente inserção."


class AuditoriaImutavel(ErroDeAplicacao):
    status_code = 409
    codigo = "auditoria_imutavel"
    mensagem = "Registro de auditoria é somente inserção."


class FichaDeVidaImutavel(ErroDeAplicacao):
    status_code = 409
    codigo = "ficha_de_vida_imutavel"
    mensagem = "Anotação da ficha de vida é somente inserção."


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


class ConfirmacaoDeGuerreiroRecusada(ErroDeAplicacao):
    """Indistinguível entre nick inexistente e nick que não é de
    Guerreiro(a) — não é uma variação de `AutenticacaoBiometricaInvalida`,
    porque aqui quem já está confirmando é o próprio Mestre ou Admin
    (`RN-01-22`)."""

    status_code = 401
    codigo = "confirmacao_de_guerreiro_recusada"
    mensagem = "Não foi possível confirmar esse nick. Confira com o Guerreiro(a) e tente de novo."


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


class SolicitacaoJaAvaliada(ErroDeAplicacao):
    status_code = 409
    codigo = "solicitacao_ja_avaliada"
    mensagem = "Esta solicitação já tem um desfecho gravado."


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


class PapelDoPoderTerritorioJaDeclarado(ErroDeAplicacao):
    status_code = 409
    codigo = "papel_do_poder_territorio_ja_declarado"
    mensagem = "Já existe um poder com o papel do Território declarado no catálogo."


class PoderDoTerritorioNaoDeclarado(ErroDeAplicacao):
    status_code = 409
    codigo = "poder_do_territorio_nao_declarado"
    mensagem = (
        "O catálogo de poderes ainda não declara o Poder do Território. "
        "Peça a um Admin para marcar o papel no poder correspondente."
    )


class SerieDeColetaJaAberta(ErroDeAplicacao):
    status_code = 409
    codigo = "serie_de_coleta_ja_aberta"
    mensagem = "Este Guerreiro(a) já tem uma série aberta para este desafio e local."


class ConfirmacaoDeRegistroInvalidadoRecusada(ErroDeAplicacao):
    status_code = 409
    codigo = "confirmacao_de_registro_invalidado_recusada"
    mensagem = "Registro invalidado não pode ser confirmado: a invalidação é terminal."


class CredencialDeDispositivoInvalida(ErroDeAplicacao):
    status_code = 401
    codigo = "credencial_de_dispositivo_invalida"
    mensagem = "Credencial de dispositivo ausente, inválida ou revogada."


class CredencialDeDispositivoJaAtiva(ErroDeAplicacao):
    status_code = 409
    codigo = "credencial_de_dispositivo_ja_ativa"
    mensagem = "Esta série já tem uma credencial de dispositivo ativa."


class DigitalizacaoDoTermoJaAnexada(ErroDeAplicacao):
    status_code = 409
    codigo = "digitalizacao_do_termo_ja_anexada"
    mensagem = "Este consentimento já tem uma digitalização anexada."


class PresencaJaAnulada(ErroDeAplicacao):
    status_code = 409
    codigo = "presenca_ja_anulada"
    mensagem = "Esta presença já foi anulada."


class TrilhaSemCulminanciaDeclarada(ErroDeAplicacao):
    status_code = 409
    codigo = "trilha_sem_culminancia_declarada"
    mensagem = "Esta trilha ainda não declarou o que a criação original precisa ser."


class CriacaoOriginalJaValidada(ErroDeAplicacao):
    status_code = 409
    codigo = "criacao_original_ja_validada"
    mensagem = "Esta criação original já foi validada; não é possível entregar de novo."


class ArquivoAcimaDoTeto(ErroDeAplicacao):
    status_code = 413
    codigo = "arquivo_acima_do_teto"
    mensagem = "Arquivo acima do limite de tamanho para este tipo de conteúdo."


class SolicitacaoDoResponsavelDuplicada(ErroDeAplicacao):
    status_code = 409
    codigo = "solicitacao_do_responsavel_duplicada"
    mensagem = "Já existe uma solicitação deste tipo em aberto para este Guerreiro(a)."


class AutorizacaoSuspensaPorOutroResponsavel(ErroDeAplicacao):
    status_code = 409
    codigo = "autorizacao_suspensa_por_outro_responsavel"
    mensagem = (
        "A autorização deste Guerreiro(a) está suspensa: outro responsável recusou, e a "
        "recusa prevalece. Procure a gestão no encontro."
    )


class RevogacaoSemAutorizacaoVigente(ErroDeAplicacao):
    status_code = 409
    codigo = "revogacao_sem_autorizacao_vigente"
    mensagem = "Não há autorização vigente para revogar sobre este Guerreiro(a)."


class FimDeVinculoImutavel(ErroDeAplicacao):
    status_code = 409
    codigo = "fim_de_vinculo_imutavel"
    mensagem = "Fim de vínculo é somente inserção: UPDATE e DELETE não são permitidos."


class VinculoDoGuerreiroJaEncerrado(ErroDeAplicacao):
    status_code = 409
    codigo = "vinculo_do_guerreiro_ja_encerrado"
    mensagem = "O vínculo deste Guerreiro(a) com o projeto já está encerrado."


class EdicaoDeDesafioExtraPublicadoRecusada(ErroDeAplicacao):
    status_code = 405
    codigo = "edicao_de_desafio_extra_publicado_recusada"
    mensagem = "Desafio extra publicado não é editável; a correção é uma proposta nova."


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
