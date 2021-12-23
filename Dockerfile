FROM python:3.9-slim-buster

WORKDIR /opt/bgone-bot

ENV PYTHONUNBUFFERED=1

COPY . .

# install git
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && apt-get purge -y --auto-remove \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install python-dotenv==0.19.2 requests==2.26.0 Pillow==8.4.0

RUN pip install -U git+https://github.com/Pycord-Development/pycord@16f9bcb5f43f614cb2eb7691c978f2e9f28548c8

RUN pip3 install -e .

CMD ["python3", "bgone/bot.py"]
