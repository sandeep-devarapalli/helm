FROM python:3.11-slim

ARG VIBE_TRADING_VERSION=0.1.11
ENV PIP_DEFAULT_TIMEOUT=120 \
    PIP_RETRIES=10
RUN useradd --create-home --uid 10001 vibe \
    && pip install --no-cache-dir "vibe-trading-ai==${VIBE_TRADING_VERSION}"

ENV FASTMCP_HOST=0.0.0.0 \
    FASTMCP_CHECK_FOR_UPDATES=off \
    HOME=/home/vibe
WORKDIR /home/vibe
COPY infra/vibe-entrypoint.sh /usr/local/bin/vibe-entrypoint
EXPOSE 8900

ENTRYPOINT ["vibe-entrypoint"]
CMD ["vibe-trading-mcp", "--transport", "sse", "--port", "8900"]
