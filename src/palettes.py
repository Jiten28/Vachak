# Generates the theme CSS and a JS table, and checks WCAG contrast for every palette in both modes.
import json
P = {
 'mayur':  ('Mayur',  'Peacock teal',   dict(bg='#DCE8E8',panel='#ECF4F3',sheet='#FBFEFD',ink='#0E2227',ink2='#3C5359',ink3='#4E656B',line='#C2D4D4',accent='#0A5563',accent2='#0F7A86',aink='#FFFFFF',soft='#CCE5E8',mark='#F4C95D',mink='#0E2227'),
                                    dict(bg='#071316',panel='#0D1D21',sheet='#12262B',ink='#E3F0EE',ink2='#AFC3C6',ink3='#8FA6AA',line='#21363B',accent='#52C6D3',accent2='#2FA3B1',aink='#04181B',soft='#133740',mark='#64490B',mink='#FFF3CF')),
 'kesari': ('Kesari', 'Saffron and maroon', dict(bg='#EBDCD2',panel='#F6ECE5',sheet='#FFFBF8',ink='#2B1511',ink2='#5A3A32',ink3='#6F5249',line='#DBC5B8',accent='#9A2A1B',accent2='#C0432A',aink='#FFFFFF',soft='#F4D6CC',mark='#FFC45E',mink='#2B1511'),
                                    dict(bg='#160B09',panel='#201210',sheet='#2A1815',ink='#F6E8E0',ink2='#CDB0A4',ink3='#B09384',line='#40251F',accent='#F59A55',accent2='#E57A33',aink='#2A1106',soft='#4A2319',mark='#6E450C',mink='#FFF1D6')),
 'neel':   ('Neel',   'Indigo and gold', dict(bg='#E0E2F0',panel='#EEF0F8',sheet='#FCFCFF',ink='#121631',ink2='#444A6E',ink3='#5B6184',line='#C8CCE3',accent='#3A3FA6',accent2='#5A5FD0',aink='#FFFFFF',soft='#DADCF6',mark='#F5CC5E',mink='#121631'),
                                    dict(bg='#090B1D',panel='#0F1229',sheet='#151936',ink='#E9EBFC',ink2='#B4B9DB',ink3='#9399BE',line='#252B52',accent='#A3ABFF',accent2='#7F89F5',aink='#0A0C25',soft='#232859',mark='#614A0E',mink='#FFF2CF')),
 'tulsi':  ('Tulsi',  'Emerald and brass', dict(bg='#DAE8DE',panel='#EAF3ED',sheet='#FAFEFB',ink='#0F2419',ink2='#3C5A4A',ink3='#4A6554',line='#C0D7C8',accent='#0C6A43',accent2='#17905F',aink='#FFFFFF',soft='#CBE8D6',mark='#ECCB5C',mink='#0F2419'),
                                    dict(bg='#06120C',panel='#0C1D14',sheet='#11271C',ink='#E1F3E8',ink2='#AECBB9',ink3='#8FAE9B',line='#1F3A2B',accent='#55D493',accent2='#34B574',aink='#03150B',soft='#123A27',mark='#604C0C',mink='#FFF3CF')),
 'gulab':  ('Gulab',  'Plum and rose',   dict(bg='#EBDCE5',panel='#F6EDF2',sheet='#FFFBFD',ink='#2A0F1F',ink2='#5C3A4D',ink3='#725065',line='#DCC4D1',accent='#8A1D5B',accent2='#B02F7C',aink='#FFFFFF',soft='#F1D4E3',mark='#F8CA7B',mink='#2A0F1F'),
                                    dict(bg='#130710',panel='#1D0D18',sheet='#271323',ink='#F7E7F0',ink2='#CFB0C2',ink3='#B293A5',line='#3C1F33',accent='#F59BC8',accent2='#E277AE',aink='#2A0A1B',soft='#4A1B38',mark='#694414',mink='#FFF1D8')),
 'kajal':  ('Kajal',  'Graphite and amber', dict(bg='#E2E2E0',panel='#EEEEEC',sheet='#FCFCFB',ink='#19191B',ink2='#48484E',ink3='#5E5E65',line='#CDCDCA',accent='#2A2A33',accent2='#4A4A57',aink='#FFFFFF',soft='#E1E1E8',mark='#F2B544',mink='#19191B'),
                                    dict(bg='#0C0C0E',panel='#141416',sheet='#1B1B1E',ink='#EEEEF0',ink2='#B9B9C0',ink3='#9A9AA3',line='#2C2C31',accent='#F3B845',accent2='#E09A1A',aink='#1A1203',soft='#3A2F12',mark='#644A0C',mink='#FFF3D0')),
 'spasht': ('Spasht', 'High contrast',   dict(bg='#FFFFFF',panel='#FFFFFF',sheet='#FFFFFF',ink='#000000',ink2='#1A1A1A',ink3='#333333',line='#000000',accent='#0020C8',accent2='#0020C8',aink='#FFFFFF',soft='#E3E8FF',mark='#FFE500',mink='#000000'),
                                    dict(bg='#000000',panel='#000000',sheet='#000000',ink='#FFFFFF',ink2='#F0F0F0',ink3='#DADADA',line='#FFFFFF',accent='#FFE500',accent2='#FFE500',aink='#000000',soft='#2A2600',mark='#FFE500',mink='#000000')),
 'kakao':  ('Cocoa',  'Vanilla, cocoa and sky', dict(bg='#F1E7D0',panel='#F7EFDC',sheet='#FBF5E6',ink='#3B2418',ink2='#614536',ink3='#745948',line='#DDCFB2',accent='#8DC2E6',accent2='#7AB4DB',aink='#2B1A10',afg='#245F8A',soft='#D9E9F4',mark='#B7DAF1',mink='#2B1A10'),
                                    dict(bg='#22150E',panel='#2B1C13',sheet='#271910',ink='#F3E9D2',ink2='#D3C3A8',ink3='#B3A187',line='#43301F',accent='#8DC2E6',accent2='#7AB4DB',aink='#1D120C',afg='#8DC2E6',soft='#27394A',mark='#285578',mink='#F4FAFF')),
 'jau':    ('Oat',    'Oat, slate and tomato', dict(bg='#F6F2E9',panel='#FAF7F0',sheet='#FDFBF7',ink='#243449',ink2='#4A5A70',ink3='#5B6A7F',line='#DAD3C4',accent='#C8351B',accent2='#B52E16',aink='#FFFFFF',afg='#B52E16',soft='#F8DDD5',mark='#F5B7A5',mink='#2A1410'),
                                    dict(bg='#18222F',panel='#1F2B3B',sheet='#1B2634',ink='#F2EDE0',ink2='#BFC6D2',ink3='#9CA6B6',line='#33425A',accent='#FF6A4D',accent2='#F25B3A',aink='#1A0A06',afg='#FF8C73',soft='#3E2A2B',mark='#8F3523',mink='#FFF1EC')),
 'ranga':  ('Racing', 'Champagne, black and green', dict(bg='#EFE7D0',panel='#F6F0DD',sheet='#FAF6E8',ink='#121413',ink2='#3E433F',ink3='#555A54',line='#DCD3B6',accent='#0F4A36',accent2='#0A3A29',aink='#F3E7BC',afg='#0F4A36',soft='#DDE5D3',mark='#E7D79F',mink='#121413'),
                                    dict(bg='#0C2B21',panel='#113628',sheet='#0F3125',ink='#F1E9CC',ink2='#CFC8A8',ink3='#A9B39A',line='#1F4A39',accent='#D8BE7E',accent2='#C4A85F',aink='#0D0F0E',afg='#D8BE7E',soft='#1B4434',mark='#5E4E1D',mink='#FFF8E0')),
 'tamra':  ('Tamra',  'Pearl, charcoal and copper', dict(bg='#EDEBEE',panel='#F4F3F5',sheet='#F9F8FA',ink='#1D212B',ink2='#464C5B',ink3='#5A6070',line='#D8D6DC',accent='#AC5B2A',accent2='#9A4A1E',aink='#FFFFFF',afg='#9A4A1E',soft='#F3E0D3',mark='#F2C7A6',mink='#2A1608'),
                                    dict(bg='#10161E',panel='#171F29',sheet='#141B24',ink='#EAEEF3',ink2='#B6C0CC',ink3='#95A2B2',line='#27323F',accent='#E39A66',accent2='#D98A54',aink='#1F1007',afg='#EDA878',soft='#352A22',mark='#7A4519',mink='#FFF1E4')),
}
def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    x,y=lum(a),lum(b); x,y=max(x,y),min(x,y); return (x+0.05)/(y+0.05)
for _k,(_n,_d,_l,_dk) in P.items():
    _l.setdefault('afg',_l['accent']); _dk.setdefault('afg',_dk['accent'])
