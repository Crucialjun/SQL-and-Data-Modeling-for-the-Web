#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#


import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    genres = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    looking_for_talent = db.Column(db.Boolean)
    description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venues', lazy=True)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(500))
    state = db.Column(db.String(500))
    phone = db.Column(db.String(500))
    genres = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    looking_for_venues = db.Column(db.Boolean)
    description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artists', lazy=True)


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.String(120))


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = Venue.query.all()
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    query = request.form.get("search_term", '')
    venues = Venue.query.filter(Venue.name.ilike("%" + query + "%")).all()
    print(venues, file=sys.stderr)
    return render_template('pages/search_venues.html', results=venues, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

    data = Venue.query.filter_by(id=venue_id).first()
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        facebook_link = request.form.get('facebook_link')
        genres = request.form.get('genres')
        website_link = request.form.get('website_link')
        description = request.form.get('seeking_description')

        venue = Venue(
            name=name,
            city=city,
            state=state,
            address=address,
            phone=phone,
            image_link=image_link,
            facebook_link=facebook_link,
            genres=genres,
            website_link=website_link,
            looking_for_talent=False,
            description=description


        )
        db.session.add(venue)
        db.session.commit()

        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        flash("An error occured Venue" +
              request.form['name'] + " could not be  listed! because of " + str(e))
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    try:
        venue = Venue.query.filter_by(id=venue_id).first()
        db.session.delete(venue)
        db.session.commit()
    except Exception as e:
        print(str(e))
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    query = request.form.get("search_term", '')
    artist = Venue.query.filter(Venue.name.ilike("%" + query + "%")).all()
    return render_template('pages/search_artists.html', results=artist, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id

    data = Artist.query.filter_by(id=artist_id).first()
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first()
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

    try:
        artist = Artist.query.filter_by(id=artist_id).first()

        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        facebook_link = request.form.get('facebook_link')
        genres = request.form.get('genres')
        website_link = request.form.get('website_link')
        seeking_venue = request.form.get('seeking_venue')
        description = request.form.get('seeking_description')

        artist.name = name,
        artist.city = city,
        artist.sartist.tate = state,
        artist.phone = phone,
        artist.image_link = image_link,
        artist.facebook_link = facebook_link,
        artist.genres = genres,
        artist.website_link = website_link,
        artist.lartist.ooking_for_venues = seeking_venue,
        artist.description = description

        db.session.commit()
    except Exception as e:
        db.session.rollback()

    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    venue = Venue.query.filter_by(id=venue_id).first()

    form.name.data = venue.name
    form.address.data = venue.address
    form.city.data = venue.city
    form.facebook_link.data = venue.facebook_link
    form.genres.data = venue.genres
    form.image_link.data = venue.image_link
    form.phone.data = venue.phone
    form.state.data = venue.state
    form.website_link.data = venue.website_link
    form.seeking_talent.data = venue.looking_for_talent
    form.seeking_description.data = venue.description

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

    venue = Venue.query.filter_by(id=venue_id).first()

    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        facebook_link = request.form.get('facebook_link')
        genres = request.form.get('genres')
        website_link = request.form.get('website_link')
        description = request.form.get('seeking_description')

        venue.name = name,
        venue.city = city,
        venue.state = state,
        venue.address = address,
        venue.phone = phone,
        venue.image_link = image_link,
        venue.facebook_link = facebook_link,
        venue.genres = genres,
        venue.website_link = website_link,
        venue.description = description

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash("An error occured Venue" +
              request.form['name'] + " could not be  edited! because of " + str(e))
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        facebook_link = request.form.get('facebook_link')
        genres = request.form.get('genres')
        website_link = request.form.get('website_link')
        seeking_venue = request.form.get('seeking_venue')
        description = request.form.get('seeking_description')

        artist = Artist(
            name=name,
            city=city,
            state=state,
            phone=phone,
            image_link=image_link,
            facebook_link=facebook_link,
            genres=genres,
            website_link=website_link,
            looking_for_venues=seeking_venue,
            description=description


        )
        db.session.add(artist)
        db.session.commit()

        flash('artst ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        flash("An error occured Artist" +
              request.form['name'] + " could not be  listed! because of " + str(e))
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    shows = Show.query.all()

    return render_template('pages/shows.html', shows=shows)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():

    try:
        artist_id = request.form.get('artist_id')
        venue_id = request.form.get('venue_id')
        start_time = request.form.get('start_time')

        show = Show(
            artist_id=artist_id,
            venue_id=venue_id,
            start_time=start_time
        )

        db.session.add(show)
        db.session.commit()

        # on successful db insert, flash success
        flash('Show was successfully listed!')

    except Exception as e:
        db.session.rollback()
        flash("Error occured")
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
# db.create_all()
# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
