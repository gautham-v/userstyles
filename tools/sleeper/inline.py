import sys
sys.argv=['x','../sleeper.css']
exec(open('gen.py').read().split("BAD_SEL")[0])
texts=[(252,43,109),(32,206,184),(89,167,255),(254,174,88),(255,42,109),(0,206,184),(0,186,255),(163,187,211),(255,166,86),(255,43,109),(255,255,255),(216,226,237),(247,92,141),(69,230,167)]
bgs=[(255,255,255),(247,92,141),(69,230,167),(89,167,255),(254,174,88),(0,206,184),(255,43,109),(32,206,184),(0,186,255)]
out=[]
for t in texts:
    v,_=role('text',(*t,1.0)); x=f'rgb({t[0]}, {t[1]}, {t[2]})'
    out.append(f'  [style^="color: {x}"], [style*="; color: {x}"] {{ color: {v} !important; }}')
for t in bgs:
    v,light=role('bg',(*t,1.0)); x=f'rgb({t[0]}, {t[1]}, {t[2]})'
    out.append(f'  [style*="background-color: {x}"], [style*="background: {x}"] {{ background-color: {v} !important; }}')
    out.append(f'  [style*="border-color: {x}"] {{ border-color: {role("border",(*t,1.0))[0]} !important; }}')
print('\n'.join(out))
