#/bin/env python3

from elastic import Client
from cProfile import Profile
from pstats import Stats
from time import time
from asyncio import set_event_loop_policy, Task, gather
try:
    from uvloop import get_event_loop, EventLoopPolicy
    set_event_loop_policy(EventLoopPolicy())
except ImportError:
    from asyncio import get_event_loop

async def main():
    e = Client()
    for n in range(1,10000):
        if n % 100 == 0:
            print(n)
        async for n in e.getNodes():
            pass
    await e.session.close()

if __name__ == '__main__':
    p = Profile()
    p.enable()
    loop = get_event_loop()
    start_time = time()
    loop.run_until_complete(main())
    print("----DONE----")
    print(time() - start_time)
    p.disable()
    Stats(p).dump_stats("aioelastic.pstats")
