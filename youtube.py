#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib,urllib2, json
from urllib2 import Request, urlopen, URLError, HTTPError
import requests
import argparse
import sys
from bs4  import BeautifulSoup
from HTMLParser import HTMLParser
import time, subprocess


baseurl = 'https://www.youtube.com/results?search_query='
target = "喵電感應"
search_page = 1
n_result = 5

def youtube_query(baseurl,target,search_page,n_result):
	search_result = {}
	search_result_titles = []
	search_result_links = []
	search_result_descriptions=[]
	search_result_thumbs = []
	shorten_url = []

	url = baseurl + '?' + urllib.quote_plus(target)+'&page='+str(search_page)

	result = urllib2.urlopen(url).read()

	soup = BeautifulSoup(result,"html.parser")
	
	parser = HTMLParser()

	vedio_title = soup.find_all('h3',{'class':['yt-lockup-title']})
	youtube_url = 'https://www.youtube.com'

	for titles in vedio_title:
		t_string = titles.find_all('a',{'class':['yt-uix-sessionlink','yt-uix-tile-link','yt-ui-ellipsis','yt-ui-ellipsis-2','spf-link']})
		t_string = unicode.join(u'\n',map(unicode,t_string))

		title = re.match(r'.*?title="([^"]*)"[^>]*', t_string, flags=0)
		link = re.match(r'.*?href="([^"]*)"[^>]*', t_string, flags=0)

		s_youtube_url =  youtube_url + link.group(1)

		if not type(title) is None:
			search_result_titles.append(title.group(1))
		if not type(link) is None:
			search_result_links.append(link.group(1))
			search_result_thumbs.append(thumbsUD(link.group(1)))
		
		shorten_url.append(shortenURL(s_youtube_url))

	vedio_descriptions = soup.find_all('div',{'class':['yt-lockup-dismissable','yt-uix-tile']})
	for description in vedio_descriptions:
		description = description.find_all('div',{'class':['yt-lockup-description', 'yt-ui-ellipsis', 'yt-ui-ellipsis-2']})
		d_string = unicode.join(u'\n',map(unicode,description))
		d_string = re.sub('<[^<]+?>','',d_string)

		if d_string is None or d_string is '':
			search_result_descriptions.append('')
		else:
			search_result_descriptions.append(d_string)

	for i in range(len(search_result_titles)):
		search_result[i] = {'title':search_result_titles[i],'link':search_result_links[i],
		'description':search_result_descriptions[i],'thumbs':search_result_thumbs[i],'s_url':shorten_url[i]}

	return search_result

def shortenURL(url):
	baseurl = 'https://developer.url.fit/api/shorten?long_url='
	s_url = urllib.quote_plus(str(url))
	url = baseurl + s_url
	try:
		result = urllib2.urlopen(url).read()
		j_data = json.loads(result)
		return j_data['url']
	except HTTPError as e:
		print 'The server couldn\'t fulfill the request'
		return 'false'
	else:
		pass

def thumbsUD(link):
	baseurl = 'https://www.youtube.com'
	url = baseurl + link
	result = urllib2.urlopen(url).read()
	soup = BeautifulSoup(result,"html.parser")
	parser = HTMLParser()
	like_string = ''
	dislike_string = ''

	likebtn = soup.find_all('span',{'class':['like-button-renderer'],'data-button-toggle-group':['optional']})

	for a in likebtn:
		like_tag = a.find_all('button',{'class':
		['like-button-renderer-like-button','like-button-renderer-like-button-unclicked']})

		for like in like_tag:
			like_string = like.find_all('span',{'class':'yt-uix-button-content'})
			like_string = unicode.join(u'\n',map(unicode,like_string))
			like_string = re.sub('<[^<]+?>','',like_string)

	for b in likebtn:
		dislike_tag = b.find_all('button',{'class':
		['like-button-renderer-dislike-button','like-button-renderer-dislike-button-unclicked']})

		for dislike in dislike_tag:
			dislike_string = dislike.find_all('span',{'class':'yt-uix-button-content'})
			dislike_string = unicode.join(u'\n',map(unicode,dislike_string))
			dislike_string = re.sub('<[^<]+?>','',dislike_string)
	
	end = []
	end.append(like_string)
	end.append(dislike_string)
	return end

def printout(search_result,n_result):
	for i in range(n_result):
		if not search_result[i]['s_url'] is 'false':
			print search_result[i]['title'] + ' (https://url.fit/'+search_result[i]['s_url']+")"
		else:
			print search_result[i]['title'] + ' (https://www.youtube.com'+search_result[i]['link']+")"
		if not search_result[i]['description'] is None or empyt:
			print search_result[i]['description']
		print "Like: "+search_result[i]['thumbs'][0]+", Dislike: "+search_result[i]['thumbs'][1]
		print '\n'

def cli_parser(target,search_page,n_result):
	parser = argparse.ArgumentParser()
	parser.add_argument("-n",help="number of search result. default is 5",type=int,default=5)
	parser.add_argument("-p",help="page that you parse",type=int,default=1)
	parser.add_argument("keyword",help="")

	args = parser.parse_args()

	if args.p:
		search_page = args.p

	if args.n:
		n_result = args.n

	if args.keyword:
		target = args.keyword

	return target,search_page,n_result

if __name__ == "__main__":
	target,search_page,n_result = cli_parser(target,search_page,n_result)
	search_result = youtube_query(baseurl,target,search_page,n_result)
	printout(search_result,n_result)