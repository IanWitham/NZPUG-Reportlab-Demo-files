from reportlab.pdfgen.canvas import Canvas

# create a Canvas object. This is your PDF.
c = Canvas("01_Hello_World.pdf", pagesize="A4")

# The canvas is very stateful. Here we adjust the font size. This will affect
# all further text until a new font size is set. (If font size is not set it
# will default to 12pt. A bit small for this demo.)
c.setFontSize(60)

width, height = c._pagesize
c.drawCentredString(width / 2, height / 2, "Hello World")

c.showPage()  # Finish page 1

# Any extra drawing commands entered here would appear on page 2!

c.save()  # Finish the pdf and save to file. This Canvas can no longer be used.
