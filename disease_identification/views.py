import os
import numpy as np
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.core.cache import cache 


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


MODEL_PATHS = {
    'rice': os.path.join(BASE_DIR, 'disease_identification/models', 'rice.h5'),
    'pumpkin': os.path.join(BASE_DIR, 'disease_identification/models', 'pumpkin.h5'),
    'potato': os.path.join(BASE_DIR, 'disease_identification/models', 'potato.h5')
}


DISEASE_LABELS = {
    'rice': ['Rice Blast', 'Bacterial Blight', 'Brown Spot'],  
    'pumpkin': ['Powdery Mildew', 'Downy Mildew'],
    'potato': ['Late Blight', 'Early Blight', 'Blackleg'] 
}

def load_model_based_on_crop(crop: str):
   
    model = cache.get(crop) 
    if model is None:
        model_path = MODEL_PATHS.get(crop)
        if model_path and os.path.exists(model_path):
            model = load_model(model_path)
            cache.set(crop, model)  
        else:
            raise ValueError(f"Model for {crop} not found!")
    return model

def disease_identification(request):
    if request.method == 'POST' and 'crop' in request.POST:
        crop = request.POST.get('crop')  
        uploaded_file = request.FILES.get('image') 

        if not uploaded_file:
            return render(request, 'upload.html', {'error': 'Please upload an image.'})

        temp_image_name = None
        try:
           
            temp_image_name = default_storage.save('temp.jpg', ContentFile(uploaded_file.read()))
            image_path = default_storage.path(temp_image_name) 

           
            model = load_model_based_on_crop(crop)

          
            img = image.load_img(image_path, target_size=(256, 256))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) / 255.0  

           
            predictions = model.predict(img_array)
            predicted_class_index = np.argmax(predictions, axis=1)[0]  # Get index of highest probability
            predicted_probabilities = dict(enumerate(predictions[0]))  # Prepare probabilities as a dictionary

          
            disease_labels = DISEASE_LABELS.get(crop, [])

            if not disease_labels:
                raise ValueError(f"No disease labels found for {crop}")

            # Map predicted class index to a class label
            predicted_class_label = disease_labels[predicted_class_index]  # Get the label for the predicted class

            # Return the predicted probabilities and class label to the frontend
            return render(request, 'result.html', {
                'predicted_classes': [predicted_class_label],  # Pass the label instead of index
                'predicted_probabilities': {disease_labels[i]: prob * 100 for i, prob in enumerate(predicted_probabilities.values())},  # Convert to percentages
                'crop': crop  # Pass the crop to the template for clarity
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
