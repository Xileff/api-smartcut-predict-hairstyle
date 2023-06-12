import cv2
import numpy as np
from tensorflow.keras.models import load_model
from flask import Flask, request, jsonify
from flask_cors import CORS
from nanoid import generate
from dotenv import load_dotenv
import os
import random
from google.cloud import storage

load_dotenv()

app = Flask(__name__)
storage_client = storage.Client.from_service_account_json(os.getenv('CLOUD_STORAGE_KEY'))
bucket = storage_client.bucket(os.getenv('BUCKET_NAME'))
model = load_model(os.getenv('MODEL_PATH'))

CORS(app)

def predict(image_path):
    # Load and preprocess the input image
    input_image = cv2.imread(image_path)
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    input_image = cv2.resize(input_image, (224, 224))  # Assuming your model expects input images of size 224x224
    input_image = input_image.astype('float32') / 255.0
    input_image = np.expand_dims(input_image, axis=0)

    # Perform face shape classification
    face_shape = model.predict(input_image)
    face_shape = np.argmax(face_shape)

    # Define the face shape labels
    face_shape_labels = ['Diamond', 'Oval', 'Square', 'Heart', 'Round', 'Oblong', 'Triangle']

    # Print the predicted face shape
    return face_shape_labels[face_shape]


@app.route("/detect-model", methods=["POST"])
def process_image():
    # Get the image from request
    file = request.files.get('image', default=None)
    if file is None:
        return jsonify({'status': 'fail', 'message': 'Image is required'}), 400
    image_path = os.getenv('IMAGE_DIR') + generate(size=16) + '.jpg'
    file.save(image_path)

    # Prediction
    face_type = predict(image_path)
    
    # Give 5 hairstyle reccomendations according to face type
    blobs = bucket.list_blobs(prefix=os.getenv('FACE_SHAPES_PATH') + '/' + face_type)
    blobs_list = list(blobs)
    files_count = len(blobs_list)
    
    reccomendations = []
    for _ in range(5):
        random_num = random.randint(0, files_count)
        reccomendation = blobs_list[random_num].public_url
        reccomendations.append(reccomendation)


    return jsonify({
        'status': 'success', 
        'data': {
            'faceType': face_type, 
            'reccomendations': reccomendations,
        }
    }), 201

if __name__ == "__main__":
    app.run(host='localhost',port=8080,debug=True)