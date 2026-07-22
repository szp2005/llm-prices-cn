# Self-hostable MCP server for the LLM Abacus price dataset.
# Builds a stdio MCP server that Glama (and any MCP client) can start and introspect.
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py prices.json ./

# MCP servers speak over stdio; the container just runs the server.
CMD ["python", "server.py"]
