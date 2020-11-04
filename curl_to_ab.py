#!/usr/bin/env python3
import sys
import os


def curl_to_ab(curl_cmd: list, num: int=200, cur: int=4) -> str:
    """
    Translate a cURL command created by Chrome's developer tools into a
    command for ``ab``, the ApacheBench HTTP benchmarking tool.
    Parameters
    ----------
    curl_cmd
        The string given to you by the "Copy to cURL" context action in
        Chrome's developer tools.
    num : int
        The number of requests ApacheBench should make in total
    cur : int
        The number of concurrent requests ApacheBench should make
    Note
    ----
    Not all headers play nice with ApacheBench, so ``headers_to_copy`` has
    been set to a reasonable default. Tweak this if you need something
    else in there.
    """
    url = curl_cmd[1]
    headers_to_copy = [
        'Origin',
        'Authorization',
        'Accept'
    ]
    headers = []

    for i, part in enumerate(curl_cmd):
        if part == '-H':
            header = curl_cmd[i+1]
            if any([h in header for h in headers_to_copy]):
                headers.append("'{}'".format(header))

    cmd = ['ab -n {} -c {}'.format(num, cur)]
    cmd += ['-H {}'.format(part) for part in headers]
    cmd.append("'{}'".format(url))

    return ' '.join(cmd)


print(curl_to_ab("curl 'http://localhost:4000/graphql?' -H 'Connection: keep-alive' -H 'Accept: application/json' -H 'Origin: http://localhost:4000' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36' -H 'Content-Type: application/json' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-Mode: cors' -H 'Referer: http://localhost:4000/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7' -H 'Cookie: _ga=GA1.1.1645298590.1569536055' --data-binary '{\"query\":\"{\n  posts {\n    id\n  }\n}\",\"variables\":null}' --compressed", 10000, 10));


#if __name__ == '__main__':
#    """Usage: python curl_to_ab.py <cURL command from Chrome>
#    """
#    os.system(curl_to_ab(sys.argv[1:]))


