from django.test import TestCase
from django.urls import reverse
from .models import PricePrediction
from .forms import PricePredictionForm
from datetime import datetime
import pandas as pd
import os
from django.conf import settings


class MarketAnalysisTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up any initial data for the tests
        cls.dataset_path = os.path.join(settings.BASE_DIR, 'dataset', 'dataset.csv')
        cls.df = pd.read_csv(cls.dataset_path)
        
        # Add some test data to the database
        PricePrediction.objects.create(
            admin1="TestAdmin1",
            admin2="TestAdmin2",
            market="TestMarket",
            category="TestCategory",
            commodity="TestCommodity",
            unit="kg",
            start_date=datetime(2025, 1, 1),
            end_date=datetime(2025, 1, 2),
            predicted_price=100.0
        )

    def test_price_prediction_form_valid(self):
        # Test if the form is valid
        form_data = {
            'admin1': 'TestAdmin1',
            'admin2': 'TestAdmin2',
            'market': 'TestMarket',
            'category': 'TestCategory',
            'commodity': 'TestCommodity',
            'unit': 'kg',
            'start_date': '2025-01-01',
            'end_date': '2025-01-02',
        }
        form = PricePredictionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_price_prediction_view_get(self):
        # Test if the view renders the correct template
        response = self.client.get(reverse('market_analysis_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'predict.html')

    def test_price_prediction_view_post(self):
        # Test if the view handles POST request and renders the correct template
        form_data = {
            'admin1': 'TestAdmin1',
            'admin2': 'TestAdmin2',
            'market': 'TestMarket',
            'category': 'TestCategory',
            'commodity': 'TestCommodity',
            'unit': 'kg',
            'start_date': '2025-01-01',
            'end_date': '2025-01-02',
        }
        response = self.client.post(reverse('predict_price'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resulte.html')

    def test_model_loading(self):
        # Test if the model is being loaded and predictions are generated
        dataset_path = os.path.join(settings.BASE_DIR, 'dataset', 'dataset.csv')
        df = pd.read_csv(dataset_path)
        predictions = self.train_and_predict(df, '2025-01-01', '2025-01-02', 'TestAdmin1', 'TestAdmin2', 'TestMarket', 'TestCategory', 'TestCommodity', 'kg')
        self.assertIsInstance(predictions, list)
        self.assertGreater(len(predictions), 0)

    def test_prediction_saved_in_db(self):
        # Test if the predictions are being saved in the database
        form_data = {
            'admin1': 'TestAdmin1',
            'admin2': 'TestAdmin2',
            'market': 'TestMarket',
            'category': 'TestCategory',
            'commodity': 'TestCommodity',
            'unit': 'kg',
            'start_date': '2025-01-01',
            'end_date': '2025-01-02',
        }
        self.client.post(reverse('predict_price'), form_data)
        predictions = PricePrediction.objects.all()
        self.assertEqual(predictions.count(), 1)

    def test_graph_generation(self):
        # Test if the graph is being generated in the response
        form_data = {
            'admin1': 'TestAdmin1',
            'admin2': 'TestAdmin2',
            'market': 'TestMarket',
            'category': 'TestCategory',
            'commodity': 'TestCommodity',
            'unit': 'kg',
            'start_date': '2025-01-01',
            'end_date': '2025-01-02',
        }
        response = self.client.post(reverse('predict_price'), form_data)
        self.assertIn('graph_url', response.context)

    def train_and_predict(self, df, start_date, end_date, admin1, admin2, market, category, commodity, unit):
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler, OneHotEncoder
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline

        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df = df.drop(columns=['date'])

        X = df[['admin1', 'admin2', 'market', 'category', 'commodity', 'unit', 'year', 'month', 'day']]
        y = df['price']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        categorical_features = ['admin1', 'admin2', 'market', 'category', 'commodity', 'unit']
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(), categorical_features),
                ('num', 'passthrough', ['year', 'month', 'day'])
            ]
        )

        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', RandomForestRegressor(n_estimators=100, random_state=42))
        ])

        pipeline.fit(X_train, y_train)

        date_range = pd.date_range(start=start_date, end=end_date)
        predictions = []

        for date in date_range:
            year, month, day = date.year, date.month, date.day
            input_features = pd.DataFrame([[admin1, admin2, market, category, commodity, unit, year, month, day]],
                                          columns=['admin1', 'admin2', 'market', 'category', 'commodity', 'unit', 'year', 'month', 'day'])
            predicted_price = pipeline.predict(input_features)
            predictions.append((date.strftime('%Y-%m-%d'), predicted_price[0]))

        return predictions
