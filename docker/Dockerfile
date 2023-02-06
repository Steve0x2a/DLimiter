FROM python:3.10-alpine

ENV LANG="C.UTF-8" \
    TZ="Asia/Shanghai" \
    PS1="\u@\h:\w \$ " \
    DLIMITER_REPO_URL="https://github.com/Steve0x2a/DLimiter" \
    DLIMITER_BRANCH=main \
    WORKDIR="/app" \
    DLIMITER_CN_UPDATE=true \
    DLIMITER_AUTO_UPDATE=true \
    DLIMITER_PORT=8088

WORKDIR ${WORKDIR}

RUN apk --no-cache add -f git bash tzdata \
    && pip install --upgrade pip wheel \
    && pip install -r https://raw.githubusercontent.com/Steve0x2a/DLimiter/${DLIMITER_BRANCH}/requirements.txt \
    && rm -rf /tmp/* /root/.cache /var/cache/apk/* \
    && git config --global pull.ff only \
    && git clone -b ${DLIMITER_BRANCH} ${DLIMITER_REPO_URL} ${WORKDIR} \
    && git config --global --add safe.directory ${WORKDIR}

VOLUME ["/app/conf"]
ENTRYPOINT ["/app/docker/start.sh"]
