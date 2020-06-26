#!/usr/bin/python3

import feedparser
import connix
import os

folder = "/home/pi/git/dendorystatus.github.io"
top = "<!DOCTYPE html><html><head><style>body{background-color:#000000;color:#FFFFFF;font-family:monospace;}</style></head><body>"
bottom = "</body></html>"
newsfeeds = [
				"http://www.ctvnews.ca/rss/ctvnews-ca-world-public-rss-1.822289",
				"http://montreal.ctvnews.ca/rss/ctv-news-montreal-1.822366"
			]
weatherfeed = "https://weather.gc.ca/rss/city/qc-147_e.xml"

# Update news panes

for i in [1, 2]:
	count = 0
	with open("{}/news{}.html".format(folder, i), "w", encoding='UTF-8') as fd:
		rss = feedparser.parse(newsfeeds[i-1])
		fd.write("{}\n".format(top))
		for item in rss['items']:
			if 'links' in item and len(item['links']) > 1:
				img = item['links'][1]['url']
			elif 'media_content' in item:
				img = item['media_content'][0]['url']
			else:
				img = ""
			if len(img) > 0 and img[0] == '/':
				img = "http:" + img
			desc = item['description'].replace('\n',' ').replace('<br>',' ').replace('<p>',' ')
			desc = connix.max_len(desc, 280)
			title = item['title']
			fd.write("<p><font size=+3><b>{}</b></font><br><table><tr><td style='vertical-align:top'><img style='width:300px;height:169px' src=\"{}\"></td><td><font size=+2>{}</font></td></table></p>\n".format(title, img, desc))
			count = count + 1
			if count > 2:
				break
		fd.write("{}\n".format(bottom))

# Get current weather

weather = "?? °C"
with open("{}/weather.txt".format(folder), "w", encoding='UTF-8') as fd:
	rss = feedparser.parse(weatherfeed)
	for item in rss['items']:
		if "Current Conditions: " in item['title']:
			weather_array = item['title'].replace("Current Conditions: ", "").split(' ')
			for weather_part in weather_array:
				if "°C" in weather_part:
					weather = weather_part
	weather = weather[0:30]
	fd.write(weather)

connix.cmd("cd {} && git commit -m \"auto update {}\" -a && git push".format(folder, connix.now()))
