FROM oven/bun:latest

WORKDIR /zeitnehmerapplikation/

COPY zeitnehmerapplikation/package.json zeitnehmerapplikation/bun.lock ./

COPY zeitnehmerapplikation/* ./

RUN bun install

ARG VITE_API_URL=${VITE_API_URL}

CMD [ "bun", "run", "dev" ]