# Oxford API base URL

from datetime import datetime
import json

import requests

oxd_api_base_url = 'https://od-api.oxforddictionaries.com:443/api/v1'
# Search language
lang = 'en'


def get_endpoint_url(endp):
    return oxd_api_base_url + '/' + endp


def get_search_url(query):
    return get_endpoint_url('search') + '/' + lang + '?q=' + query.lower() + '&prefix=true&regions=us'


class OxfordDictionaryApi:
    def __init__(self, id, key):
        self.id = id
        self.key = key

    def get(self, url):
        return requests.get(url, headers={'app_id': self.id, 'app_key': self.key})

    def prefix_search(self, query):
        url = get_search_url(query)
        req = self.get(url)
        if req.status_code != 200:
            print('Search failed. (%d: %s)' % (req.status_code, req.text))
            return {}
        data = req.json()
        return sorted(data['results'], key=lambda r: len(r['id']))

    def define(self, word):
        word_id = word.casefold().replace(" ", "_")
        url = get_endpoint_url('entries/') + lang + '/' + word_id
        req = self.get(url)
        if req.status_code != 200:
            return []
        # print(req.text)
        defns = json.loads(req.text)['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions']
        return defns

    def fetch_english_words(self):
        url = get_endpoint_url('wordlist/') + lang + '/regions=us'
        req = self.get(url)
        print(len(req.json()['results']))

    def map_to_defns(self, data):
        return
