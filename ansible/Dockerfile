FROM python:3.12-slim
RUN apt update && apt install -y openssh-client vim
RUN pip install --no-cache-dir ansible passlib==1.7.4
WORKDIR /ansible
