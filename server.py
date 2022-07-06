from flask_app import app

# Add Controller Routes As Needed!
from flask_app.controllers import movie_controller, user_controller

if __name__ == "__main__":
    app.run(debug=True)