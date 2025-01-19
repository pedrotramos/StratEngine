FROM python:3.12.8-slim

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

ARG MONGODB_URI
ENV MONGODB_URI=${MONGODB_URI}

ARG BRAPI_TOKEN
ENV BRAPI_TOKEN=${BRAPI_TOKEN}

ENTRYPOINT ["python"]