FROM ubuntu

MAINTAINER Saurabh Gupta

ARG DEBIAN_FRONTEND=noninteractive

ENV FOLDER_PROJECT /usr/src/bluevoyant_challenge_saurabh

RUN mkdir -p $FOLDER_PROJECT

COPY docker_run_mysql.sh $FOLDER_PROJECT
COPY start.sql $FOLDER_PROJECT
COPY /app $FOLDER_PROJECT
COPY requirements.txt /tmp/

RUN apt update && apt install -y python3 python3-pip mysql-server net-tools vim mc wget curl less && apt-get clean

RUN pip3 install -r /tmp/requirements.txt

EXPOSE 3306

RUN chmod +x /usr/src

RUN echo 'alias jump="cd /usr/src/bluevoyant_challenge_saurabh"' >> ~/.bashrc

CMD ["/usr/src/bluevoyant_challenge_saurabh/docker_run_mysql.sh"]
