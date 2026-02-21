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
    

FROM base AS builder
ARG SERVERLESS_PLUGINS="serverless-offline serverless-python-requirements"
ARG PYTHON_MINIMAL="python3 python3-dev py3-pip"
ARG PIP_INSTALL_OPTIONS="--no-cache-dir --break-system-packages"
COPY ./code/requirements.txt /tmp/
RUN set -xe && apk add --no-cache ${PYTHON_MINIMAL} && \
    pip install ${PIP_INSTALL_OPTIONS} -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt
USER ${USER_NAME}
WORKDIR /app
COPY ./services/app/bashrc ${USER_HOME}/.bashrc
COPY ./code/serverless.yml .
RUN sudo npm install -g osls && sls plugin install -n ${SERVERLESS_PLUGINS}
CMD ["bash"]

