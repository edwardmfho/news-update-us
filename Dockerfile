FROM python:3.7

RUN pip install python-telegram-bot
RUN pip install google-cloud-storage
RUN pip install requests

RUN mkdir /app
ADD . /app
WORKDIR /app

CMD python /app/news_bot.py

heroku container:release --app news-update-us web