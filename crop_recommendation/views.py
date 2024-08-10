from django.shortcuts import render
from django.http import JsonResponse
import joblib
from .forms import CropRecommendationForm
import os

# Determine the path to the model file
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'crop_recommendation_model.joblib')

# Load the model
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print("Error loading model:", e)
    model = None

def index(request):
    if request.method == "POST":
        form = CropRecommendationForm(request.POST)
        if form.is_valid():
            try:
                nitrogen = form.cleaned_data['nitrogen']
                phosphorus = form.cleaned_data['phosphorus']
                potassium = form.cleaned_data['potassium']
                temperature = form.cleaned_data['temperature']
                humidity = form.cleaned_data['humidity']
                ph = form.cleaned_data['ph']
                rainfall = form.cleaned_data['rainfall']

                # Prepare the data for prediction
                input_data = [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]]

                if model:
                    recommended_crop = model.predict(input_data)[0]  # Predict the crop
                    return JsonResponse({'recommended_crop': recommended_crop})
                else:
                    return JsonResponse({'error': 'Model could not be loaded'}, status=500)
            except Exception as e:
                print("Error during prediction:", e)
                return JsonResponse({'error': 'Prediction error: ' + str(e)}, status=500)
        else:
            print("Form validation errors:", form.errors)
            return JsonResponse({'error': 'Form is not valid', 'details': form.errors}, status=400)
    else:
        form = CropRecommendationForm()

    return render(request, 'crop_recommendation.html', {'form': form})
