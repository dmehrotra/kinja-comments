import requests



def parse_sitemap(limit,site):
	response = make_request(site)

def make_request(site):
	return requests.get('https://'+site+'/sitemap.xml')
