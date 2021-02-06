FROM python:3.8

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD ["service/app.py"]