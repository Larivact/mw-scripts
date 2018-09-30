#!/usr/bin/python3

import mw

# For when you don't have [[mw:Extension:Disambiguator]].

aw = mw.Session('https://wiki.archlinux.org/api.php', 'disambiguation-backlinks.py by User:Larivact')

NAMESPACE='0|4|8|10|12|14'

for member in aw.query('categorymembers', list='categorymembers', cmtitle="Category:Disambiguation pages", cmlimit="max"):
	backlinks = []
	for backlink in aw.query('backlinks', list='backlinks', bltitle=member['title'], bllimit='max', blnamespace=NAMESPACE, blfilterredir='nonredirects', blredirect=''):
		backlinks.append(backlink['title'])
	# second query needed because blfilterredir only applies to the second level when blredirect (follow redirects) is used.
	for backlink in aw.query('backlinks', list='backlinks', bltitle=member['title'], bllimit='max', blnamespace=NAMESPACE, blfilterredir='redirects'):
		backlinks.remove(backlink['title'])
	for backlink in backlinks:
		print(backlink)
