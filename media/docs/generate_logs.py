import os
import sys
import random
from datetime import datetime


endpoints = [
    '/login',
    '/logout',
    '/malfunctions',
    '/relays',
    '/users',
    '/equipment',
]
chars = list('eofuhgresf')


def main():
    if len(sys.argv) == 2:
        dirpath = sys.argv[1]
    else:
        dirpath = os.path.dirname(__file__)
    for n in range(100):
        with open(os.path.join(dirpath, f'log{n:03d}'), 'w', encoding='utf8') as fp:
            for i in range(1_000_000):
                dt = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
                method = random.choice(['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
                status = random.choice([200, 201, 302, 400, 401, 403, 404, 503, 502])
                req_size = random.randint(0, 800)
                resp_size = random.randint(300, 900)
                time = random.randint(40, 500)
                uri = random.choice(endpoints)
                if i % 2:
                    random.shuffle(chars)
                    uri += '/' + ''.join(chars)
                if i % 3:
                    random.shuffle(chars)
                    p = ''.join(chars[:2])
                    v = ''.join(chars[-2:])
                    uri += f'?{p}={v}'
                fp.write(f'{dt} {method} {status} {req_size} {resp_size} {time} {uri}\n')


if __name__ == '__main__':
    main()
