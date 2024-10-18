import os
import numpy as np
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.core.cache import cache  # Added for model caching

# Define the base directory of your Django project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths to the models using absolute paths
MODEL_PATHS = {
    'rice': os.path.join(BASE_DIR, 'disease_identification/models', 'rice.h5'),
    'pumpkin': os.path.join(BASE_DIR, 'disease_identification/models', 'pumkin.h5'),
    'potato': os.path.join(BASE_DIR, 'disease_identification/models', 'potato.h5')
}

def load_model_based_on_crop(crop: str):
    """
    Loads the model based on the selected crop, with caching for performance.
    """
    model = cache.get(crop)  # Try to retrieve the model from cache
    if model is None:
        model_path = MODEL_PATHS.get(crop)
        if model_path and os.path.exists(model_path):
            model = load_model(model_path)
            cache.set(crop, model)  # Cache the model after loading it
        else:
            raise ValueError(f"Model for {crop} not found!")
    return model

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

            # Load and preprocess the image
            img = image.load_img(image_path, target_size=(256, 256))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize the image

            # Make prediction
            predictions = model.predict(img_array)
            predicted_classes = np.argmax(predictions, axis=1)
            predicted_probabilities = dict(enumerate(predictions[0]))  # Prepare probabilities as a dictionary

            # Return the predicted probabilities and classes to the frontend
            return render(request, 'result.html', {
                'predicted_classes': predicted_classes,
                'predicted_probabilities': predicted_probabilities,
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
