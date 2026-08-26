#!/usr/bin/env python3
"""Build the standalone, offline copy of the notes from navamsha-notes.html.

Reads the artifact fragment, inlines the web fonts as base64, adds the print
stylesheet, and writes Navamsha-notes.html. Run build-pdf.mjs afterwards for
the PDF.
"""
import re, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAG = os.path.join(HERE, 'navamsha-notes.html')
FONTS = os.path.join(HERE, 'tools', 'embedded-fonts.css')
OUT = os.path.join(HERE, 'Navamsha-notes.html')

PRINT_CSS = r'''
@media print{
  :root, :root[data-theme="dark"], :root:not([data-theme="light"]){
    --ground:#FFFFFF; --ground-2:#F7EFF5; --paper:#FFFFFF; --paper-2:#FAF3F7;
    --ink:#3D1240; --ink-soft:#542A5A; --muted:#7A6180;
    --line:#E3D1DC; --line-soft:#F0E4EC;
    --blush:#F7D3E4; --lilac:#E1CCF7; --orchid:#D8B6EC; --peri:#C9D2F8;
    --gold:#9A6C18; --gold-bright:#C99A34; --gold-soft:#F0D6A2;
    --rose:#A93F68; --violet:#6A37A8; --aubergine:#4A1550; --jade:#5C8A7C;
    --shadow-s:none; --shadow:none; --shadow-l:none; --hi-line:transparent;
  }
  @page{ size:A4; margin:14mm 12mm 16mm; }
  html,body{ background:#fff !important; }
  body{ font-size:11.4pt; line-height:1.6; }
  body::before, body::after{ display:none !important; }
  nav.chapters, .rail, #progress, #toTop, .theme-toggle, .sparkles, .cue,
  .ex-tabs, .counter, .tally-foot{ display:none !important; }
  .hero-art::before{ display:none !important; }
  .rot-a, .rot-b, .breathe, .hero .lift{ animation:none !important; }
  .hero-art svg{ overflow:hidden; width:74mm; transform:none !important; }
  .wrap{ max-width:none; padding:0; }
  .col, .col-wide{ max-width:none; }
  .hero{ padding:0 0 8mm; break-after:page; }
  .hero h1{ font-size:44pt; }
  .hero .sub{ font-size:15pt; }
  main section{ break-before:page; padding:0 0 6mm; }
  main section:first-of-type{ break-before:avoid; }
  svg.divider{ display:none; }
  .sec-head h2{ font-size:24pt; }
  .sec-head .lede{ font-size:12pt; }
  h3.sub{ font-size:16pt; }
  .ghost{ font-size:70pt; opacity:.05; top:0; }
  .card, .sutra, .asked, .voice, .callout, .fire, .chart-pair, .band, .pot, figure, .sheet{
    break-inside:avoid; box-shadow:none !important; border-color:var(--line) !important;
  }
  .card::after{ display:none; }
  tr, .def{ break-inside:avoid; }
  .voice{ background:#FBF4F8 !important; }
  .voice p{ font-size:15pt; }
  .kundali{ max-width:52mm; }
  .pot output{ display:none; }
  .print-only{ display:block !important; }
  .grid{ gap:5mm; }
  a{ color:inherit; text-decoration:none; }
  .hero h1 .it, .sec-head h2 .it{
    -webkit-text-fill-color:var(--violet); color:var(--violet); background:none;
  }
  footer{ break-before:page; padding:20mm 0; }
}
.print-only{ display:none; }
'''

def main():
    frag = open(FRAG, encoding='utf8').read()
    fonts = open(FONTS, encoding='utf8').read()
    frag = frag.replace('<title>Karakamsha & the Khara Pada</title>\n', '')
    frag = re.sub(r'<link rel="preconnect"[^>]*>\n', '', frag)
    frag = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\n', '', frag)
    # the tabbed examples collapse to one on paper, so say where the rest are
    frag = frag.replace(
        "Nine placements worked out live across the two classes, on the students' own charts. Tap through them.",
        "Nine placements worked out live across the two classes, on the students' own charts."
        "<span class=\"print-only\"><br>On paper only the first is shown; open the HTML file to step through all nine.</span>")
    frag = frag.replace(
        "<p class=\"tally-foot\">",
        "<p class=\"print-only\" style=\"margin-top:14px;color:var(--muted);font-size:14px\">"
        "Open the HTML file to tally your own ten bodies and watch the cloth weave itself.</p>\n        <p class=\"tally-foot\">")
    head = (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>Karakamsha &amp; the Khara Pada</title>\n'
        '<meta name="description" content="Visual notes from the 22 August Navamsha lesson, '
        'English and Hindi sessions merged.">\n'
        '<style>\n' + fonts + '\n</style>\n<style>\n' + PRINT_CSS + '\n</style>\n</head>\n<body>\n'
    )
    open(OUT, 'w', encoding='utf8').write(head + frag + '\n</body>\n</html>\n')
    print('wrote', OUT, os.path.getsize(OUT), 'bytes')

if __name__ == '__main__':
    main()
