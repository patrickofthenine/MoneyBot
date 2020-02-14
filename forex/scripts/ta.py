from oanda.models import Price
from datetime import datetime

class TA:
	def __init__(self):
		None

	def analyze(self):
		events = Price.objects.all().order_by('time')
		candles = self.candlyze(events)

	def candlyze(self, prices):
		results = {
			'open': 0.0,
			'high': 0.0,
			'low': 0.0,
			'close': 0.0,
			'volume': len(prices)
		}

		counter = 1
		for price in prices:
			results['open'] = results['open'] if results['open'] else price.closeout_bid
		
			if not results['high']:
				results['high'] = price.closeout_bid
			else: 
				results['high'] = results['high'] if results['high'] > price.closeout_bid else price.closeout_bid

			if not results['low']:
				results['low'] = price.closeout_bid
			else:
				results['low'] = results['low'] if results['low'] < price.closeout_bid else price.closeout_bid

			if counter == len(prices):
				results['close'] = price.closeout_bid

			counter = counter + 1

		return results


def run():
	TA().analyze()