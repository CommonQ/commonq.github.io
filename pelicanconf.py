#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'CommonQ'
SITENAME = u"CommmonQ's Blog"
SITEURL = 'http://commonq.github.io'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zhs'

GITHUB_URL='<https://github.com/CommonQ>'

OUTPUT_PATH = '.'
ARCHIVES_URL = 'archives.html'
ARTICLE_URL = 'pages/{slug}.html'
ARTICLE_SAVE_AS = 'pages/{slug}.html'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
