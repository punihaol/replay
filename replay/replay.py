#!/usr/bin/env python3
import argparse
import sys
import base64

import requests

from rehook import RehookGateway
from rehook.webhook import Webhook


def replay_webhook(session: requests.Session, webhook: Webhook, target: str):
    kwargs = {}
    if webhook.body_base64:
        kwargs['data'] = base64.b64decode(webhook.body_base64)
    elif webhook.body:
        kwargs['data'] = webhook.body
    elif webhook.data:
        kwargs['json'] = webhook.data
    req = requests.Request(method=webhook.method,
                           url=target,
                           headers=webhook.headers,
                           params=webhook.query_params,
                           **kwargs)
    response = session.send(req.prepare())
    if response.status_code >= 400:
        print(f'Error replaying webhook {webhook}: {response}.')
        return False
    return True


def main(cmd, argv):
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', '--path', required=True)
    arg_parser.add_argument('-t', '--target', required=True)
    arg_parser.add_argument('--cleanup', dest='cleanup', action='store_true')
    arg_parser.add_argument('--pause', dest='pause', action='store_true')

    args = arg_parser.parse_args()

    gateway = RehookGateway()
    replayed = 0
    success = 0
    removed = 0
    session = requests.Session()
    for webhook in gateway.webhooks.search().filter(path=args.path).execute():
        if args.pause:
            print(webhook)
            input(f'Press Enter to confirm replay to {args.target}: ')
        replayed += 1
        if replay_webhook(session, webhook, args.target):
            success += 1
        if args.cleanup:
            if not gateway.webhooks.delete(webhook.id):
                print(f'Error cleaning up webhook {webhook}.')
            else:
                removed += 1
    print(f'Replayed {replayed} webhooks.')
    print(f'Removed {removed} webhooks.')


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
