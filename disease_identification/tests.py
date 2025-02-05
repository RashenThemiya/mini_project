import requests
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
import os
from io import BytesIO

class DiseaseIdentificationTestCase(TestCase):

    def setUp(self):
        # Set up a test user with email as required by the custom user model
        self.user = get_user_model().objects.create_user(
            username='testuser', 
            email='testuser@example.com',  # Ensure email is provided
            password='testpassword'
        )

        # Image URL for testing
        self.image_url = "https://i0.wp.com/geopard.tech/wp-content/uploads/2021/12/Crop-Diseases_-Types-Causes-and-Symptoms-2-min.jpg?resize=810%2C439&ssl=1"

        # Login the user before testing views
        self.client.login(username='testuser', password='testpassword')

    def download_image(self, url):
        """
        Helper function to download an image from a URL and return it as a SimpleUploadedFile.
        """
        response = requests.get(url)
        if response.status_code == 200:
            return SimpleUploadedFile("test_image.jpg", response.content, content_type="image/jpeg")
        else:
            raise ValueError(f"Unable to download image. Status code: {response.status_code}")

    def test_disease_identification_form_get(self):
        """
        Test that the disease identification form is rendered correctly.
        """
        response = self.client.get(reverse('disease_identification_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crop')
        self.assertContains(response, 'Upload Image')

    def test_disease_identification_post_valid_image(self):
        """
        Test POST request with valid crop and online image.
        """
        uploaded_image = self.download_image(self.image_url)  # Download the image from URL

        response = self.client.post(reverse('disease_identification_index'), {
            'crop': 'rice',
            'image': uploaded_image
        })

        # Check if response is successful and contains prediction result
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Predicted Classes')  # Assuming you display classes in result template

    def test_disease_identification_post_no_image(self):
        """
        Test POST request without an image.
        """
        response = self.client.post(reverse('disease_identification_index'), {'crop': 'rice'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please upload an image.')

    def test_disease_identification_post_low_confidence(self):
        """
        Test POST request with low-confidence prediction.
        """
        uploaded_image = self.download_image(self.image_url)  # Download the image from URL

        response = self.client.post(reverse('disease_identification_index'), {
            'crop': 'rice',
            'image': uploaded_image
        })
        
        # Check if response contains error for low confidence
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Prediction confidence is too low. Please upload a clearer image.')

    def test_disease_identification_invalid_crop(self):
        """
        Test POST request with invalid crop.
        """
        uploaded_image = self.download_image(self.image_url)  # Download the image from URL

        response = self.client.post(reverse('disease_identification_index'), {
            'crop': 'invalid_crop',
            'image': uploaded_image
        })
        
        # Check if response contains error for invalid crop
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No model path found for invalid_crop in MODEL_PATHS dictionary!')

    def test_disease_identification_error_handling(self):
        """
        Test error handling for unexpected errors during image processing.
        """
        uploaded_image = self.download_image(self.image_url)  # Download the image from URL

        response = self.client.post(reverse('disease_identification_index'), {
            'crop': 'rice',
            'image': uploaded_image
        })

        # Check if an error message is returned in case of unexpected error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Error processing image')

    def tearDown(self):
        """
        Cleanup any resources, if necessary.
        """
        pass
