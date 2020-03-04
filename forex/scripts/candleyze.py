from oanda.models import Price, Candle
from datetime import datetime
from datetime import timedelta
import logging
import pytz
import time

class Candleyze:
	def __init__(self):
		None

	def run(self, interval=60):
		price_buckets  = self.create_buckets(interval=interval, buckets=4)
		sorted_buckets = self.sort_buckets(price_buckets)
		candles = self.candlyze(sorted_buckets)

		last_candled = None
		while(True):
			if not last_candled:
				last_candled = int(time.time())
				self.save_candles(candles)
			if int(time.time()) - last_candled > interval:
				last_candled = int(time.time())
				logging.warning('...saving candles')
				self.save_candles(candles)
		return

	def candlyze(self, buckets):
		candled = {}
		for bucket in buckets:
			for instrument, prices in bucket.items():
				candles = self.create_simple_candles(prices)
				candled[instrument] = candles
		return candled

	def create_buckets(self, interval=60, buckets=4):
		ranges = self.get_time_ranges(interval, buckets)
		price_buckets = []
		for r in ranges:
			start  = pytz.utc.localize(r['start'])
			end    = pytz.utc.localize(r['end'])
			price_buckets.append(Price.objects.filter(time__lt=start, time__gt=end))
		return price_buckets

	def create_simple_candles(self, prices):
		results = {
			'open': 0.0,
			'close': 0.0,
			'volume': len(prices)
		}
		counter = 1
		for price in prices:
			results['open'] = results['open'] if results['open'] else price.closeout_bid
		
			if not 'high' in results:
				results['high'] = price.closeout_bid
			else: 
				results['high'] = results['high'] if results['high'] > price.closeout_bid else price.closeout_bid

			if not 'low' in results:
				results['low'] = price.closeout_bid
			else:
				results['low'] = results['low'] if results['low'] < price.closeout_bid else price.closeout_bid

			if counter == len(prices):
				results['close'] = price.closeout_bid

			counter = counter + 1
		return results

	def get_time_ranges(self, interval, buckets):
		ranges = []
		step = int(interval / buckets)
		i = 0
		j = 0
		while i < interval:
			r = {}
			if i == 0:
				r['start'] = datetime.now()
			if i > 0:
				r['start'] = ranges[j-1]['end']

			r['end'] = r['start']-timedelta(seconds=step)

			ranges.append(r)
			i = i + step
			j = j + 1
		return ranges

	def save_candles(self, candles):
		batch_id = int(time.time()) 
		for instrument, candle in candles.items():
			now = datetime.now()
			Candle.objects.create(
				instrument=instrument,
				open=candle['open'],
				high=candle['high'],
				low=candle['low'],
				close=candle['close'],
				volume=candle['volume'],
				batch=batch_id
			),

	def sort_buckets(self, buckets):
		sorted_buckets = []
		for bucket in buckets:
			prices = {}
			for price in bucket:
				instrument = price.instrument
				if instrument not in prices:
					prices[instrument] = [price]
				else:
					prices[instrument].append(price)
			sorted_buckets.append(prices)
		return sorted_buckets

def run():
	Candleyze().run()