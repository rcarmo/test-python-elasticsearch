#/bin/env python3

from elasticsearch import Elasticsearch as Client
from cProfile import Profile
from pstats import Stats
from time import time

def main():
    e = Client()
    for n in range(1,10000):
        if n % 100 == 0:
            print(n)
        for n in e.nodes.info():
            pass

if __name__ == '__main__':
    p = Profile()
    p.enable()
    start_time = time()
    main()
    print("----DONE----")
    print(time() - start_time)
    p.disable()
    Stats(p).dump_stats("elastic.pstats")