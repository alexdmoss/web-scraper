# web-scraper

Goals:

1. Practice TDD
2. Scrape a web page using Python's Beautiful Soup
3. Set up as a Google Cloud Function on a schedule
4. Write a log-based metric which Stackdriver can have an alert for (because there's no SMTP service in GCP!)

---

## To Do

- [ ] Bootstrap project
- [ ] Init BeautifulSoup
- [ ] Run as Cloud Function
- [ ] Wire up a Schedule
- [ ] Generate Log-Based Metric
- [ ] Create Alert in Stackdriver

---

## Usage

You need either `docker` or `python` on your local machine - both are easy to install on most common OSes.

If using python directly, `pipenv install --dev` from the root directory.

There is a wrapper script (`./go` in `bash`) to make this easier (**Note:** CI does not currently use this):

- `./go run`- run go locally without building
- `./go test` - run unit tests and benchmarks
- `./go build` - builds docker image locally and runs smoke tests

NB: You can use `pipenv run ptw` to continuously run your tests in the background - quite helpful!

## Replicating

**Repo name** is included in the following locations:

- `setup.py`
- top of `./go`
- `.coveragerc`

**Package names** are included in:

- `Pipfile`
