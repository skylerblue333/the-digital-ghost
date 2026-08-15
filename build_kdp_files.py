from pathlib import Path
import markdown
from weasyprint import HTML
import zipfile
import shutil

ROOT = Path(__file__).parent
source = ROOT / 'manuscript.md'
out = ROOT / 'kdp_build'
out.mkdir(exist_ok=True)
text = source.read_text(encoding='utf-8')
html_body = markdown.markdown(text, extensions=['extra', 'sane_lists'])
css = '''
@page { size: 6in 9in; margin: 0.8in 0.72in 0.75in 0.85in; @bottom-center { content: counter(page); font-size: 9pt; color: #555; } }
body { font-family: Georgia, serif; font-size: 11.5pt; line-height: 1.42; color: #111; }
h1 { page-break-before: always; text-align: center; font-size: 20pt; margin-top: 2.5in; letter-spacing: 0.04em; }
h2 { page-break-before: always; text-align: center; font-size: 16pt; margin-top: 2.2in; }
h3 { text-align: center; font-size: 13pt; margin-top: 1.3in; }
p { text-align: left; text-indent: 0.22in; margin: 0 0 0.12in 0; }
blockquote { margin: 0.2in 0.4in; font-style: italic; }
hr { border: 0; page-break-after: always; }
'''
html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Loathing in the Woes of Ruthlessness</title><style>{css}</style></head><body>{html_body}</body></html>'''
(out / 'manuscript.html').write_text(html, encoding='utf-8')
HTML(string=html, base_url=str(ROOT)).write_pdf(str(out / 'paperback_interior_working.pdf'))

# Create a basic reflowable EPUB working file.
meta_inf = out / 'META-INF'; meta_inf.mkdir(exist_ok=True)
content = out / 'content'; content.mkdir(exist_ok=True)
(out / 'mimetype').write_text('application/epub+zip', encoding='ascii')
(meta_inf / 'container.xml').write_text('''<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="content/book.opf" media-type="application/oebps-package+xml"/></rootfiles></container>''', encoding='utf-8')
(content / 'book.xhtml').write_text(f'''<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Loathing in the Woes of Ruthlessness</title><style>body{{font-family:serif;line-height:1.4}} h1,h2,h3{{text-align:center;page-break-before:always}} p{{text-indent:1em;margin:0 0 .6em}}</style></head><body>{html_body}</body></html>''', encoding='utf-8')
(content / 'book.opf').write_text('''<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="bookid">urn:uuid:loathing-in-the-woes-of-ruthlessness-2026</dc:identifier><dc:title>Loathing in the Woes of Ruthlessness: The Chosen One</dc:title><dc:creator>Skyler Blue</dc:creator><dc:language>en</dc:language><meta property="dcterms:modified">2026-08-15T00:00:00Z</meta></metadata><manifest><item id="book" href="book.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="book"/></spine></package>''', encoding='utf-8')
with zipfile.ZipFile(out / 'kindle_ebook_working.epub', 'w') as z:
    z.write(out / 'mimetype', 'mimetype', compress_type=zipfile.ZIP_STORED)
    for p in [meta_inf / 'container.xml', content / 'book.xhtml', content / 'book.opf']:
        z.write(p, p.relative_to(out).as_posix(), compress_type=zipfile.ZIP_DEFLATED)

shutil.copy2(ROOT / 'front_cover.png', out / 'front_cover_for_ebook.png')
print('Created', out / 'kindle_ebook_working.epub')
print('Created', out / 'paperback_interior_working.pdf')
