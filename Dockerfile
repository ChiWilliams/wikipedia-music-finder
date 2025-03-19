FROM python:3.12.7

# Clean start
WORKDIR /code
ADD ./requirements.txt /code/requirements.txt

# Clear pip cache and reinstall everything
RUN pip cache purge && \
    pip install --no-cache-dir -r requirements.txt

ADD . /code
RUN pip install --no-cache-dir -e .

CMD ["python", "src/wiki_music/api/run.py"]