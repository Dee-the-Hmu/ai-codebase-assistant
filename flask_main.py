from flask import Flask 
from flask_cors import CORS #React will connect with this 
from routers.flask.repositories import repositories_router
from routers.flask.questions import questions_router
from routers.flask.health import health_router

import models

def create_app() -> Flask:
    app = Flask(__name__)
    
    CORS(#tells Flask which Frontend websites are allowed to call my Flask backend from a browser
        app,
        origins=[
            "http://localhost:5173",
            "https://d12mwdjp9rnq6y.cloudfront.net" #CloudFront frontend domain
        ]
    )

    app.register_blueprint(repositories_router) #connects the repository Blueprint to the Flask app
    app.register_blueprint(questions_router)
    app.register_blueprint(health_router)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, port=5001, host="0.0.0.0") #use_reloader = does not restart automatically -> to not load the embedding model twice

"""
127.0.0.1
→ only this container can reach Flask

0.0.0.0
→ Flask accepts connections coming into the container
"""