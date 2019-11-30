ARG BASE_IMAGE=3.7.5-alpine3.10

FROM python:$BASE_IMAGE AS requirements
ADD . /app
WORKDIR /app
RUN pip install pipenv=='2018.11.26'
RUN pipenv lock -r > requirements.txt
RUN pipenv lock --dev -r > requirements-dev.txt

FROM python:$BASE_IMAGE AS runtime-pips
COPY --from=requirements /app /app
WORKDIR /app
RUN apk update --no-cache && \
  apk upgrade && \
  apk add gcc musl-dev libffi-dev openssl-dev && \
  pip install -r requirements.txt --no-use-pep517

FROM python:$BASE_IMAGE AS pytest
COPY --from=runtime-pips /app /app
COPY --from=runtime-pips /usr/local /usr/local
RUN apk update --no-cache && \
  apk upgrade && \
  apk add gcc musl-dev
WORKDIR /app
RUN pip install -r requirements-dev.txt
RUN /usr/local/bin/pytest

FROM python:$BASE_IMAGE
COPY --from=runtime-pips /app /app
COPY --from=runtime-pips /usr/local /usr/local
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/python", "/app/main.py"]
