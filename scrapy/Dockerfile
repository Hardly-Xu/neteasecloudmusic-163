FROM python:3.6

MAINTAINER  Har

# 配置默认放置 spider 的目录
RUN mkdir -p /spider
# 把Dockerfile所在目录及其子目录的文件复制到/spider目录下
COPY . /spider/
# 指定其为当前的工作目录
WORKDIR /spider

# 默认启动命令
CMD ["bash"]  
