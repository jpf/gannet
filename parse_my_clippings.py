#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gannet import parse_my_clippings
import codecs
import json
import sys

clippings = []
with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
    clippings = parse_my_clippings(f)

print(json.dumps(clippings, indent=4))
