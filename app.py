from flask import Flask, render_template, request
import random
import pickle

app = Flask(__name__)

loaded_objects = []

# Загрузка данных из файла pickle
def load_movies(genre=None):
    with open('randomfilms.pickle', 'rb') as pickle_file:
        while True:
            try:
                obj = pickle.load(pickle_file)
                loaded_objects.append(obj)
            except EOFError:
                break
    return loaded_objects


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/random_movie', methods=['POST'])
def random_movie():
    select_genre = request.form.get('genre')
    is_series = request.form.get('is_series')
    rating_from = float(request.form.get('rating_from') or 0)
    rating_to = float(request.form.get('rating_to') or 10)
    year_from = int(request.form.get('year_from') or 1959)
    year_to = int(request.form.get('year_to') or 2023)

    loaded_objects = load_movies()
    filtered_movies = []

    for movie in loaded_objects:
        for j in movie:
            if select_genre in [genre.genre for genre in j.genres]:
                if is_series == 'on' and j.serial:
                    if (
                        j.rating_kinopoisk is not None
                        and rating_from <= j.rating_kinopoisk <= rating_to
                        and year_from <= j.year <= year_to
                    ):
                        filtered_movies.append(j)
                elif is_series != 'on' and not j.serial:
                    if (
                        j.rating_kinopoisk is not None
                        and rating_from <= j.rating_kinopoisk <= rating_to
                        and year_from <= j.year <= year_to
                    ):
                        filtered_movies.append(j)

    if filtered_movies:
        random_movie = random.choice(filtered_movies)
        return render_template('random_movie.html', movie=random_movie)
    else:
        return render_template('no_results.html')


if __name__ == '__main__':
    app.run()
