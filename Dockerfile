FROM python:3.12.7

# docker will not re-pip install if requirements.txt doesn't change
WORKDIR /code
ADD ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

ADD . /code
RUN pip install -e .

CMD ["python", "src/wiki_music/api/run.py"]