FROM python:3.6

ADD . /
RUN pip3 install -r requirements.txt

WORKDIR /

CMD ["python3" , "/floor_bot.py"]
