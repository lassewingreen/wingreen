from pathlib import Path
import json, html
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether

root=Path(__file__).parent
d=json.loads((root/'content.json').read_text())
e=html.escape

def header(active):
    nav=''.join(f'<a href="{url}"'+(' aria-current="page"' if key==active else '')+f'>{label}</a>' for key,url,label in [('letter','dedalus.html','Application'),('cv','cv.html','CV')])
    return f'''<a class="skip-link" href="#main">Skip to content</a><header class="masthead"><div class="wrap topbar"><a class="identity" href="dedalus.html" aria-label="Lasse Wingreen application"><span class="mark" aria-hidden="true">lw.</span><span>Lasse Wingreen</span></a><nav class="nav" aria-label="Main navigation">{nav}<a class="contact-link" href="mailto:{d['email']}">Get in touch ↗</a></nav></div></header>'''

def footer():
    return f'''<footer class="footer"><div class="wrap footer-inner"><div><span class="footer-name">Lasse Wingreen</span><br>Product Owner · Aarhus, Denmark</div><div class="footer-links"><a href="mailto:{d['email']}">{d['email']}</a><a href="tel:+4528578189">{d['phone']}</a><a href="{d['linkedin']}">LinkedIn ↗</a><button class="print-button" data-print hidden>Print this page</button></div></div></footer>'''

def print_header(sub):
    return f'<div class="print-only print-header"><h1>Lasse Wingreen</h1><p>{sub}</p><p>Aarhus, Denmark · {d["email"]} · {d["phone"]}</p></div>'

def page(title,description,body):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{e(description)}"><meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#162f3e"><title>{e(title)}</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css?v=2"><script src="site.js" defer></script></head><body>{body}</body></html>'''

wave='<div class="wave" aria-hidden="true">'+''.join(f'<i style="--h:{h}px"></i>' for h in [4,7,12,8,16,22,14,8,12,19,24,15,7,4,8,14,19,12,6,3,6,10,6,3])+'</div>'
letter_paras=''.join('<p>'+e(p)+'</p>' for p in d['letter'])
projects=''.join(f'<div class="project-row"><span class="project-number">{p["number"]}</span><div><h3>{e(p["title"])}</h3><span class="product">{e(p["product"])}</span></div><p>{e(p["text"])}</p></div>' for p in d['projects'])
letter_body=header('letter')+f'''<main id="main" class="wrap"><section class="hero" aria-labelledby="name"><div><p class="eyebrow">Product Owner / Aarhus, Denmark</p><h1 id="name">Lasse <span class="surname">Wingreen<span class="period">.</span></span></h1><p class="subtitle">A background in understanding customers.<br>A focus on defining useful software.</p></div><div class="hero-side"><p class="eyebrow">An application to</p><h2>Dedalus</h2><p>Product Owner · Aarhus<br>28 October 2026</p><a class="button" href="Lasse-Wingreen-Dedalus-Application.pdf" download>Download application <span class="arrow" aria-hidden="true">↓</span></a></div></section><div class="context-strip"><span>Customer support → Implementation → Product ownership</span><span>iPaper · 2017–2026</span></div>{print_header('Application for Product Owner at Dedalus · 28 October 2026')}<div class="document-layout"><aside aria-label="Application context"><p class="section-index">01 / Application</p><h2 class="aside-title">Good work starts<br>with listening.</h2><p class="aside-note">Bringing customer understanding and technical curiosity into product work.</p><a class="aside-link" href="cv.html">Explore my experience ↗</a>{wave}</aside><article class="letter" aria-labelledby="letter-title"><h2 id="letter-title">From understanding users<br>to defining the product.</h2><p class="salutation">Dear Dedalus team,</p>{letter_paras}<p class="signoff">Best regards,<span class="signature">Lasse Wingreen</span></p></article></div><section class="selected" aria-labelledby="selected-title"><div class="section-heading"><h2 id="selected-title">Selected product work</h2><span>Specifications and collaboration at iPaper</span></div>{projects}</section><section class="closing" aria-labelledby="conversation-title"><div><h2 id="conversation-title">Let's talk about your product.</h2><p>{d['email']} · {d['phone']}</p></div><a class="button secondary" href="mailto:{d['email']}?subject=Product%20Owner%20at%20Dedalus">Get in touch <span class="arrow" aria-hidden="true">↗</span></a></section></main>'''+footer()
(root/'dedalus.html').write_text(page('Lasse Wingreen · Product Owner application to Dedalus','Application to Dedalus from Lasse Wingreen, a Product Owner with a background in SaaS support, implementation and digital design.',letter_body))

