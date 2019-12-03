from parse_bt_payload import ParseBTPayload
from datetime import datetime

class NormalizedWebhookData(object):

  def __init__(self, webhook):

    self.raw_webhook = webhook
    self.provider = None
    self.id = None
    self.date = None
    self.user_id = None
    self.user_name = None
    self.type = None
    self.raw_type = None

    # parse data for filtering (bt)
    if hasattr(webhook, 'data') and 'bt_payload' in webhook.data and bool(len(webhook.data['bt_payload'])):
      parsed_data = ParseBTPayload(webhook.data['bt_payload'][0]).to_dict()
      webhook = parsed_data['notification']
      self.provider = 'braintree'
      self.id = webhook['subject']['subscription']['id']
      self.date = self.convert_bt_timestamp(webhook['timestamp']['value'])
      self.raw_type = webhook['kind']
    # stripe
    else: 
      self.provider = 'stripe'
      self.id = webhook.data['data']['object']['customer']
      self.date = datetime.fromtimestamp(webhook.data['created'])
      self.raw_type = webhook.data['type']
      self.user_name = webhook.data['data']['object']['source']['name']
  
  def meets_criteria(self, criteria):
    conditions = criteria.split('&')
    
    # stage 1, transform data into iterables/other types if needed for comparators
    comparatorTransform = {
      ':in->': lambda actual, given: [actual, list(map(lambda x: x.strip(), given.split(',')))]
    }

    # stage 2, primitives / iterable of primitives each transformed by their attribute type
    typeTransform = {
      'date': [
        lambda actual: actual, 
        lambda given: datetime.strptime(given.replace(':', '').replace('-',''), "%Y%m%d")
      ]
    }

    # stag 3, comparison is done 
    dic = {
      ':in->': lambda actual, given: actual in given,
      '=' : lambda actual, given: actual == given,
      '<' : lambda actual, given: actual < given,
      '>' : lambda actual, given: actual > given,
    }
    
    meets_criteria = True
    for condition in conditions:
      activeComparator = None
      comparatorPossiblities = dic.keys()
      for possibleComparator in comparatorPossiblities:
        if possibleComparator in condition:
          activeComparator = possibleComparator
          break
      if activeComparator is not None and activeComparator in dic:
        [actualKey, givenValue] = condition.split(activeComparator)
        actualValue = getattr(self, actualKey)
        if actualValue is not None:
          if activeComparator in comparatorTransform:
            
            [actualValue, givenValue] = comparatorTransform[activeComparator](actualValue, givenValue)
          if actualKey in typeTransform:
            modifierFnActual = typeTransform[actualKey][0]
            modifierFnGiven = typeTransform[actualKey][1]
            actualValue = list(map(lambda x: modifierFnActual(x), actualValue)) if isinstance(actualValue, list) else modifierFnActual(actualValue)
            givenValue = list(map(lambda x: modifierFnGiven(x), givenValue)) if isinstance(givenValue, list) else modifierFnGiven(givenValue)
          meets_criteria = dic[activeComparator](actualValue, givenValue)
          if not meets_criteria:
            break
        
    return meets_criteria

  def max_text(self, text, _max=None):
    text = str(text)
    buffer = 3
    ellipsis = '...'
    extra = buffer + len(ellipsis)
    if _max is None:
      return text
    elif len(text) <= _max - extra:
      return text + ''.join(map(lambda x: ' ', range(0, _max - len(text))))
    else:
      return text[0: _max - extra] + ''.join(map(lambda x: ' ', range(0, len(text[0: _max - extra]) - _max))) + ellipsis + ' '.join(map(lambda x: '', range(0, buffer + 1)))

  def to_str_row(self):
    return f'{self.max_text(self.provider, 15)}{self.max_text(self.id, 24)}{self.max_text(self.raw_type, 42)}{self.max_text(self.date, 25)}{(self.user_name if self.user_name is not None else "Unknown User")} {f"({self.user_id})" if self.user_id is not None else ""}'
  
  def convert_bt_timestamp(self, ts):
    return datetime.strptime(ts.replace(':', '').replace('-',''), "%Y%m%dT%H%M%SZ")