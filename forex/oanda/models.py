from django.db import models

# Create your models here.
class Prices(models.Model):
	instrument = models.CharField(max_length=10)
	bids = models.TextField()
	asks = models.TextField()
	closeoutBid = models.FloatField(default=0.0)
	closeoutAsk = models.FloatField(default=0.0)
	tradeable= models.BooleanField(default=False)
	time = models.DateField()
