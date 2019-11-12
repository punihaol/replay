# Overview
Replay webhooks from the rehook service.

# Installation
Make sure rehook_python is installed first and then `python setup.py install`.

# Usage
```bash
$ replay.py -p "/braintree/notifications/" -t "http://127.0.0.1:8000/v1/bt/handle_webhook"
```

Note that this will replay all the braintree sandbox webhooks which may cause issues if a webhook 
corresponds to a sandbox user or subscription that doesn't exist on your local installation.
