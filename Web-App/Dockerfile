# Stage 1: install dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# copy package.json/lock first for caching
COPY package.json package-lock.json* ./
RUN npm ci --silent

# Stage 2: build the application
FROM node:20-alpine AS builder
WORKDIR /app

COPY . .
COPY --from=deps /app/node_modules ./node_modules

RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm","start"]
