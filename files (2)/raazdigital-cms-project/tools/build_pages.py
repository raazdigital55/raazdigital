import sys,os,json,shutil,subprocess,tempfile,datetime
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,HERE)
from common import *
OUT=os.environ.get('SITE_OUT') or os.path.normpath(os.path.join(HERE,'..','site'))
DOMAIN=(sys.argv[1] if len(sys.argv)>1 else 'https://YOURDOMAIN.com').rstrip('/')
TMP=tempfile.mkdtemp()
def load_products():
    js="""const fs=require('fs');const s=fs.readFileSync(process.argv[2],'utf8');
const a=s.indexOf('const SETTINGS'),b=s.indexOf('const DE=PRODUCTS.map');const e=s.indexOf('\\n',b);
const r=new Function(s.slice(a,e)+';return PRODUCTS')();process.stdout.write(JSON.stringify(r))"""
    f=os.path.join(TMP,'x.js');open(f,'w').write(js)
    return json.loads(subprocess.check_output(['node',f,os.path.join(OUT,'index.html')]).decode('utf-8'))
allp=load_products()
TODAY=datetime.date.today().isoformat(); BRAND='RaaZ Digital'; WA='8801325977732'; PHONE='01325-977732'; MAIL='raazdigital55@gmail.com'
ADDR='Mirpur, Dhaka, Bangladesh'
for d in ('products',):
    shutil.rmtree(f'{OUT}/{d}',ignore_errors=True)
os.makedirs(f'{OUT}/products',exist_ok=True)
for x in allp: x['slug']=slugify(x['name'])
assert len({x['slug'] for x in allp})==len(allp),'slug clash'
def lowprice(x):
    if x.get('plans'): return min(p[1] for p in x['plans'])
    return x['price']
def cut(t,n):
    t=' '.join(t.split()); return t if len(t)<=n else t[:n-1].rsplit(' ',1)[0].rstrip('.,;—- ')+'…'
