#!/usr/bin/env python3
#
# github-info.py
# Gets info from Github for my CV.
#
# Brandon Amos <http://bamos.github.io>
# 2014.02.22

from urllib.request import Request, urlopen
import json
import argparse
import sys

def getRepos(user):
  url = 'https://api.github.com/users/' + user + '/repos'
  try:
    request = Request(url)
    handler = urlopen(request)
    reposJson = json.loads(handler.read().decode('utf8'))
    handler.close()
    return reposJson
  except:
    print('Failed to get repos.')
    sys.exit(-1)

if __name__=="__main__":
  repos = getRepos('bamos')
  forkCount = len(list(filter(lambda r: r['fork'], repos)))
  origCount = len(repos) - forkCount
  print(
    "{} original repositories, {} forked repositories.".format(
      origCount,
      forkCount
    )
  )
