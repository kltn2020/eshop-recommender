FROM python:3.9.1-alpine3.12

RUN apk update \
  && apk add --upgrade --no-cache \
  bash openssh curl ca-certificates openssl less htop postgresql-libs \
  g++ make wget rsync gcc musl-dev postgresql-dev \
  build-base libpng-dev freetype-dev libexecinfo-dev openblas-dev libgomp lapack-dev \
  libgcc libquadmath musl  \
  libgfortran \
  lapack-dev \
  && pip install --no-cache-dir --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app
EXPOSE 5000
CMD python ./app.py
