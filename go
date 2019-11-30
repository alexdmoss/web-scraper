#!/usr/bin/env bash
set -euo pipefail


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

if [[ ${1:-} =~ ^(help|run|build|test|init|watch-tests)$ ]]; then
  COMMAND=${1}
  shift
  $COMMAND "$@"
else
  help
  exit 1
fi
