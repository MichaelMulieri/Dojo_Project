from flask_app import app
from flask_app.controllers import user_controller
from flask_app.controllers import pedal_controller
import os
from decouple import config
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    app.run(debug = True)