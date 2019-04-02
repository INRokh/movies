import signal
import time

import sheets
import imdb

from absl import app
from absl import flags
from google.oauth2 import service_account

# To create a VM do the following:
#  1. Create new project in GCP.
#  2. Enable Google Sheets API.
#  3. Create a small (f1-mini) Virtual Machine.
#  4. Create or use existing service account and download credentials.
#
# To deploy the service to a Ubuntu VM do the following:
#  1. Download movie files:
#    $ wget https://datasets.imdbws.com/title.basics.tsv.gz
#    $ wget https://datasets.imdbws.com/title.ratings.tsv.gz
#  2. Unzip the files:
#    $ ungzip *.gz
#  3. Update available Linux packages:
#    $ apt update
#  4. Install pip for python3 using sudo:
#    $ sudo apt install python3-pip
#  5. Install Google Sheets dependencies:
#    $ pip3 install --upgrade google-api-python-client /
#      google-auth-httplib2 google-auth-oauthlib
#  6. Upload sctip files to the VM using Google Cloud Console UI or `scp`
#  7. Start service:
#    $ python3 service.py
#
#  Use command `top` to monitor CPU and memory usage. Press `q` to quit.
#  Use command `exit` to close the session to VM. This will stop the
#  service as well. If you want to keep service running start it like this:
#    $ python3 service.py &
#  Use kill <PID> to exit gracefully.

SCOPE = [
    "https://www.googleapis.com/auth/logging.read",
    "https://www.googleapis.com/auth/logging.write",
    "https://www.googleapis.com/auth/spreadsheets",
]
SERVICE_ACCOUNT_FILE = 'secret.json'

FLAGS = flags.FLAGS
flags.DEFINE_string("movie_file", "title.basics.tsv", "Path to tsv file with movie data.")
flags.DEFINE_string("rating_file", "title.ratings.tsv", "Path to tsv file with ratings data.")
# Need to redact.
flags.DEFINE_string("sheet_id", "1RHl4Pl6UmS_CUkZtAg4ksWsccoQhOMRMsKqmKhFdMgY",
                    "ID of Google spreadsheet.")
flags.DEFINE_integer("min_votes", 1000,
                     "Movies with the number of votes less than this value won't be included.")
flags.DEFINE_integer("polling_interval", 120,
                     "Interval in seconds between spreadsheet updates.")


class GracefulShutdown(object):
    def __init__(self):
        self.is_shutdown = False

    def exit(self, signum, frame):
        self.is_shutdown = True

    def is_exit(self):
        return self.is_shutdown

def main(argv):
    del argv  # Unused

    #TODO(Nina): Integrate GCP Logging with abseil logging.
    from google.cloud import logging
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPE)
    logging_client = logging.Client(project="calm-velocity-232700", credentials=creds)
    logger = logging_client.logger("imdb")

    shutdown_handler = GracefulShutdown()
    signal.signal(signal.SIGTERM, shutdown_handler.exit)
    movie_list = imdb.LoadMovies(
        imdb.LoadRatings(FLAGS.rating_file), FLAGS.min_votes, FLAGS.movie_file)
    while True:
        logger.log_text("Start")
        sheets_service = sheets.BuildService(creds)

        movies = sheets.ReadMovieNames(sheets_service, FLAGS.sheet_id)
        logger.log_text(str(movies))

        ratings = imdb.GetRating(movies, movie_list)
        logger.log_text(str(ratings))

        logger.log_text(str(sheets.WriteMovieInfo(ratings, sheets_service, FLAGS.sheet_id)))
        logger.log_text("End")
        if shutdown_handler.is_exit():
            break
        time.sleep(FLAGS.polling_interval)
    logger.log_text("Exit")

if __name__ == '__main__':
    app.run(main)








