FROM python:alpine3.19
WORKDIR /sponsorship/
COPY ./requirements.txt .
RUN apk update && apk add --no-cache \
        postgresql-dev \
        build-base \
        pkgconfig \
    && rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt
COPY . /sponsorship/
CMD ["python", "manage.py", "runserver"]