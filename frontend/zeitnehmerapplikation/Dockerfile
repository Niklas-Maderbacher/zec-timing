# ---------- Base ----------
FROM node:20-alpine AS base
WORKDIR /app

# ---------- Dependencies ----------
FROM base AS deps

COPY package.json package-lock.json* ./
RUN npm install

# ---------- Builder ----------
FROM base AS builder

# Copy deps
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build-time envs (must match Next public vars)
ARG NEXT_PUBLIC_DESKTOP_APP_API_URL
ARG NEXT_PUBLIC_MQTT_WORKER_API_URL
ARG NEXT_PUBLIC_API_KEY

ENV NEXT_PUBLIC_DESKTOP_APP_API_URL=$NEXT_PUBLIC_DESKTOP_APP_API_URL
ENV NEXT_PUBLIC_MQTT_WORKER_API_URL=$NEXT_PUBLIC_MQTT_WORKER_API_URL
ENV NEXT_PUBLIC_API_KEY=$NEXT_PUBLIC_API_KEY

# Disable Next telemetry
ENV NEXT_TELEMETRY_DISABLED=1

# Build Next.js
RUN npm run build

# ---------- Runner ----------
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Security user
RUN addgroup --system --gid 1001 nodejs \
    && adduser  --system --uid 1001 nextjs

# Copy standalone output
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Runtime envs (same names!)
ENV NEXT_PUBLIC_DESKTOP_APP_API_URL=$NEXT_PUBLIC_DESKTOP_APP_API_URL
ENV NEXT_PUBLIC_MQTT_WORKER_API_URL=$NEXT_PUBLIC_MQTT_WORKER_API_URL
ENV NEXT_PUBLIC_API_KEY=$NEXT_PUBLIC_API_KEY

RUN chown -R nextjs:nodejs /app
USER nextjs

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

CMD ["node", "server.js"]
