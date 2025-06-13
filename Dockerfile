FROM python:3.13.4-alpine3.22 AS builder

ENV UV_SYSTEM_PYTHON 1
WORKDIR /app

RUN apk add --no-cache bash gcc musl-dev

COPY --from=ghcr.io/astral-sh/uv:0.7.12 /uv /uvx /bin/
COPY requirements.txt /app/requirements.txt
RUN uv pip install -r requirements.txt

COPY src/ /app/src/

RUN pyinstaller src/main.py --onefile --name "fromcord"

FROM alpine:3.22 AS runner

WORKDIR /app

COPY --from=builder /app/dist/fromcord /app/fromcord
COPY version.txt /app/version.txt
RUN chmod +x /app/fromcord

CMD ["./fromcord"]
