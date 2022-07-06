from flask_app import app
from flask import render_template, request, redirect, session, flash, jsonify
import requests, os
from flask_app.models.movie import Movie

@app.route('/')
def index():
    if 'query' in session:
        session.pop('query')
    if 'results' in session:
        session.pop('results')
    if 'one_result' in session:
        session.pop('one_result')

    return render_template("index.html")

@app.route('/searching', methods=['POST'])
def search_processing():

    r = requests.get(f"https://api.watchmode.com/v1/autocomplete-search/?apiKey={os.environ.get('WATCHMODE_API_KEY')}&search_value={request.form['query']}&search_type=1")

    if 'query' in session:
        session.pop('query')
    if 'results' in session:
        session.pop('results')
    if 'one_result' in session:
        session.pop('one_result')

    session['query'] = request.form['query']
    session['results'] = r.json()

    return redirect('/search')

@app.route('/search')
def search():
    query = session['query']
    # print(query)
    results = session['results']
    # print(results)

    return render_template("/search.html", query = query, results = results)

@app.route('/<int:id>/processing')
def movie_processing(id):

    r = requests.get(f"https://api.watchmode.com/v1/title/{id}/details/?apiKey={os.environ.get('WATCHMODE_API_KEY')}&append_to_response=sources")
    
    if 'one_result' in session:
        session.pop('one_result')
    session['one_result'] = r.json()
    return redirect(f'/{id}')

@app.route('/<int:id>')
def one_movie(id):
    results = session['one_result']
    favorites = None

    movie_data = {
        'watchmode_id' : results['id'],
        'title' : results['title'],
        'poster_link' : results['poster']
    }

    if (len(Movie.movie_in_db(movie_data)) >= 1) and 'user_id' in session:
        response = Movie.movie_in_db(movie_data)
        one_movie = response[0]['id']

        favorite_data = {
            'user_id' : session['user_id'],
            'show_id' : one_movie
        }

        if (len(Movie.get_specific_favorite(favorite_data)) >= 1):
            favorites = "favorited"

    return render_template("content.html", results = results, favorites = favorites)

@app.route('/favorite/<int:id>')
def favorite_processing(id):
    movie_data = {
        'watchmode_id' : session['one_result']['id'],
        'title' : session['one_result']['title'],
        'poster_link' : session['one_result']['poster']
    }

    if (len(Movie.movie_in_db(movie_data)) >= 1):
        one_movie = Movie.movie_in_db(movie_data)[0]['id']
    else:
        one_movie = Movie.save_movie(movie_data)

    favorite_data = {
        'user_id' : session['user_id'],
        'show_id' : one_movie
    }

    if (len(Movie.get_specific_favorite(favorite_data)) >= 1):
        Movie.remove_favorite(favorite_data)
        return redirect(f'/{id}')
    else:
        Movie.favorite_movie(favorite_data)

    return redirect(f'/{id}')
