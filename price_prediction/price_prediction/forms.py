from django import forms

class PricePredictionForm(forms.Form):
    admin1 = forms.CharField(label='Admin1', max_length=100)
    admin2 = forms.CharField(label='Admin2', max_length=100)
    market = forms.CharField(label='Market', max_length=100)
    category = forms.CharField(label='Category', max_length=100)
    commodity = forms.CharField(label='Commodity', max_length=100)
    unit = forms.CharField(label='Unit', max_length=50)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
