"""Example Use."""


# [ Imports ]
# [ -Python ]
import asyncio
import time
import pprint

# [ -Project ]
import a_sync


# [ Examples ]
if __name__ == '__main__':
    def hello(name, seconds):
        """Hello."""
        print('hello {}'.format(name))
        time.sleep(seconds)
        print('bye {}'.format(name))
        return name

    async def async_hello(name, seconds):
        """Hello."""
        print('hello {}'.format(name))
        await asyncio.sleep(seconds)
        print('bye {}'.format(name))
        return name

    # parallel_1 = a_sync.Parallel()
    # parallel_1.schedule(hello, 'joe', 5)
    # parallel_1.schedule(hello, 'sam', 3)
    # parallel_1.schedule(async_hello, 'bob', 1)
    # asyncio.get_event_loop().run_until_complete(parallel_1.run())

    # parallel_1.block()

    # serial_1 = a_sync.Serial()
    # serial_1.schedule(hello, 'joe', 5)
    # serial_1.schedule(hello, 'sam', 3)
    # serial_1.schedule(async_hello, 'bob', 1)
    # asyncio.get_event_loop().run_until_complete(serial_1.run())

    # serial_1.block()

    # a_sync.block(async_hello, 'jeff', 6)

    parallel_1 = a_sync.Parallel()
    parallel_1.schedule(hello, 'joe', 5)
    parallel_1.schedule(hello, 'sam', 3)
    parallel_1.schedule(async_hello, 'bob', 1)
    # expect start in any order, stop in bob, sam, joe

    parallel_2 = a_sync.Parallel()
    parallel_2.schedule(async_hello, 'jill', 4)
    parallel_2.schedule(async_hello, 'jane', 2)
    parallel_2.schedule(hello, 'mary', 1)
    # expect start in any order, stop in mary, jane, jill

    serial_1 = a_sync.Serial()
    serial_1.schedule(parallel_1.run)
    serial_1.schedule(parallel_2.block)
    # expect bob/sam/joe to end before mary/jane/jill start

    parallel_3 = a_sync.Parallel()
    parallel_3.schedule(async_hello, 'joseph', 5)
    parallel_3.schedule(hello, 'joey', 3)
    parallel_3.schedule(async_hello, 'jo', 1)
    # expect start in any order, stop in jo, joey, joseph

    parallel_4 = a_sync.Parallel()
    parallel_4.schedule(hello, 'alex', 4)
    parallel_4.schedule(async_hello, 'alexandria', 2)
    parallel_4.schedule(hello, 'alexandra', 1)
    # expect start in any order, stop in alexandra, alexandria, alex

    serial_2 = a_sync.Serial()
    serial_2.schedule(parallel_3.run)
    serial_2.schedule(parallel_4.block)
    # expect joe/joey/joseph to stop before alexandra/alexandria/alex start

    final_parallel = a_sync.Parallel()
    final_parallel.schedule(serial_1.block)
    final_parallel.schedule(serial_2.run)

    final_parallel.block()
    # pprint.pprint(all_results)
    # expect bob/sam/joe to start with jo/joey/joseph
    # expect jill/jane/mary to start with alex/alexandria/alexandra
    # total expected ordering:
    # start joe/sam/bob/joseph/joey/jo
    # stop bob/jo
    # stop sam/joey
    # stop joe/joseph
    # start jill/jane/mary/alex/alexandria/alexandra
    # stop mary/alexandra
    # stop alexandria/jane
    # stop alex/jill
