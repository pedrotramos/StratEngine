FROM python:3.12.8-slim

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python"]