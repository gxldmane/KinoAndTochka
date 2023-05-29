import random
from flask import Flask, render_template, request
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.model.filter_genre import FilterGenre
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest
from kinopoisk_unofficial.request.films.film_request import FilmRequest

app = Flask(__name__)
api_client = KinopoiskApiClient("66cfec9c-4a01-47fd-9fc3-1caa79ecf41c")

film_cache = {}  # Кэш для сохранения результатов запросов к API

def get_filtered_films(genre):
    if genre in film_cache:
        filtered_list_of_films = film_cache[genre]
    else:
        film_request = FilmSearchByFiltersRequest()
        film_request.add_genre(FilterGenre(24, genre))

        response = api_client.films.send_film_search_by_filters_request(film_request)
        result = response.items

        filtered_list_of_films = []

        for i in result:
            film = get_film_details(i.kinopoisk_id)
            filtered_list_of_films.append(film)

        film_cache[genre] = filtered_list_of_films

    return filtered_list_of_films

def get_film_details(kinopoisk_id):
    if kinopoisk_id in film_cache:
        film = film_cache[kinopoisk_id]
    else:
        film_request = FilmRequest(kinopoisk_id)
        response_film = api_client.films.send_film_request(film_request)
        film = response_film.film

        film_cache[kinopoisk_id] = film

    return film

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random_movie', methods=['POST'])
def random_movie():
    genre = request.form.get('genre')

    filtered_list_of_films = get_filtered_films(genre)

    if filtered_list_of_films:
        random_movie = random.choice(filtered_list_of_films)
        name = random_movie.name_ru
        length = random_movie.film_length
        opisanie = random_movie.description
        poster = random_movie.poster_url
        serial = random_movie.serial
        ongoing = random_movie.completed

        return render_template('random_movie.html', movie=random_movie)
    else:
        return render_template('no_results.html')

if __name__ == '__main__':
    app.run()
