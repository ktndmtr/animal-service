# Animal service

## Start the app

To build the project locally follow the next steps:

1. Clone the repository by tipying in a terminal `$ git clone https://github.com/ktndmtr/animal-service.git`
2. After cloning the repository you can install the required packages with: `$ pip install -r /path/to/requirements.txt`. (I recomend to install everything in a virtual environment.)
3. `cd` to `animal-service` and `$ mkdir images`.
4. Run `$ python app.py` and visit `http://127.0.0.1:5000/`

## Usage

The web service can respond to five requests for links:

- /animal/cat
- /animal/dog
- /animal/fox
- /history
- /history/static/\<uuid\>
