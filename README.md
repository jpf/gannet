# About

This is *yet another* Python library to parse the "My Clippings.txt" files generated by the Amazon Kindle.

The name "gannet" is inspired by the Monty Python "[Bookshop](http://youtu.be/p62uutgNN4c)" sketch.

In the hopes of making a more flexible and understandable parser, this one makes use of the [Pyparsing](http://pyparsing.wikispaces.com/) library for parsing the various parts of a "My Clippings.txt" file.

# Installing

```
pip install -r requirements.txt
```

# Using

```python
from gannet import parse_my_clippings
import codecs

clippings = []
with codecs.open(sys.argv[1], 'r', 'utf-8') as f:
    clippings = parse_my_clippings(f)
```

# To convert a "My Clippings.txt" file to JSON
```
$ python parse_my_clippings.py "My Clippings.txt" 
```


# Testing
```
$ nosetests
```
