FROM node:16.15.0-alpine3.15

WORKDIR /app

COPY package*.json /app/

RUN npm install

RUN npm install -g @angular/cli

COPY ./ /app/

EXPOSE 4200

CMD [ "ng", "serve", "--host", "0.0.0.0"]
