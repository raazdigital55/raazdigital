import re,json,html
def esc(s): return html.escape(s,quote=True)
def slugify(n): return re.sub(r'^-|-$','',re.sub(r'[^a-z0-9]+','-',n.lower()))
def glyph(l,name): return l if re.fullmatch(r'[A-Za-z0-9+]{1,3}',l or '') else name[0].upper()
def fs(name,big,mid,small): n=len(name); return big if n<=16 else mid if n<=24 else small
def tile_svg(name,cat,c1,c2,letter):
    g=glyph(letter,name); gs=160 if len(g)==1 else 118 if len(g)==2 else 90
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
     f'<rect width="800" height="600" fill="url(#g)"/><circle cx="670" cy="80" r="190" fill="#fff" fill-opacity=".1"/><circle cx="110" cy="570" r="150" fill="#fff" fill-opacity=".08"/>'
     f'<rect x="270" y="70" width="260" height="260" rx="70" fill="#fff"/><text x="400" y="262" font-size="{gs}" font-weight="800" text-anchor="middle" fill="{c1}" font-family="Arial,Helvetica,sans-serif">{esc(g)}</text>'
     f'<text x="400" y="430" font-size="{fs(name,66,54,44)}" font-weight="800" text-anchor="middle" fill="#fff" font-family="Arial,Helvetica,sans-serif">{esc(name)}</text>'
     f'<text x="400" y="494" font-size="28" letter-spacing="5" text-anchor="middle" fill="#fff" fill-opacity=".88" font-family="Arial,Helvetica,sans-serif">{esc(cat.upper())}</text></svg>')
def og_svg(name,cat,c1,c2,letter):
    g=glyph(letter,name); gs=150 if len(g)==1 else 110 if len(g)==2 else 84
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
     f'<rect width="1200" height="630" fill="url(#g)"/><circle cx="1010" cy="90" r="260" fill="#fff" fill-opacity=".1"/><circle cx="140" cy="600" r="210" fill="#fff" fill-opacity=".08"/>'
     f'<rect x="470" y="60" width="260" height="260" rx="70" fill="#fff"/><text x="600" y="255" font-size="{gs}" font-weight="800" text-anchor="middle" fill="{c1}" font-family="Arial,Helvetica,sans-serif">{esc(g)}</text>'
     f'<text x="600" y="430" font-size="{fs(name,64,52,42)}" font-weight="800" text-anchor="middle" fill="#fff" font-family="Arial,Helvetica,sans-serif">{esc(name)}</text>'
     f'<text x="600" y="486" font-size="28" letter-spacing="6" text-anchor="middle" fill="#fff" fill-opacity=".88" font-family="Arial,Helvetica,sans-serif">{esc(cat.upper())}</text>'
     f'<text x="600" y="580" font-size="26" text-anchor="middle" fill="#fff" fill-opacity=".75" font-family="Arial,Helvetica,sans-serif">Buy in Bangladesh - RaaZ Digital - bKash / Nagad / Rocket</text></svg>')
