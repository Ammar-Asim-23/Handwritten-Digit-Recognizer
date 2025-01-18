from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import base64

# Initialize the Flask app
app = Flask(__name__)

# Load the model
model = tf.keras.models.load_model('model.keras')

# Route to render the HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Route to predict digit
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    image_data = data['image']  # Base64-encoded image

    # Decode the image
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes)).convert('L').resize((28, 28))
    image_array = np.array(image) / 255.0
    image_array = image_array.reshape(1, 28, 28, 1)

    # Predict
    prediction = model.predict(image_array)
    predicted_digit = np.argmax(prediction)

    return jsonify({'digit': int(predicted_digit)})

if __name__ == '__main__':
    app.run(debug=True)
