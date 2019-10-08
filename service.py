import signal
import time
import logging

import sheets
import imdb
import util

from absl import app
from absl import flags
from google.oauth2 import service_account
import google.cloud.logging as gcp_logging

SCOPE = [
    "https://www.googleapis.com/auth/logging.read",
    "https://www.googleapis.com/auth/logging.write",
    "https://www.googleapis.com/auth/spreadsheets",
]

FLAGS = flags.FLAGS

# IMDB settings.
flags.DEFINE_string("movie_file", "title.basics.tsv", "Path to tsv file with movie data.")
flags.DEFINE_string("rating_file", "title.ratings.tsv", "Path to tsv file with ratings data.")
flags.DEFINE_integer("min_votes", 1000,
                     "Movies with the number of votes less than this value won't be included.")
# Google Sheets API settings.
flags.DEFINE_string("api_secret", "secret.json", "Path to Google API secret file.")
flags.DEFINE_string("sheet_id", "1RHl4Pl6UmS_CUkZtAg4ksWsccoQhOMRMsKqmKhFdMgY",
                    "ID of Google spreadsheet.")
flags.DEFINE_integer("polling_interval", 60,
                     "Interval in seconds between spreadsheet updates.")


def main(argv):
    del argv  # Unused

    creds = service_account.Credentials.from_service_account_file(
        FLAGS.api_secret, scopes=SCOPE)

    logging_client = gcp_logging.Client(project=creds.project_id, credentials=creds)
    logging_client.setup_logging(log_level=logging.INFO)

    movie_service = imdb.Service(FLAGS.min_votes, FLAGS.movie_file, FLAGS.rating_file)

    shutdown_handler = util.GracefulShutdown()
    signal.signal(signal.SIGTERM, shutdown_handler.exit)

    while not shutdown_handler.is_exit():
        logging.info("Start iteration.")

        sheets_service = sheets.BuildService(creds)

        titles = sheets.ReadMovieNames(sheets_service, FLAGS.sheet_id)
        ratings = movie_service.GetRating(titles)

        logging.info(str(sheets.WriteMovieInfo(ratings, sheets_service, FLAGS.sheet_id)))

        logging.info("End iteration.")
        time.sleep(FLAGS.polling_interval)

    logging.info("Exit")


if __name__ == '__main__':
    app.run(main)








