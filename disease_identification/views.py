import os
import numpy as np
import tensorflow as tf
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
from tensorflow import keras
import cv2
from .disease_description import DISEASE_DESCRIPTIONS
from django.conf import settings
# Define the base directory of your Django project

model_dir = os.path.join(settings.BASE_DIR, 'models')
# Paths to the models using absolute paths (dynamic handling for .keras models)
MODEL_PATHS = {
    'rice': os.path.join(model_dir, 'rice.keras'),
    'pumpkin': os.path.join(model_dir, 'pumpkin.keras'),
    'potato': os.path.join(model_dir, 'potato.keras')
}
print("Checking file:", os.path.exists(MODEL_PATHS['rice']))  # Check if the file exists
# Dictionary mapping each crop to the diseases that its model predicts
DISEASE_LABELS = {
    'rice': ['Bacterial blight', 'Brown spot', 'Leafsmut'],
    'pumpkin': ['Powdery Mildew', 'Downy Mildew'],
    'potato': ['Early_blight', 'Late_blight', 'Healthy']
}

def load_model_based_on_crop(crop: str):
    model_path = MODEL_PATHS.get(crop)
    
    print(f"🔍 Checking model path: {model_path}")  # Debugging line
    
    if not model_path:
        raise ValueError(f"🚨 No model path found for {crop} in MODEL_PATHS dictionary!")

    if not os.path.exists(model_path):
        raise ValueError(f"🚨 Model file not found at: {model_path}. Check if the file exists!")

    # If the file exists, try loading the model
    model = keras.models.load_model(model_path)
    return model

def preprocess_image(image_path):
    """
    Preprocess the image by resizing and normalizing it.
    """
    image = cv2.imread(image_path)
    IMAGE_SIZE = (256, 256)
    resized_image = tf.image.resize(image, IMAGE_SIZE)
    scaled_image = resized_image / 255.0  # Normalize the image to [0, 1] range
    return np.expand_dims(scaled_image, axis=0)

def disease_identification(request):
    if request.method == 'POST' and 'crop' in request.POST:
        crop = request.POST.get('crop')  # Get selected crop
        uploaded_file = request.FILES.get('image')  # Get the uploaded image

        if not uploaded_file:
            return render(request, 'upload.html', {'error': 'Please upload an image.'})

        temp_image_name = None
        try:
            # Save the uploaded image to a temporary file
            temp_image_name = default_storage.save('temp.jpg', ContentFile(uploaded_file.read()))
            image_path = default_storage.path(temp_image_name)  # Get the full path to the saved file

            # Load the relevant model based on the crop
            model = load_model_based_on_crop(crop)

            # Preprocess the image
            preprocessed_image = preprocess_image(image_path)

            # Make prediction
            predictions = model.predict(preprocessed_image)
            predicted_class_index = np.argmax(predictions, axis=1)[0]  # Get index of highest probability

            # Retrieve the disease labels for the selected crop
            disease_labels = DISEASE_LABELS.get(crop, [])

            if not disease_labels:
                raise ValueError(f"No disease labels found for {crop}")

            # Map predicted class index to a class label
            detected_disease = disease_labels[predicted_class_index]
            prediction_probability = predictions[0][predicted_class_index] * 100

            # If probability is less than 75%, ask for clearer image
            if prediction_probability < 50:
                return render(request, 'upload.html', {
                    'error': 'Prediction confidence is too low. Please upload a clearer image.'
                })

            # Get disease description if not healthy
            description = DISEASE_DESCRIPTIONS.get(detected_disease, 'No description available.')

            # Return the detected disease and prediction probabilities to the frontend
            return render(request, 'result.html', {
                'predicted_classes': [detected_disease],
                'predicted_probabilities': {disease_labels[i]: prob * 100 for i, prob in enumerate(predictions[0])},
                'crop': crop,
                'description': description if detected_disease != 'Healthy' else None
            })

        except Exception as e:
            # Handle any exceptions and log them
            import logging
            logging.error(f"Error processing image: {e}")
            return render(request, 'upload.html', {'error': str(e)})

        finally:
            # Delete the temporary image after processing
            if temp_image_name:
                default_storage.delete(temp_image_name)

    # If GET request, return the upload form
    return render(request, 'upload.html')
