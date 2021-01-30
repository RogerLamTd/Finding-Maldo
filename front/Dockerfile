FROM node:14.15-alpine3.12

WORKDIR /app
COPY --chown=node package*.json ./
RUN chown node /app && \
    npm install 
COPY --chown=node src src
COPY --chown=node public public
USER node
EXPOSE 3000

CMD npm start
