from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from oanda.models import Price, Instrument
import logging

# Create your views here.
def index(View):
	try:
		instruments = Instrument.objects.all()
		[print(i.name) for i in instruments]
		return HttpResponse(instruments)
	except Exception as e:
		logging.warning(e)