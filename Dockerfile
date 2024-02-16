FROM python:3.11.7-alpine
RUN mkdir -p /service-user
WORKDIR /service-user

COPY requirements.txt /service-user/
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
COPY . /service-user
EXPOSE 8080

CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8080"]