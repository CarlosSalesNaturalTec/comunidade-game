FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./

RUN pip install . \
    && useradd --create-home --shell /usr/sbin/nologin nucleo \
    && chown -R nucleo:nucleo /app

USER nucleo

# O Cloud Run injeta PORT em tempo de execução (padrão 8080); 8000 é o valor de
# desenvolvimento local, onde a variável não é declarada.
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn nucleo.principal:app --host 0.0.0.0 --port ${PORT}"]
