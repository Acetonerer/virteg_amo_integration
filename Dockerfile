FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev

WORKDIR /code

COPY ./requirements.txt /code/

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r /code/requirements.txt

FROM python:3.11-slim

COPY --from=builder /opt/venv /opt/venv

WORKDIR /code

COPY . .

ENV PATH="/opt/venv/bin:$PATH"

RUN useradd -m nonrootuser
USER nonrootuser

CMD ["gunicorn", "-c", "gunicorn.conf.py", "project.wsgi:application"]
