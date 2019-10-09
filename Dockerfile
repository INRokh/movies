FROM python:3-slim

WORKDIR /app

COPY *.py /app/
COPY requirements.txt /app/

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Load IMDB data.
RUN apt-get update && apt-get install -y curl
RUN curl -o title.basics.tsv.gz https://datasets.imdbws.com/title.basics.tsv.gz
RUN curl -o title.ratings.tsv.gz https://datasets.imdbws.com/title.ratings.tsv.gz
RUN gunzip *.gz

CMD ["python3", "service.py"]