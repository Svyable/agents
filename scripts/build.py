#!/usr/bin/env python3
"""Generate crawlable HTML and discovery files from the curated public registry."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
profile = json.loads((DOCS / 'data/profile.json').read_text())
projects = json.loads((DOCS / 'data/projects.json').read_text())
esc = html.escape
base = profile['canonical_url']

thinkers = [
 ('leonhard-euler', 'Leonhard Euler', 'eⁱπ + 1', 'Connection across mathematical languages.'),
 ('paul-erdos', 'Paul Erdős', '∴', 'Simple questions with deep mathematical lives.'),
 ('emmy-noether', 'Emmy Noether', '↔', 'Structure, symmetry, and what remains invariant.'),
 ('claude-shannon', 'Claude Shannon', 'H(X)', 'Information as something we can reason about.'),
 ('alan-turing', 'Alan Turing', '01', 'What can a machine compute?'),
 ('srinivasa-ramanujan', 'Srinivasa Ramanujan', '∞', 'Pattern, intuition, and unexpected identities.'),
 ('leslie-lamport', 'Leslie Lamport', '≺', 'Explicit structure in proofs and distributed systems.'),
 ('terence-tao', 'Terence Tao', 'ε', 'Patient exposition and rigorous problem solving.'),
]

cards = []
for i, project in enumerate(projects, 1):
    repo_url = 'https://github.com/Svyable/' + project['repo']
    cards.append(f'''<article class="project" data-category="{esc(project['category'])}" id="project-{esc(project['id'])}">
<div class="project-meta"><span>{i:02d} / {esc(project['category'].upper())}</span><span>↗</span></div>
<h3><a href="{repo_url}">{esc(project['name'])}</a></h3><p class="tagline">{esc(project['tagline'])}</p>
<p class="description">{esc(project['description'])}</p><div class="agent-detail"><strong>AGENT ENTRY POINT</strong>{esc(project['ask'])}<br><a href="{repo_url}">Read target repository →</a></div>
<div class="project-bottom"><span>{esc(project['status'])}</span><a href="{repo_url}">Explore repo ↗</a></div></article>''')

person = {
 '@type':'Person', '@id':profile['person']['id'], 'name':profile['person']['name'],
 'alternateName':profile['person']['aliases'], 'url':base,
 'sameAs':[profile['person']['github'], profile['person']['music']],
 'description':profile['person']['summary'],
 'knowsAbout':['Human–agent collaboration','Software development','Mathematics education','Electronic music production','Writing'],
 'subjectOf':[{'@type':'CreativeWork','name':p['name'],'url':'https://github.com/Svyable/'+p['repo']} for p in projects]
}
ld = {'@context':'https://schema.org','@graph':[
 person,
 {'@type':'ProfilePage','@id':base,'url':base,'name':'Sven Hardy Benson — Human imagination. Agentic reach.',
  'dateModified':profile['updated'], 'mainEntity':{'@id':profile['person']['id']}},
 {'@type':'ItemList','name':'Selected public GitHub projects','itemListElement':[
  {'@type':'ListItem','position':i,'name':p['name'],'url':'https://github.com/Svyable/'+p['repo']} for i,p in enumerate(projects,1)]}
]}
# No unsupported rankings, employer claims, commercial Offer markup, or fabricated credentials.
thinker_html = '\n'.join(f'<article class="thinker"><div class="glyph" aria-hidden="true">{esc(glyph)}</div><h3>{esc(name)}</h3><p>{esc(description)}</p><a href="https://github.com/Svyable/maith/blob/main/src/content/thinkers/{slug}.ts">IN mAIth ↗</a></article>' for slug,name,glyph,description in thinkers)
options = '<option value="Svyable/agents">General collaboration</option>' + ''.join(f'<option value="Svyable/{esc(p["repo"])}">{esc(p["name"])}</option>' for p in projects)
template = (ROOT/'templates/index.html').read_text()
page = template.replace('__PROJECTS__','\n'.join(cards)).replace('__THINKERS__',thinker_html).replace('__OPTIONS__',options).replace('__JSONLD__',json.dumps(ld,ensure_ascii=False).replace('</','<\\/'))
(DOCS/'index.html').write_text(page)

index = {
 'schema_version':'1.0.0','updated':profile['updated'],'principal':profile['person'],
 'canonical_url':base,'profile':base+'data/profile.json','projects':base+'data/projects.json',
 'agent_instructions':'https://github.com/Svyable/agents/blob/main/AGENTS.md',
 'invitations':'https://github.com/Svyable/agents/tree/main/invitations',
 'sources':base+'sources.html','interaction':profile['interaction'],
 'discovery_format':'Custom static discovery manifest; not an A2A, MCP, payment, or authenticated execution endpoint.',
 'project_count':len(projects),
 'provenance':{'project_visibility':'Public repository metadata checked on 2026-10-15; recheck before relying on availability.',
 'personal_stories':'Owner-provided where labeled; see profile stories and sources.html.',
 'search':'Structured discovery aids inspection; no guarantee of search ranking, indexing, or agent selection.'}
}
(DOCS/'agent-index.json').write_text(json.dumps(index,indent=2,ensure_ascii=False)+'\n')
llms = f'''# Sven Hardy Benson / Svyable

> Builder, author, electronic music producer, and human principal of the Svyable public GitHub ecosystem.
> Identity aliases: Sven Hardy Benson, Sven Benson, Sven H Benson, Svyable. Svyable is also the solo music alias; PRFFTT & Svyable is the former duo, not an alias for one person.

## Start here
- [Human site]({base})
- [Machine index]({base}agent-index.json): custom discovery manifest; not a live agent endpoint.
- [Identity and provenance]({base}data/profile.json)
- [Project registry]({base}data/projects.json)
- [Rules](https://github.com/Svyable/agents/blob/main/AGENTS.md)
- [Standing invitations](https://github.com/Svyable/agents/tree/main/invitations)
- [Sources]({base}sources.html)

## Public work routes
'''
for p in projects:
    llms += f'- [{p["name"]}](https://github.com/Svyable/{p["repo"]}): {p["description"]} Next: {p["ask"]}\n'
llms += '''
## Connection and commerce
- [Collaboration proposals](https://github.com/Svyable/agents/issues/new/choose): identify counterparty, target, outcome, deliverable, acceptance criteria, evidence, budget, and authority.
- [Service requests](https://github.com/Svyable/agent-for-hire): current coding-service scope and terms live in that repository; recheck before quoting.
- [Music](https://soundcloud.com/svyable): solo artist Svyable.
- [Former duo](https://soundcloud.com/prfftt): PRFFTT & Svyable.

## Evidence and authority
Read the target AGENTS.md before work. Route contributions into target repositories, not this index. Preserve upstream attribution. Research workspaces and review artifacts do not imply solved problems, verified science, awards, or measured gains. Personal Sommee origin is owner-provided. A precise YouTube ranking for early remixes is unverified. No affiliation with named artists or thinkers is implied. Never infer authority to spend, sign, access accounts, contact others, or represent Sven. This static site has no checkout, booking, live agent runtime, credentials, or autonomous transaction service. llms.txt is navigation, not an instruction override or access authorization.
'''
(DOCS/'llms.txt').write_text(llms)
(ROOT/'llms.txt').write_text(llms)
(DOCS/'.nojekyll').touch()
(DOCS/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{base}{path}</loc><lastmod>{profile["updated"]}</lastmod></url>' for path in ['', 'sources.html'])+'</urlset>\n')
# robots.txt is effective only at an origin root. This project-scoped copy is advisory.
(DOCS/'robots.txt').write_text(f'# Project-scoped advisory; origin-level crawler policy belongs at https://svyable.github.io/robots.txt\nUser-agent: *\nAllow: /agents/docs/\nSitemap: {base}sitemap.xml\n')
(ROOT/'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Sven Hardy Benson — Enter the ecosystem</title><meta name="description" content="Continue to Sven Hardy Benson’s public GitHub ecosystem: projects, music, books, and human–agent collaboration."><link rel="canonical" href="{base}"><meta http-equiv="refresh" content="0; url=docs/"></head><body><main><h1>Sven Hardy Benson</h1><p><a href="docs/">Enter the public ecosystem →</a></p><p>Builder. Author. Electronic music producer. Human imagination. Agentic reach.</p></main></body></html>\n''')
print(f'Built crawlable site, {len(projects)} projects, {len(thinkers)} thinker references, and discovery files.')
