from oanda.models import Price, Candle
from datetime import datetime
from datetime import timedelta
from django.db.models import Max
import logging
import pytz
import time

class Candleyze:
	def __init__(self):
		self.batch_id = self.get_max_batch()


	def candleyze(self, events):
		candles = {}
		for instrument, prices in events.items():
			candles[instrument] = self.create_candles(prices)
		return candles


	def create_candles(self, prices):
		# simple candles check only the closeout_bid 
		results = {
			'open': None,
			'close': None,
			'high': 0,
			'volume': len(prices)
		}

		counter = 0 #determines 'close' price
		for price in prices:
			results['open'] = results['open'] if results['open'] else price.closeout_bid
			results['high'] = results['high'] if results['high'] > price.closeout_bid else price.closeout_bid

			#determine low
			if not 'low' in results:
				results['low']  = price.closeout_bid
			else:
				results['low']  = results['low'] if results['low'] < price.closeout_bid else price.closeout_bid

			#increment and check for close
			counter = counter + 1
			if counter == len(prices):
				results['close'] = price.closeout_bid
		return results

	def fetch_prices(self, interval=60):
		r = self.get_time_range(interval)
		return Price.objects.filter(time__lt=r['start'], time__gt=r['end'])

	def get_max_batch(self):
		max_batch = Candle.objects.aggregate(Max('batch'))['batch__max']

		if not max_batch:
			return int(time.time())
		else:
			return int(max_batch)

	def get_time_range(self, interval):
		start = pytz.utc.localize(datetime.now())
		end   = pytz.utc.localize(datetime.now()-timedelta(seconds=interval))
		return {
			'start': start,
			'end':   end,
		}

	def run(self, interval=60):
		last_saved = None
		
		while(True):
			if not last_saved:
				last_saved = int(time.time())
			if int(time.time()) - last_saved > interval:
				events      = self.fetch_prices(interval=interval)
				sort        = self.sort_events(events)
				candles     = self.candleyze(sort)
				last_saved = int(time.time())
				logging.warning('...saving candles')
				self.save_candles(candles)
		return

	def save_candles(self, candles):
		self.batch_id = self.batch_id + 1 
		for instrument, candle in candles.items():
			now = datetime.now()
			Candle.objects.create(
				instrument=instrument,
				open=candle['open'],
				high=candle['high'],
				low=candle['low'],
				close=candle['close'],
				volume=candle['volume'],
				batch=self.batch_id,
			),

	

	def sort_events(self, bucket):
		prices = {}
		for price in bucket:
			instrument = price.instrument
			if instrument not in prices:
				prices[instrument] = [price]
			else:
				prices[instrument].append(price)
		return prices

def run():
	Candleyze().run()