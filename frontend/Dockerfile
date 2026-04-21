# ---------- Stage 1: Build ----------
FROM node:22-alpine AS build

WORKDIR /frontend

# Copy dependency manifests first (for caching)
COPY package*.json ./

RUN npm ci

# Copy the rest of the source
COPY . .

# Build for production
RUN npm run build

# ---------- Stage 2: Serve ----------
FROM nginx:1.27-alpine

# Copy built files from previous stage
COPY --from=build /frontend/dist /usr/share/nginx/html

# Optional: replace default nginx.conf
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]
