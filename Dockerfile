FROM python:3.9-slim-buster

WORKDIR /opt/bgone-bot

ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip3 install py-cord==1.7.3 python-dotenv==0.19.2 requests==2.26.0 Pillow==8.4.0

CMD ["python3", "bgone/bgone_bot.py"]
