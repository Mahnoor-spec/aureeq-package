# Use Node.js base image for building
FROM node:20-slim AS build

# Set working directory
WORKDIR /app

# Copy package files
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY frontend/ .

# Build the project
RUN npm run build

# Use Nginx for serving the build
FROM nginx:stable-alpine

# Copy the custom nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy build files from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose the port Nginx is listening on
EXPOSE 5173

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
