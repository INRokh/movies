import signal
import time
import logging

import sheets
import imdb
import drive

from absl import app
from absl import flags
from google.oauth2 import service_account
import google.cloud.logging as gcp_logging

SCOPE = [
    "https://www.googleapis.com/auth/logging.read",
    "https://www.googleapis.com/auth/logging.write",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
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
flags.DEFINE_integer("polling_interval", 60,
                     "Interval in seconds between spreadsheet updates.")
flags.DEFINE_integer("imdb_refresh_interval", 24*60*60,
                     "Interval in seconds between imdb data is reloaded.")
flags.DEFINE_string("imdb_base_url", "https://datasets.imdbws.com/", "Base URL of the IMDB data server.")


class GracefulShutdown(object):
    def __init__(self):
        self.is_shutdown = False

    def exit(self, signum, frame):
        self.is_shutdown = True

    def is_exit(self):
        return self.is_shutdown

def main(argv):
    del argv  # Unused

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPE)

    logging_client = gcp_logging.Client(project=creds.project_id, credentials=creds)
    logging_client.setup_logging(log_level=logging.INFO)

    shutdown_handler = GracefulShutdown()
    signal.signal(signal.SIGTERM, shutdown_handler.exit)

    movie_service = imdb.Service(FLAGS.imdb_base_url, FLAGS.imdb_refresh_interval,
                                 FLAGS.min_votes, FLAGS.movie_file, FLAGS.rating_file)

    sheet_last_update = ""

    while not shutdown_handler.is_exit():
        logging.info("Start iteration.")

        drive_service = drive.BuildDrive(creds)
        if drive.GetModificationTime(drive_service, FLAGS.sheet_id) == sheet_last_update:
            logging.info("Spreadsheet hasn't changed since the last iteration. Skipping.")
            continue

        sheets_service = sheets.BuildService(creds)

        titles = sheets.ReadMovieNames(sheets_service, FLAGS.sheet_id)
        ratings = movie_service.GetRating(titles)

        logging.info(str(sheets.WriteMovieInfo(ratings, sheets_service, FLAGS.sheet_id)))

        drive_service = drive.BuildDrive(creds)
        sheet_last_update = drive.GetModificationTime(drive_service, FLAGS.sheet_id)

        logging.info("End iteration.")
        time.sleep(FLAGS.polling_interval)

    logging.info("Exit")

if __name__ == '__main__':
    app.run(main)