FAQ=[("How do I order?","মিরপুর"),]  # placeholder (overwritten below)
FAQ=[("How do I order?","কীভাবে অর্ডার করব?","Press Buy now, send the price by bKash, Nagad or Rocket (Send Money), then confirm with your name, number and TrxID. Your order reaches us on WhatsApp.","Buy now চাপুন, বিকাশ/নগদ/রকেটে Send Money করুন, তারপর নাম, নম্বর ও TrxID দিয়ে কনফার্ম করুন। অর্ডার আমাদের WhatsApp-এ পৌঁছে যাবে।"),
("How long does delivery take?","ডেলিভারি পেতে কত সময় লাগে?","Delivery usually happens shortly after payment is verified. It may take longer when we are busy.","পেমেন্ট যাচাইয়ের পর সাধারণত অল্প সময়ের মধ্যেই ডেলিভারি দেওয়া হয়। ব্যস্ত সময়ে একটু দেরি হতে পারে।"),
("Which payment methods do you accept?","কোন কোন মাধ্যমে পেমেন্ট করা যায়?","bKash, Nagad and Rocket — pay by Send Money. Paying from outside Bangladesh? Message us on WhatsApp.","বিকাশ, নগদ ও রকেট, Send Money করে। বাংলাদেশের বাইরে থেকে পেমেন্ট করলে WhatsApp-এ মেসেজ দিন।"),
("What if I have a problem after delivery?","ডেলিভারির পর সমস্যা হলে কী করব?","Message us on WhatsApp with a screenshot. We check the issue and try to fix it or arrange an alternative.","WhatsApp-এ স্ক্রিনশটসহ জানান। আমরা যাচাই করে সমাধান বা বিকল্পের চেষ্টা করব।"),
("How long is the validity?","মেয়াদ কতদিনের?","It depends on the plan. Check the plans on this page or confirm the duration on WhatsApp before ordering.","প্ল্যান অনুযায়ী ভিন্ন। এই পেজের প্ল্যান দেখুন বা অর্ডারের আগে WhatsApp-এ মেয়াদ জেনে নিন।")]
CSS='''*{box-sizing:border-box}:root{--bg:#060a16;--card:#0e1428;--tx:#eef1ff;--mut:#98a3c7;--pri:#8b7cff;--bd:rgba(255,255,255,.1);--gold:#f6c660;--grad:linear-gradient(135deg,#6d5efc,#9b5cff 55%,#c05cff)}
:root[data-theme=light]{--bg:#f4f6fd;--card:#fff;--tx:#0f1735;--mut:#56618a;--pri:#5b45e8;--bd:rgba(15,23,53,.12);--gold:#b45309}
body{margin:0;background:var(--bg);color:var(--tx);font-family:system-ui,-apple-system,"Segoe UI","Noto Sans Bengali",sans-serif;line-height:1.65}a{color:inherit}
.w{max-width:1100px;margin:auto;padding:0 20px}header{border-bottom:1px solid var(--bd);background:var(--card)}header .w{display:flex;align-items:center;gap:22px;padding:14px 20px;flex-wrap:wrap}
.logo{font-weight:800;font-size:20px;text-decoration:none;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}nav{display:flex;gap:18px;font-weight:600;font-size:14.5px}nav a{text-decoration:none;color:var(--mut)}nav a:hover{color:var(--tx)}
.bc{font-size:13.5px;color:var(--mut);padding:16px 0 0}.bc a{color:var(--pri);text-decoration:none}
.hero{display:grid;grid-template-columns:1.1fr 1fr;gap:34px;margin:18px 0 8px;align-items:center}@media(max-width:800px){.hero{grid-template-columns:1fr}}
.hero img{width:100%;height:auto;border-radius:22px;border:1px solid var(--bd);box-shadow:0 24px 60px -24px rgba(109,94,252,.5)}
.tag{color:var(--pri);font-weight:800;font-size:12px;letter-spacing:1.4px;text-transform:uppercase}h1{font-size:clamp(26px,4.4vw,40px);line-height:1.15;letter-spacing:-.8px;margin:8px 0 10px}
.price{font-size:32px;font-weight:800;color:var(--gold);margin:6px 0 10px}.price small{font-size:14px;color:var(--mut);font-weight:600}
.cta{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}.btn{display:inline-block;padding:13px 22px;border-radius:12px;font-weight:700;text-decoration:none;color:#fff;background:var(--grad)}.btn.wa{background:linear-gradient(135deg,#22c55e,#16a34a)}
section{margin:34px 0}h2{font-size:23px;margin:0 0 12px}.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media(max-width:700px){.cols{grid-template-columns:1fr}}
.box{background:var(--card);border:1px solid var(--bd);border-radius:18px;padding:18px 20px}.box h3{margin:0 0 8px;font-size:16px}.box ul{margin:0;padding-left:20px;color:var(--mut)}.box li{margin:4px 0}
table{width:100%;border-collapse:collapse}td,th{padding:10px 12px;border-bottom:1px solid var(--bd);text-align:left}th{color:var(--mut);font-size:13px}
details{background:var(--card);border:1px solid var(--bd);border-radius:14px;margin-top:10px}summary{cursor:pointer;padding:14px 18px;font-weight:700}details div{padding:0 18px 16px;color:var(--mut)}details p{margin:6px 0}
.rel{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px}.rel a{display:block;background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:14px;text-decoration:none}.rel b{display:block}.rel span{color:var(--gold);font-weight:700}
footer{margin-top:50px;border-top:1px solid var(--bd);background:var(--card);padding:26px 0;color:var(--mut);font-size:14px}footer a{color:var(--pri);text-decoration:none}'''
HEAD_THEME='<script>try{document.documentElement.dataset.theme=localStorage.getItem("theme")==="light"?"light":"dark"}catch(e){document.documentElement.dataset.theme="dark"}</script>'
# upgrade relative URLs to absolute at runtime (Google renders JS); keeps files domain-independent
FIX='''<script>(function(){var o=location.origin,f=function(u){return u&&u.charAt(0)=="/"?o+u:u};
var c=document.querySelector('link[rel=canonical]');if(c)c.href=f(c.getAttribute("href"));
document.querySelectorAll('meta[property="og:image"],meta[property="og:url"],meta[name="twitter:image"]').forEach(function(m){m.content=f(m.getAttribute("content"))});
var l=document.getElementById("ld");if(l){try{var j=JSON.parse(l.textContent),w=function(v){if(typeof v=="string")return f(v);if(Array.isArray(v))return v.map(w);if(v&&typeof v=="object"){for(var k in v)v[k]=w(v[k])}return v};l.textContent=JSON.stringify(w(j))}catch(e){}}})();</script>'''
def foot():
    return f'''<footer><div class="w"><b style="color:var(--tx)">{BRAND}</b> — trusted digital subscription store in Bangladesh · ডিজিটাল সাবস্ক্রিপশন স্টোর<br>📍 {ADDR} · 📞 <a href="tel:+{WA}">{PHONE}</a> · ✉ <a href="mailto:{MAIL}">{MAIL}</a><br><a href="/">Home</a> · <a href="/products/">All products</a> · <a href="/#faq">FAQ</a> · <a href="/#terms">Terms</a> · <a href="/#privacy">Privacy</a> · <a href="/#refund">Refund policy</a><br>© 2026 {BRAND}</div></footer>'''
