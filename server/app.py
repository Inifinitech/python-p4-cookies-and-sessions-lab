#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    authors = [article.to_dict(rules=('-date', '-minutes_to_read', '-preview', '-user', '-user_id', )) for article in Article.query.all()]
    response = make_response(jsonify(authors), 200)

    return response

@app.route('/articles/<int:id>')
def show_article(id):
    # set session['page_views'] to 0 if it doesn't exist, if not leave it as it is
    session['page_views'] = session.get('page_views', 0) + 1

    # check if the user has viewed 3 or fewer pages
    if session['page_views'] <= 3:
        article = {
        "id": id,
        "title": f"Article {id}",
        "content": "This is the content of the article",
        "author": "Author Name"
        }
        response_dict = {"article": article, "page_views": session['page_views']}
        response = make_response(jsonify(response_dict))
        return response
    else:
        response_dict = {"message": "Maximum pageview limit reached"}
        response = make_response(jsonify(response_dict), 401)

        return response


if __name__ == '__main__':
    app.run(port=5000, debug=True)
