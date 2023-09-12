from flask import Flask, render_template, request, redirect, url_for
from deepface import DeepFace
import os

# Initialize Flask app
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

AGE_CATEGORIES = {
    1: 'young',
    2: 'adult',
    3: 'old'
}

EMOTION_CATEGORIES = {
    1: 'angry',
    2: 'disgust',
    3: 'fear',
    4: 'happy',
    5: 'sad',
    6: 'surprise',
    7: 'neutral'
}

RACE_CATEGORIES = {
    1: 'asian',
    2: 'black',
    3: 'indian',
    4: 'latino hispanic',
    5: 'middle eastern',
    6: 'white'
}

# Dictionary of dogs
dogs = {
    1: (2, 7, 6),
    2: (2, 2, 3),
    3: (1, 5, 2),
    4: (2, 6, 5),
    5: (1, 4, 4),
    6: (3, 5, 2),
    7: (2, 7, 4),
    8: (2, 2, 2),
    9: (3, 5, 1),
    10: (2, 7, 5),
    11: (3, 1, 4),
    12: (1, 7, 2),
    13: (2, 4, 5),
    14: (2, 7, 4),
    15: (3, 5, 3),
    16: (1, 4, 2),
    17: (2, 3, 4),
    18: (2, 5, 6),
    19: (1, 4, 4),
    20: (2, 7, 4),
    21: (1, 4, 4),
    22: (2, 7, 4)
}

def extract_attributes_from_analysis(result):
    """Extract dominant emotion, age, and race from the analysis result."""
    dominant_emotion = result["dominant_emotion"]
    dominant_age = "young" if result["age"] <= 20 else ("adult" if result["age"] <= 50 else "old")
    dominant_race = result["dominant_race"]
    
    emotion_index = list(EMOTION_CATEGORIES.values()).index(dominant_emotion) + 1
    age_index = list(AGE_CATEGORIES.values()).index(dominant_age) + 1
    race_index = list(RACE_CATEGORIES.values()).index(dominant_race) + 1
    
    return (age_index, emotion_index, race_index)

def compare_dogs_to_analysis(attributes):
    """Compare given attributes to each dog and find the most similar dog."""
    similarities = []
    for dog_id, dog in dogs.items():
        score = sum([(dog[i] - attributes[i]) ** 2 for i in range(3)])
        similarities.append((dog_id, score))
    
    # Return the dog_id with the minimum score
    most_similar_dog_id, _ = min(similarities, key=lambda x: x[1])
    return most_similar_dog_id

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle image upload and show the most similar dog."""
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            result = DeepFace.analyze(filename)
            attributes = extract_attributes_from_analysis(result[0])
            most_similar_dog_id = compare_dogs_to_analysis(attributes)
            
            uploaded_img_url = url_for('static', filename=f'uploads/{file.filename}')
            dog_img_url = url_for('static', filename=f'perritos/{most_similar_dog_id}.jpg')

            return render_template('resultado.html', uploaded_img_url=uploaded_img_url, dog_img_url=dog_img_url)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
