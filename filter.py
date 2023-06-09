import json
import sqlite3


class Film:
    def __init__(self, name, genres, countries, poster, rating_kinopoisk, rating_imdb, year_of_film, film_length,
                 web_url, description, is_serial):
        self.name = name
        self.genres = genres
        self.countries = countries
        self.poster = poster
        self.rating_kinopoisk = rating_kinopoisk
        self.rating_imdb = rating_imdb
        self.year_of_film = year_of_film
        self.film_length = film_length
        self.web_url = web_url
        self.description = description
        self.is_serial = is_serial

    def __str__(self):
        return f"{self.name}, {self.genres}, {self.countries}, {self.poster}, {self.rating_kinopoisk}, {self.rating_imdb}, {self.year_of_film}, {self.film_length}, {self.web_url}, {self.description}, {self.is_serial}"


def filtered_films(genre, genre2, is_series=False, is_russia=False, rating_from=7, rating_to=10, year_from=1984, year_to=2023):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    filter = []
    cursor.execute(
        'SELECT name, genres, countries, poster, rating_kinopoisk, rating_imdb, year_of_film, film_length, web_url, '
        'description, is_serial FROM movies')
    results = cursor.fetchall()

    for row in results:
        name = row[0]
        genres = json.loads(row[1])
        countries = json.loads(row[2])
        poster = row[3]
        rating_kinopoisk = row[4]
        rating_imdb = row[5]
        year_of_film = row[6]
        film_length = row[7]
        web_url = row[8]
        description = row[9]
        is_serial = bool(row[10])

        print(is_series)
        film = Film(name, genres, countries, poster, rating_kinopoisk, rating_imdb, year_of_film, film_length, web_url, description, is_serial)
        if genre in film.genres and genre2 in film.genres:
            if is_series=='on' and film.is_serial:
                if (
                        film.rating_kinopoisk is not None
                        and rating_from <= film.rating_kinopoisk <= rating_to
                        and film.year_of_film is not None and year_from <= film.year_of_film <= year_to
                ):
                    if is_russia:
                        if 'Россия' in film.countries:
                            filter.append(film)
                        else:
                            continue
                    filter.append(film)
            elif is_series != 'on' and not film.is_serial:
                if (
                        film.rating_kinopoisk is not None
                        and rating_from <= film.rating_kinopoisk <= rating_to
                        and film.year_of_film is not None and year_from <= film.year_of_film <= year_to
                ):
                    if is_russia:
                        if 'Россия' in film.countries:
                            filter.append(film)
                        else:
                            continue
                    filter.append(film)
    conn.close()
    return filter
