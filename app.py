# Import necessary libraries and modules
from flask import Flask, render_template, request, redirect, url_for
from deepface import DeepFace
from PIL import Image, ExifTags
from datetime import datetime
from logging.handlers import RotatingFileHandler
import sentry_sdk

from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

import pyheif
import random
import os
import logging
import sqlite3

DATABASE = 'matches.db'

sentry_sdk.init(
    dsn="https://5f408ebe0451d9efe0c7c68924fa5ec8@o4505920028475392.ingest.sentry.io/4505920036470784",
    integrations=[FlaskIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

app.logger.addHandler(handler)

# Initialize Flask app
app = Flask(__name__)
# Set the upload folder for images
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Define categories for age, emotion, and race
CATEGORIES = {
    'age': {1: 'young', 2: 'adult', 3: 'old'},
    'emotion': {1: 'angry', 2: 'disgust', 3: 'fear', 4: 'happy', 5: 'sad', 6: 'surprise', 7: 'neutral'},
    'race': {1: 'asian', 2: 'black', 3: 'indian', 4: 'latino hispanic', 5: 'middle eastern', 6: 'white'}
}

# Define weights for each category
WEIGHTS = {'age': 0.35, 'emotion': 0.40, 'race': 0.25}

def setup_database():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        # Create the table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            datetime TEXT,
            human_age TEXT,
            human_emotion TEXT,
            human_race TEXT,
            human_photo_filepath TEXT,
            dog_age TEXT,
            dog_emotion TEXT,
            dog_race TEXT,
            dog_photo_filepath TEXT
        )
        ''')
        
        conn.commit()
        print("Database setup completed and 'matches' table is ready.")


def insert_into_database(data):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO matches (datetime, human_age, human_emotion, human_race, human_photo_filepath, dog_age, dog_emotion, dog_race, dog_photo_filepath)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)

        conn.commit()

# Function to extract attributes from DeepFace result
def extract_attributes(result):
    print(result)
    return (
        # Get index of age category based on age value
        list(CATEGORIES['age'].values()).index("young" if result["age"] <= 20 else ("adult" if result["age"] <= 50 else "old")) + 1,
        # Get index of dominant emotion category
        list(CATEGORIES['emotion'].values()).index(result['dominant_emotion']) + 1,
        # Get index of dominant race category
        list(CATEGORIES['race'].values()).index(result["dominant_race"]) + 1
    )

# Function to compare user's attributes with dogs' attributes
def compare(attributes, dogs):
    # Calculate similarities between user's attributes and dogs' attributes
    similarities = [
        (
            dog_id, 
            # Calculate the weighted sum of squared differences for each attribute
            sum(((dog[i] - attributes[i]) ** 2) * WEIGHTS[attr] for i, attr in enumerate(WEIGHTS))
        )
        for dog_id, dog in dogs.items()
    ]
    # Find the minimum similarity score
    min_score = min(similarities, key=lambda x: x[1])[1]
    print(min_score)
    # Return a random dog ID with the minimum similarity score
    return random.choice([dog_id for dog_id, score in similarities if score == min_score])

# Function to resize and compress an image from a given path


def correct_image_rotation(image):
    try:
        # Get the image's EXIF data
        exif = image._getexif()

        # If there's no EXIF data, return the image as it is
        if exif is None:
            return image

        # Check for the existence of the orientation tag
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        # Rotate the image according to the orientation tag value
        if exif[orientation] == 2:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        elif exif[orientation] == 3:
            image = image.rotate(180)
        elif exif[orientation] == 4:
            image = image.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
        elif exif[orientation] == 5:
            image = image.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
        elif exif[orientation] == 6:
            image = image.rotate(-90, expand=True)
        elif exif[orientation] == 7:
            image = image.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)

    except (AttributeError, KeyError, IndexError):
        # If there's an issue with the image's EXIF data or the orientation tag doesn't exist, return the image as it is
        pass

    return image

def resize_image_to_long_side(img, target_long_side=1024):
    # Get the image dimensions
    width, height = img.size

    # Determine the scaling factor based on the long side
    if width > height:
        scaling_factor = target_long_side / width
    else:
        scaling_factor = target_long_side / height

    # Calculate the new dimensions
    new_width = int(width * scaling_factor)
    new_height = int(height * scaling_factor)

    # Resize the image using LANCZOS filter
    return img.resize((new_width, new_height), Image.LANCZOS)

def resize_and_compress_image_from_path_updated(image_path):
    # Check if the image is in .heic format
    if image_path.lower().endswith(".heic"):
        heif_file = pyheif.read(image_path)
        img = Image.frombytes(
            heif_file.mode, 
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
    else:
        # Open the image with Pillow
        img = Image.open(image_path)

    # Correct the image orientation based on its EXIF data
    img = correct_image_rotation(img)

    # Resize the image if its long side is more than 1024
    if max(img.size) > 1024:
        img = resize_image_to_long_side(img)

    # Save the image with compression
    img.save(image_path, "JPEG", quality=75)


# Function to generate a new filename for an image based on the current timestamp
def generate_new_filename(image_path):
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Produces format like "20230913170550"
    
    # Use the timestamp to generate the new filename
    new_filename = f"{timestamp}.jpg"
    
    return new_filename

# Define the index route for the Flask app

@app.route('/debug-sentry')
def trigger_error():
  division_by_zero = 1 / 0

@app.route('/colabora')
def colabora():
    return render_template('colabora.html')

@app.route('/galeria')
def galeria():
    return render_template('perros-en-adopcion.html')

@app.route('/requisitos')
def requisitos():
    return render_template('requisitos.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/vermas')
def vermas():
    return render_template('vermas.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    app.logger.info('Upload endpoint hit')

    # Check if the request method is POST
    if request.method == 'POST':

        app.logger.info('Processing POST request')
        # Check if there's no file in the request or if the filename is empty
        if 'file' not in request.files or request.files['file'].filename == '':
            app.logger.warning('No file part in request or filename is empty')
            return redirect(request.url)

        # Get the uploaded file from the request
        file = request.files['file']
        # Save the file to the upload folder with its original filename
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        app.logger.info(f'File saved as {filename}')

        # Resize and compress the saved image
        resize_and_compress_image_from_path_updated(filename)
        app.logger.info(f'File resized and compressed: {filename}')

        # Generate a new filename
        new_filename = generate_new_filename(filename)
        new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

        # Rename the file
        os.rename(filename, new_filepath)

        app.logger.info(f'File renamed to {new_filepath}')

        # Try analyzing the image with face detection enforced
        try:
            result = DeepFace.analyze(new_filepath, enforce_detection=True)
        except ValueError as e:
            app.logger.error(f"Face detection error: {str(e)}")# Here, we're sending the error_face_detection flag to the template
            return render_template('upload.html', error_face_detection=True)

        # Define the dogs data (ID, attributes, name, description)
        dogs = {
            1: (2, 4, 2, 'Chabella', 'Un año y medio. Castrada. Fue abandonada en el portón del refugio cuando era cachorra. Busca hogar donde la llenen de mimos y amor.'),
            2: (2, 2, 5, 'Polo', 'Es adulto jóven y está castrado. 50% fila, 50% gran danés. 100% cariñoso.'),
            3: (2, 7, 4, 'Colita', 'Huérfano. Su dueño falleció y buscaban eutanaziarlo. Pero logramos salvarlo. Está castrado, es tímido pero tiene un corazón de oro. Es el perro más bueno del refugio.'),
            4: (2, 1, 2, 'Barby', 'Lo que tiene de rescatado lo tiene de amoroso. Es un perro muy alegre y juguetón.'),
            5: (2, 7, 5, 'Rubia', 'Castrada. Es una perra tímida pero extremadamente cariñosa. Es guardiana y muy mimosa.'),
            6: (1, 4, 2, 'Panther', 'Jóven cruza con labrador. Amorosa, sociable y cariñosa; la opción perfecta para cualquier hogar que quiera dar amor.'),
            7: (1, 6, 4, 'Chocolate', 'Anciana castrada. Es muy amorosa, tierna y mimosa.'),
            8: (1, 4, 3, 'Tigresa', 'Cachorra de 6 meses, próxima a ser castrada. Juguetona, mimosa y buena, va a ser una perra de tamaño mediano pero con un corazón enorme.'),
            9: (3, 1, 4, 'Yessy', 'Cuando llegó al refugio tenía la columna fracturada. Hoy en día está castrada y recuperada. Amorosa y tierna.'),
            10: (2, 5, 4, 'Lobita', 'Fue rescatada con una fractura en su columna. Luego de 6 meses luchando, volvió a caminar. Castrada, cariñosa y amante de estar dentro de casa.'),
            11: (3, 7, 4, 'Milly', 'Jóven, castrada. Es cruza con weimeraner. Mediana, amorosa y cariñosa con todos, menos con los gatos.'),
            12: (1, 4, 4, 'Slowy', 'Macho, muy guardián. Es bueno, amigable y de tamaño mediano.'),
            13: (2, 7, 4, 'Dexter', 'Cachorro, 4 meses. Es cariñoso a niveles extremos. El más bueno de todos.'),
            14: (1, 4, 2, 'Preto', 'Castrado, cruza con pitbull. Tuvo un accidente y perdió un brazo. Mimoso pero garronero con quienes no conoce.'),
            15: (2, 5, 1, 'Mi nena', 'Rescatada de cachorra, castrada. Le encanta dar besos y jugar. Súper cariñosa.'),
            16: (1, 4, 6, 'Rubia', 'Cachorra, próxima a ser castrada. Muy cariñosa e ingeniosa. Le encantan las siestas al sol.'),
            17: (2, 6, 6, 'Galy', 'Galga, castrada. Es una perra muy tímida y miedosa, tuvo un pasado difícil pero hoy en día tiene muchísimo amor para dar. Es buena, dulce y compañera.'),
            18: (1, 4, 4, 'Guismu', 'Cachorro macho, dos meses y medio. Es muy tímido, muy dulce y muy amoroso. Y es cruza con shitzu.'),
            19: (1, 4, 6, 'Aaron', '3 meses. Va a ser un perro grande. Es muy juguetón y mimoso. Le gusta estár a upa.'),
            20: (2, 7, 6, 'Kala', 'Galga, abandonada. Fue abandonada en el portón con un cable en la garganta. Camina, pero no corre por distensión en sus patitas traseras. Es muy cariñosa, juguetona y dulce.')
            }
        
        attributes = extract_attributes(result[0])
        app.logger.info(f'Extracted attributes: {attributes}')

        most_similar_dog_id = compare(attributes, dogs)
        app.logger.info(f'Most similar dog ID: {most_similar_dog_id}')

        most_similar_dog = dogs[most_similar_dog_id]
        app.logger.info(f'Most similar dog data: {most_similar_dog}')

        #SQLite
        
        data_to_insert = (

            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Current datetime
            CATEGORIES['age'][attributes[0]],  # Human Age
            CATEGORIES['emotion'][attributes[1]],  # Human Emotion
            CATEGORIES['race'][attributes[2]],  # Human Race
            new_filepath,  # Human Photo filepath
            CATEGORIES['age'][most_similar_dog[0]],  # Dog Age
            CATEGORIES['emotion'][most_similar_dog[1]],  # Dog Emotion
            CATEGORIES['race'][most_similar_dog[2]],  # Dog Race
            f'static/perritos/{most_similar_dog_id}.jpg'  # Dog photo filepath
        )

        insert_into_database(data_to_insert)

        # Render the result template with the uploaded image URL, dog image URL, dog name, and dog description
        return render_template(
            'resultado.html', 
            uploaded_img_url=url_for('static', filename=f'uploads/{new_filename}'),
            dog_img_url=url_for('static', filename=f'perritos/{most_similar_dog_id}.jpg'),
            dog_name=most_similar_dog[3], 
            dog_description=most_similar_dog[4]
        )

    app.logger.info('Rendering upload template')
    return render_template('upload.html')

# Run the Flask app
if __name__ == '__main__':
    setup_database()
    app.run(debug=False)    