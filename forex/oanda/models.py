from django.db import models

# Create your models here.
class Price(models.Model):
	instrument = models.CharField(max_length=10)
	bids = models.TextField()
	asks = models.TextField()
	closeout_bid = models.FloatField(default=0.0)
	closeout_ask = models.FloatField(default=0.0)
	tradeable= models.BooleanField(default=False)
	time = models.DateTimeField()

class Instrument(models.Model):
	name = models.CharField(max_length=10)