def header():
    return f'''<header><div class="w"><a class="logo" href="/">{BRAND}</a><nav><a href="/">Home</a><a href="/products/">All products</a><a href="/#contact">Contact</a><a href="/#faq">FAQ</a></nav></div></header>'''
for x in allp:
    sl=x['slug'];n=x['name'];cat=x['category'];lp=lowprice(x);en=x['en'];bn=x['bn']
    d=f"/products/{sl}/"; img=f"{d}og.png"
    title=f"{n} Price in Bangladesh — Buy with bKash/Nagad | {BRAND}"
    pr_txt=f"from ৳{lp:,}. " if lp else ""
    desc=cut(f"Buy {n} in Bangladesh {pr_txt}{en['about']} Pay via bKash, Nagad or Rocket. WhatsApp support.",158)
    # JSON-LD
    prod={"@type":"Product","name":n,"description":en['about'],"image":[img],"category":cat,"url":d}
    if x.get('plans'):
        pr=[p[1] for p in x['plans']]
        prod["offers"]={"@type":"AggregateOffer","priceCurrency":"BDT","lowPrice":min(pr),"highPrice":max(pr),"offerCount":len(pr),"availability":"https://schema.org/InStock","url":d,"seller":{"@type":"Organization","name":BRAND}}
    elif lp:
        prod["offers"]={"@type":"Offer","priceCurrency":"BDT","price":lp,"availability":"https://schema.org/InStock","url":d,"seller":{"@type":"Organization","name":BRAND}}
    bc={"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"/"},{"@type":"ListItem","position":2,"name":"Products","item":"/products/"},{"@type":"ListItem","position":3,"name":n,"item":d}]}
    ld=json.dumps({"@context":"https://schema.org","@graph":[prod,bc]},ensure_ascii=False)
    price_html=(f'<div class="price">{"From " if x.get("plans") else ""}৳{lp:,} <small>BDT</small></div>' if lp else '<div class="price" style="font-size:20px">Contact us on WhatsApp for the price · দামের জন্য WhatsApp-এ যোগাযোগ করুন</div>')
    plans=''
    if x.get('plans'):
        plans='<section><h2>Plans &amp; prices · প্ল্যান ও দাম</h2><div class="box"><table><tr><th>Plan</th><th>Price (BDT)</th></tr>'+''.join(f'<tr><td>{esc(p[0])}</td><td>৳{p[1]:,}</td></tr>' for p in x['plans'])+'</table></div></section>'
    rel=[y for y in allp if y['category']==cat and y['slug']!=sl][:4]
    if len(rel)<4: rel+= [y for y in allp if y['category']!=cat and y['slug']!=sl][:4-len(rel)]
    rel_html=''.join(f'<a href="/products/{y["slug"]}/"><b>{esc(y["name"])}</b><small style="color:var(--mut)">{esc(y["category"])}</small><br><span>{("৳"+format(lowprice(y),",")) if lowprice(y) else "Contact us"}</span></a>' for y in rel)
    wa_msg=f"I want to buy {n} / আমি {n} কিনতে চাই"
    from urllib.parse import quote
    faq_html=''.join(f'<details><summary>{esc(q)} <span lang="bn" style="color:var(--mut);font-weight:500">· {esc(qb)}</span></summary><div><p>{esc(a)}</p><p lang="bn">{esc(ab)}</p></div></details>' for q,qb,a,ab in FAQ)
    page=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{HEAD_THEME}
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{d}"><meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="product"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{d}"><meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{img}">
<style>{CSS}</style><script type="application/ld+json" id="ld">{ld}</script></head><body>
{header()}<main class="w"><nav class="bc" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/products/">Products</a> › {esc(cat)} › {esc(n)}</nav>
<div class="hero"><img src="{img}" alt="{esc(n)} subscription price in Bangladesh — {BRAND}" width="1200" height="630" fetchpriority="high"><div><div class="tag">{esc(cat)}</div><h1>{esc(n)} Price in Bangladesh</h1>{price_html}
<p>{esc(en['about'])}</p><p lang="bn">{esc(bn['about'])}</p><div class="cta"><a class="btn" href="/#{'p-'+sl}">Buy now · কিনুন</a><a class="btn wa" href="https://wa.me/{WA}?text={quote(wa_msg)}" rel="noopener">WhatsApp</a></div></div></div>
<section class="cols"><div class="box"><h3>What you get</h3><ul>{''.join(f'<li>{esc(t)}</li>' for t in en['points'])}</ul></div><div class="box" lang="bn"><h3>কী কী পাবেন</h3><ul>{''.join(f'<li>{esc(t)}</li>' for t in bn['points'])}</ul></div></section>
{plans}
<section><h2>How to order · কীভাবে অর্ডার করবেন</h2><div class="cols"><div class="box"><ol style="margin:0;padding-left:20px;color:var(--mut)"><li>Press Buy now</li><li>Send Money via bKash, Nagad or Rocket</li><li>Confirm with your name, number and TrxID</li><li>Get delivery on WhatsApp after verification</li></ol></div><div class="box" lang="bn"><ol style="margin:0;padding-left:20px;color:var(--mut)"><li>Buy now চাপুন</li><li>বিকাশ, নগদ বা রকেটে Send Money করুন</li><li>নাম, নম্বর ও TrxID দিয়ে কনফার্ম করুন</li><li>যাচাইয়ের পর WhatsApp-এ ডেলিভারি পান</li></ol></div></div></section>
<section><h2>FAQ · সচরাচর জিজ্ঞাসা</h2>{faq_html}</section>
<section><h2>More products · আরও প্রোডাক্ট</h2><div class="rel">{rel_html}</div></section></main>{foot()}{FIX}</body></html>'''
    os.makedirs(f'{OUT}{d}',exist_ok=True)
    open(f'{OUT}{d}index.html','w',encoding='utf-8').write(page)
    open(os.path.join(TMP,f'og_{sl}.svg'),'w',encoding='utf-8').write(og_svg(n,cat,x['color'][0],x['color'][1],x['letter']))
# ---- hub page
cats=[]
for x in allp:
    if x['category'] not in cats: cats.append(x['category'])
items=''
for c in cats:
    items+=f'<section><h2>{esc(c)}</h2><div class="rel">'+''.join(f'<a href="/products/{y["slug"]}/"><b>{esc(y["name"])}</b><small style="color:var(--mut)">{esc(cut(y["en"]["about"],70))}</small><br><span>{("৳"+format(lowprice(y),",")) if lowprice(y) else "Contact us"}</span></a>' for y in allp if y['category']==c)+'</div></section>'
hub_title=f"All Digital Subscriptions & Tools in Bangladesh | {BRAND}"
hub_desc="Browse Netflix, Prime Video, YouTube Premium, ChatGPT, Claude, Canva, Adobe, VPNs and 60+ premium subscriptions in Bangladesh. Pay with bKash, Nagad or Rocket."
hub_ld=json.dumps({"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","name":hub_title,"description":hub_desc,"url":"/products/"},{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"/products/{y['slug']}/","name":y['name']} for i,y in enumerate(allp)]}]},ensure_ascii=False)
hub=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{HEAD_THEME}<title>{esc(hub_title)}</title><meta name="description" content="{esc(hub_desc)}"><link rel="canonical" href="/products/"><meta name="robots" content="index,follow"><meta property="og:type" content="website"><meta property="og:title" content="{esc(hub_title)}"><meta property="og:description" content="{esc(hub_desc)}"><style>{CSS}</style><script type="application/ld+json" id="ld">{hub_ld}</script></head><body>{header()}<main class="w"><nav class="bc"><a href="/">Home</a> › Products</nav><h1 style="margin-top:14px">All digital subscriptions &amp; tools in Bangladesh</h1><p style="color:var(--mut)">সব ডিজিটাল সাবস্ক্রিপশন ও টুল এক জায়গায় — {len(allp)}টি প্রোডাক্ট। Pay with bKash, Nagad or Rocket.</p>{items}</main>{foot()}{FIX}</body></html>'''
open(f'{OUT}/products/index.html','w',encoding='utf-8').write(hub)
# ---- sitemap + robots (replace YOURDOMAIN.com with the real domain)
urls=['/','/products/']+[f'/products/{y["slug"]}/' for y in allp]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{DOMAIN}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{"weekly" if u=="/" else "monthly"}</changefreq><priority>{"1.0" if u=="/" else "0.9" if u=="/products/" else "0.8"}</priority></url>\n' for u in urls)+'</urlset>\n'
open(f'{OUT}/sitemap.xml','w',encoding='utf-8').write(sm)
open(f'{OUT}/robots.txt','w',encoding='utf-8').write(f'User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {DOMAIN}/sitemap.xml\n')
print('pages',len(allp),'urls in sitemap',len(urls))

# ---- PNG share images (needs: npm i -g sharp) ----
png="""const sharp=require('sharp');const fs=require('fs'),path=require('path');
(async()=>{const d=process.argv[2],out=process.argv[3];let n=0;
for(const f of fs.readdirSync(d).filter(f=>/^og_.*\\.svg$/.test(f))){const sl=f.slice(3,-4);
await sharp(path.join(d,f),{density:96}).png({compressionLevel:9}).toFile(path.join(out,'products',sl,'og.png'));n++}
console.log('png images:',n)})();"""
pf=os.path.join(TMP,'png.js');open(pf,'w').write(png)
env=dict(os.environ);env['NODE_PATH']=os.path.join(HERE,'..','node_modules')+os.pathsep+subprocess.run(['npm','root','-g'],capture_output=True,text=True).stdout.strip()+os.pathsep+env.get('NODE_PATH','')
r=subprocess.run(['node',pf,TMP,OUT],env=env)
if r.returncode!=0: print('WARNING: share images (og.png) were not created — is the sharp package installed?')
shutil.rmtree(TMP,ignore_errors=True)
print('DONE. Domain used in sitemap/robots:',DOMAIN)
