FROM github/super-linter:v5 AS ci-linting
ARG WKDIR=/tmp/lint
WORKDIR "${WKDIR}"
RUN mkdir -p "${WKDIR}"
COPY . "${WKDIR}"
FROM python:3.12.4-slim-bookworm AS noninteractive
ARG USERNAME
ARG USER_UID=1066
ARG USER_GID=$USER_UID
ARG WKDIR=/tcolors
ENV PATH="/venv/bin:$PATH"
WORKDIR "${WKDIR}"
RUN mkdir -p "${WKDIR}" && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        bash=5.2.15-2+b7 \
        tar=1.34+dfsg-1.2+deb12u1 \
        sudo=1.9.13p3-1+deb12u1 && \
    rm -rf /var/lib/apt/lists/./* && \
    groupadd --gid "${USER_GID}" "${USERNAME}" && \
    useradd --uid "${USER_GID}" --gid "${USER_GID}" --shell /bin/bash --create-home "${USERNAME}" && \
    echo "${USERNAME}" ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/"${USERNAME}" && \
    chmod 0440 /etc/sudoers.d/"${USERNAME}"
FROM noninteractive AS interactive
RUN mkdir -p /root/.vscode-server/extensions \
        /root/.vscode-server-insiders/extensions \
        /root/.vscode-remote/extensions \
        /root/.vscode-remote-insiders/extensions \
        /root/.vscode-server/bin \
        /root/.vscode-server-insiders/bin \
        /root/.vscode-remote/bin \
        /root/.vscode-remote-insiders/bin && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-transport-https=2.6.1 \
        bsdextrautils=2.38.1-5+deb12u1 \
        git=1:2.39.2-1.1 \
        openssh-client=1:9.2p1-2+deb12u3 \
        curl=7.88.1-10+deb12u6 \
        unzip=6.0-28 \
        software-properties-common=0.99.30-4.1~deb12u1 && \
    rm -rf /var/lib/apt/lists/./*
FROM noninteractive as transfer
COPY . ${WKDIR}
RUN chown -R "${USERNAME}" "${WKDIR}"
USER ${USERNAME}
FROM transfer AS staging
FROM transfer AS production
FROM transfer AS ci-testing
FROM noninteractive AS testing
USER ${USERNAME}
FROM interactive AS developing
COPY ./.devcontainer/install.sh /tmp/install
COPY ./scripts/.sleeping_daemon.sh /tmp/.sleeping_daemon
COPY ./.devcontainer/bash-src/ /tmp/bash-src/
USER ${USERNAME}
