from flask import Flask, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from PIL import Image, ImageFilter
import requests
import uuid
import io
import datetime

from config import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class HistoryEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String(25))
    processed_image = db.Column(db.String(50))
    created = db.Column(db.DateTime)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'animal_type': self.animal_type,
            'processed_image': self.processed_image,
            'created': self.created
        }


def save_event(animal_type, filename):
    """Create class instance of HistoryEvent and add it to database"""
    event = HistoryEvent(
        animal_type=animal_type,
        processed_image=filename,
        created=datetime.datetime.now()
    )
    db.session.add(event)
    db.session.commit()


def process_image(path_to_image, image_binary, filter):
    """Process given image in binary format using a filter and save"""
    image = Image.open(io.BytesIO(image_binary))
    image = image.convert('RGB')
    processed_image = image.filter(filter)
    processed_image.save(path_to_image)


@app.route('/animal/cat')
def get_cat_image():
    try:
        request = requests.get('https://api.thecatapi.com/v1/images/search',
                               headers={
                                   'x-api-key': '0daca2c3-8485-4cad-b554-17c58ca39f51'
                               })
    except requests.ConnectionError as err:
        print(err)
        return CONNECTION_ERROR_MESSAGE
    image_url = request.json()[0]['url']
    image_binary = requests.get(image_url).content
    filename = str(uuid.uuid4()) + IMAGE_FORMAT
    path_to_image = PATH_TO_IMAGES + filename
    process_image(path_to_image, image_binary, ImageFilter.DETAIL)
    save_event('cat', filename)
    return send_file(path_to_image, mimetype='image/gif')


@app.route('/animal/dog')
def get_dog_image():
    try:
        request = requests.get('http://shibe.online/api/shibes',
                               params={'count': 1})
    except requests.ConnectionError as err:
        print(err)
        return CONNECTION_ERROR_MESSAGE
    image_url = request.json()[0]
    image_binary = requests.get(image_url).content
    filename = str(uuid.uuid4()) + IMAGE_FORMAT
    path_to_image = PATH_TO_IMAGES + filename
    process_image(path_to_image, image_binary, ImageFilter.SHARPEN)
    save_event('dog', filename)
    return send_file(path_to_image, mimetype='image/gif')


@app.route('/animal/fox')
def get_fox_image():
    try:
        request = requests.get('https://randomfox.ca/floof/')
    except requests.ConnectionError as err:
        print(err)
        return CONNECTION_ERROR_MESSAGE
    image_url = request.json()['image']
    image_binary = requests.get(image_url).content
    filename = str(uuid.uuid4()) + IMAGE_FORMAT
    path_to_image = PATH_TO_IMAGES + filename
    process_image(path_to_image, image_binary, ImageFilter.BLUR)
    save_event('fox', filename)
    return send_file(path_to_image, mimetype='image/gif')


@app.route('/history')
def get_history():
    events = HistoryEvent.query.all()
    return jsonify([event.serialize for event in events])


@app.route('/history/static/<uuid:id>')
def get_image_from_history(id):
    filename = str(id) + IMAGE_FORMAT
    path_to_image = PATH_TO_IMAGES + filename
    try:
        return send_file(path_to_image, mimetype='image/gif')
    except FileNotFoundError as err:
        print(err)
        return FILE_NOT_FOUND_MESSAGE


if __name__ == "__main__":
    db.create_all()
    app.run(debug=False)
