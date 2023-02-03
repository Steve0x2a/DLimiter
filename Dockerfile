# 基于镜像基础
FROM python:3.10
# 维护者信息
MAINTAINER name 0x2a
# 复制当前代码文件到容器中 /app
ADD . /app
# 设置app文件夹是工作目录 /app
WORKDIR /app
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# Run server.py when the container launches
CMD ["hypercorn", "main:app"]