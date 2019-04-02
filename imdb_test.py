import os
import imdb
from absl.testing import absltest
from absl import flags


FLAGS = flags.FLAGS

class IMDBTests(absltest.TestCase):
    def test_LoadRatings(self):
        file_content = [
            "header\n",
            "tt0000001\t5.8\t1463\n",
            "tt0000002\t6.4\t176\n",
        ]
        file_path = os.path.join(FLAGS.test_tmpdir, "ratings.tsv")
        with open(file_path, "w") as f:
            f.writelines(file_content)

        actual = imdb.LoadRatings(file_path)
        expected = {
            'tt0000001': [5.8, 1463],
            'tt0000002': [6.4, 176],
        }

        self.assertDictEqual(expected, actual)

        os.remove(file_path)

    def test_LoadMovies(self):
        file_content = [
            "header\n",
            "tt0000001\tmovie\tMovie title1\tMovie1\t0\t1894\t\\N\t120\tDocumentary, Short\n",
            "tt0000002\ttvMovie\tMovie title2\tMovie2\t0\t2010\t\\N\t138\tDrama\n",
            "tt0000003\tshort\tMovie title3\tMovie3\t0\t2017\t\\N\t65\tAnimation,Short\n",
        ]
        file_path = os.path.join(FLAGS.test_tmpdir, "movies.tsv")
        with open(file_path, "w") as f:
            f.writelines(file_content)
        ratings = {
            'tt0000001': [5.8, 1463],
            'tt0000002': [6.4, 176],
            'tt0000003': [5.4, 2076],
        }
        actual = imdb.LoadMovies(ratings, 1000, file_path)
        expected = [
            ['tt0000001', 'movie', 'Movie title1', '1894', 5.8, 1463, 'https://www.imdb.com/title/tt0000001'],
        ]

        self.assertListEqual(expected, actual)

        os.remove(file_path)



    def test_GetRating(self):
        movie_list = [
            ["tt0000001", "movie", "Movie title1", "2012", 5.8, 1463, "https://www.imdb.com/title/tt0000001"],
            ["tt0000002", "Drama", "Movie title2", "1998", 6.0, 2000, "https://www.imdb.com/title/tt0000002"],
            ["tt0000003", "Animation", "Movie title3", "2017", 7.8, 3463, "https://www.imdb.com/title/tt0000003"],

        ]

        movie_names = [
            "Movie title1",
            "Movie title2",
            "Movie title4",
        ]
        actual = imdb.GetRating(movie_names, movie_list)
        expected = [
            ['movie', 'Movie title1', '2012', 5.8, 1463, 'https://www.imdb.com/title/tt0000001'],
            ['Drama', 'Movie title2', '1998', 6.0, 2000, 'https://www.imdb.com/title/tt0000002'],
        ]

        self.assertListEqual(expected, actual)




if __name__ == '__main__':
    absltest.main()









