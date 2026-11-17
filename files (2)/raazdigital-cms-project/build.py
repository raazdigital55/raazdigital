#!/usr/bin/env python3
"""Builds the website into dist/ from content/ (edited in the /admin dashboard).
   Cloudflare Pages runs:   npm install && python3 build.py     output folder: dist
"""
import os,sys,json,glob,shutil,subprocess
ROOT=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(ROOT,'tools'))
from common import slugify,tile_svg
DIST=os.path.join(ROOT,'dist')
def load(p): return json.load(open(p,encoding='utf-8'))
def num(v):
    if v in (None,''): return None
    try: f=float(v); return int(f) if f==int(f) else f
    except (TypeError,ValueError): return None
def strs(v):
    out=[]
    for x in (v or []):
        if isinstance(x,dict): x=next(iter(x.values()),'')
        x=str(x).strip()
        if x: out.append(x)
    return out
def js(obj):  # safe to embed inside <script>
    return json.dumps(obj,ensure_ascii=False).replace('</','<\\/').replace('\u2028','\\u2028').replace('\u2029','\\u2029')

settings=load(os.path.join(ROOT,'content','settings.json'))
rows=[]
for f in sorted(glob.glob(os.path.join(ROOT,'content','products','*.json'))):
    d=load(f)
    name=str(d.get('name','')).strip(); cat=str(d.get('category','')).strip()
    if not name or not cat: print('WARNING: skipped (needs name and category):',os.path.basename(f)); continue
    rows.append((num(d.get('order')) if num(d.get('order')) is not None else 9999,name.lower(),d))
rows.sort(key=lambda r:(r[0],r[1]))
shutil.rmtree(DIST,ignore_errors=True)
shutil.copytree(os.path.join(ROOT,'static'),DIST)
os.makedirs(os.path.join(DIST,'images','tiles'),exist_ok=True)
products=[];seen=set()
for _,_,d in rows:
    name=d['name'].strip(); cat=d['category'].strip(); sl=slugify(name)
    if sl in seen: sys.exit(f'ERROR: two products make the same web address "{sl}" — rename one: {name}')
    seen.add(sl)
    c1=d.get('color1') or '#2563eb'; c2=d.get('color2') or '#1e3a8a'; letter=(d.get('letter') or '').strip()
    img=(d.get('image') or '').strip()
    if not img:   # no picture uploaded → draw a branded tile
        open(os.path.join(DIST,'images','tiles',sl+'.svg'),'w',encoding='utf-8').write(tile_svg(name,cat,c1,c2,letter or name[0].upper()))
        img=f'/images/tiles/{sl}.svg'
    plans=[[str(p.get('label','')).strip(),num(p.get('price'))] for p in (d.get('plans') or []) if isinstance(p,dict) and num(p.get('price')) is not None and str(p.get('label','')).strip()]
    bn={'about':(d.get('about_bn') or '').strip(),'points':strs(d.get('points_bn'))}
    en={'about':(d.get('about_en') or '').strip(),'points':strs(d.get('points_en'))}
    products.append({'name':name,'category':cat,'price':num(d.get('price')),'badge':(d.get('badge') or '').strip(),'letter':letter or name[0].upper(),
        'color':[c1,c2],'image':img,'plans':plans,'bn':bn,'en':en})
tpl=open(os.path.join(ROOT,'template','index.template.html'),encoding='utf-8').read()
assert '__SETTINGS__' in tpl and '__PRODUCTS__' in tpl
open(os.path.join(DIST,'index.html'),'w',encoding='utf-8').write(tpl.replace('__SETTINGS__',js(settings)).replace('__PRODUCTS__',js(products)))
env=dict(os.environ); env['SITE_OUT']=DIST
subprocess.run([sys.executable,os.path.join(ROOT,'tools','build_pages.py'),settings.get('siteUrl') or 'https://YOURDOMAIN.com'],check=True,env=env)
print(f'BUILD OK — {len(products)} products → {DIST}')
