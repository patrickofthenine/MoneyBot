from oanda.models import Candle, Instrument
class Monitor:
	def __init__(self):
		self.results = {}

	def get_instruments(self):
		return [i.name for i in Instrument.objects.all()]
	
	def get_candles(self, instruments):
		candles = {}
		for i in instrument:
			c = Candle.objects.filter(instrument=i)
			candles[i] = c
		return candles

	def process_candles(self, candles):
		print(candles)

	def run(self):
		instruments 	= self.get_instruments()
		candles 		= self.get_candles(instruments)
		processed 		= self.process_candles(candles)


Monitor().run()