FROM node:24-alpine AS base
ARG USER_NAME=app
ARG USER_HOME=/home/${USER_NAME}
ARG USER_ID=1000
ARG GROUP_NAME=app
ARG GROUP_ID=1000
ARG DIALOUT_GROUP_ID=20

RUN set -xe && apk update &&apk add --no-cache bash shadow sudo &&\
    usermod -u ${USER_ID} -l ${USER_NAME} -d /home/${USER_NAME} -m node && \
    if [ ${GROUP_ID} -eq ${DIALOUT_GROUP_ID} ]; then \
        groupdel dialout 2>/dev/null || true && \
        groupmod -g ${GROUP_ID} -n ${GROUP_NAME} node; \
    else \
        groupmod -g ${GROUP_ID} -n ${GROUP_NAME} node; \
    fi && \
    echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/${USER_NAME}
    
#ローカル開発環境
FROM base AS app
ARG PYTHON_MINIMAL="python3 python3-dev py3-pip"
ARG PIP_INSTALL_OPTIONS="--no-cache-dir --break-system-packages --pre"
ARG ADDITIONAL_PACKAGES="aws-cli"
COPY ./code/backend/requirements.txt /tmp/
RUN set -xe && apk add --no-cache ${PYTHON_MINIMAL} ${ADDITIONAL_PACKAGES} && \
    pip install ${PIP_INSTALL_OPTIONS} -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt
USER ${USER_NAME}
WORKDIR /app
COPY ./services/common/bashrc ${USER_HOME}/.bashrc
COPY ./services/app/aws/config ${USER_HOME}/.aws/config
COPY ./services/app/aws/credentials ${USER_HOME}/.aws/credentials
COPY ./code/backend/package.json .
COPY ./code/backend/serverless.yml .
RUN sudo npm install -g osls && npm install 
CMD ["bash"]

