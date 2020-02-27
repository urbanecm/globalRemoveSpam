#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
import re

data = open('input.tsv').read().split('\n')
data.pop(0)
data.pop()

PATTERN_RAW = r'file:\/\/\/[-a-zA-Z0-9@:%._\+~#=\/()]+'
PATTERN = re.compile(PATTERN_RAW)

for row_raw in data:
	row = row_raw.split('\t')
	wiki = row[0].split('.')
	site = pywikibot.Site(wiki[0], wiki[1])
	page = pywikibot.Page(site, row[1])
	print(page)
	text = page.text
	for m in PATTERN.finditer(text):
		url = m.group(0)
		text = re.sub(r'<ref>[^<]*' + PATTERN_RAW + '[^<]*</ref>', '', text)
		m = re.search(r'\[' + PATTERN_RAW + '( [^]]+)?\]', text)
		if m:
			m = m.group(1)
			if m is None:
				text = text.replace('[' + url + ']', '')
			else:
				m = m.strip()
				text = text.replace('[%s %s]' % (url, m), m)
	page.text = text
	page.save('Remove inaccessible file:// url')
