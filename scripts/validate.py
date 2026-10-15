#!/usr/bin/env python3
"""Check public routing, crawlability, structured identity, and local assets."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.h1s = 0
        self.ld = []
        self.in_ld = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            require(attrs['id'] not in self.ids, f'Duplicate id: {attrs["id"]}')
            self.ids.add(attrs['id'])
        if tag == 'h1':
            self.h1s += 1
        for attribute in ['href', 'src']:
            if attribute in attrs:
                self.links.append(attrs[attribute])
        self.in_ld = tag == 'script' and attrs.get('type') == 'application/ld+json'
    def handle_data(self, data):
        if self.in_ld:
            self.ld.append(data)
    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_ld = False

pages = {}
for path in DOCS.rglob('*.html'):
    page = Page()
    text = path.read_text()
    page.feed(text)
    pages[path.resolve()] = page
    require(page.h1s == 1, f'{path.name}: expected one H1')
    require(not re.search(r'__[A-Z]+__', text), f'{path.name}: unresolved template token')
    require('name="description"' in text, f'{path.name}: missing description')
    require('rel="canonical"' in text, f'{path.name}: missing canonical')
for path, page in pages.items():
    for link in page.links:
        url = urlsplit(link)
        require(url.scheme not in ['javascript', 'data'], f'Unsafe link: {link}')
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir():
            target /= 'index.html'
        require(target.is_file(), f'{path.name}: missing local file {link}')
        if url.fragment and target in pages:
            require(unquote(url.fragment) in pages[target].ids, f'{path.name}: missing fragment {link}')

profile = json.loads((DOCS/'data/profile.json').read_text())
projects = json.loads((DOCS/'data/projects.json').read_text())
manifest = json.loads((DOCS/'agent-index.json').read_text())
require(len(projects) == manifest['project_count'], 'Manifest project count drift')
require(len({p['id'] for p in projects}) == len(projects), 'Duplicate project id')
require(len({p['repo'] for p in projects}) == len(projects), 'Duplicate project repo')
require(profile['person']['name'] == 'Sven Hardy Benson', 'Public identity drift')
require(profile['interaction']['delegated_authority'] == 'none', 'Unapproved authority claim')
require(not profile['interaction']['payments_enabled_here'], 'Unsupported payment capability')
index = pages[(DOCS/'index.html').resolve()]
ld = json.loads(''.join(index.ld))
person = next(item for item in ld['@graph'] if item['@type'] == 'Person')
require(person['name'] == profile['person']['name'], 'Structured identity mismatch')
require(person['@id'] == profile['person']['id'], 'Structured identity id mismatch')
for project in projects:
    require('project-'+project['id'] in index.ids, f'Project missing from static HTML: {project["id"]}')
    require('https://github.com/Svyable/'+project['repo'] in index.links, 'Missing repository route')
require((ROOT/'llms.txt').read_bytes() == (DOCS/'llms.txt').read_bytes(), 'llms.txt mirrors differ')
for prohibited in ['Svyable/sommee', 'Svyable/Sommyv2', 'Svyable/SSNC', 'Svyable/innerbull', 'Svyable/omega-race', 'Svyable/vintage-era-radio']:
    for path in [DOCS/'index.html', DOCS/'data/projects.json', DOCS/'agent-index.json', ROOT/'README.md']:
        require(prohibited not in path.read_text(), f'Private repo link exposed: {prohibited} in {path.name}')
require('sgsllc-jr/zarr-pyramid-audit' in (DOCS/'data/projects.json').read_text(), 'Missing upstream credit')
for path in DOCS.rglob('*.json'):
    json.loads(path.read_text())
if errors:
    print('\n'.join('ERROR: '+error for error in errors), file=sys.stderr)
    sys.exit(1)
print(f'Validated {len(pages)} static pages, {len(projects)} project routes, local links, JSON-LD, and authority/provenance boundaries.')
