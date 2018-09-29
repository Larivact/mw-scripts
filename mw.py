"""
Lightweight MediaWiki API wrapper.

Tip: set limits to 'max'
"""

import re

import requests

# ArchWiki specific way of localizing page titles, see [[Help:i18n]].
LANGS = [" العربية", "Български", "Català", "简体中文", "正體中文", "Hrvatski", "Česky",
"Dansk", "Nederlands", "Esperanto", "Suomi", "Français", "Deutsch", "Ελληνικά",
"עברית", "Magyar", "Bahasa Indonesia", "Italiano", "日本語", "한국어", "Lietuviškai",
"Norsk Bokmål", "فارسی", "Polski", "Português", "Română", "Русский", "Српски (Srpski)",
"Slovenský", "Español", "Svenska", "ไทย", "Türkçe", "Українська", "Tiếng Việt"]

### Helper functions ###

def get_title_lang(title):
	match = re.search("\(([^\(]+)\)(/|$)", title);
	if match:
		return match.group(1)

def chunks(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]

def join(l):
	return '|'.join([str(x) for x in l])

#TODO: implement Session.login()

class Session():
	def __init__(self, api_url, useragent):
		self.api_url = api_url
		self.session = requests.session()
		self.session.headers.update({'User-agent': useragent})

	def get(self, action, **kwargs):
		resp = self.session.get(self.api_url, params={'action':action,'format':'json', **kwargs})
		#print(resp.request.url)
		return resp.json()

	def post(self, action, **kwargs):
		return self.session.post(self.api_url, params={'action':action,'format':'json'}, data=kwargs).json()

	def query(self, resp_key, cont={}, **kwargs):
		resp = self.get('query', **kwargs)

		# TODO: detect error status codes
		if 'warnings' in resp:
			raise ValueError(resp)

		results = resp['query'][resp_key]
		if type(results) == dict:
			results = results.values()
		for r in results:
			yield r

		if 'continue' in resp:
			kwargs.update(resp['continue'])
			for r in self.query(resp_key, **kwargs):
				yield r

	def login(self, username, password):
		pass
