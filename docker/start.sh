#!/bin/sh

cd ${WORKDIR}
if [ ! -s /tmp/requirements.txt.sha256sum ]; then
     sha256sum requirements.txt > /tmp/requirements.txt.sha256sum
fi
    echo "更新程序..."
    git remote set-url origin "${REPO_URL}" &> /dev/null
    find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
    git fetch --depth 1 origin ${BRANCH}
    git reset --hard origin/${BRANCH}
    if [ $? -eq 0 ]; then
        echo "更新成功..."
        # Python依赖包更新
        hash_old=$(cat /tmp/requirements.txt.sha256sum)
        hash_new=$(sha256sum requirements.txt)
        if [ "${hash_old}" != "${hash_new}" ]; then
            echo "检测到requirements.txt有变化，重新安装依赖..."
            if [ "${CN_UPDATE}" = "true" ]; then
                pip install --upgrade pip wheel -i https://pypi.tuna.tsinghua.edu.cn/simple
                pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
            else
                pip install --upgrade pip wheel
                pip install -r requirements.txt
            fi
            if [ $? -ne 0 ]; then
                echo "无法安装依赖，请更新镜像..."
            else
                echo "依赖安装成功..."
                sha256sum requirements.txt > /tmp/requirements.txt.sha256sum
            fi
        fi
    else
        echo "更新失败，继续使用旧的程序来启动..."
    fi
hypercorn -b 0.0.0.0:8088 main:app