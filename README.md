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
- [x] Run in Cloud Run
- [x] Convert to authenticated access only
- [x] Wire up a Schedule
- [x] Generate Log-Based Metric
- [x] Create Alert in Stackdriver
- [x] Check receive alert
- [ ] Convert metric & alert to Success
- [ ] Check how much it costs to run!
- [ ] Blog post on this stuff perhaps?

## Extensions

- [ ] Make the word match case-insensitive
- [ ] Make the word match only for words in the body
- [ ] Allow a list of words to search for
- [ ] Can you set up the log metric & stackdriver alert via an API?

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
2. Come up with a `gcloud run deploy` command - see the deploy function in `./go` for what this ended up being!
3. When switching to CI, the Service Account needs the **Cloud Run Admin** and **Service Account User** roles to successfully use `gcloud run deploy`
4. When authentication is turned on, this command can allow you to grant yourself access to the API: `gcloud run services add-iam-policy-binding ${SERVICE_NAME} --member='user:<your-gcp-email-address>' --role='roles/run.invoker'`

### Hacks

- I set the PORT in the Dockerfile to 8080, which is the Cloud Run default. Solutions proposed by Google involved hacking about with my Dockerfile, which I wasn't wild about - I don't think `$PORT` should be a mandatory env variable

### Further Experiments

- [ ] Try out Cloud Build to auto-deploy to it
- [ ] Give it a nicer hostname
