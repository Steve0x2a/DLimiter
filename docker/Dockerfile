FROM python:3.10-alpine

ENV REPO_URL="https://github.com/Steve0x2a/DLimiter" \
    BRANCH=main \
    WORKDIR="/app" \
    CN_UPDATE=true \
    AUTO_UPDATE=true 

WORKDIR ${WORKDIR}

RUN apk --no-cache add -f git \
    && pip install --upgrade pip wheel \
    && pip install -r https://raw.githubusercontent.com/Steve0x2a/DLimiter/main/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && rm -rf /tmp/* /root/.cache /var/cache/apk/* \
    && git config --global pull.ff only \
    && git clone ${REPO_URL} ${WORKDIR} \
    && git config --global --add safe.directory ${WORKDIR}

EXPOSE 8088
VOLUME ["/app/conf"]
ENTRYPOINT ["/app/docker/start.sh"]    