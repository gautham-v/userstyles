import re, colorsys, collections, sys
src = open(sys.argv[1]).read()
src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
# drop @keyframes / @font-face blocks entirely
def strip_blocks(s, kw):
    out=[];i=0
    while True:
        j=s.find(kw,i)
        if j<0: out.append(s[i:]); break
        out.append(s[i:j]); k=s.find('{',j); depth=0; m=k
        while m<len(s):
            if s[m]=='{': depth+=1
            elif s[m]=='}':
                depth-=1
                if depth==0: break
            m+=1
        i=m+1
    return ''.join(out)
for kw in ('@keyframes','@-webkit-keyframes','@font-face','@-moz-keyframes'):
    src=strip_blocks(src,kw)
rules = re.findall(r'([^{}@;]+)\{([^{}]*)\}', src)

COL = re.compile(r'#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)', re.I)
def parse(c):
    c=c.lower()
    if c.startswith('#'):
        h=c[1:]
        if len(h) in (3,4): h=''.join(x*2 for x in h)
        if len(h) not in (6,8): return None
        return int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),(int(h[6:8],16)/255 if len(h)==8 else 1.0)
    n=[float(x) for x in re.findall(r'[\d.]+',c)]
    if len(n)<3: return None
    return n[0],n[1],n[2],(n[3] if len(n)>3 else 1.0)

def alpha(expr,a):
    if a>=0.995: return expr
    if a<=0.005: return 'transparent'
    return f'color-mix(in srgb, {expr} {round(a*100)}%, transparent)'

POSN=re.compile(r'\.(qb|rb|wr|te|k|def|dl|lb|db|flex|super_flex|rec_flex|wrrb_flex|idp_flex)(?![\w-])', re.I)
def role(kind, rgba, pos=False):
    r,g,b,a = rgba
    h,l,s = colorsys.rgb_to_hls(r/255,g/255,b/255)
    H=h*360
    chroma = s>0.45 and 0.15<l<0.92
    raw=f'rgb({int(r)} {int(g)} {int(b)})'
    if chroma:
        muted=f'color-mix(in oklab, {raw} 50%, var(--c-text))'
        brand = 160<=H<=235 and not pos
        if kind=='bg':
            if brand: return alpha('var(--c-accent)',a), (a>0.6)
            return alpha(muted,a), (a>0.6)
        if kind=='border':
            if brand: return alpha('var(--c-accent)',a), False
            return alpha(f'color-mix(in oklab, {raw} 40%, var(--c-line))',a), False
        if brand: return alpha('var(--c-accent)',a), False
        return alpha(muted,a), False
    # neutral / navy
    if kind=='bg':
        if a<0.995:
            base = 'var(--c-text)' if l>0.5 else 'var(--c-line)'
            if l<=0.05: return f'color-mix(in srgb, #000 {round(a*100)}%, transparent)', False  # scrims
            return alpha(base,a), False
        if l<0.135: return 'var(--c-bg)', False
        if l<0.2:  return 'var(--c-surface)', False
        if l<0.33: return 'var(--c-raised)', False
        if l<0.5:  return 'var(--c-line)', False
        if l<0.8:  return 'var(--c-dim)', False
        return 'var(--c-accent)', True
    if kind=='border':
        return alpha('var(--c-line)',a), False
    # text
    if l>=0.8:  return alpha('var(--c-text)',a), False
    if l>=0.45: return alpha('var(--c-dim)',a), False
    return alpha('var(--c-on-accent)',a), False

BAD_SEL = re.compile(r'::?-(webkit|moz|ms)-|^\s*(from|to|\d+(\.\d+)?%)\s*$', re.I)
groups = collections.OrderedDict()
def add(sel, prop, val):
    groups.setdefault((prop,val),[]).append(sel)

def emit(sels, body, pos):
    decls=[d for d in body.split(';') if ':' in d]
    on_light_bg=False; has_color=False
    for d in decls:
        p,v=d.split(':',1); p=p.strip().lower(); v=v.strip()
        cols=COL.findall(v)
        if not cols: continue
        if p in ('background','background-color','background-image'):
            if 'gradient' in v:
                rg=parse(cols[0])
                if rg:
                    val,light=role('bg',rg,pos); on_light_bg|=light
                    for s_ in sels: add(s_,'background-image','none'); add(s_,'background-color',val)
                continue
            if p=='background-image': continue
            rg=parse(cols[0])
            if rg:
                val,light=role('bg',rg,pos); on_light_bg|=light
                for s_ in sels: add(s_,'background-color',val)
        elif p=='color':
            rg=parse(cols[0])
            if rg:
                has_color=True
                val,_=role('text',rg,pos)
                for s_ in sels: add(s_,'color',val)
        elif p in ('border-color','border','border-top','border-bottom','border-left','border-right',
                   'border-top-color','border-bottom-color','border-left-color','border-right-color','outline','outline-color'):
            rg=parse(cols[0])
            if rg:
                val,_=role('border',rg,pos)
                prop = p if p.endswith('-color') else p+'-color'
                for s_ in sels: add(s_,prop,val)
        elif p in ('fill','stroke'):
            rg=parse(cols[0])
            if rg:
                val,_=role('text',rg,pos)
                for s_ in sels: add(s_,p,val)
    if on_light_bg and not has_color:
        for s_ in sels: add(s_,'color','var(--c-on-accent)')

for sel, body in rules:
    allsels=[x.strip() for x in sel.split(',') if x.strip() and not BAD_SEL.search(x)]
    if not allsels: continue
    for pos in (False, True):
        sels=[x for x in allsels if bool(POSN.search(x))==pos]
        if sels: emit(sels, body, pos)

out=[]
for (prop,val),sels in groups.items():
    # dedupe, keep order
    seen=set(); ss=[x for x in sels if not (x in seen or seen.add(x))]
    for i in range(0,len(ss),60):
        chunk=ss[i:i+60]
        out.append(',\n'.join('  '+x for x in chunk)+f' {{ {prop}: {val} !important; }}')
print('\n'.join(out))
