FROM python:3.12 as python-base

ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

ENV POETRY_CACHE_DIR=/opt/.cache

FROM python-base as poetry-base

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM python-base as backend-app

COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry check

RUN poetry install --no-interaction --no-cache

COPY . /app

EXPOSE 8000
CMD [ "poetry", "run", "python", "-m", "main" ]