# Use the official Node.js image as the base image
FROM node:16 AS build-stage

# Set the working directory in the Docker container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies in the container
RUN npm install

# Copy the rest of the files to the container
COPY . .

# Build the Vue.js app
RUN npm run build

# Start with a base image containing Nginx
FROM nginx:stable-alpine AS production-stage

# Copy the compiled app to the Nginx container
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
