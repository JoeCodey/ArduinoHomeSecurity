# This Dockerfiles is ONLY used when NOT using nginx proxy server 

FROM node:latest 

# Create app directory 
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app 

COPY package.json /usr/src/app/
RUN npm install 

CMD ["npm","run","start"]


