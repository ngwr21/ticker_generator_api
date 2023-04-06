# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install wkhtmltopdf dependencies
RUN apk add --no-cache \
    libffi-dev \
    openssl-dev \
    libxslt-dev \
    libxml2-dev \
    zlib-dev \
    ttf-freefont \
    fontconfig \
    libxrender \
    libxext \
    libjpeg-turbo \
    libpng

# install wkhtmltopdf
RUN apk add --no-cache --virtual .build-deps \
    msttcorefonts-installer \
    wkhtmltopdf \
    && update-ms-fonts \
    && fc-cache -f



# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]