roles=''.join(f'<section class="role"><h4>{e(r["title"])}</h4><div class="date">{e(r["dates"])}</div><ul>'+''.join(f'<li>{e(b)}</li>' for b in r['bullets'])+'</ul></section>' for r in d['roles'])
earlier=''.join(f'<article class="past-role"><h3>{e(r["title"])}</h3><p class="role-meta">{e(r["company"])}'+(' · ' if r['company'] else '')+f'{e(r["dates"])}</p><p>{e(r["description"])}</p></article>' for r in d['earlier'])
education=''.join(f'<article><h3>{e(r["title"])}</h3><p>{e(r["detail"])}</p><span class="date">{e(r["dates"])}</span></article>' for r in d['education'])
skill_blocks=''.join(f'<p><strong>{e(s["title"])}</strong><br>{e(s["detail"])}</p>' for s in d['skills'])
cv_body=header('cv')+f'''<main id="main" class="wrap"><section class="hero compact" aria-labelledby="name"><div><p class="eyebrow">Curriculum vitae / 2026</p><h1 id="name">Lasse <span class="surname">Wingreen<span class="period">.</span></span></h1><p class="subtitle">Product Owner · SaaS · Digital Design</p></div><div class="hero-side"><p class="eyebrow">Experience, in context</p><h2>From customer needs<br>to product specifications.</h2><p>Based in Aarhus, Denmark</p><a class="button" href="Lasse-Wingreen-CV.pdf" download>Download CV <span class="arrow" aria-hidden="true">↓</span></a></div></section><div class="context-strip"><span>Product specifications · Accessibility · Developer collaboration</span><span>English CV / 2-page PDF</span></div>{print_header('Product Owner · SaaS · Digital Design')}<div class="cv-layout"><aside class="cv-sidebar" aria-label="Contact and skills"><section><h2>Contact</h2><p>Aarhus, Denmark<br><a href="mailto:{d['email']}">{d['email']}</a><br><a href="tel:+4528578189">{d['phone']}</a><br><a href="{d['linkedin']}">LinkedIn ↗</a></p></section><section><h2>Languages</h2><p>{e(d['languages'])}</p></section><section><h2>Capabilities</h2>{skill_blocks}</section></aside><div class="cv-main"><section aria-labelledby="profile-title"><h2 id="profile-title">Profile</h2><p class="profile">{e(d['profile'])}</p></section><section aria-labelledby="experience-title"><h2 id="experience-title">Experience</h2><div class="company-heading"><div><h3>iPaper</h3><p>B2B SaaS · Aarhus</p></div><span class="date">Nov 2017 – 2026</span></div>{roles}</section><section class="earlier-section" aria-labelledby="earlier-title"><h2 id="earlier-title">Earlier experience</h2>{earlier}</section><section aria-labelledby="education-title"><h2 id="education-title">Education</h2><div class="education">{education}</div></section><section class="print-only print-skills"><h2>Capabilities & languages</h2>{skill_blocks}<p>{e(d['languages'])}</p></section><section aria-labelledby="personal-title"><h2 id="personal-title">Beyond work</h2><p class="profile">{e(d['personal'])}</p></section></div></div><section class="closing" aria-labelledby="cv-contact"><div><h2 id="cv-contact">A conversation is a good start.</h2><p>{d['email']} · {d['phone']}</p></div><a class="button secondary" href="dedalus.html">Read my application <span class="arrow" aria-hidden="true">↗</span></a></section></main>'''+footer()
(root/'cv.html').write_text(page('Lasse Wingreen · Product Owner CV','The CV of Lasse Wingreen: Product Owner with experience in SaaS implementation, customer support, accessibility and digital design.',cv_body))
(root/'index.html').write_text(page('Lasse Wingreen · Career documents','Application and CV for Lasse Wingreen.',header('letter')+'<main id="main" class="wrap"><section class="hero"><div><p class="eyebrow">Career documents / 2026</p><h1>Lasse Wingreen<span class="period">.</span></h1><p><a href="dedalus.html">Read my Dedalus application ↗</a></p><p><a href="cv.html">View my CV ↗</a></p></div></section></main>'+footer()))
(root/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="8" fill="#162f3e"/><text x="9" y="44" font-family="Georgia,serif" font-size="40" fill="#fff">lw.</text></svg>')

# PDFs use the same content as the HTML, in a linear reading order.
for name,file,fallback in [('Arial','Arial.ttf','Helvetica'),('ArialBold','Arial Bold.ttf','Helvetica-Bold'),('Georgia','Georgia.ttf','Times-Roman')]:
    fontpath=Path('/System/Library/Fonts/Supplemental')/file
    if fontpath.exists():
        pdfmetrics.registerFont(TTFont(name,str(fontpath)))
    else:
        pdfmetrics.registerFont(pdfmetrics.Font(name,fallback,'WinAnsiEncoding'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold',italic='Arial',boldItalic='ArialBold')
ink=colors.HexColor('#162f3e'); blue=colors.HexColor('#146c86'); muted=colors.HexColor('#5f7079')
styles={
 'name':ParagraphStyle('name',fontName='Georgia',fontSize=30,leading=36,textColor=ink,spaceAfter=6),
 'subtitle':ParagraphStyle('subtitle',fontName='Arial',fontSize=10,leading=14,textColor=blue,spaceAfter=7),
 'contact':ParagraphStyle('contact',fontName='Arial',fontSize=8.5,leading=13,textColor=muted,spaceAfter=16),
 'h2':ParagraphStyle('h2',fontName='Georgia',fontSize=17,leading=21,textColor=ink,spaceBefore=12,spaceAfter=8),
 'h3':ParagraphStyle('h3',fontName='ArialBold',fontSize=10.7,leading=14,textColor=ink,spaceBefore=8,spaceAfter=2),
 'meta':ParagraphStyle('meta',fontName='Arial',fontSize=8.5,leading=12,textColor=muted,spaceAfter=5),
 'body':ParagraphStyle('body',fontName='Arial',fontSize=9.6,leading=14,textColor=ink,spaceAfter=7),
 'bullet':ParagraphStyle('bullet',fontName='Arial',fontSize=9.3,leading=13.7,textColor=ink,leftIndent=11,firstLineIndent=-9,spaceAfter=4),
 'letter':ParagraphStyle('letter',fontName='Arial',fontSize=10.2,leading=15.3,textColor=ink,spaceAfter=11),
}
def p(text,sty='body'):return Paragraph(escape(text),styles[sty])
def boldline(title,text):return Paragraph('<b>'+escape(title)+'</b> '+escape(text),styles['body'])
def pdf_header(sub):
    return [p(d['name'],'name'),p(sub,'subtitle'),p(d['location']+'  |  '+d['email']+'  |  '+d['phone'],'contact')]
def foot(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(colors.HexColor('#cdd7d9'));canvas.line(45,40,A4[0]-45,40)
    canvas.setFont('Arial',8);canvas.setFillColor(muted);canvas.drawString(45,27,'Lasse Wingreen  |  '+d['email']);canvas.drawRightString(A4[0]-45,27,str(doc.page));canvas.restoreState()
def doc(name,story):
    pdf=SimpleDocTemplate(str(root/name),pagesize=A4,rightMargin=45,leftMargin=45,topMargin=39,bottomMargin=53,title=name.replace('-',' ').replace('.pdf',''),author=d['name'])
    pdf.build(story,onFirstPage=foot,onLaterPages=foot)

story=pdf_header('Application for Product Owner at Dedalus  |  28 October 2026')
story+=[p('Dear Dedalus team,','h3'),Spacer(1,8)]
story += [p(t,'letter') for t in d['letter']]
story += [Spacer(1,5),p('Best regards,','letter'),p('Lasse Wingreen','h2')]
doc('Lasse-Wingreen-Dedalus-Application.pdf',story)

story=pdf_header('Product Owner  |  SaaS  |  Digital Design')
story += [p('Profile','h2'),p(d['profile']),p('Experience','h2'),p('iPaper · Aarhus','h3'),p('Nov 2017 – 2026  |  B2B SaaS','meta')]
for r in d['roles']:
    block=[p(r['title'],'h3'),p(r['dates'],'meta')]+[p('• '+b,'bullet') for b in r['bullets']]
    story.append(KeepTogether(block))
story += [PageBreak(),p('Lasse Wingreen','h2'),p('Earlier experience','h2')]
for r in d['earlier']:
    story.append(KeepTogether([p(r['title'],'h3'),p((r['company']+'  |  ' if r['company'] else '')+r['dates'],'meta'),p(r['description'])]))
story += [p('Education','h2')]
for r in d['education']:
    story.append(KeepTogether([p(r['title'],'h3'),p(r['detail']+'  |  '+r['dates'],'meta')]))
story += [p('Capabilities','h2')]+[boldline(s['title']+'.',s['detail']) for s in d['skills']]
story += [boldline('Languages.',d['languages']),p('Beyond work','h2'),p(d['personal']),p('LinkedIn: linkedin.com/in/lassewingreen','meta')]
doc('Lasse-Wingreen-CV.pdf',story)
print('Built HTML and PDFs in',root)
print('Letter words:',sum(len(x.split()) for x in d['letter']))
