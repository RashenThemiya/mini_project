from django import forms
import os
import pandas as pd
from django.conf import settings

# Load the dataset and extract unique values
dataset_path = os.path.join(settings.BASE_DIR, 'dataset', 'dataset.csv')
df = pd.read_csv(dataset_path)

admin1_choices = [(value, value) for value in df['admin1'].unique()]
admin2_choices = [(value, value) for value in df['admin2'].unique()]
market_choices = [(value, value) for value in df['market'].unique()]
category_choices = [(value, value) for value in df['category'].unique()]
commodity_choices = [(value, value) for value in df['commodity'].unique()]
unit_choices = [(value, value) for value in df['unit'].unique()]

class PricePredictionForm(forms.Form):
    admin1 = forms.ChoiceField(label='Admin1', choices=admin1_choices)
    admin2 = forms.ChoiceField(label='Admin2', choices=admin2_choices)
    market = forms.ChoiceField(label='Market', choices=market_choices)
    category = forms.ChoiceField(label='Category', choices=category_choices)
    commodity = forms.ChoiceField(label='Commodity', choices=commodity_choices)
    unit = forms.ChoiceField(label='Unit', choices=unit_choices)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
