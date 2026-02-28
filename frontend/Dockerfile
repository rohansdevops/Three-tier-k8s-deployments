FROM node:20-alpine AS builder
WORKDIR /app

ENV NEXT_PUBLIC_API_URL=k8s-myauthapp-8ec284185f-139836622.eu-north-1.elb.amazonaws.com

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm", "start"]