from xml.etree import cElementTree as ElementTree
from base64 import decodebytes
from collections import defaultdict

class ParseBTPayload(object):
  def __init__(self, payload):
    # xml String
    self.payload_xml_str = decodebytes(payload.encode('ascii') if isinstance(payload, str) else payload)

  def to_dict(self):
    e = ElementTree.XML(self.payload_xml_str)
    xmldict = self.etree_to_dict(e)
    return xmldict

  def etree_to_dict(self, t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(self.etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['value'] = text
        else:
            d[t.tag] = text
    return d