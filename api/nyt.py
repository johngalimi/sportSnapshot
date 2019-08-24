import requests
import pprint

my_api_key = 'K91QbuNCPYmqqLCn1Uj1C5cyJBH9EPri'

get_url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key={my_api_key}'

r = requests.get(get_url)

print(r.status_code)

print(r.headers['content-type'])

print(r.encoding)

print(r.text[0])

# print(r.json())

pprint.pprint(r.json())