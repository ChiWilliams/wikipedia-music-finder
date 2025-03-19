FROM python:3.12.3
WORKDIR /app

# docker will not re-pip install if requirements.txt doesn't change
WORKDIR /code
ADD ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -e .

ADD . /code

# Make sure the app is accessible from outside
ENV HOST=0.0.0.0
CMD ["python", "src/wiki_music/api/run.py"]