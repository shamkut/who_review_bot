FROM python:3.7

RUN mkdir -p /usr/src/review/
WORKDIR /usr/src/review/

COPY . /usr/src/review/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]