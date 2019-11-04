from flow import *
from site import *
import time
links = get_sitemap_links(limit(),get_site())
h = []
for l in links:
	for link_date in get_articles(l):
		if ".com/" in link_date['link']:
			time.sleep(5)
			l = archive(link_date)
			h.append(l)


with open('data.json', 'w') as outfile:
    json.dump(h, outfile)