from flow import *
from site import *
import time
links = get_sitemap_links(limit(),get_site())
for l in links:
	for link_date in get_articles(l):
		if ".com/" in link_date['link'] and ".com/c" not in link_date['link']:
			time.sleep(5)
			l = archive(link_date)

