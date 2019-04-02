def LoadRatings(file_name):
    """
    Loads the movie ratings.

    :param file_name: Path to tsv file with ratings data.
    :return: Dictionary mapping movie ID to a list with rating and
             number of votes.
    """
    ratings = {}
    with open(file_name) as ratings_file:
        # The first line of the file is the header.
        # We read it and ignore.
        ratings_file.readline()

        # Start reading the actual records from the second line.
        for line in ratings_file:
            rating = line.split('\t')
            # Convert strings to floats to save space.
            ratings[rating[0]] = [float(rating[1]), int(rating[2])]
    return ratings


def LoadMovies(ratings, min_votes, file_name):
    """
    Loads movie data into memory.

    :param ratings: A dictionary mapping movie ID to rating and votes num.
    :param min_votes: The votes threshold, movies with less votes are ignored.
    :param file_name: Path to tsv file with movie data.
    :return: A list of movies with ratings.
    """
    movie_list = []
    with open(file_name) as movie_file:
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
                if votes >= min_votes:
                    # Join the basic movie data with the rating data.
                    movie_list.append([record_list[0], record_list[1], record_list[2], record_list[5]].copy() + rating.copy() + [link[0] + record_list[0]])
        return movie_list


def GetRating(movie_names, movie_list):
    """
    Find ratings for a given movie name.

    :param movie_names: List of movies names.
    :param movie_list: A list of movies with ratings.
    :return: List of movies with rating information.
    """
    matched_movies = []
    movie_names = [name.lower() for name in movie_names]
    name_set = set(movie_names)
    for movie_record in movie_list:
        if movie_record[2].lower() in name_set:
            matched_movies.append(movie_record[1:])
    sorted_matches = []
    for name in movie_names:
        for movie in matched_movies:
            if name == movie[1].lower():
                sorted_matches.append(movie)
    return sorted_matches







