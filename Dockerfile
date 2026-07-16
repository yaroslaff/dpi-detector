FROM python:3.14-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir .

ENTRYPOINT ["dpi-detector"]
