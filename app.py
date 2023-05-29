import json
from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Загрузка данных из .json файла с использованием кодировки UTF-8
with open('movies.json', 'r', encoding='utf-8') as json_file:
    movies_db = json.load(json_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random_movie', methods=['POST'])
def random_movie():
    selected_genre = request.form.get('genre')
    selected_duration = request.form.get('duration')
    selected_novelty = request.form.get('novelty')
    selected_age_limit = request.form.get('age_limit')
    selected_country = request.form.get('country')

    filtered_movies = [movie for movie in movies_db if
                       movie['genre'] == selected_genre and
                       (selected_duration == 'short' and movie['duration'] < 120 or
                        selected_duration == 'long' and movie['duration'] >= 120) and
                       (selected_novelty == 'old' and movie['year'] < 2010 or
                        selected_novelty == 'new' and movie['year'] >= 2010) and
                       movie['age_limit'] == selected_age_limit and
                       (selected_country == 'Россия' and movie['country'] == 'Россия' or
                        selected_country == 'Не Россия' and movie['country'] != 'Россия')
                       ]

    if filtered_movies:
        random_movie = random.choice(filtered_movies)
        return render_template('random_movie.html', movie=random_movie)
    else:
        return render_template('no_results.html')

if __name__ == '__main__':
    app.run()