checks=[('ink','bg',7),('ink','sheet',7),('ink2','sheet',4.5),('ink2','panel',4.5),('ink2','bg',4.5),('ink3','sheet',4.5),('ink3','panel',4.5),('ink3','bg',4.5),('aink','accent',4.5),('afg','sheet',4.5),('afg','soft',4.5),('mink','mark',7),('afg','panel',4.5),('ink2','soft',4.5)]
bad=0
for k,(n,d,l,dk) in P.items():
    for mode,t in (('light',l),('dark',dk)):
        for a,b,need in checks:
            r=cr(t[a],t[b])
            if r<need: bad+=1; print('LOW',k,mode,a,'on',b,round(r,2),'need',need)
print('contrast problems:',bad)
names={'bg':'bg','panel':'panel','sheet':'sheet','ink':'ink','ink2':'ink-2','ink3':'ink-3','line':'line','accent':'accent','accent2':'accent-2','afg':'accent-fg','aink':'accent-ink','soft':'accent-soft','mark':'mark','mink':'mark-ink'}
def block(t): return ';'.join('--%s:%s'%(names[k],v) for k,v in t.items())
css=[]
first=list(P)[0]
css.append(':root{%s;color-scheme:light}'%block(P[first][2]))
css.append('@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){%s;color-scheme:dark}}'%block(P[first][3]))
for k,(n,d,l,dk) in P.items():
    css.append(':root[data-palette="%s"][data-theme="light"]{%s;color-scheme:light}'%(k,block(l)))
    css.append(':root[data-palette="%s"][data-theme="dark"]{%s;color-scheme:dark}'%(k,block(dk)))
open(__import__('os').path.dirname(__import__('os').path.abspath(__file__))+'/palettes.css','w').write('\n'.join(css))
js={k:dict(name=n,desc=d,light=dict(bg=l['bg'],sheet=l['sheet'],accent=l['accent'],mark=l['mark']),dark=dict(bg=dk['bg'],sheet=dk['sheet'],accent=dk['accent'],mark=dk['mark'])) for k,(n,d,l,dk) in P.items()}
open(__import__('os').path.dirname(__import__('os').path.abspath(__file__))+'/palettes.json','w').write(json.dumps(js,separators=(',',':')))
