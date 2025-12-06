FROM oven/bun:latest

WORKDIR /zeitnehmerapplikation

COPY package.json bun.lock ./

RUN bun install

COPY . .

ARG VITE_API_URL=${VITE_API_URL}

CMD [ "bun", "run", "start" ]