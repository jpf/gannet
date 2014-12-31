#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyparsing as pp
import datetime


def match(x):
    return pp.Suppress(pp.Literal(x))

record_start = match('-')
word = pp.Word(pp.alphas)
comma = match(',')
colon = match(':')
dash = match('-')

###
# https://en.wikipedia.org/wiki/Roman_numerals
# Roman numerals, as used today, are based on seven symbols:
#  Symbol  Value
#  ------  -----
#  I       1
#  V       5
#  X       10
#  L       50
#  C       100
#  D       500
#  M       1,000
###
roman_numerals = pp.Word('ivxlcdm')
number = pp.Word(pp.nums)
location_number = pp.Or([number, roman_numerals])
location_number_range = location_number + dash + location_number
kindle_location = pp.Or([location_number, location_number_range])

numbered_page = match('Page') + kindle_location
unnumbered_page = pp.Literal('Unnumbered') + match('Page')

day_of_week = word
month = word
day_of_month = number
year = number

hour = number
minute = number
second = number

###

date = (
    day_of_week + comma +
    month + day_of_month + comma + year +
    pp.Optional(comma))
time = (
    hour + colon +
    minute + pp.Optional(colon + second) +
    pp.Or(['AM', 'PM']) + pp.Optional("\r"))
record_create_date = (
    match('Added on') +
    date.setResultsName('date') +
    time.setResultsName('time'))

location_matcher = match('Location') + kindle_location + match('|')
location_range = location_matcher.setResultsName('locations')

page_matcher = (
    match('on') +
    pp.Or([numbered_page, unnumbered_page]) +
    match('|'))
page_range = page_matcher.setResultsName('pages')

record_type = match('Your') + word.setResultsName('type')

note_information_line_parser = (
    record_start +
    record_type +
    pp.Optional(page_range) +
    pp.Optional(location_range) +
    record_create_date)

# TODO: Convert this into something that uses pp.Word, and splits out authors
parenthetical = pp.QuotedString('(', endQuoteChar=')').setResultsName('author')
author = parenthetical + pp.LineEnd()
titleParts = pp.Group(pp.OneOrMore(~author + pp.Word(pp.printables))
                      ).setResultsName('title')
book_information_line_parser = titleParts + author


def date_time_to_datetime(date, time):
    ampm = time.pop()
    if(len(time) < 3):
        time.append('0')

    date_str = ("{month_name} {day_of_month:02d}, {year} "
                "{hour:02d}:{minute:02d}:{second:02d} {ampm}").format(
                    month_name=date[1],
                    day_of_month=int(date[2]),
                    year=date[3],
                    hour=int(time[0]),
                    minute=int(time[1]),
                    second=int(time[2]),
                    ampm=ampm)
    date_format = "%B %d, %Y %I:%M:%S %p"
    return datetime.datetime.strptime(date_str, date_format)


def make_clipping(book_information_line,
                  note_information_line,
                  note_contents_line):
    info = note_information_line_parser.parseString(note_information_line)
    # If present, remove the UTF-8 BOM code point
    if book_information_line.startswith(u'\ufeff'):
        book_information_line = book_information_line[1:]
    book_information_line = book_information_line.strip()
    spine = book_information_line_parser.parseString(book_information_line)
    # pprint.pprint(spine)
    record = {}
    record['title'] = ' '.join(list(spine['title']))
    authors = spine['author'].split(';')
    record['authors'] = []
    for author in authors:
        fixed = author
        if ',' in author:
            (last_name, first_name) = author.split(',')
            fixed = "{} {}".format(first_name.strip(), last_name.strip())
        record['authors'].append(fixed)
    # FIXME: Turn page and location numbers into integers?
    for key in ['type', 'pages', 'locations']:
        if key not in info:
            continue
        value = info[key]
        if type(info[key]) is pp.ParseResults:
            value = list(sorted(set(info[key])))
        record[key] = value
    if 'date' in info and 'time' in info:
        datetime = date_time_to_datetime(info['date'], info['time'])
        record['date'] = datetime.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    # if record['type'] == "Highlight":
    #     record['highlight'] = note_contents_line.strip()
    record['content'] = note_contents_line.strip()
    return record


def parse_my_clippings(clips, hide_errors=True):
    found = []
    last = None
    for book_information_line in clips:
        note_information_line = clips.next()
        clips.next()
        note_contents_line = clips.next()
        clips.next()

        clipping = None
        try:
            clipping = make_clipping(book_information_line,
                                     note_information_line,
                                     note_contents_line)
        except Exception, e:
            if hide_errors:
                continue
            else:
                raise(e)

        if clipping is None:
            continue

        if clipping['type'] == 'Note':
            last = clipping
            continue

        if (last is not None and clipping['type'] == 'Highlight'):
            loc = last['locations'][0]
            highlight_begin = clipping['locations'][0]
            highlight_end = highlight_begin
            if len(clipping['locations']) > 1:
                highlight_end = clipping['locations'][1]
            if highlight_begin <= loc <= highlight_end:
                clipping['note'] = last['content']
            last = None

        if clipping['type'] == 'Highlight':
            clipping['highlight'] = clipping['content']
            del(clipping['content'])

        found.append(clipping)

    return found
