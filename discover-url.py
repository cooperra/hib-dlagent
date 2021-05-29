#!/usr/bin/env python

import humblebundle
import sys
import os

filename = sys.argv[2]
username = sys.argv[3]
password = os.environ['PASSWORD']

client = humblebundle.HumbleApi()
try:
    client.login(username, password)
except humblebundle.exceptions.HumbleTwoFactorException as e:
    print(e, end=': ', file=sys.stderr)
    client.login(username, password, input())
except humblebundle.exceptions.HumbleAuthenticationException as e:
    print(e, file=sys.stderr)
    exit()

def find_url(order_list, filename):
    for order in order_list:
        for subproduct in order.subproducts or []:
            for download in subproduct.downloads or []:
                for download_struct in download.download_struct or []:
                    url = download_struct.url.web
                    if url and filename in url:
                        return url

try:
    order_list = client.order_list()
    url = find_url(order_list, filename)
    if url:
        print(url)
finally:
    client.logout()

