from datetime import datetime, timedelta
from oanda.models import Candle, Instrument
import pytz
from statistics import mean, stdev

class Monitor:
	def __init__(self):
		self.monitor = {}

	def calculate_results(self, candles):
		all_candles = [c for c in candles]
		last_candle = all_candles[-1]
		rest_candles = all_candles[:-1]

		avg_all = self.calc_avg(all_candles)
		dev_all = self.calc_std_dev(all_candles)
		print(avg_all, dev_all, "\n")

	def calc_avg(self, candles):
		v = mean([c.volume for c in candles])
		o = mean([c.open for c in candles])
		c = mean([c.close for c in candles])
		return {'volume': v, 'open': o, 'close': c}

	def calc_std_dev(self, candles):
		v = stdev([c.volume for c in candles])
		o = stdev([c.open for c in candles])
		c = stdev([c.close for c in candles])
		return {'volume': v, 'open': o, 'close': c}

	def get_instruments(self):
		return [i.name for i in Instrument.objects.all()]
	
	def get_candles(self, instruments):
		minutes = 10
		step_count = 60 * minutes
		interval = pytz.utc.localize(datetime.now()-timedelta(seconds=step_count))
		candles = {}
		for instrument in instruments:
			c = Candle.objects.filter(instrument=instrument, time__gte=interval)
			candles[instrument] = c
		return candles

	def process_candles(self, candles):
		for instrument, unprocessed in candles.items():
			try:
				if instrument == 'EUR_USD':
					self.monitor[instrument] = self.calculate_results(unprocessed) if instrument in self.monitor else {}
			except Exception as e:
				print(e)
		return 

	def run_monitor(self):
		instruments = self.get_instruments()
		candles     = self.get_candles(instruments)
		processed   = self.process_candles(candles)
		return

	def run(self):
		monitor_every  = 1 #seconds 
		last_monitored = None
		should_monitor = True

		while should_monitor:
			if not last_monitored:
				self.run_monitor()
				last_monitored = datetime.now()

			now = datetime.now()
			delta = now-timedelta(seconds=monitor_every)
			
			if last_monitored < delta:
				self.run_monitor()
				last_monitored = datetime.now()

Monitor().run()