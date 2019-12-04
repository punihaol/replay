# Overview
Replay webhooks from the rehook service.

# Installation
Make sure rehook_python is installed first and then `python setup.py install`.

# Usage
```bash
# pull from http://host:port/braintee/notification/ and replay hooks on http://127.0.0.1:8000/v1/bt/handle_webhook
$ replay.py -p "/braintree/notification/" -t "http://127.0.0.1:8000/v1/bt/handle_webhook"

# list available replay-able hooks instead of running them.. will print like below
#
# braintree      83gr96                  subscription_charged_successfully         2019-12-02 10:16:43      Unknown User 
# braintree      f7mnjw                  subscription_charged_unsuccessfully       2019-12-02 10:14:55      Unknown User 
# braintree      gmy2kr                  subscription_charged_successfully         2019-12-01 14:39:55      Unknown User 
# braintree      4y54gb                  subscription_charged_successfully         2019-12-01 12:06:13      Unknown User 
# ..
$ replay.py -p "/braintree/notification/" -t "http://127.0.0.1:8000/v1/bt/handle_webhook" --ls

# filter hooks based on condition, chain conditions with & (in these cases below we are just printing them, not running..remove ls to run)
# available attributes (visible in list mode): provider, id (subscription id), date, user_name*, user_id* 
# *note: braintree / stripe may not have this data so use at discretion
#
# available comparators : attribute=val, attribute<val, attribute>val, :in->val1,val2
# dates higher than 2019-12-01
$ replay.py -p "/braintree/notification/" -t "http://127.0.0.1:8000/v1/bt/handle_webhook" -f 'date>2019-12-01' --ls 
# dates between 11-26 -> 11-29
$ replay.py -p "/braintree/notification/" -t "http://127.0.0.1:8000/v1/bt/handle_webhook" -f 'date>2019-11-26&date<2019-11-29' --ls
# raw_type is in the list 'subscription_canceled,subscriptio_went_activ' and also subscription id is 83zq6w
$ replay.py -p "/braintree/notification/" -t "http://127.0.0.1:8000/v1/bt/handle_webhook" -f 'id=83zq6w&raw_type:in->subscription_canceled,subscription_went_active' --ls
```


Note that this will replay all the braintree sandbox webhooks which may cause issues if a webhook 
corresponds to a sandbox user or subscription that doesn't exist on your local installation.
