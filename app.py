from flask import Flask, render_template, request
import random

app = Flask(__name__)

movies_db = [
    {"title": "Фильм 1", "genre": "драма", "tags": ["тег1", "тег2", "тег3"]},
    {"title": "Фильм 2", "genre": "комедия", "tags": ["тег2", "тег3"]},
    {"title": "Фильм 3", "genre": "фантастика", "tags": ["тег1", "тег3"]},
    {"title": "Фильм 4", "genre": "драма", "tags": ["тег1", "тег2"]},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random_movie', methods=['POST'])
def random_movie():
    selected_genre = request.form.get('genre')
    selected_tags = request.form.getlist('tags')

    filtered_movies = [movie for movie in movies_db if movie['genre'] == selected_genre and all(tag in movie['tags'] for tag in selected_tags)]

    if filtered_movies:
        random_movie = random.choice(filtered_movies)
        return render_template('random_movie.html', movie=random_movie)
    else:
        return render_template('no_results.html')

if __name__ == '__main__':
    app.run()
