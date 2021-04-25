FROM groovy

USER root

WORKDIR /usr/app

COPY . .

RUN rm -rf /usr/app/neovim/env
