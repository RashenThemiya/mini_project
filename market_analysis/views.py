from django.shortcuts import render
import os
from django.conf import settings
def index(request):
    return render(request, 'market_analysis.html')

from django.shortcuts import render

# Create your views here.
import joblib
from django.shortcuts import render
from .forms import PricePredictionForm
from .models import PricePrediction
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def train_and_predict(df, start_date, end_date, admin1, admin2, market, category, commodity, unit):
    # Ensure the 'models' directory exists
    model_dir = os.path.join(settings.BASE_DIR, 'models')
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Path to save the trained model
    model_path = os.path.join(model_dir, 'market_analysis.pkl')

    # Check if the model already exists
    if os.path.exists(model_path):
        try:
            # Load the saved model
            pipeline = joblib.load(model_path)
        except Exception as e:
            # Handle error if the model cannot be loaded
            print(f"Error loading the model: {e}")
            # Optionally, retrain the model if loading fails
            return []
    else:
        # Preprocess the data
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df = df.drop(columns=['date'])

        # Select features and target
        X = df[['admin1', 'admin2', 'market', 'category', 'commodity', 'unit', 'year', 'month', 'day']]
        y = df['price']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Preprocessing pipeline for categorical and numeric features
        categorical_features = ['admin1', 'admin2', 'market', 'category', 'commodity', 'unit']
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(), categorical_features),
                ('num', 'passthrough', ['year', 'month', 'day'])
            ]
        )

        # Define the model pipeline
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', RandomForestRegressor(n_estimators=100, random_state=42))
        ])

        # Train the model
        pipeline.fit(X_train, y_train)

        # Save the trained model for future use
        joblib.dump(pipeline, model_path)
    
    # Generate predictions for the input date range
    date_range = pd.date_range(start=start_date, end=end_date)
    predictions = []

    for date in date_range:
        year, month, day = date.year, date.month, date.day
        input_features = pd.DataFrame([[admin1, admin2, market, category, commodity, unit, year, month, day]],
                                      columns=['admin1', 'admin2', 'market', 'category', 'commodity', 'unit', 'year', 'month', 'day'])
        predicted_price = pipeline.predict(input_features)
        predictions.append((date.strftime('%Y-%m-%d'), predicted_price[0]))

    return predictions 
def predict_price_view(request):
    if request.method == 'POST':
        form = PricePredictionForm(request.POST)
        if form.is_valid():
            admin1 = form.cleaned_data['admin1']
            admin2 = form.cleaned_data['admin2']
            market = form.cleaned_data['market']
            category = form.cleaned_data['category']
            commodity = form.cleaned_data['commodity']
            unit = form.cleaned_data['unit']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']


            dataset_path = os.path.join(settings.BASE_DIR, 'dataset', 'dataset.csv')
            df = pd.read_csv(dataset_path)

            # Get predictions for each date
            predictions = train_and_predict(df,start_date, end_date, admin1, admin2, market, category, commodity, unit)

            # Save the result in the database
            for date, predicted_price in predictions:
                PricePrediction.objects.create(
                    admin1=admin1,
                    admin2=admin2,
                    market=market,
                    category=category,
                    commodity=commodity,
                    unit=unit,
                    start_date=date,
                    end_date=end_date,
                    predicted_price=predicted_price
                )

            return render(request, 'result.html', {'predictions': predictions})

    else:
        form = PricePredictionForm()

    return render(request, 'predict.html', {'form': form})

