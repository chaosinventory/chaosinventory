FROM python:latest

RUN mkdir /chaosinventory
RUN mkdir /data

COPY . /chaosinventory/
WORKDIR /chaosinventory/

RUN pip install -r src/requirements.txt
RUN pip install gunicorn

ENV CHAOSINVENTORY_CONFIG_FILE /data/chaosinventory.cfg
ENV CHAOSINVENTORY_SQLITE3_FILE /data/chaosinventory.sqlite3

EXPOSE 8000
ENTRYPOINT ["scripts/entry.sh"]
