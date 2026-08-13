from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from nucleo.apoio_escolar import modelo as modelo_apoio_escolar  # noqa: F401
from nucleo.auditoria import modelo as modelo_auditoria  # noqa: F401
from nucleo.aulas import modelo as modelo_aulas  # noqa: F401
from nucleo.banco import Base
from nucleo.biometria import modelo as modelo_biometria  # noqa: F401
from nucleo.chaves import modelo  # noqa: F401 — registra as tabelas em Base.metadata
from nucleo.configuracao import obter_configuracao
from nucleo.consentimentos import modelo as modelo_consentimentos  # noqa: F401
from nucleo.criacoes_originais import modelo as modelo_criacoes_originais  # noqa: F401
from nucleo.equipes import modelo as modelo_equipes  # noqa: F401
from nucleo.fila import modelo as modelo_fila  # noqa: F401
from nucleo.ods import modelo as modelo_ods  # noqa: F401
from nucleo.personas import modelo as modelo_personas  # noqa: F401
from nucleo.poderes import modelo as modelo_poderes  # noqa: F401
from nucleo.ponto_extra import modelo as modelo_ponto_extra  # noqa: F401
from nucleo.pontuacao import modelo as modelo_pontuacao  # noqa: F401
from nucleo.quiz import modelo as modelo_quiz  # noqa: F401
from nucleo.responsaveis import modelo as modelo_responsaveis  # noqa: F401
from nucleo.resultados import modelo as modelo_resultados  # noqa: F401
from nucleo.sessoes import modelo as modelo_sessoes  # noqa: F401
from nucleo.trilhas import modelo as modelo_trilhas  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", obter_configuracao().dsn_banco)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
