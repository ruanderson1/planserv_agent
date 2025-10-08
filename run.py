# from flask import Flask
# from app.routes.query_route import query_bp

# app = Flask(__name__)
# app.register_blueprint(query_bp)

# if __name__ == "__main__":
#     app.run(port=8000, debug=True)

## run.py

from app.main import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
