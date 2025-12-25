# Multi-stage build for Master Toolbox v2.0
FROM python:3.11-slim as python-base
FROM node:20-alpine as node-base

FROM python-base as builder
WORKDIR /app
COPY master-toolbox/requirements.txt* ./
RUN pip install --no-cache-dir -r requirements.txt

FROM node-base as node-builder  
WORKDIR /app/mcp-integration
COPY mcp-integration/package.json* ./
RUN npm ci --only=production

FROM python-base as runtime
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=node-builder /app/mcp-integration/node_modules ./mcp-integration/node_modules
COPY master-toolbox/ ./master-toolbox/
COPY skills/ ./skills/
EXPOSE 3000 8080
CMD ["./master-toolbox/scripts/start.sh"]
