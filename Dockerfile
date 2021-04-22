FROM python:3
MAINTAINER Piotr Frohlich
COPY *.py /app/
COPY *.txt /app/
WORKDIR /app
ENV token="Secret_token_value"
RUN pip install -r ./requirements.txt
CMD python3 ./discordTimeBot.py $token