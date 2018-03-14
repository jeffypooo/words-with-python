import os
import sys
import time
import threading
import queue
import itertools
import argparse

import wwf
from oxd_api import OxfordDictionaryApi

envname_app_id = 'OXD_APP_ID'
envname_api_key = 'OXD_API_KEY'

if envname_app_id not in os.environ:
    print("environment variable '%s' not defined." % envname_app_id)
    exit(-1)
if envname_api_key not in os.environ:
    print("environment variable '%s' not defined." % envname_app_id)
    exit(-1)

args_parser = argparse.ArgumentParser()
sub_parsers = args_parser.add_subparsers(help='commands', dest='command')
search_parser = sub_parsers.add_parser('search')
search_parser.add_argument('query', type=str)
search_parser.add_argument('-s', '--size', type=int, default=15)
define_parser = sub_parsers.add_parser('define')
define_parser.add_argument('query', type=str)

api = OxfordDictionaryApi(os.environ[envname_app_id], os.environ[envname_api_key])
size_limit = 15
res_queue = queue.Queue()


def transform_and_filter_results(results):
    for item in results:
        word = item['word'].casefold()
        if " " in word:
            continue
        if "-" in word:
            continue
        if "." in word:
            continue
        if len(word) > size_limit:
            continue
        if wwf.word_violates_tilecounts(word):
            continue
        yield (word, wwf.compute_word_score(word))


def prefix_search(query):
    results = api.prefix_search(query)
    processed = sorted(list(transform_and_filter_results(results)), key=lambda r: r[1], reverse=True)
    res_queue.put(processed)


def define(word):
    res = api.define(word)
    res_queue.put(res)


def wait_for_results(msg):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while True:
        try:
            res = res_queue.get(timeout=0.1)
            os.system('clear')
            return res
        except queue.Empty:
            print("\r[%c] %s..." % (next(spinner), msg), end='', flush=True)


def run_search(query, size=size_limit):
    global size_limit
    size_limit = size
    search_thread = threading.Thread(target=prefix_search, args=(query,), daemon=True)
    search_thread.start()
    data = wait_for_results("searching for '%s'" % query)
    for word, score in data:
        print("%d - %s" % (score, word))
    print("\n%s results" % len(data))


def run_define(query):
    def_thread = threading.Thread(target=define, args=(query,), daemon=True)
    def_thread.start()
    defns = wait_for_results("defining '%s'" % query)
    if len(defns) == 0:
        print("no definition found for '%s'" % query)
        return
    print("\n'%s':" % query)
    for d in defns:
        print("%s" % d)


def main():
    os.system('clear')
    args = args_parser.parse_args()
    if args.command == 'search':
        run_search(args.query, args.size)
    if args.command == 'define':
        run_define(args.query)

    return


if __name__ == '__main__':
    main()
