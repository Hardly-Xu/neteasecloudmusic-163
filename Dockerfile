FROM python:3.6

WORKDIR /spider
COPY . ./
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt


CMD ["bash"]  
