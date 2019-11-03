from flow import *
from site import *

links = get_sitemap_links(limit(),get_site())
h = []
for l in links:
	for link_date in get_articles(l):
		if ".com/" in link_date['link']:
			post = get_comments(link_date)
			if post:
				h.append(post)
				print (post['count'])
				print(post['comments'])

with open('data.json', 'w') as outfile:
    json.dump(h, outfile)