"""Low level PDF operations with pdfgen -- PART II

This demonstration introduces the concept of the state stack.

In a new canvas object, all operations are performed relative to the origin (0,
0) in the lower left corner of the page. Canvas transformations such as scale,
translate, rotate and skew, effect the origin and all drawing operations
performed after the transformation. These transformations are also cumulative.

It is very useful to save the canvas in its current state with
canvas.saveState(). You can "undo" any subsequent transformations by calling
canvas.restoreState(). Canvas.saveState() can "push" multiple states on to the
state stack.

There are also a few other canvas states which get saved to the state stack by
this operation, such as fill colour, stroke colour, and font face.
"""

from os.path import join

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm, cm

c = Canvas("02_Text.pdf", pagesize=(210*mm, 297*mm))
text_file = open("02_The_Raven.txt")
text = (l.strip() for l in text_file if l.strip())

c.setFontSize(10)
leading = 14 # line spacing.

c.saveState()

# translate halfway across page
c.translate(105*mm, 0) 

# draw a light grey vertical line 
c.setStrokeColorRGB(255, 0, 0)
c.line(0, 0, 0, 297*mm)

# move up the page
c.translate(0, 260*mm)

c.drawString(-100*mm, 0, "Canvas.drawString")
c.translate(0, -leading)
for i in range(2):
    c.translate(0, -leading)
    c.drawString(0, 0, text.next())

c.translate(0, -20*mm)
c.drawString(-100*mm, 0, "Canvas.drawCentredString")
c.translate(0, -leading)
for i in range(2):
    c.translate(0, -leading)
    c.drawCentredString(0, 0, text.next())

c.translate(0, -20*mm)
c.drawString(-100*mm, 0, "Canvas.drawRightString")
c.translate(0, -leading)
for i in range(2):
    c.translate(0, -leading)
    c.drawRightString(0, 0, text.next())

c.translate(0, -20*mm)
c.drawString(-100*mm, 0, "Canvas.beginText (Text object)")
c.translate(0, -leading*2)

# Text objects are more efficient for anything more than simple labels
textobject = c.beginText()
textobject.setTextOrigin(0, 0)
textobject.setFont("Times-Italic", 10)

# supply text one line at a time:
for i in range(6):
    textobject.textLine(text.next())
textobject.textLine()

# or select several lines of newline separated text
text_lines = '\n'.join(text.next() for i in range(5))
textobject.textLines(text_lines)

# or perhaps a word at a time...
text_words = text.next().split()
for word in text_words:
    textobject.textOut(word + " ")
    # Draw a red arrow to mark the cursor position
    x, y = textobject.getCursor()
    c.saveState()
    c.setFillColorRGB(255, 0, 0)
    c.drawCentredString(x, y-10, '|')
    c.drawCentredString(x, y-10, '^')
    c.restoreState()

# Finally render the text object
c.drawText(textobject)

# Return the canvas to its original state (origin in the bottom left
# corner of the page).
c.restoreState()

# Draw an image file to the page
c.drawImage(join("images", "234-The-Raven-Corvus-Corax-q75-445x500.jpg"),
            x=10*mm, y=10*mm, width=70*mm, height=100*mm,
            preserveAspectRatio=True,
            anchor='c'
            )

text_file.close()
c.showPage()
c.save()

print "done"
