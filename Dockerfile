ARG BASE_IMAGE=3.7.5-alpine3.10

FROM python:$BASE_IMAGE AS requirements
ADD . /app
WORKDIR /app
RUN pip install pipenv
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
ENV USER=web-app
ENV UID=1337
ENV GID=1337
RUN addgroup --gid "$GID" "$USER" \
  && adduser --disabled-password --gecos "" --home "$(pwd)" --ingroup "$USER" --no-create-home --uid "$UID" "$USER" \
  && chown $USER /app
USER web-app
WORKDIR /app
ENV FLASK_APP=webscraper
# ENTRYPOINT [ "pipenv", "run", "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT ["gunicorn", "-t", "200", "-w", "2", "--bind", "0.0.0.0:5000", "webscraper:app"]
