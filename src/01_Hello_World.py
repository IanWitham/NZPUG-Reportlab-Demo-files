"""Low level PDF operations with pdfgen.

Underneath the PLATYPUS engine lies the pdfgen API.

The pdfgen API allows you to draw text, shapes and images directly to a canvas
object. The canvas object <i>is</i> your PDF.

All drawing operations are performed by calling various methods of the canvas
object.
"""

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm

# create a Canvas object. This is your PDF.
c = Canvas("01_Hello_World.pdf", pagesize=(210*mm, 297*mm))

# The canvas is very stateful. Here we adjust the font size. This will affect
# all further text until a new font size is set. (If font size is not set it
# will default to 12pt. A bit small for this demo.)
c.setFontSize(60)

# The native unit of measurement in PDFs is the postscript point (The unit of
# measurement most often used for defining font sizes.) To use measurements in
# mm, cm, inch or pica, simply multiply the value by the appropriate unit from
# reportlab.lib.units. This converts the measurement to points.
width, height = 210*mm, 297*mm

# When placing objects on the page keep in mind that by default, measurements are taken
# from the lower left-hand corner of the page.
c.drawCentredString(width / 2, height / 2, "Hello World")

c.showPage()  # Finish page 1

# Any extra drawing commands entered here would appear on page 2!

c.save()  # Finish the pdf and save to file. This Canvas can no longer be used.
