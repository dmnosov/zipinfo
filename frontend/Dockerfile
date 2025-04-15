# Этап 1: Установка зависимостей и сборка
FROM node:20-alpine AS builder

WORKDIR /app

# Установка зависимостей
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN \
    if [ -f pnpm-lock.yaml ]; then npm install -g pnpm && pnpm install; \
    elif [ -f yarn.lock ]; then npm install -g yarn && yarn install; \
    else npm install; \
    fi

# Копируем все остальные файлы
COPY . .

# Сборка приложения
RUN npm run build

# Этап 2: Запуск с минимальным образом
FROM node:20-alpine AS runner

WORKDIR /app

# Копируем собранное приложение
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/next.config.ts ./next.config.ts

# Указываем порт
EXPOSE 3000

# Запуск приложения
CMD ["npm", "start"]
