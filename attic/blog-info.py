#!/usr/bin/env python3
#
# blog-posts.py
# Counts the posts in my jekyll blog.
#
# Brandon Amos
# 2013.08.10

import operator
import sys
import urllib.request
from bs4 import BeautifulSoup
import re

import html.parser; h = html.parser.HTMLParser()

def getContent(url):
  response = urllib.request.urlopen(url)
  html = response.read().decode("utf8")
  if not html: sys.exit(42)
  return h.unescape(html)

def numPostsFromArchives(archiveContent):
  soup = BeautifulSoup(archiveContent)
  mainCol = soup.find('div', attrs={'id': 'col1'})
  return len(mainCol.find_all('li'))

def parseTags(tagContent):
  soup = BeautifulSoup(tagContent)
  mainCol = soup.find('div', attrs={'id': 'col1'})
  headers = mainCol.find_all('h3')
  tags = {}
  for header in headers:
    tp = re.match("(\S*) - (\d*) Posts?", header.text)
    tags[tp.group(1)] = int(tp.group(2))

  sortedTags = sorted(tags.items(), key=operator.itemgetter(1), reverse=True)
  return [x[0] for x in sortedTags]

if __name__=='__main__':
  archiveContent = getContent('http://bamos.github.io/archives/')
  tagContent = getContent('http://bamos.github.io/tags/')
  print(
    "{} posts across the following tags, listed by highest frequency.".format(
      numPostsFromArchives(archiveContent)
    )
  )
  print(", ".join(parseTags(tagContent)))
