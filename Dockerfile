FROM python:3.6

RUN mkdir -p /usr/src/review/
WORKDIR /usr/src/review/

COPY . /usr/src/review/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

RUN chmod a+x ./run.sh

ENTRYPOINT ["./run.sh"]

#CMD ["python", "app.py"]