FROM ubuntu:latest

ADD crontab /etc/cron.d/hello
ADD tmp.sh /root/tmp.sh
ADD main.py /root/main.py

RUN chmod 0644 /etc/cron.d/hello
RUN chmod 0744 /root/tmp.sh
RUN chmod 0777 /root/main.py

RUN touch /var/log/cron.log

RUN apt update
RUN apt install cron -y
RUN apt install python3-pip -y
RUN pip3 install requests
RUN pip3 install beautifulsoup4
RUN pip3 install mysql-connector

CMD cron && tail -f /var/log/cron.log

