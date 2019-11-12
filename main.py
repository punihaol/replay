#!/usr/bin/env python3
import getopt
import sys

import requests

from rehook import RehookGateway
from rehook.webhook import Webhook


def usage(cmd):
    return '%s -p <path to replay> -t <target url>' % cmd


def replay_webhook(session: requests.Session, webhook: Webhook, target: str):
    req = requests.Request(method=webhook.method,
                           url=target,
                           headers=webhook.headers,
                           params=webhook.query_params,
                           data=webhook.post_data)
    response = session.send(req.prepare())
    if response.status_code >= 400:
        print(f'Error replaying webhook {webhook}: {response}.')
        return False
    return True


def main(cmd, argv):
    try:
        opts, args = getopt.getopt(argv, 'hp:t:', ['path=', 'target=', ])
    except getopt.GetoptError:
        print(usage(cmd))
        sys.exit(1)

    source = None
    target = None

    for opt, arg in opts:
        if opt == '-h':
            print(usage(cmd))
            sys.exit(0)
        elif opt in ('-p', '--path'):
            source = arg
        elif opt in ('-t', '--target'):
            target = arg

    rehook = RehookGateway()
    webhooks = rehook.webhooks.list()
    replayed = 0
    success = 0
    session = requests.Session()
    for webhook in webhooks:
        if webhook.path == source:
            replayed += 1
            if replay_webhook(session, webhook, target):
                success += 1
    print(f'Replayed {replayed} webhooks.')


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
