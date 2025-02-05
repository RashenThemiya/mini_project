from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from crop_recommendation.forms import CropRecommendationForm

class CropRecommendationViewTest(TestCase):

    def setUp(self):
        # Valid data for testing form submission
        self.valid_data = {
            'nitrogen': 50,
            'phosphorus': 30,
            'potassium': 20,
            'temperature': 25.5,
            'humidity': 80.0,
            'ph': 6.5,
            'rainfall': 100.0
        }
        # Invalid data with missing nitrogen value
        self.invalid_data = {
            'nitrogen': '',  # Missing required field
            'phosphorus': 30,
            'potassium': 20,
            'temperature': 25.5,
            'humidity': 80.0,
            'ph': 6.5,
            'rainfall': 100.0
        }

    @patch("crop_recommendation.views.model")  # Mock the model to avoid real loading
    def test_valid_form_submission(self, mock_model):
        """Test if valid form data returns a crop recommendation."""
        # Mock the prediction result to return 'Wheat'
        mock_model.predict.return_value = ["Wheat"]

        # Simulate a POST request with valid data
        response = self.client.post(reverse("crop_recommendation_index"), self.valid_data)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the response contains the expected recommended crop
        self.assertEqual(response.json(), {'recommended_crop': 'Wheat'})

    def test_invalid_form_submission(self):
        """Test if invalid form data returns an error response."""
        # Simulate a POST request with invalid data (missing nitrogen)
        response = self.client.post(reverse("crop_recommendation_index"), self.invalid_data)

        # Check if the response status is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)
        # Check if the response contains form validation errors
        self.assertIn("nitrogen", response.json()['details'])

    @patch("crop_recommendation.views.model", None)  # Simulate model loading failure
    def test_model_not_loaded(self, mock_model):
        """Test if an error is returned when the model fails to load."""
        # Simulate a POST request with valid data
        response = self.client.post(reverse("crop_recommendation_index"), self.valid_data)

        # Check if the response status is 500 (Internal Server Error)
        self.assertEqual(response.status_code, 500)
        # Check if the response contains the expected error message
        self.assertEqual(response.json(), {'error': 'Model could not be loaded'})

    @patch("crop_recommendation.views.model")  # Mock the model to avoid real loading
    def test_prediction_error_handling(self, mock_model):
        """Test if an exception during prediction is handled properly."""
        # Simulate an error during prediction
        mock_model.predict.side_effect = Exception("Mock Prediction Error")

        # Simulate a POST request with valid data
        response = self.client.post(reverse("crop_recommendation_index"), self.valid_data)

        # Check if the response status is 500 (Internal Server Error)
        self.assertEqual(response.status_code, 500)
        # Check if the response contains the expected error message
        self.assertEqual(response.json(), {'error': 'Prediction error: Mock Prediction Error'})
