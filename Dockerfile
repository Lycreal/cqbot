FROM alpine:latest

RUN apk add --no-cache tzdata python3 &&\
    pip3 install --no-cache-dir --upgrade pip wheel

ADD requirements.txt /root/

#使用apk安装某些缺少编译环境的包
RUN apk add --no-cache py3-yarl py3-multidict py3-lxml &&\
    pip3 install --no-cache-dir -r /root/requirements.txt &&\
    rm /root/requirements.txt