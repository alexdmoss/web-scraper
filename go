#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME=webscraper

function help() {
  echo -e "Usage: go <command>"
  echo -e
  echo -e "    help               Print this help"
  echo -e "    run                Run locally without building binary"
  echo -e "    build              Build binary locally"
  echo -e "    test               Run local unit tests and linting"
  echo -e "    watch-tests        Run pytest continuously on save. Useful for TDD"
  echo -e "    init               Set up local virtual env"
  echo -e 
  exit 0
}

function init() {

  _console_msg "Initialising local virtual environment ..." INFO true

  pipenv install --dev

  _console_msg "Init complete" INFO true

}

function run() {

  _console_msg "Running app ..." INFO true

  export FLASK_APP=webscraper
  export FLASK_DEBUG=1
  pipenv run flask run

  _console_msg "Execution complete" INFO true

}

function test() {

    _console_msg "Running flake8 ..." INFO true

    pipenv run flake8 .

    _console_msg "Running unit tests ..." INFO true

    pipenv run pytest -v

    _console_msg "Tests complete" INFO true

}

function watch-tests() {

    _console_msg "Watching unit tests ..." INFO true

    pipenv run ptw
    
    _console_msg "Tests complete" INFO true

}

function build() {

  _assert_variables_set IMAGE_NAME

  _console_msg "Building python docker image ..." INFO true

  docker build -t ${IMAGE_NAME} .

  _console_msg "Build complete" INFO true

}

function deploy() {

  _assert_variables_set GCP_PROJECT_ID SERVICE_NAME

  _console_msg "Deploying to Google Cloud Run ..." INFO true

  if [[ ${DRONE:-} == "true" ]]; then
    _assert_variables_set CLOUD_RUN_CREDS
    _console_msg "-> Authenticating with GCloud"
    echo "${CLOUD_RUN_CREDS}" | gcloud auth activate-service-account --key-file -
    trap "gcloud auth revoke --verbosity=error" EXIT
  fi

  if [[ -z ${DRONE_COMMIT_SHA:-} ]]; then
    LATEST_TAG=$(gcloud container images list-tags eu.gcr.io/moss-work/web-scraper --limit=1 --format='value(tags)')
  else
    LATEST_TAG=${DRONE_COMMIT_SHA}
  fi

  gcloud run deploy ${SERVICE_NAME} \
    --image=eu.gcr.io/moss-work/web-scraper:${LATEST_TAG} \
    --platform=managed \
    --region=europe-west1 \
    --project=${GCP_PROJECT_ID} \
    --timeout=10 \
    --concurrency=1 \
    --max-instances=1 \
    --memory=128Mi \
    --no-allow-unauthenticated \
    --update-env-vars TARGET_URL="https://www.olympiccinema.co.uk/film/Star-Wars:-Rise-Of-Skywalker",WORD_TO_FIND="book"

  _console_msg "Deploy complete" INFO true

}

function configure-schedule() {

  _assert_variables_set GCP_PROJECT_ID SERVICE_NAME SERVICE_URL

  _console_msg "Setting permissions for Cloud Run access" INFO true

  gcloud run services add-iam-policy-binding ${SERVICE_NAME} \
    --member=serviceAccount:web-scraper-runner@${GCP_PROJECT_ID}.iam.gserviceaccount.com \
    --role=roles/run.invoker \
    --project=${GCP_PROJECT_ID} \
    --region=europe-west1 \
    --platform=managed

  _console_msg "Configuring Cloud Scheduler job" INFO true

  gcloud beta scheduler jobs create http ${SERVICE_NAME}-job \
    --schedule "5 * * * *" \
    --http-method=GET \
    --uri=${SERVICE_URL} \
    --oidc-service-account-email=web-scraper-runner@${GCP_PROJECT_ID}.iam.gserviceaccount.com   \
    --oidc-token-audience=${SERVICE_URL}

    _console_msg "Schedule setup complete" INFO true

}

function _assert_variables_set() {

  local error=0
  local varname
  
  for varname in "$@"; do
    if [[ -z "${!varname-}" ]]; then
      echo "${varname} must be set" >&2
      error=1
    fi
  done
  
  if [[ ${error} = 1 ]]; then
    exit 1
  fi

}

function _console_msg() {

  local msg=${1}
  local level=${2:-}
  local ts=${3:-}

  if [[ -z ${level} ]]; then level=INFO; fi
  if [[ -n ${ts} ]]; then ts=" [$(date +"%Y-%m-%d %H:%M")]"; fi

  echo ""

  if [[ ${level} == "ERROR" ]] || [[ ${level} == "CRIT" ]] || [[ ${level} == "FATAL" ]]; then
    (echo 2>&1)
    (echo >&2 "-> [${level}]${ts} ${msg}")
  else 
    (echo "-> [${level}]${ts} ${msg}")
  fi

  echo ""

}

function ctrl_c() {
    if [ ! -z ${PID:-} ]; then
        kill ${PID}
    fi
    exit 1
}

trap ctrl_c INT

if [[ ${1:-} =~ ^(help|run|build|test|init|watch-tests|deploy|configure-schedule)$ ]]; then
  COMMAND=${1}
  shift
  $COMMAND "$@"
else
  help
  exit 1
fi
