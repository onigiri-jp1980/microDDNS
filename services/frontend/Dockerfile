FROM node:24-alpine AS base
ARG USER_NAME=app
ARG USER_HOME=/home/${USER_NAME}
ARG USER_ID=1000
ARG GROUP_NAME=app
ARG GROUP_ID=1000
RUN set -xe && apk update &&apk add --no-cache bash shadow sudo &&\
    usermod -u ${USER_ID} -l ${USER_NAME} -d /home/${USER_NAME} -m node && \
    groupmod -g ${GROUP_ID} -n ${GROUP_NAME} node && \
    echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/${USER_NAME}
    
#ローカル開発環境
FROM base AS frontend
WORKDIR /app
COPY ./services/common/bashrc ${USER_HOME}/.bashrc
COPY ./code/frontend/package.json .
COPY ./code/frontend/tsconfig.json .
COPY ./code/frontend/tsconfig.app.json .
COPY ./code/frontend/tsconfig.node.json .
COPY ./code/frontend/src .
RUN npm install && chown -R ${USER_ID}:${GROUP_ID} /app
USER ${USER_NAME}
ENTRYPOINT ["bash"]