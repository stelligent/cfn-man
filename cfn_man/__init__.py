#!/usr/bin/env python

# Author: Steven Miller

import requests
import urllib
import sys
import os
import lxml.html as html
from random import randint
from subprocess import check_output
import pydoc

want_tags = ['p','h1','h2','h3','div']
want_divs = ['variablelist','aws-note','YAML']

def build_search_url():
  # Build URL to query Google
  google_url = 'https://www.google.com/search?'
  # I'm feeling lucky: go to first result
  google_url += 'btnI=1'
  # Limit results to only this specific website
  google_url += '&as_sitesearch=docs.aws.amazon.com'
  # Build query
  query = "aws cloudformation "
  for arg in sys.argv[1:]:
      query += arg + " "
  # This line escapes spaces and the like
  query = urllib.quote_plus(query.strip())
  # Attach query to URL
  return google_url + "&q=" + query

def get_docs_html_content(url):
  response = requests.get(url)
  content = []
  # Parse the raw HTML
  parsed = html.fromstring(response.text)
  # Print out the HTML elements we want
  try:
    main_content = parsed.get_element_by_id("main-col-body")
  except KeyError:
    print("Sorry! Did not find a document.")
    print(url)
    exit(1)
  for el in main_content:
    if (el.tag not in want_tags) or \
       (el.tag == 'div') and not ( \
         ('class' in el.attrib.keys() and el.attrib['class'] in want_divs) or \
         ('id' in el.attrib.keys() and el.attrib['id'] in want_divs)
       ):
      continue
    content.append(html.tostring(el))
  return "".join(content)

def format_html_content(content):
  temp_file = str(randint(0,10000000000)) + ".html"
  try:
      with open(temp_file,'w') as f:
          f.write(content)
      return check_output(['links','-dump',temp_file])
  except OSError as e:
    if '[Errno 2] No such file or directory' in str(e):
      print("OS Error: please make sure command line utility 'links' is installed")
      exit(1)
    raise e
  finally:
      os.remove(temp_file)

def main():
  if len(sys.argv) < 2:
      print("usage:\ncfn_docs security group\ncfn_docs ec2")
      exit(1)
  url = build_search_url()
  html_content = get_docs_html_content(url)
  doc = format_html_content(html_content)
  pydoc.pager(doc)
