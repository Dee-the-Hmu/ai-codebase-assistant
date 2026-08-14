# start from an image that already has Node installed (React/Vite needs Node)
FROM node:22

# working dir inside the container for frontend
WORKDIR /app

# copy all package*.json files from current folder to the curr dir /app inside the image
COPY package*.json .

#Install the frontend dependencies inside the iamge
RUN npm install

# copy the rest of the frontend src code into the image
COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
# host0.0.0.0 = makes Vite listen for traffic coming into the container
