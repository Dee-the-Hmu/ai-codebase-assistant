from flask import Flask 
from flask_cors import CORS #React will connect with this 
from routers.flask.repositories import repositories_router
from routers.flask.questions import questions_router

import models

def create_app() -> Flask:
    app = Flask(__name__)
    
    #tells Flask to include response headers that permit requests from React development server
    CORS(
        app,
        origins=["http://localhost:5173"]
    )

    app.register_blueprint(repositories_router) #connects the repository Blueprint to the Flask app
    app.register_blueprint(questions_router)

    @app.get("/health")
    def health_check():
        return{
            "status" : "ok",
            "framework" : "flask"
        },200

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001, host="0.0.0.0") #use_reloader = does not restart automatically -> to not load the embedding model twice

"""
127.0.0.1
→ only this container can reach Flask

0.0.0.0
→ Flask accepts connections coming into the container
"""