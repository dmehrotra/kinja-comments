import sys
import requests
import xml.etree.ElementTree as ET
import xmltodict
import json
import datetime
from bs4 import BeautifulSoup
import time
def limit():
	# this means only include sitemaps before a year
	limit = []
	try:
		ulimit=sys.argv[2]
		limit = sys.argv[3]
	except:
		print(" No Limit ")
	return [ulimit,limit]

def get_site():
	return sys.argv[1]

def get_sitemap_links(limit,site):
	if limit == False:
		# print('FLOW :: GETTING ALL SITEMAP LINKS FOR', site)
		return parse_sitemap(limit,site)
	else:
		# print('FLOW :: GETTING MOST RECENT SITEMAP LINKS', site)
		return parse_sitemap(limit,site)

def archive(link):
	response = requests.get("https://web.archive.org/save/"+link['link'])
	if response.status_code == 200:
		print('saved: ' + link['link'])
		link['saved'] = True
	else:
		link['saved'] = False
	return link

def parse_sitemap(limit,site):
	response = make_request(site)
	d = xmltodict.parse(response.content)
	
	links = []
	for d in d['sitemapindex']['sitemap']:
		if checkdate(limit,d):
			# print("APPENDING :: "+d['loc'])
			links.append(d['loc'])
	
	return links

def get_articles(link):
	response = requests.get(link)
	d = xmltodict.parse(response.content)
	links = []
	for l in d['urlset']['url']:
		try:
			a = {"link":l['loc']}
			links.append(a)
		except:
			print("issue with lastmod")
	return links

def get_comments(link):
	post = {"link": link['link'],"date":link['date'], "comments":[],"count":0}
	site = link['link'].split('/')[2]
	post_id = link['link'].split('-')[-1]
	response = requests.get("https://"+site+"/ajax/comments/views/replies/"+post_id+"?startIndex=0&maxReturned=100&maxChildren=10&approvedOnly=false&cache=true&experimental=true&sorting=top")
	try:
		d = json.loads(response.text)
		print("got blog")
		for comment in d['data']['items']:
			try:
				c = comment['reply']['body'][0]['value'][0]['value'].lower()
			except:
				c = "uncommentable"

			if " ad " in c or " ads " in c or " advertis" in c or "pop ups" in c or "pop up" in c or "pop-up" in c or "pop-ups" in c or "autoplay" in c:	
				post['comments'].append(c)
				post['count'] = post['count'] + 1
			
			for child in comment["children"]['items']:
				p = child['plaintext'].lower()
				if " ad " in p or " ads " in p or " advertis" in p or "pop ups" in p or "pop up" in p or "pop-up" in p or "pop-ups" in p or "autoplay" in p:
					post['comments'].append(p)
					post['count'] = post['count'] + 1
	except:
		print("error")
	if post['count'] > 0:
		return post

def get_hed(link):
	try:
		response = requests.get(link)
		d = response.text
		soup = BeautifulSoup(d, "html.parser")
		h = soup.find_all('h1')[-1].text
		print(h.encode('utf-8').strip())
		return h
	except:
		print("issue getting headline for "+link)

def make_request(site):
	return requests.get('https://'+site+'/sitemap.xml')

def checkdate(limit,d):
	da = datetime.datetime.strptime(d['lastmod'].split('T')[0], '%Y-%m-%d')
	if len(limit) < 2:
		return True
	else:
		start=datetime.datetime.strptime(limit[0], '%Y')
		end = datetime.datetime.strptime(limit[1], '%Y')
		if start < da and end > da:
			print(da)
			return True
		else:
			return False
