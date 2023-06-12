import os
import random
from tensorflow.keras.models import load_model
import cv2
import numpy as np
from google.cloud import storage
from flask import Flask, request, make_response
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
from nanoid import generate
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")
TEMP_IMAGE_DIR = os.getenv("TEMP_IMAGE_DIR")
CLOUD_STORAGE_KEY = os.getenv("CLOUD_STORAGE_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")
FACE_SHAPES_PATH = os.getenv("FACE_SHAPES_PATH")

storage_client = storage.Client.from_service_account_json(CLOUD_STORAGE_KEY)
bucket = storage_client.bucket(BUCKET_NAME)
model = load_model(MODEL_PATH)

app = Flask(__name__)

CORS(app)


def predict(image_path):
    # Load and preprocess the input image
    input_image = cv2.imread(image_path)
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    input_image = cv2.resize(input_image, (224, 224))
    input_image = input_image.astype("float32") / 255.0
    input_image = np.expand_dims(input_image, axis=0)

    # Perform face shape classification
    face_shape = model.predict(input_image)
    face_shape = np.argmax(face_shape)

    # Define the face shape labels
    face_shape_labels = [
        "Diamond",
        "Oval",
        "Square",
        "Heart",
        "Round",
        "Oblong",
        "Triangle",
    ]

    # Return the predicted face shape
    return face_shape_labels[face_shape]


@app.route("/detect-model", methods=["POST"])
def process_image():
    # Temporarily store the image from request
    file = request.files.get("image", default=None)
    if file is None:
        return make_response({"status": "fail", "message": "Image is required"}, 400)

    file_ext = file.filename.split(".")[-1]
    if file_ext not in ["jpg", "jpeg", "png"]:
        raise BadRequest("Image format must be jpg or jpeg or png")

    image_path = TEMP_IMAGE_DIR + generate(size=16) + "." + file_ext
    file.save(image_path)

    # Prediction
    face_type = predict(image_path)

    # Give 5 hairstyle reccomendations according to face type
    blobs = bucket.list_blobs(prefix=FACE_SHAPES_PATH + "/" + face_type)
    images_list = list(blobs)

    reccomendations = []
    for _ in range(5):
        n = random.randint(0, len(images_list) - 1)
        url = images_list[n].public_url
        reccomendations.append(url)

    # Remove the temporarily stored image from request
    os.remove(image_path)

    return make_response(
        {
            "status": "success",
            "data": {
                "reccomendations": reccomendations,
            },
        },
        201,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
