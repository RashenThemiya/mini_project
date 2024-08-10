# crop_recommendation/forms.py
from django import forms

class CropRecommendationForm(forms.Form):
    nitrogen = forms.FloatField(label="Nitrogen (N)")
    phosphorus = forms.FloatField(label="Phosphorus (P)")
    potassium = forms.FloatField(label="Potassium (K)")
    temperature = forms.FloatField(label="Temperature (°C)")
    humidity = forms.FloatField(label="Humidity (%)")
    ph = forms.FloatField(label="pH")
    rainfall = forms.FloatField(label="Rainfall (mm)")
