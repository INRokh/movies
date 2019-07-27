import gzip
import urllib.request
import datetime
import logging

class Service(object):
    _MOVIE_FILENAME = "title.basics.tsv"
    _RATING_FILENAME = "title.ratings.tsv"

    def __init__(self, base_url, refresh_interval, min_votes):
        self.base_url = base_url
        self.refresh_interval = refresh_interval
        self.min_votes = min_votes
        self.movie_list = []
        self.update_time = None

    def _FetchFile(self, base_url, filename):
        """Download gz file and unzip it."""
        response = urllib.request.urlopen(base_url + filename + ".gz")
        with open(filename, 'wb') as outfile:
            outfile.write(gzip.decompress(response.read()))

    def GetRating(self, movie_names):
        """
        Find ratings for a given movie name.

        :param movie_names: List of movies names.
        :return: List of movies with rating information.
        """
        self._Refresh()
        matched_movies = []
        movie_names = [name.lower() for name in movie_names]
        name_set = set(movie_names)
        for movie_record in self.movie_list:
            if movie_record[2].lower() in name_set:
                matched_movies.append(movie_record[1:])
        sorted_matches = []
        for name in movie_names:
            for movie in matched_movies:
                if name == movie[1].lower():
                    sorted_matches.append(movie)
        return sorted_matches

    def _Refresh(self):
        """Update files according to refresh interval."""
        # Check if data is already loaded.
        if self.update_time is not None:
            if self.refresh_interval < 0:
                # Never update.
                return
            delta_time = datetime.datetime.now() - self.update_time
            if delta_time.seconds < self.refresh_interval:
                return
        logging.info("Refreshing imdb data")
        self._FetchFile(self.base_url, self._MOVIE_FILENAME)
        self._FetchFile(self.base_url, self._RATING_FILENAME)
        self.update_time = datetime.datetime.now()
        self.movie_list = self._LoadMovies(self._LoadRatings())

    def _LoadRatings(self):
        """Loads the movie ratings."""
        ratings = {}
        with open(self._RATING_FILENAME) as ratings_file:
            # The first line of the file is the header.
            # We read it and ignore.
            ratings_file.readline()

            # Start reading the actual records from the second line.
            for line in ratings_file:
                rating = line.split('\t')
                # Convert strings to floats to save space.
                ratings[rating[0]] = [float(rating[1]), int(rating[2])]
        return ratings

    def _LoadMovies(self, ratings):
        """
        Loads movie data into memory.

        :param ratings: A dictionary mapping movie ID to rating and votes num.
        :return: A list of movies with ratings.
        """
        movie_list = []
        with open(self._MOVIE_FILENAME) as movie_file:
            # The first line of the file is the header.
            # We read it and ignore.
            movie_file.readline()

            for movie_record in movie_file:
                link = ['https://www.imdb.com/title/']
                record_list = movie_record.split('\t')
                if record_list[1] not in ['tvMovie', 'movie', 'tvSeries']:
                    continue
                if record_list[0] in ratings:
                    rating = ratings[record_list[0]]
                    votes = rating[1]
                    if votes >= self.min_votes:
                        # Join the basic movie data with the rating data.
                        movie_list.append([record_list[0], record_list[1], record_list[2], record_list[5]].copy() + rating.copy() + [link[0] + record_list[0]])
            return movie_list










