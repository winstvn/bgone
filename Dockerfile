FROM python:3.9-slim-buster

WORKDIR /opt/bgone-bot

ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "bgone/bgone_bot.py"]
