from django.db import models

class PricePrediction(models.Model):
    admin1 = models.CharField(max_length=100)
    admin2 = models.CharField(max_length=100)
    market = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    commodity = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    predicted_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commodity} in {self.market} from {self.start_date} to {self.end_date}"
