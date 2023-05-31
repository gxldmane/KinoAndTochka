import random
from flask import Flask, render_template, request
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.model.filter_genre import FilterGenre
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.model.filter_country import FilterCountry
from kinopoisk_unofficial.model.filter_order import FilterOrder
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest

app = Flask(__name__)
api_client = KinopoiskApiClient("24218a6d-e4a1-4a18-8d01-92a3b6750ee4")

genres_maps = {
    "триллер": 1,
    "драма": 2,
    "криминал": 3,
    "мелодрама": 4,
    "детектив": 5,
    "фантастика": 6,
    "приключения": 7,
    "биография": 8,
    "фильм-нуар": 9,
    "вестерн": 10,
    "боевик": 11,
    "фэнтези": 12,
    "комедия": 13,
    "военный": 14,
    "история": 15,
    "музыка": 16,
    "ужасы": 17,
    "мультфильм": 18,
    "семейный": 19,
    "мюзикл": 20,
    "спорт": 21,
    "документальный": 22,
    "короткометражка": 23,
    "аниме": 24,
    "": 25,
    "новости": 26,
    "концерт": 27,
    "для взрослых": 28,
    "церемония": 29,
    "реальное ТВ": 30,
    "игра": 31,
    "ток-шоу": 32,
    "детский": 33
}

film_cache = {}  # Кэш для сохранения результатов запросов к API

def get_filtered_films(genre_id, rating_from, rating_to, year_from, year_to):
    film_request = FilmSearchByFiltersRequest()
    if film_request.genres:
        film_request.genres = []
    film_request.add_genre(FilterGenre(genre_id, ""))
    film_request.rating_from = rating_from
    film_request.rating_to = rating_to
    film_request.year_from = year_from
    film_request.year_to = year_to
    film_request.order=FilterOrder.RATING
    response = api_client.films.send_film_search_by_filters_request(film_request)
    result = response.items

    filtered_list_of_films = []

    for i in result:
        film = get_film_details(i.kinopoisk_id)
        filtered_list_of_films.append(film)

    return filtered_list_of_films

def get_film_details(kinopoisk_id):
    film_request = FilmRequest(kinopoisk_id)
    response_film = api_client.films.send_film_request(film_request)
    film = response_film.film

    return film

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/random_movie', methods=['POST'])
def random_movie():
    genre = request.form.get('genre')
    is_series = request.form.get('is_series')
    if is_series is None:
        is_series = 'off'
    ongoing = request.form.get('ongoing')
    if ongoing is None:
        ongoing = 'off'
    rating_from = int(request.form.get('rating_from', 0))
    rating_to = int(request.form.get('rating_to', 10))
    year_from = int(request.form.get('year_from', 1959))
    year_to = int(request.form.get('year_to', 2023))

    if genre in genres_maps:
        genre_id = genres_maps[genre]
        filtered_list_of_films = get_filtered_films(genre_id, rating_from, rating_to, year_from, year_to)

        if is_series == 'on':
            filtered_list_of_films = [film for film in filtered_list_of_films if film.serial]
            if ongoing == 'on':
                filtered_list_of_films = [film for film in filtered_list_of_films if film.completed]
            elif ongoing == 'off':
                filtered_list_of_films = [film for film in filtered_list_of_films if not film.completed]
        else:
            if ongoing == 'on':
                filtered_list_of_films = [film for film in filtered_list_of_films if not film.serial or film.completed]
            elif ongoing == 'off':
                filtered_list_of_films = [film for film in filtered_list_of_films if not film.serial or not film.completed]
        filtered_list_of_films = [film for film in filtered_list_of_films if film.rating_kinopoisk and ((rating_from <= float(film.rating_kinopoisk)) and ((film.rating_kinopoisk)<= float(rating_to)))]
        filtered_list_of_films=[film for film in filtered_list_of_films if (year_from<=film.year<=year_to)]

        if filtered_list_of_films:
            random_movie = random.choice(filtered_list_of_films)
            name = random_movie.name_ru
            length = random_movie.film_length
            opisanie = random_movie.description
            poster = random_movie.poster_url
            serial = random_movie.serial
            ongoing = random_movie.completed

            return render_template('random_movie.html', movie=random_movie)

    return render_template('no_results.html')


if __name__ == '__main__':
    app.run()
