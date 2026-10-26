FROM node:24-bookworm-slim AS node-runtime

FROM node-runtime AS frontend-build
WORKDIR /web
COPY frontend/package*.json ./
RUN npm ci --ignore-scripts --no-audit --no-fund
COPY frontend ./
ENV VITE_API_URL=/
RUN npm run build

FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends libstdc++6 ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=node-runtime /usr/local/bin/node /usr/local/bin/node
COPY --from=node-runtime /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm

WORKDIR /app
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt
COPY backend/template-runtime/package*.json /app/backend/template-runtime/
RUN cd /app/backend/template-runtime && npm ci --ignore-scripts --no-audit --no-fund
COPY backend /app/backend
COPY examples /app/examples
COPY LICENSE /app/LICENSE
COPY --from=frontend-build /web/dist /app/frontend/dist
RUN useradd --uid 10001 --create-home snap2ship && chown -R snap2ship:snap2ship /app/backend/template-runtime
USER snap2ship
ENV PYTHONUNBUFFERED=1
ENV PORT=10000
WORKDIR /app/backend
EXPOSE 10000
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}"]
