#!/usr/bin/python3

import mw

# For when you don't have [[mw:Extension:Disambiguator]].

aw = mw.Session('https://wiki.archlinux.org/api.php', 'disambiguation-backlinks.py by User:Larivact')

for member in aw.query('categorymembers', list='categorymembers', cmtitle="Category:Disambiguation pages", cmlimit="max"):
	for backlink in aw.query('backlinks', list='backlinks', bltitle=member['title'], bllimit='max', blnamespace='0|4|8|10|12|14', blfilterredir='nonredirects'):
		print(backlink['title'])
