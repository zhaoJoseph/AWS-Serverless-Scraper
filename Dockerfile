FROM python:3.10.7

ENV PYTHONUNBUFFERED=0

ENV VIRTUAL_ENV=/opt/venv

RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /pyscraper

COPY requirements.txt .

RUN pip3 install -r requirements.txt 

COPY pyscraper .

RUN playwright install

RUN playwright install-deps

ENV URL=""

CMD  python webscraper/pyscraper.py ${URL}

