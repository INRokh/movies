import gzip
import urllib.request
import datetime
import logging

class Service(object):

    def __init__(self, min_votes, movie_file, rating_file):
        self.min_votes = min_votes
        self.movie_file = movie_file
        self.rating_file = rating_file
        self.movie_list = self._LoadMovies(self._LoadRatings())

    def GetRating(self, movie_names):
        """
        Find ratings for a given movie name.

        :param movie_names: List of movies names.
        :return: List of movies with rating information.
        """
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

    def _LoadRatings(self):
        """Loads the movie ratings."""
        ratings = {}
        with open(self.rating_file) as f:
            # The first line of the file is the header.
            # We read it and ignore.
            f.readline()

            # Start reading the actual records from the second line.
            for line in f:
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
        with open(self.movie_file) as f:
            # The first line of the file is the header.
            # We read it and ignore.
            f.readline()

            for movie_record in f:
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










