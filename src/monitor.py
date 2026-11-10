"""Public-page change monitor. No authentication or paywall bypass."""
import argparse
import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from html.parser import HTMLParser

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','noscript'): self.skip+=1
    def handle_endtag(self, tag):
        if tag in ('script','style','noscript') and self.skip: self.skip-=1
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def normalize_html(raw):
    parser=VisibleText(); parser.feed(raw)
    return re.sub(r'\s+', ' ', ' '.join(parser.parts)).strip()

def fingerprint(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def fetch(url, timeout=15):
    if not url.startswith('https://'):
        raise ValueError('Only HTTPS URLs are supported')
    request=urllib.request.Request(url,headers={'User-Agent':'CompetitorRadarAI/0.1 (public change monitor; contact via repository)'})
    with urllib.request.urlopen(request,timeout=timeout) as response:
        content_type=response.headers.get('Content-Type','')
        if 'text/html' not in content_type:
            raise ValueError('Expected HTML content')
        raw=response.read(2_000_000)
    return normalize_html(raw.decode('utf-8',errors='replace'))

def run(config_path, state_path, report_path):
    entries=json.loads(Path(config_path).read_text(encoding='utf-8'))['competitors']
    state_file=Path(state_path)
    previous=json.loads(state_file.read_text(encoding='utf-8')) if state_file.exists() else {}
    current=dict(previous)
    results=[]
    for entry in entries:
        name,url=entry['name'],entry['url']
        try:
            text=fetch(url)
            digest=fingerprint(text)
            old=previous.get(name,{}).get('hash')
            status='baseline' if old is None else ('changed' if old!=digest else 'unchanged')
            current[name]={'url':url,'hash':digest,'last_checked':datetime.now(timezone.utc).isoformat()}
            results.append({'name':name,'url':url,'status':status,'excerpt':text[:220]})
        except Exception as exc:
            results.append({'name':name,'url':url,'status':'error','error':str(exc)})
    state_file.parent.mkdir(parents=True,exist_ok=True)
    state_file.write_text(json.dumps(current,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    report=Path(report_path);report.parent.mkdir(parents=True,exist_ok=True)
    lines=['# Competitor Radar AI — Change Report','',f'Generated: {datetime.now(timezone.utc).isoformat()}','', 'Status: baseline = first observation; changed = page text changed; unchanged = same text; error = collection failed.','']
    for item in results:
        lines += [f"## {item['name']} — {item['status']}",item['url'],item.get('error',item.get('excerpt','')),'']
    report.write_text('\n'.join(lines),encoding='utf-8')
    return results

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',default='config/competitors.example.json');p.add_argument('--state',default='data/state.json');p.add_argument('--report',default='reports/latest.md');a=p.parse_args()
    results=run(a.config,a.state,a.report)
    print(json.dumps(results,ensure_ascii=False,indent=2))
