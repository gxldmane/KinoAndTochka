from flask import Flask, render_template, request
import random
from filter import filtered_films

app = Flask(__name__)


@app.route('/')
def index():
    movie = None  # Добавляем переменную movie
    if 'movie' in request.args:
        movie = request.args['movie']
    return render_template('index.html', movie=movie)  # Передаем переменную movie в шаблон


@app.route('/random_movie', methods=['POST'])
def random_movie():
    genre = request.form.get('genre')
    genre2 = request.form.get('genre2')
    is_series = request.form.get('is_series')
    is_russia = request.form.get('is_russia')
    rating_from = float(request.form.get('rating_from') or 7)
    rating_to = float(request.form.get('rating_to') or 10)
    year_from = int(request.form.get('year_from') or 1984)
    year_to = int(request.form.get('year_to') or 2023)

    filtered_movies = filtered_films(genre, genre2, is_series, is_russia, rating_from, rating_to, year_from, year_to)

    if filtered_movies:
        random_movie = random.choice(filtered_movies)
        return render_template('index.html', movie=random_movie)  # Отправляем выбранный фильм в шаблон index.html
    else:
        return render_template('index.html', movie=None)  # Отправляем None, если нет результатов


if __name__ == '__main__':
    app.run()
