FROM python:3.11.7-alpine
RUN mkdir -p /service-user
WORKDIR /service-user

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev
COPY requirements.txt /service-user/
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
COPY . /service-user
EXPOSE 8080

CMD ["uvicorn", "index:service_user", "--host", "0.0.0.0", "--port", "8080"]