from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Movie:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.poster_link = data['poster_link']
        self.watchmode_id = data['watchmode_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.user = None

    @classmethod
    def save_movie(cls, data):
        query = "INSERT INTO shows (title, poster_link, watchmode_id, created_at, updated_at) VALUES (%(title)s, %(poster_link)s, %(watchmode_id)s, NOW(), NOW());"
        return connectToMySQL("stream_schema").query_db(query, data)

    @classmethod
    def favorite_movie(cls, data):
        query = "INSERT INTO favorites (user_id, show_id) VALUES (%(user_id)s, %(show_id)s);"
        return connectToMySQL("stream_schema").query_db(query, data)

    @classmethod
    def get_favorites(cls, data):
        query = "SELECT * FROM favorites JOIN users ON users.id = favorites.user_id JOIN shows ON shows.id = favorites.show_id WHERE users.id = %(user_id)s;"
        results = connectToMySQL("stream_schema").query_db(query, data)
        all_faves = []

        for row in results:
            user_data = {
                'id' : row['users.id'],
                'username' : row['username'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at'],
            }
            
            movie_data = {
                'id' : row['shows.id'],
                'title' : row['title'],
                'poster_link' : row['poster_link'],
                'watchmode_id' : row['watchmode_id'],
                'created_at' : row['shows.created_at'],
                'updated_at' : row['shows.updated_at'],
            }
            movie = Movie(movie_data)
            movie.user = user.User(user_data)
            all_faves.append(movie)


        return all_faves

    @classmethod
    def get_specific_favorite(cls, data):
        query = "SELECT * FROM favorites JOIN users ON users.id = favorites.user_id JOIN shows ON shows.id = favorites.show_id WHERE users.id = %(user_id)s AND favorites.show_id = %(show_id)s;"
        results = connectToMySQL("stream_schema").query_db(query, data)
        return results

    @classmethod
    def remove_favorite(cls, data):
        query = "DELETE FROM favorites WHERE favorites.user_id = %(user_id)s AND favorites.show_id = %(show_id)s;"
        return connectToMySQL("stream_schema").query_db(query, data)

    @classmethod
    def movie_in_db(cls, data):
        query = "SELECT * FROM shows WHERE watchmode_id = %(watchmode_id)s;"
        results = connectToMySQL("stream_schema").query_db(query, data)
        return results


