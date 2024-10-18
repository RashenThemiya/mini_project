from django import forms

class CropRecommendationForm(forms.Form):
    nitrogen = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phosphorus = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    potassium = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    temperature = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    humidity = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    ph = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    rainfall = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
