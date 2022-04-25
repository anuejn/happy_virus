import fontforge
from lxml import etree
import psMat
from svgpathtools import parse_path

from string import ascii_lowercase
import tempfile
from math import ceil

top = 33
middle = 50
bottom = 81
extent = 4

font = fontforge.font()
font.em = top + middle + bottom
font.ascent = top + middle
font.descent = bottom

all_svg = etree.parse('happy_virus.svg')

for c in ascii_lowercase:
    element = all_svg.xpath(f'//*[@id="{c}"]')[0]
    d = parse_path(element.get("d"))
    xmin, xmax, ymin, ymax = d.bbox()
    d = d.translated(complex(-xmin + extent))
    
    glyph = font.createChar(ord(c))
    glyph.width = int(ceil(xmax - xmin + extent * 2))

    with tempfile.NamedTemporaryFile(suffix=".svg") as tmp:
        element.set("d", d.d())
        el_string = etree.tostring(element)
        tmp.write(f"""
        <svg>
            {el_string}
        </svg>
        """.encode())
        tmp.flush()
        glyph.importOutlines(tmp.name)
        glyph.transform(psMat.translate(0, -top))

font.save('happy_virus.sfd')
