# Step 1: Build the React Application
FROM node:18-slim as build

WORKDIR /workspace

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Step 2: Serve the application with Nginx
FROM nginx:alpine

COPY --from=build /workspace/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
