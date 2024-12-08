FROM python:3.11-slim

RUN mkdir -p /project
WORKDIR /project

COPY tests /project/tests

RUN pip install selenium pytest

ENTRYPOINT ["pytest", "tests"]
#ENTRYPOINT ["sh", "-c", "while true; do sleep 1000; done"]
