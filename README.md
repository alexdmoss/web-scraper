# web-scraper

Goals:

1. Practice TDD
2. Scrape a web page using Python's Beautiful Soup
3. Run in Cloud Run
4. Set up a Schedule
5. Write a log-based metric which Stackdriver can have an alert for (because there's no SMTP service in GCP!)

---

## To Do

- [x] Bootstrap project
- [x] Init BeautifulSoup
- [x] Search for word on cinema booking page!
- [ ] Run in Cloud Run
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
- `./go watch-tests` - to run pytest continously in the CLI - helpful when developing

---

## Getting It Running in Google Cloud Run

1. Enable the API in your GCP project with `gcloud services enable run.googleapis.com`

### Hacks

- I set the PORT in the Dockerfile to 8080, which is the Cloud Run default. Solutions proposed by Google involved hacking about with my Dockerfile, which I wasn't wild about - I don't think `$PORT` should be a mandatory env variable
