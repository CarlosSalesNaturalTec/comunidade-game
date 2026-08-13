import logging

logger = logging.getLogger("nucleo.protecao")


def registrar_premissa_de_conteiner_unico() -> None:
    """A cota e o freio contam só em memória: mais de um contêiner ao mesmo
    tempo multiplica os limites (documento 03 §1, princípio 13). Esta linha
    é o que faz a violação aparecer no log de produção em vez de passar
    despercebida (design — Risks).
    """
    logger.warning(
        "Proteção das rotas públicas pressupõe um único contêiner (Cloud Run "
        "sem escala horizontal, documento 03 §1, princípio 13) — a cota e o "
        "freio contam em memória, e mais de um contêiner simultâneo "
        "multiplica os limites."
    )
