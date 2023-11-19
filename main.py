from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import desc
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, URL
import requests
import pprint

db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-movies-collection.db"
# initialize the app with the extension
db.init_app(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)

api_key = "761b9764dc14fad26bb0bf065c584a09"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Float, nullable=False)
    review = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


# with app.app_context():
#     db.create_all()
with app.app_context():
    new_movie = Movie(
        title="Phone Booth",
        year=2002,
        description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
        rating=7.3,
        ranking=10,
        review="My favourite character was the caller.",
        img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    )
    db.session.add(new_movie)
    # db.session.commit()


class MovieForm(FlaskForm):
    rating = StringField('Your Rating Out of 10 e.g. 4.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')


class AddMovieForm(FlaskForm):
    movie_title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


@app.route('/')
def home():
    with app.app_context():
        # all_movies = db.session.query(Movie).all()
        all_movies = Movie.query.order_by('rating').all()
    return render_template('index.html', movies=all_movies)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = MovieForm()
    movie_id = request.args.get("id_m")
    print(f"movie_id is {movie_id}")
    if form.validate_on_submit():

        with app.app_context():
            movie_to_update = db.session.get(Movie, movie_id)
            movie_to_update.rating = form.rating.data
            movie_to_update.review = form.review.data
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        base_image_url = "http://image.tmdb.org/t/p/original/"
        search_path = "https://api.themoviedb.org/3/search/movie?api_key=761b9764dc14fad26bb0bf065c584a09"
        movie_name = form.movie_title.data
        params = {
            'query': movie_name
        }
        response = requests.get(url=search_path, params=params)
        data = response.json()
        print(data)
        movie_id = request.args.get('id')
        print(movie_id)
        return render_template('select.html', data=data)

    return render_template('add.html', form=form)


@app.route('/select')
def select():
    return render_template('select.html')


@app.route('/trial')
def trial():
    movie_id = request.args.get('search_id')
    resp = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US")
    data = resp.json()
    # pprint.pprint(data)
    # print(movie_id)
    with app.app_context():
        new_movie = Movie(
            title=data['original_title'],
            year=data['release_date'][:4],
            description=data['overview'],
            rating=7.3,
            ranking=10,
            review="My favourite character was the caller.",
            img_url=f"https://image.tmdb.org/t/p/original/{data['poster_path']}"
        )
        db.session.add(new_movie)
        db.session.commit()
        mov = Movie.query.filter_by(title=data['original_title']).first()
        m_id = mov.id
        print(f"id from trial: {m_id}")
    return redirect(url_for('edit', id_m=m_id))


@app.route('/delete/<int:id>')
def delete(id):
    movie_id = id
    movie_to_delete = db.session.get(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
