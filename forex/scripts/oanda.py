import os
import json
from datetime import datetime
import logging
import requests
from oanda.models import Price
from oanda.models import Instrument

class OANDA:
	def __init__(self):
		self.auth_headers = self.generate_auth_headers()
		self.accounts = self.fetch_account_list()
		self.instruments = self.fetch_instrument_list()

	def fetch_account_list(self):
		account_url = 'https://api-fxpractice.oanda.com/v3/accounts'
		res = self.req(account_url)
		accs_raw = res.json()
		return [acc['id'] for acc in accs_raw['accounts']]

	def generate_auth_headers(self):
		token = os.environ['OANDA_TOKEN']
		bearer = 'Bearer ' + str(token)
		headers = {'authorization': bearer}
		return headers

	def fetch_instrument_list(self):
		account_id = self.accounts[0]
		instrument_url = 'https://api-fxpractice.oanda.com/v3/accounts/'+account_id+'/instruments'
		res = self.req(instrument_url)
		instruments_raw = res.json()
		instruments = [instrument['name'] for instrument in instruments_raw['instruments']]
		[Instrument.objects.update_or_create(name=instrument) for instrument in instruments]
		return instruments;

	def make_money(self):
		prices = self.stream_prices()

	def req(self, url, params=None, stream=False):
		return requests.get(url, headers=self.auth_headers, params=params, stream=stream)

	def create_price_event(self, price):
		try:
			p = json.loads(price)
			print('price', price, p)
			if not p['type'] == 'HEARTBEAT':
				print(p)
				Price.objects.create(
					instrument=p['instrument'],
					bids=p['bids'],
					asks=p['asks'],
					closeout_bid=p['closeoutBid'],
					closeout_ask=p['closeoutAsk'],
					tradeable=p['tradeable'],
					time=p['time']
				)
		except Exception as e:
			logging.warn('When: {}, {}, {}'.format(datetime.now(), e, price))

	def stream_prices(self):
		account_id = self.accounts[0]
		instruments = None
		for instrument in self.instruments:
			if not instruments:
				instruments = instrument + ','
			else:
				instruments = instruments+instrument+','
		price_url = 'https://stream-fxpractice.oanda.com/v3/accounts/' + account_id + '/pricing/stream'
		params = {
			'instruments': instruments,
		}
		prices = self.req(price_url, params=params, stream=True)
		[self.create_price_event(price) for price in prices.iter_lines()]

def run():
	OANDA().make_money()